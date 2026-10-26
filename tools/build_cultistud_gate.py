# -*- coding: utf-8 -*-
"""Build the password screen that guards the university seminar form.

Output: static/cultistudgate.html
The page posts the password to /cultistudform/unlock and, on success, goes to
the form with a signed token in the URL so it also works inside a Tilda iframe.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_apply_form import CSS as APPLY_CSS

S = {
    "kicker": "Регистрация",
    "title": "Доступ по паролю",
    "lead": "Регистрация на семинар открыта по персональному приглашению.",
    "hint": "Введите пароль, который выдал организатор.",
    "placeholder": "Пароль",
    "button": "Войти",
    "error": "Неверный пароль. Проверьте раскладку и попробуйте ещё раз.",
    "note": "Если пароль не подходит, напишите на nastavnikmashuk@yandex.ru",
    "event": "«Студенческие сообщества как пространство поликультурного взаимодействия»",
    "dates": "5–8 ноября 2026",
}

EXTRA_CSS = r"""
html,body{height:100%}
.mshk-gate{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:clamp(18px,4vw,40px) 0;background-color:#fafafa;background-image:radial-gradient(ellipse 70% 55% at 8% 12%,rgba(84,164,219,.16),transparent 58%),radial-gradient(ellipse 55% 50% at 92% 8%,rgba(34,63,154,.12),transparent 52%),radial-gradient(ellipse 50% 45% at 78% 88%,rgba(162,133,95,.11),transparent 55%);font-family:"Geologica",Verdana,system-ui,sans-serif;color:#332d24;-webkit-font-smoothing:antialiased}
.mshk-gate__card{position:relative;width:min(460px,calc(100% - 32px));box-sizing:border-box;padding:clamp(26px,5vw,40px);background:#fff;border:1px solid rgba(34,63,154,.08);border-radius:24px;box-shadow:0 18px 60px rgba(34,63,154,.10);text-align:center;animation:mshk-gate-in .5s cubic-bezier(.22,1,.36,1) both}
@keyframes mshk-gate-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.mshk-gate__lock{display:flex;align-items:center;justify-content:center;width:64px;height:64px;margin:0 auto 20px;border-radius:50%;background:rgba(34,63,154,.08);color:#223f9a}
.mshk-gate__lock svg{display:block;width:30px;height:30px}
.mshk-gate__kicker{margin:0 0 10px;font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#a2855f}
.mshk-gate__title{margin:0 0 12px;font-size:clamp(24px,4vw,30px);font-weight:600;letter-spacing:-.03em;color:#223f9a;line-height:1.15}
.mshk-gate__lead{margin:0 0 6px;font-size:15px;font-weight:300;line-height:1.55;color:rgba(51,45,36,.8)}
.mshk-gate__event{margin:0 0 22px;font-family:"Noto Serif","Times New Roman",serif;font-style:italic;font-size:14px;line-height:1.5;color:rgba(51,45,36,.62)}
.mshk-gate__form{margin:0}
.mshk-gate__label{display:block;margin:0 0 8px;font-size:13px;font-weight:500;color:#332d24;text-align:left}
.mshk-gate__input{box-sizing:border-box;width:100%;height:54px;padding:0 18px;border:1px solid rgba(34,63,154,.18);border-radius:14px;background:#fafafa;font-family:inherit;font-size:26px;font-weight:500;letter-spacing:.34em;text-align:center;color:#223f9a;outline:none;transition:border-color .2s,box-shadow .2s,background-color .2s}
.mshk-gate__input::placeholder{font-size:14px;letter-spacing:.02em;font-weight:300;color:rgba(51,45,36,.4)}
.mshk-gate__input:focus{border-color:#223f9a;background:#fff;box-shadow:0 0 0 4px rgba(34,63,154,.10)}
.mshk-gate__input.is-bad{border-color:#b23b3b;box-shadow:0 0 0 4px rgba(178,59,59,.10)}
.mshk-gate__btn{appearance:none;width:100%;height:52px;margin:16px 0 0;border:0;border-radius:999px;background:#223f9a;color:#fff;font-family:inherit;font-size:15px;font-weight:500;cursor:pointer;transition:background-color .2s,transform .2s}
.mshk-gate__btn:hover{background:#1b327c;transform:translateY(-1px)}
.mshk-gate__btn:disabled{opacity:.6;cursor:default;transform:none}
.mshk-gate__err{margin:12px 0 0;font-size:13px;line-height:1.45;color:#b23b3b;text-align:left}
.mshk-gate__note{margin:20px 0 0;font-size:12px;line-height:1.5;color:rgba(51,45,36,.55)}
.mshk-gate__note a{color:#223f9a;text-decoration:none;box-shadow:0 1px 0 0 rgba(34,63,154,.3)}
.mshk-gate__dates{margin:18px 0 0;padding-top:16px;border-top:1px solid #dcdedd;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:rgba(51,45,36,.5)}
@media(max-width:560px){.mshk-gate__card{border-radius:20px;padding:24px 18px}.mshk-gate__input{height:52px;font-size:24px}}
"""

LOCK = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<rect x="4.5" y="10" width="15" height="10.5" rx="2.5" stroke="currentColor" stroke-width="1.7"/>'
    '<path d="M8 10V7.6a4 4 0 0 1 8 0V10" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round"/><circle cx="12" cy="15.2" r="1.3" fill="currentColor"/>'
    "</svg>"
)

JS = r"""
(function(){
  var form = document.getElementById("mshk-gate-form");
  var input = document.getElementById("mshk-gate-password");
  var button = document.getElementById("mshk-gate-submit");
  var error = document.getElementById("mshk-gate-error");
  if (!form || !input) return;
  form.addEventListener("submit", function(ev){
    ev.preventDefault();
    var value = (input.value || "").trim();
    if (!value) { showError(true); return; }
    button.disabled = true;
    error.hidden = true;
    fetch("/cultistudform/unlock", {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: new URLSearchParams({password: value}).toString()
    }).then(function(r){
      if (!r.ok) throw new Error("bad");
      return r.json();
    }).then(function(data){
      var token = data && data.token ? data.token : "";
      window.location.replace("/cultistudform?t=" + encodeURIComponent(token));
    }).catch(function(){
      button.disabled = false;
      showError(false);
      input.select();
    });
  });
  function showError(empty){
    error.textContent = empty ? "Введите пароль" : "Неверный пароль. Проверьте раскладку и попробуйте ещё раз.";
    error.hidden = false;
    input.classList.add("is-bad");
    setTimeout(function(){ input.classList.remove("is-bad"); }, 900);
  }
})();
"""


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
        '<div class="mshk-gate">'
        '<div class="mshk-gate__card">'
        '<div class="mshk-gate__lock">' + LOCK + "</div>"
        '<p class="mshk-gate__kicker">' + eh(S["kicker"]) + "</p>"
        '<h1 class="mshk-gate__title">' + eh(S["title"]) + "</h1>"
        '<p class="mshk-gate__lead">' + eh(S["lead"]) + "</p>"
        '<p class="mshk-gate__event">' + eh(S["event"]) + "</p>"
        '<form class="mshk-gate__form" id="mshk-gate-form" autocomplete="off">'
        '<label class="mshk-gate__label" for="mshk-gate-password">' + eh(S["hint"]) + "</label>"
        '<input class="mshk-gate__input" id="mshk-gate-password" name="password" type="password" '
        'inputmode="numeric" autocomplete="one-time-code" maxlength="8" placeholder="'
        + eh(S["placeholder"]) + '" required autofocus>'
        '<p class="mshk-gate__err" id="mshk-gate-error" hidden></p>'
        '<button class="mshk-gate__btn" id="mshk-gate-submit" type="submit">' + eh(S["button"]) + "</button>"
        "</form>"
        '<p class="mshk-gate__note">' + eh(S["note"]).replace(
            "nastavnikmashuk@yandex.ru",
            '<a href="mailto:nastavnikmashuk@yandex.ru">nastavnikmashuk@yandex.ru</a>',
        ) + "</p>"
        '<p class="mshk-gate__dates">' + eh(S["dates"]) + "</p>"
        "</div></div>"
    )
    page = (
        "<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + eh(S["title"]) + " \u2014 " + eh(S["event"]) + "</title>\n"
        '<meta name="robots" content="noindex, nofollow">\n'
        "<style>" + APPLY_CSS + EXTRA_CSS + "</style>\n"
        "</head>\n<body>\n" + body + "\n<script>" + JS + "</script>\n</body>\n</html>\n"
    )
    out = ROOT / "static" / "cultistudgate.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out, len(page))


if __name__ == "__main__":
    main()
