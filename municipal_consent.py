# -*- coding: utf-8 -*-
from datetime import date
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
BLANK = ROOT / "consent" / "municipal-consent.pdf"
FONT = ROOT / "fonts" / "serif.ttf"
FONT_NAME = "MshkSerif"
INK = Color(0.10, 0.08, 0.07)

if FONT.exists() and FONT_NAME not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT)))


def _txt(data: dict, key: str) -> str:
    return " ".join(str(data.get(key) or "").split())


def _passport(data: dict) -> str:
    return " ".join(p for p in (_txt(data, "passport_series"), _txt(data, "passport_number")) if p)


MONTHS = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)


def _date_parts(data: dict) -> tuple[str, str, str]:
    raw = _txt(data, "fill_date")
    dt = date.today()
    if raw:
        for fmt, sep in (("%d.%m.%Y", "."), ("%Y-%m-%d", "-"), ("%d/%m/%Y", "/")):
            try:
                parts = raw.replace("/", sep).replace(".", sep).split(sep)
                if fmt.startswith("%Y"):
                    dt = date(int(parts[0]), int(parts[1]), int(parts[2]))
                else:
                    dt = date(int(parts[2]), int(parts[1]), int(parts[0]))
                break
            except (ValueError, IndexError):
                continue
    return ("%02d" % dt.day, MONTHS[dt.month - 1], str(dt.year))


def _has_fill(data: dict) -> bool:
    keys = (
        "fio",
        "address",
        "phone",
        "email",
        "passport_series",
        "passport_number",
        "passport_issued",
    )
    return any(_txt(data, k) for k in keys)


def blank_pdf_bytes() -> bytes:
    if not BLANK.exists():
        raise FileNotFoundError("municipal consent PDF is missing")
    return BLANK.read_bytes()


def _draw(c, text, x, y, size=10.5, width=430):
    if not text:
        return
    c.setFillColor(INK)
    c.setFont(FONT_NAME, size)
    while text and c.stringWidth(text, FONT_NAME, size) > width:
        text = text[:-1]
    c.drawString(x, y, text)


def _draw_wrap(c, text, x, y, size, width, extra_x, extra_y, extra_w=500):
    if not text:
        return
    c.setFont(FONT_NAME, size)
    if c.stringWidth(text, FONT_NAME, size) <= width:
        _draw(c, text, x, y, size, width)
        return
    words = text.split()
    acc = []
    rest = []
    for i, word in enumerate(words):
        trial = " ".join(acc + [word])
        if c.stringWidth(trial, FONT_NAME, size) <= width:
            acc.append(word)
        else:
            rest = words[i:]
            break
    _draw(c, " ".join(acc) or text, x, y, size, width)
    if rest:
        _draw(c, " ".join(rest), extra_x, extra_y, size, extra_w)


def _draw_form_date(c, parts, x, y, size=10):
    day, month, year = parts
    text = "\u00ab%s\u00bb %s %s \u0433." % (day, month, year)
    c.setFont(FONT_NAME, size)
    c.setFillColor(white)
    c.rect(x - 2, y - 5, 585 - x, size + 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.drawString(x, y, text)


def _overlay(data: dict, width: float, height: float) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))
    fio = _txt(data, "fio")
    address = _txt(data, "address")
    phone = _txt(data, "phone")
    email = _txt(data, "email")
    passport = _passport(data)
    issued = _txt(data, "passport_issued")
    dated = _date_parts(data)

    # page 1: dissemination
    _draw(c, fio, 68, 748, 11, 470)
    _draw_wrap(c, address, 204, 716, 10, 340, 48, 701)
    _draw(c, passport, 368, 685, 10, 170)
    _draw(c, issued, 50, 656, 10, 490)
    _draw(c, phone, 136, 627, 10.5, 360)
    c.showPage()

    # page 2: closing of dissemination
    _draw(c, email, 48, 136, 10, 250)
    _draw(c, fio, 172, 94, 10, 150)
    _draw_form_date(c, dated, 397, 92.9, 10)
    c.showPage()

    # page 3: accommodation
    _draw(c, fio, 100, 774, 10.5, 430)
    _draw_wrap(c, address, 246, 750, 9.5, 300, 88, 737)
    _draw(c, passport, 368, 724, 9.5, 160)
    _draw(c, issued, 88, 697, 9.5, 450)
    _draw(c, phone, 160, 660, 10, 340)
    _draw(c, email, 312, 569, 9.5, 220)
    _draw(c, fio, 198, 42, 9.5, 200)
    _draw_form_date(c, dated, 425, 40.4, 9)
    c.showPage()

    # page 4: house rules
    _draw(c, fio, 100, 796, 10.5, 450)
    _draw(c, fio, 230, 87, 9.5, 220)
    _draw_form_date(c, dated, 444, 85.8, 9)
    c.showPage()

    # page 5: event participant
    _draw(c, fio, 62, 791, 11, 470)
    _draw_wrap(c, address, 232, 765, 10, 300, 50, 751)
    _draw(c, passport, 368, 738, 10, 170)
    _draw(c, issued, 50, 712, 10, 490)
    _draw(c, phone, 134, 673, 10.5, 360)
    _draw(c, email, 308, 581, 10, 230)
    c.showPage()

    # page 6: signature
    _draw(c, fio, 175, 68, 10, 200)
    _draw_form_date(c, dated, 428, 66, 10)
    c.showPage()
    c.save()
    return buf.getvalue()


def filled_pdf_bytes(data: dict) -> bytes:
    if not BLANK.exists():
        raise FileNotFoundError("municipal consent PDF is missing")
    if not FONT.exists() or not _has_fill(data):
        return blank_pdf_bytes()
    src = PdfReader(str(BLANK))
    width = float(src.pages[0].mediabox.width)
    height = float(src.pages[0].mediabox.height)
    overlay = PdfReader(BytesIO(_overlay(data, width, height)))
    out = PdfWriter()
    for i, page in enumerate(src.pages):
        if i < len(overlay.pages):
            page.merge_page(overlay.pages[i])
        out.add_page(page)
    buf = BytesIO()
    out.write(buf)
    return buf.getvalue()
