# -*- coding: utf-8 -*-
"""Standalone page for the municipalities seminar when signing up is over.

Not wired into the app: GET /muni serves the registration form from
static/muni.html. Keep this builder only to reuse the page later — for example
as a Tilda block replacing the registration block on a landing page, or as the
next closed-form notice. Random re-runs would put the file back into
static/ where it is no longer served, so run it deliberately.

Writes:
  static/muni-closed.html          (page meant for a Tilda iframe)
  tilda/muni-closed-block.html     (same page, standalone HTML block)

The build is not destructive: the registration form stays in the repo as
tilda/tilda-muni-block.html and is rebuilt with tools/build_muni_form.py.
All non-ASCII text is HTML-entity encoded, like the other builders.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_apply_form import CSS as APPLY_CSS

VK_URL = "https://vk.ru/czmashuk"
VK_LABEL = "vk.ru/czmashuk"
MAIL = "online@czmashuk.ru"

S = {
    "kicker": "\u041e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0435",
    "title1": "\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430",
    "event": "\u00ab\u041c\u0435\u0436\u043d\u0430\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u0438 \u043c\u0435\u0436\u043a\u043e\u043d\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f \u0432 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u0438\u0442\u0435\u0442\u043e\u0432\u00bb",
    "lead": "\u041c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u0443\u0436\u0435 \u043f\u0440\u043e\u0448\u043b\u043e \u2014 \u0438 \u043e\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0438\u043b\u043e\u0441\u044c \u043f\u043e-\u043d\u0430\u0441\u0442\u043e\u044f\u0449\u0435\u043c\u0443 \u0442\u0451\u043f\u043b\u044b\u043c.",
    "p1": "\u0421\u043f\u0430\u0441\u0438\u0431\u043e, \u0447\u0442\u043e \u0431\u044b\u043b\u0438 \u0441 \u043d\u0430\u043c\u0438: \u0437\u0430 \u0432\u043e\u043f\u0440\u043e\u0441\u044b, \u0441\u043f\u043e\u0440\u044b, \u0436\u0438\u0432\u044b\u0435 \u043f\u0440\u0438\u043c\u0435\u0440\u044b \u0438\u0437 \u043f\u0440\u0430\u043a\u0442\u0438\u043a\u0438 \u0438 \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c \u0443\u0447\u0438\u0442\u044c\u0441\u044f \u0434\u0440\u0443\u0433 \u0443 \u0434\u0440\u0443\u0433\u0430.",
    "p2": "\u041d\u043e\u0432\u044b\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b \u0438 \u0434\u0430\u0442\u044b \u043c\u044b \u043e\u0431\u044a\u044f\u0432\u043b\u044f\u0435\u043c \u0432 \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0435 \u2014 \u043f\u0440\u0438\u0441\u043e\u0435\u0434\u0438\u043d\u044f\u0439\u0442\u0435\u0441\u044c, \u0431\u0443\u0434\u0435\u043c \u0440\u0430\u0434\u044b \u0432\u0438\u0434\u0435\u0442\u044c \u0432\u0430\u0441 \u0441\u043d\u043e\u0432\u0430.",
    "vk": "\u041c\u044b \u0412\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0435",
    "vk_note": "\u0410\u043d\u043e\u043d\u0441\u044b \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c, \u0430\u0440\u0445\u0438\u0432 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u043e\u0432 \u0438 \u0436\u0438\u0437\u043d\u044c \u0426\u0435\u043d\u0442\u0440\u0430 \u0437\u043d\u0430\u043d\u0438\u0439 \u00ab\u041c\u0430\u0448\u0443\u043a\u00bb",
    "support": "\u0415\u0441\u0442\u044c \u0432\u043e\u043f\u0440\u043e\u0441?",
    "support_mail": "\u041d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 \u043d\u0430\u043c:",
    "center": "\u0410\u041d\u041e \u00ab\u0426\u0435\u043d\u0442\u0440 \u0437\u043d\u0430\u043d\u0438\u0439 \u00ab\u041c\u0430\u0448\u0443\u043a\u00bb\u00bb",
    "place": "\u0413. \u041f\u044f\u0442\u0438\u0433\u043e\u0440\u0441\u043a, \u041f\u0438\u043e\u043d\u0435\u0440\u043b\u0430\u0433\u0435\u0440\u043d\u0430\u044f \u0443\u043b., \u0437\u0434. 8\u0432",
    "title_plain": "\u041c\u0435\u0436\u043d\u0430\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u0438 \u043c\u0435\u0436\u043a\u043e\u043d\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f \u0432 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u0438\u0442\u0435\u0442\u043e\u0432",
}

CLOSED_CSS = r"""
/* status mark */
.mshk-closed__mark{display:flex;align-items:center;justify-content:center;width:64px;height:64px;margin:0 0 22px;border-radius:50%;background:var(--navy);color:#fff;box-shadow:0 10px 28px rgba(34,63,154,.22)}
.mshk-closed__mark svg{display:block;width:30px;height:30px}
/* card */
.mshk-closed__card{position:relative;padding:clamp(24px,4vw,44px);background:var(--white);border:1px solid rgba(34,63,154,.08);border-radius:24px;box-shadow:0 14px 48px rgba(34,63,154,.08)}
.mshk-closed__rule{height:1px;margin:24px 0;background:var(--stone)}
.mshk-closed__meta{margin:18px 0 0;font-size:13px;font-weight:300;line-height:1.6;color:rgba(51,45,36,.62);font-family:var(--sans)!important}
/* VK button */
.mshk-closed__btn{display:flex;align-items:center;gap:14px;margin:22px 0 0;padding:16px 20px;border-radius:18px;background:var(--navy);color:#fff!important;transition:transform .25s var(--ease),background-color .25s var(--ease)}
.mshk-closed__btn:hover,.mshk-closed__btn:focus-visible{background:#1b327c;transform:translateY(-1px);outline:none}
.mshk-closed__btn-ic{display:flex;align-items:center;justify-content:center;flex:0 0 auto;width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.14)}
.mshk-closed__btn-ic svg{display:block;width:26px;height:26px}
.mshk-closed__btn-tx{display:block;min-width:0}
.mshk-closed__btn-tx b{display:block;font-size:16px;font-weight:600;letter-spacing:-.01em;font-family:var(--sans)!important}
.mshk-closed__btn-tx span{display:block;margin-top:3px;font-size:13px;font-weight:300;line-height:1.4;color:rgba(255,255,255,.78);font-family:var(--sans)!important}
.mshk-closed__btn-arrow{margin-left:auto;flex:0 0 auto;width:20px;height:20px;opacity:.85}
.mshk-closed__btn-arrow svg{display:block;width:20px;height:20px}
/* support line */
.mshk-closed__support{margin:26px 0 0;font-size:14px;font-weight:300;line-height:1.6;color:rgba(51,45,36,.72);font-family:var(--sans)!important}
.mshk-closed__support a{font-weight:500;box-shadow:0 1px 0 0 rgba(34,63,154,.35)}
@media(max-width:560px){
  .mshk-closed__card{padding:22px 18px;border-radius:20px}
  .mshk-closed__btn{padding:14px 16px;gap:12px}
  .mshk-closed__btn-ic{width:40px;height:40px}
  .mshk-closed__btn-arrow{display:none}
}
"""

CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M5 12.8l4.2 4.2L19 7.4" stroke="currentColor" stroke-width="2.4" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

VK_ICON = (
    '<svg viewBox="0 0 100 100" fill="none" aria-hidden="true">'
    '<path fill-rule="evenodd" clip-rule="evenodd" d="M50 100c27.614 0 50-22.386 50-50S77.614 0 50 0 0 '
    '22.386 0 50s22.386 50 50 50ZM25 34c.406 19.488 10.15 31.2 27.233 31.2h.968V54.05c6.278.625 11.024 '
    '5.216 12.93 11.15H75c-2.436-8.87-8.838-13.773-12.836-15.647C66.162 47.242 71.783 41.62 73.126 34h-8.058c-1.749 '
    '6.184-6.932 11.805-11.867 12.336V34h-8.057v21.611C40.147 54.362 33.838 48.304 33.556 34H25Z" '
    'fill="currentColor"/></svg>'
)

ARROW = (
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
    '<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def eh(s):
    out = []
    for c in s:
        o = ord(c)
        if o > 127:
            out.append("&#%d;" % o)
        elif c == "&":
            out.append("&amp;")
        elif c == "<":
            out.append("&lt;")
        elif c == ">":
            out.append("&gt;")
        elif c == '"':
            out.append("&quot;")
        else:
            out.append(c)
    return "".join(out)


def h(key):
    return eh(S[key])


def body():
    html = []
    html.append('<section id="mshk-apply">')
    html.append('<div class="mshk-apply__geo mshk-apply__geo--lg"></div>')
    html.append('<div class="mshk-apply__geo mshk-apply__geo--sm"></div>')
    html.append('<div class="mshk-apply__shell">')
    html.append('<p class="mshk-apply__kicker">' + h("kicker") + "</p>")
    html.append(
        '<h1 class="mshk-apply__title"><span>'
        + h("event")
        + "</span>"
        + h("title1")
        + "</h1>"
    )
    html.append('<div class="mshk-closed__card">')
    html.append('<div class="mshk-closed__mark">' + CHECK + "</div>")
    html.append('<p class="mshk-apply__lead">' + h("lead") + "</p>")
    html.append('<p class="mshk-apply__p">' + h("p1") + "</p>")
    html.append('<p class="mshk-apply__p">' + h("p2") + "</p>")
    html.append(
        '<a class="mshk-closed__btn" href="'
        + VK_URL
        + '" target="_blank" rel="noopener">'
        '<span class="mshk-closed__btn-ic">' + VK_ICON + "</span>"
        '<span class="mshk-closed__btn-tx"><b>' + h("vk") + "</b>"
        "<span>" + h("vk_note") + "</span></span>"
        '<span class="mshk-closed__btn-arrow">' + ARROW + "</span></a>"
    )
    html.append('<div class="mshk-closed__rule"></div>')
    html.append(
        '<p class="mshk-closed__support">'
        + h("support")
        + " "
        + h("support_mail")
        + ' <a href="mailto:'
        + MAIL
        + '">'
        + MAIL
        + "</a></p>"
    )
    html.append(
        '<p class="mshk-closed__meta">'
        + h("center")
        + ". "
        + h("place")
        + "</p>"
    )
    html.append("</div>")
    html.append("</div></section>")
    return "\n".join(html)


def page():
    css = APPLY_CSS + CLOSED_CSS
    return (
        "<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + h("title_plain") + " \u2014 " + h("title1") + "</title>\n"
        '<meta name="robots" content="noindex, nofollow">\n'
        "<style>html,body{margin:0;padding:0;height:auto;min-height:0;max-width:100%;"
        "overflow-x:hidden;background:#fafafa}</style>\n"
        "<style>" + css + "</style>\n"
        "</head>\n<body>\n" + body() + "\n</body>\n</html>\n"
    )


def main():
    html = page()
    static_dir = ROOT / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    (static_dir / "muni-closed.html").write_text(html, encoding="utf-8")
    tilda = ROOT / "tilda"
    tilda.mkdir(parents=True, exist_ok=True)
    (tilda / "muni-closed-block.html").write_text(html, encoding="utf-8")
    print("wrote", static_dir / "muni-closed.html", len(html))


if __name__ == "__main__":
    main()
