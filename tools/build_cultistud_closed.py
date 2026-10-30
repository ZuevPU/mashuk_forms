# -*- coding: utf-8 -*-
"""Build the "registration closed" page for the university seminar.

Output: static/cultistudclosed.html
Served by GET /cultistudform while CULTISTUD_FORM_CLOSED is on.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_apply_form import CSS as APPLY_CSS

VK_URL = "https://vk.ru/czmashuk"
VK_LABEL = "vk.ru/czmashuk"
MAIL = "nastavnikmashuk@yandex.ru"

S = {
    "kicker": "Регистрация",
    "title": "Регистрация завершена",
    "lead": "Набор участников семинара закрыт.",
    "p1": "Спасибо всем, кто подал заявку и интересуется программой. Организаторы свяжутся с участниками по контактам, указанным в анкете.",
    "p2": "Следите за следующими программами Центра знаний «Машук» — рассказываем о них в сообществе.",
    "vk": "Мы ВКонтакте",
    "vk_note": "Анонсы программ, архив материалов и жизнь Центра знаний «Машук»",
    "support": "Есть вопрос?",
    "support_mail": "Напишите нам:",
    "event": "«Студенческие сообщества как пространство поликультурного взаимодействия»",
    "dates": "5–8 ноября 2026",
    "center": "АНО «Центр знаний «Машук»»",
    "place": "Г. Пятигорск, Пионерлагерная ул., зд. 8в",
}

CLOSED_CSS = r"""
html,body{height:100%}
.mshk-closed{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:clamp(18px,4vw,40px) 0;background-color:#fafafa;background-image:radial-gradient(ellipse 70% 55% at 8% 12%,rgba(84,164,219,.16),transparent 58%),radial-gradient(ellipse 55% 50% at 92% 8%,rgba(34,63,154,.12),transparent 52%),radial-gradient(ellipse 50% 45% at 78% 88%,rgba(162,133,95,.11),transparent 55%);font-family:"Geologica",Verdana,system-ui,sans-serif;color:#332d24;-webkit-font-smoothing:antialiased}
.mshk-closed__card{position:relative;width:min(520px,calc(100% - 32px));box-sizing:border-box;padding:clamp(26px,5vw,42px);background:#fff;border:1px solid rgba(34,63,154,.08);border-radius:24px;box-shadow:0 18px 60px rgba(34,63,154,.10);text-align:center;animation:mshk-closed-in .5s cubic-bezier(.22,1,.36,1) both}
@keyframes mshk-closed-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.mshk-closed__mark{display:flex;align-items:center;justify-content:center;width:68px;height:68px;margin:0 auto 20px;border-radius:50%;background:rgba(34,63,154,.08);color:#223f9a}
.mshk-closed__mark svg{display:block;width:32px;height:32px}
.mshk-closed__kicker{margin:0 0 10px;font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#a2855f}
.mshk-closed__title{margin:0 0 12px;font-size:clamp(25px,4.2vw,32px);font-weight:600;letter-spacing:-.03em;line-height:1.14;color:#223f9a}
.mshk-closed__lead{margin:0 0 6px;font-size:15px;font-weight:400;line-height:1.55;color:#332d24}
.mshk-closed__event{margin:0 0 18px;font-family:"Noto Serif","Times New Roman",serif;font-style:italic;font-size:14px;line-height:1.5;color:rgba(51,45,36,.62)}
.mshk-closed__p{margin:0 0 12px;font-size:14px;font-weight:300;line-height:1.6;color:rgba(51,45,36,.8);text-align:left}
.mshk-closed__btn{display:flex;align-items:center;gap:14px;margin:20px 0 0;padding:14px 18px;border-radius:18px;background:#223f9a;color:#fff;text-decoration:none;transition:background-color .2s,transform .2s}
.mshk-closed__btn:hover{background:#1b327c;transform:translateY(-1px)}
.mshk-closed__btn-ic{display:flex;align-items:center;justify-content:center;flex:0 0 auto;width:42px;height:42px;border-radius:12px;background:rgba(255,255,255,.14)}
.mshk-closed__btn-ic svg{display:block;width:25px;height:25px}
.mshk-closed__btn-tx{display:block;text-align:left;min-width:0}
.mshk-closed__btn-tx b{display:block;font-size:15px;font-weight:600}
.mshk-closed__btn-tx span{display:block;margin-top:3px;font-size:12px;font-weight:300;line-height:1.4;color:rgba(255,255,255,.78)}
.mshk-closed__btn-arrow{margin-left:auto;flex:0 0 auto;width:18px;height:18px;opacity:.85}
.mshk-closed__btn-arrow svg{display:block;width:18px;height:18px}
.mshk-closed__rule{height:1px;margin:22px 0;background:#dcdedd}
.mshk-closed__support{margin:0;font-size:14px;font-weight:300;line-height:1.6;color:rgba(51,45,36,.72);text-align:left}
.mshk-closed__support a{color:#223f9a;font-weight:500;text-decoration:none;box-shadow:0 1px 0 0 rgba(34,63,154,.35)}
.mshk-closed__meta{margin:16px 0 0;font-size:12px;line-height:1.6;color:rgba(51,45,36,.5);text-align:left}
.mshk-closed__dates{margin:18px 0 0;padding-top:16px;border-top:1px solid #dcdedd;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:rgba(51,45,36,.5)}
@media(max-width:560px){.mshk-closed__card{border-radius:20px;padding:24px 18px}.mshk-closed__btn{padding:13px 15px;gap:12px}.mshk-closed__btn-arrow{display:none}}
"""

CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M5 12.8l4.2 4.2L19 7.4" stroke="currentColor" stroke-width="2.2" '
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


def main():
    body = (
        '<div class="mshk-closed">'
        '<div class="mshk-closed__card">'
        '<div class="mshk-closed__mark">' + CHECK + "</div>"
        '<p class="mshk-closed__kicker">' + eh(S["kicker"]) + "</p>"
        '<h1 class="mshk-closed__title">' + eh(S["title"]) + "</h1>"
        '<p class="mshk-closed__lead">' + eh(S["lead"]) + "</p>"
        '<p class="mshk-closed__event">' + eh(S["event"]) + "</p>"
        '<p class="mshk-closed__p">' + eh(S["p1"]) + "</p>"
        '<p class="mshk-closed__p">' + eh(S["p2"]) + "</p>"
        '<a class="mshk-closed__btn" href="' + VK_URL + '" target="_blank" rel="noopener">'
        '<span class="mshk-closed__btn-ic">' + VK_ICON + "</span>"
        '<span class="mshk-closed__btn-tx"><b>' + eh(S["vk"]) + "</b><span>" + eh(S["vk_note"]) + "</span></span>"
        '<span class="mshk-closed__btn-arrow">' + ARROW + "</span></a>"
        '<div class="mshk-closed__rule"></div>'
        '<p class="mshk-closed__support">' + eh(S["support"]) + " " + eh(S["support_mail"])
        + ' <a href="mailto:' + MAIL + '">' + MAIL + "</a></p>"
        '<p class="mshk-closed__meta">' + eh(S["center"]) + ". " + eh(S["place"]) + "</p>"
        '<p class="mshk-closed__dates">' + eh(S["dates"]) + "</p>"
        "</div></div>"
    )
    page = (
        "<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + eh(S["title"]) + " \u2014 " + eh(S["event"]) + "</title>\n"
        '<meta name="robots" content="noindex, nofollow">\n'
        "<style>html,body{margin:0;padding:0}" + APPLY_CSS + CLOSED_CSS + "</style>\n"
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    out = ROOT / "static" / "cultistudclosed.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out, len(page))


if __name__ == "__main__":
    main()
