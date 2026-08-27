# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
STATIC.mkdir(exist_ok=True)


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
        else:
            out.append(c)
    return "".join(out)


T = {
    "title": "\u0410\u0434\u043c\u0438\u043d\u043a\u0430 \u0437\u0430\u044f\u0432\u043e\u043a",
    "kicker": "\u041c\u0430\u0448\u0443\u043a",
    "login_lead": "\u0412\u0445\u043e\u0434 \u0434\u043b\u044f \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u043e\u0432 \u0446\u0435\u043d\u0442\u0440\u0430",
    "password": "\u041f\u0430\u0440\u043e\u043b\u044c",
    "enter": "\u0412\u043e\u0439\u0442\u0438",
    "bad": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c",
    "search": "\u041f\u043e\u0438\u0441\u043a: \u0424\u0418\u041e, email, \u0442\u0435\u043b\u0435\u0444\u043e\u043d, \u0441\u0442\u0440\u0430\u043d\u0430, \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f",
    "stream": "\u041f\u043e\u0442\u043e\u043a",
    "country": "\u0421\u0442\u0440\u0430\u043d\u0430",
    "gender": "\u041f\u043e\u043b",
    "from": "\u0421 \u0434\u0430\u0442\u044b",
    "to": "\u041f\u043e \u0434\u0430\u0442\u0443",
    "all": "\u0412\u0441\u0435",
    "reset": "\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c",
    "excel": "\u0421\u043a\u0430\u0447\u0430\u0442\u044c Excel",
    "consents": "\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u0441\u043e\u0433\u043b\u0430\u0441\u0438\u044f",
    "dl_portfolio": "\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u043f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e",
    "dl_consent": "\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u0441\u043e\u0433\u043b\u0430\u0441\u0438\u0435",
    "logout": "\u0412\u044b\u0439\u0442\u0438",
    "form1": "\u0424\u043e\u0440\u043c\u0430 1",
    "form2": "\u0424\u043e\u0440\u043c\u0430 2",
    "title_apply": "\u0424\u043e\u0440\u043c\u0430 1 \u2014 \u0417\u0430\u044f\u0432\u043a\u0430",
    "title_info": "\u0424\u043e\u0440\u043c\u0430 2 \u2014 \u0414\u0430\u043d\u043d\u044b\u0435 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432",
    "search": "\u041f\u043e\u0438\u0441\u043a: \u0424\u0418\u041e, email, \u0442\u0435\u043b\u0435\u0444\u043e\u043d, \u0441\u0442\u0440\u0430\u043d\u0430, \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f",
    "search_info": "\u041f\u043e\u0438\u0441\u043a: \u0424\u0418\u041e, \u0441\u0442\u0440\u0430\u043d\u0430, \u0433\u043e\u0440\u043e\u0434, \u043f\u043e\u0442\u043e\u043a",
    "empty": "\u0417\u0430\u044f\u0432\u043e\u043a \u043f\u043e\u043a\u0430 \u043d\u0435\u0442",
    "empty_info": "\u0410\u043d\u043a\u0435\u0442 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442",
    "count": "\u0437\u0430\u044f\u0432\u043e\u043a",
    "count_info": "\u0430\u043d\u043a\u0435\u0442",
    "th_meal": "\u041f\u0438\u0442\u0430\u043d\u0438\u0435",
    "th_visa": "\u0412\u0438\u0437\u0430",
    "th_city": "\u0413\u043e\u0440\u043e\u0434",
    "close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
    "card": "\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u0437\u0430\u044f\u0432\u043a\u0438",
    "files": "\u0424\u0430\u0439\u043b\u044b",
    "portfolio": "\u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e",
    "consent": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435",
    "no_file": "\u041d\u0435\u0442 \u0444\u0430\u0439\u043b\u0430",
    "err_file": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0441\u043a\u0430\u0447\u0430\u0442\u044c \u0444\u0430\u0439\u043b. \u0415\u0433\u043e \u043d\u0435\u0442 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0435 \u0438\u043b\u0438 \u0441\u0435\u0441\u0441\u0438\u044f \u0438\u0441\u0442\u0435\u043a\u043b\u0430.",
    "prev": "\u041d\u0430\u0437\u0430\u0434",
    "next": "\u0414\u0430\u043b\u0435\u0435",
    "of": "\u0438\u0437",
    "count": "\u0437\u0430\u044f\u0432\u043e\u043a",
    "th_id": "ID",
    "th_date": "\u0414\u0430\u0442\u0430",
    "th_fio": "\u0424\u0418\u041e",
    "th_email": "E-mail",
    "th_phone": "\u0422\u0435\u043b\u0435\u0444\u043e\u043d",
    "th_country": "\u0421\u0442\u0440\u0430\u043d\u0430",
    "th_org": "\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f",
    "th_stream": "\u041f\u043e\u0442\u043e\u043a",
}

LABELS = {
    "id": "ID",
    "created_at": T["th_date"],
    "program": "\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430",
    "fio_latin": "\u0424\u0418\u041e (passport)",
    "fio_ru": "\u0424\u0418\u041e \u0440\u0443\u0441.",
    "birth_date": "\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f",
    "gender": T["gender"],
    "country": T["country"],
    "city": "\u0413\u043e\u0440\u043e\u0434",
    "arrival": "\u041e\u0442\u043a\u0443\u0434\u0430 \u043f\u0440\u0438\u0431\u044b\u0432\u0430\u0435\u0442",
    "citizenship": "\u0413\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u043e",
    "all_citizenships": "\u0412\u0441\u0435 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u0430",
    "phone": T["th_phone"],
    "email": "E-mail",
    "messenger": "\u041c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440",
    "messenger_link": "\u0421\u0441\u044b\u043b\u043a\u0430 \u043c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440\u0430",
    "messenger_other": "\u0414\u0440\u0443\u0433\u043e\u0439 \u043c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440",
    "org_name": T["th_org"],
    "org_spec": "\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f",
    "org_location": "\u0421\u0442\u0440\u0430\u043d\u0430 \u0438 \u0433\u043e\u0440\u043e\u0434 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438",
    "position": "\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c",
    "audience": "\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0438\u044f",
    "audience_other": "\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0438\u044f (\u0434\u0440\u0443\u0433\u043e\u0435)",
    "stream": T["stream"],
    "how_learned": "\u041e\u0442\u043a\u0443\u0434\u0430 \u0443\u0437\u043d\u0430\u043b",
    "intl_programs": "\u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b",
    "intl_details": "\u0414\u0435\u0442\u0430\u043b\u0438 \u043c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0445 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c",
    "ru_programs": "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0438\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b",
    "ru_details": "\u0414\u0435\u0442\u0430\u043b\u0438 \u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0438\u0445 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c",
    "why": "\u041f\u043e\u0447\u0435\u043c\u0443 \u0432\u0430\u0436\u043d\u043e \u0443\u0447\u0430\u0441\u0442\u0438\u0435",
    "coop": "\u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043f\u043e \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u0447\u0435\u0441\u0442\u0432\u0443",
    "mentor": "\u041d\u0430\u0441\u0442\u0430\u0432\u043d\u0438\u043a",
    "directions": "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f",
    "directions_other": "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 (\u0434\u0440\u0443\u0433\u043e\u0435)",
    "address": "\u0410\u0434\u0440\u0435\u0441 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438",
    "passport_series": "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u0441\u0435\u0440\u0438\u044f",
    "passport_number": "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u043d\u043e\u043c\u0435\u0440",
    "passport_date": "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u0434\u0430\u0442\u0430",
    "passport_issued": "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u043a\u0435\u043c \u0432\u044b\u0434\u0430\u043d",
}

LABELS_INFO = {
    "id": "ID",
    "created_at": T["th_date"],
    "fio_latin": "\u0424\u0418\u041e",
    "health_limits": "\u041e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u0438\u044f \u043f\u043e \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044e",
    "meal_type": T["th_meal"],
    "id_doc_type": "\u0422\u0438\u043f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430",
    "id_doc_series": "\u0421\u0435\u0440\u0438\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430",
    "id_doc_number": "\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430",
    "id_doc_issued": "\u0414\u0430\u0442\u0430 \u0432\u044b\u0434\u0430\u0447\u0438",
    "id_doc_valid_from": "\u0421\u0440\u043e\u043a \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u0441",
    "id_doc_valid_to": "\u0421\u0440\u043e\u043a \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043f\u043e",
    "id_doc_issuer": "\u041a\u0435\u043c \u0432\u044b\u0434\u0430\u043d",
    "entry_doc_name": "\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442 \u0434\u043b\u044f \u0432\u044a\u0435\u0437\u0434\u0430 \u0432 \u0420\u0424",
    "entry_doc_series": "\u0412\u044a\u0435\u0437\u0434: \u0441\u0435\u0440\u0438\u044f",
    "entry_doc_number": "\u0412\u044a\u0435\u0437\u0434: \u043d\u043e\u043c\u0435\u0440",
    "entry_doc_issued": "\u0412\u044a\u0435\u0437\u0434: \u0434\u0430\u0442\u0430 \u0432\u044b\u0434\u0430\u0447\u0438",
    "entry_doc_valid_from": "\u0412\u044a\u0435\u0437\u0434: \u0441\u0440\u043e\u043a \u0441",
    "entry_doc_valid_to": "\u0412\u044a\u0435\u0437\u0434: \u0441\u0440\u043e\u043a \u043f\u043e",
    "entry_doc_issuer": "\u0412\u044a\u0435\u0437\u0434: \u043a\u0435\u043c \u0432\u044b\u0434\u0430\u043d",
    "stream": T["stream"],
    "depart_country": "\u0421\u0442\u0440\u0430\u043d\u0430 \u043e\u0442\u044a\u0435\u0437\u0434\u0430",
    "depart_city": "\u0413\u043e\u0440\u043e\u0434 \u043e\u0442\u044a\u0435\u0437\u0434\u0430",
    "return_ticket": "\u041e\u0431\u0440\u0430\u0442\u043d\u044b\u0439 \u0431\u0438\u043b\u0435\u0442",
    "baggage": "\u0411\u0430\u0433\u0430\u0436",
    "visa_needed": "\u0412\u0438\u0437\u0430 \u0432 \u0420\u0424",
    "transit_visa": "\u0422\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u0430\u044f \u0432\u0438\u0437\u0430",
    "agree_tickets": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435: \u0431\u0438\u043b\u0435\u0442\u044b \u0431\u0435\u0437 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430",
    "agree_notice": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435: \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0435 \u0437\u0430 10 \u0434\u043d\u0435\u0439",
    "agree_truth": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435: \u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\u043e\u0441\u0442\u044c",
    "agree_extra_docs": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435: \u0434\u043e\u043f. \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b",
    "agree_refusal": "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435: \u043e\u0442\u043a\u0430\u0437 \u043f\u0440\u0438 \u0442\u0440\u0443\u0434\u043d\u043e\u0441\u0442\u044f\u0445 \u0432\u044a\u0435\u0437\u0434\u0430",
}

JS_I18N = json.dumps(T, ensure_ascii=True)
JS_LABELS = json.dumps(LABELS, ensure_ascii=True)
JS_LABELS_INFO = json.dumps(LABELS_INFO, ensure_ascii=True)

CSS = r"""
@import url("https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700&display=swap");
:root{--navy:#223f9a;--sky:#54a4db;--ink:#332d24;--paper:#fafafa;--gold:#a2855f;--sans:"Geologica",Verdana,system-ui,sans-serif}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--navy)}
.wrap{width:min(1280px,calc(100% - 32px));margin:0 auto;padding:28px 0 64px}
.kicker{margin:0 0 8px;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
h1{margin:0 0 18px;font-size:clamp(28px,4vw,40px);color:var(--navy);letter-spacing:-.03em}
.card{background:#fff;border:1px solid rgba(34,63,154,.08);border-radius:20px;box-shadow:0 10px 40px rgba(34,63,154,.06)}
.login{max-width:420px;margin:12vh auto 0;padding:28px}
.login p{margin:0 0 18px;font-weight:300}
label{display:block;margin:0 0 6px;font-size:13px;font-weight:500}
input,select{width:100%;padding:11px 12px;border:1px solid rgba(34,63,154,.18);border-radius:12px;background:var(--paper);font:inherit}
.btn{appearance:none;border:0;cursor:pointer;min-height:44px;padding:0 18px;border-radius:999px;font:inherit;font-weight:500}
.btn-navy{background:var(--navy);color:#fff}
.btn-gold{background:var(--gold);color:#fff}
.btn-ghost{background:transparent;color:var(--navy);border:1px solid rgba(34,63,154,.2)}
.btn-on{background:var(--navy);color:#fff}
.btn-off{background:#fff;color:var(--navy);border:1px solid rgba(34,63,154,.2)}
.err{color:#9a2233;font-size:13px;min-height:18px}
.top{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;justify-content:space-between;margin-bottom:16px}
.filters{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr auto;gap:10px;padding:16px;margin-bottom:14px}
.table-wrap{overflow:auto}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:12px 14px;text-align:left;border-bottom:1px solid rgba(34,63,154,.08);vertical-align:top}
th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--navy);cursor:pointer;white-space:nowrap;user-select:none}
tr.row{cursor:pointer}
tr.row:hover{background:rgba(34,63,154,.04)}
.pager{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:14px 16px}
.drawer-bg{position:fixed;inset:0;background:rgba(10,16,20,.35);display:none;z-index:20}
.drawer{position:fixed;top:0;right:0;height:100%;width:min(640px,100%);background:#fff;overflow:auto;z-index:21;transform:translateX(110%);transition:transform .35s cubic-bezier(.22,1,.36,1);box-shadow:-20px 0 40px rgba(10,16,20,.12)}
.drawer.open{transform:none}
.drawer-bg.show{display:block}
.drawer-in{padding:28px 24px 80px}
.kv{margin:0 0 14px}
.kv b{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);margin-bottom:4px}
.kv span{white-space:pre-wrap;font-weight:300;line-height:1.5}
.drawer .btn{display:inline-flex;align-items:center;margin:8px 8px 0 0;text-decoration:none}
.hidden{display:none!important}
@media(max-width:960px){.filters{grid-template-columns:1fr 1fr}}
"""

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{eh(T['title'])}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div id="login-view" class="card login">
    <p class="kicker">{eh(T['kicker'])}</p>
    <h1>{eh(T['title'])}</h1>
    <p>{eh(T['login_lead'])}</p>
    <label for="password">{eh(T['password'])}</label>
    <input id="password" type="password" autocomplete="current-password">
    <p class="err" id="login-err"></p>
    <button class="btn btn-navy" id="login-btn" type="button">{eh(T['enter'])}</button>
  </div>

  <div id="app-view" class="hidden">
    <div class="top">
      <div>
        <p class="kicker">{eh(T['kicker'])}</p>
        <h1 id="page-title">{eh(T['title_apply'])}</h1>
        <p id="count-line"></p>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-on" id="form-apply" type="button">{eh(T['form1'])}</button>
        <button class="btn btn-off" id="form-info" type="button">{eh(T['form2'])}</button>
        <button class="btn btn-gold" id="excel-btn" type="button">{eh(T['excel'])}</button>
        <button class="btn btn-navy" id="consents-btn" type="button">{eh(T['consents'])}</button>
        <button class="btn btn-ghost" id="logout-btn" type="button">{eh(T['logout'])}</button>
      </div>
    </div>
    <div class="card filters">
      <input id="f-q" placeholder="{eh(T['search'])}">
      <select id="f-stream"><option value="">{eh(T['stream'])}: {eh(T['all'])}</option></select>
      <select id="f-country"><option value="">{eh(T['country'])}: {eh(T['all'])}</option></select>
      <span id="f-gender-wrap"><select id="f-gender"><option value="">{eh(T['gender'])}: {eh(T['all'])}</option></select></span>
      <input id="f-from" type="date" title="{eh(T['from'])}">
      <input id="f-to" type="date" title="{eh(T['to'])}">
      <button class="btn btn-ghost" id="reset-btn" type="button">{eh(T['reset'])}</button>
    </div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead id="thead">
            <tr>
              <th data-sort="id">{eh(T['th_id'])}</th>
              <th data-sort="created_at">{eh(T['th_date'])}</th>
              <th data-sort="fio_latin">{eh(T['th_fio'])}</th>
              <th data-sort="email">{eh(T['th_email'])}</th>
              <th data-sort="phone">{eh(T['th_phone'])}</th>
              <th data-sort="country">{eh(T['th_country'])}</th>
              <th data-sort="org_name">{eh(T['th_org'])}</th>
              <th data-sort="stream">{eh(T['th_stream'])}</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
      <div class="pager">
        <button class="btn btn-ghost" id="prev-btn" type="button">{eh(T['prev'])}</button>
        <span id="page-line"></span>
        <button class="btn btn-ghost" id="next-btn" type="button">{eh(T['next'])}</button>
      </div>
    </div>
  </div>
</div>
<div class="drawer-bg" id="drawer-bg"></div>
<aside class="drawer" id="drawer">
  <div class="drawer-in">
    <p class="kicker">{eh(T['card'])}</p>
    <h1 id="card-title"></h1>
    <div id="card-body"></div>
    <p style="margin-top:20px"><button class="btn btn-ghost" id="close-btn" type="button">{eh(T['close'])}</button></p>
  </div>
</aside>
<script>
(function(){{
  var T = {JS_I18N};
  var LABELS = {JS_LABELS};
  var LABELS_INFO = {JS_LABELS_INFO};
  var state = {{ page:1, sort:"created_at", order:"desc", form:"apply" }};
  var loadSeq = 0;
  var ignoreFilterChange = false;
  var loginView = document.getElementById("login-view");
  var appView = document.getElementById("app-view");
  function qs(){{
    var p = new URLSearchParams();
    p.set("q", document.getElementById("f-q").value.trim());
    p.set("stream", document.getElementById("f-stream").value);
    p.set("country", document.getElementById("f-country").value);
    p.set("gender", document.getElementById("f-gender").value);
    p.set("date_from", document.getElementById("f-from").value);
    p.set("date_to", document.getElementById("f-to").value);
    p.set("sort", state.sort);
    p.set("order", state.order);
    p.set("page", String(state.page));
    p.set("limit", "50");
    return p.toString();
  }}
  function fmtDate(s){{
    if (!s) return "";
    return String(s).replace("T", " ").slice(0, 16);
  }}
  function fmtVal(v){{
    if (v == null || v === "") return "—";
    if (Array.isArray(v)) return v.join(", ") || "—";
    if (typeof v === "object") return JSON.stringify(v);
    return String(v);
  }}
  function api(url, opts){{
    opts = opts || {{}};
    opts.credentials = "include";
    opts.headers = Object.assign({{"Accept":"application/json"}}, opts.headers || {{}});
    return fetch(url, opts).then(function(r){{
      if (r.status === 401) throw new Error("auth");
      if (!r.ok) throw new Error("bad");
      var ct = r.headers.get("content-type") || "";
      if (ct.indexOf("json") >= 0) return r.json();
      return r;
    }});
  }}
  function showApp(){{
    loginView.classList.add("hidden");
    appView.classList.remove("hidden");
    try {{
      var saved = sessionStorage.getItem("mshk-admin-form");
      if (saved === "info" || saved === "apply") state.form = saved;
    }} catch (e) {{}}
    setForm(state.form, true);
  }}
  function showLogin(){{
    appView.classList.add("hidden");
    loginView.classList.remove("hidden");
  }}
  function isInfo(){{ return state.form === "info"; }}
  function clearFilters(){{
    ignoreFilterChange = true;
    document.getElementById("f-q").value = "";
    document.getElementById("f-stream").value = "";
    document.getElementById("f-country").value = "";
    document.getElementById("f-gender").value = "";
    document.getElementById("f-from").value = "";
    document.getElementById("f-to").value = "";
    ignoreFilterChange = false;
  }}
  function setForm(form, skipReset){{
    var next = form === "info" ? "info" : "apply";
    if (!skipReset && next === state.form) return;
    state.form = next;
    try {{ sessionStorage.setItem("mshk-admin-form", state.form); }} catch (e) {{}}
    document.getElementById("form-apply").className = "btn " + (isInfo() ? "btn-off" : "btn-on");
    document.getElementById("form-info").className = "btn " + (isInfo() ? "btn-on" : "btn-off");
    document.getElementById("page-title").textContent = isInfo() ? T.title_info : T.title_apply;
    document.getElementById("f-q").placeholder = isInfo() ? T.search_info : T.search;
    document.getElementById("f-gender-wrap").style.display = isInfo() ? "none" : "";
    document.getElementById("consents-btn").style.display = isInfo() ? "none" : "";
    if (!skipReset) {{
      state.page = 1;
      state.sort = "created_at";
      state.order = "desc";
      clearFilters();
      closeCard();
    }}
    renderHead();
    document.getElementById("tbody").innerHTML = "";
    loadSeq += 1;
    loadMeta(loadSeq);
    loadList(loadSeq);
  }}
  function renderHead(){{
    var head = document.getElementById("thead");
    var cols = isInfo()
      ? [["id", T.th_id],["created_at", T.th_date],["fio_latin", T.th_fio],["meal_type", T.th_meal],["depart_country", T.th_country],["depart_city", T.th_city],["visa_needed", T.th_visa],["stream", T.th_stream]]
      : [["id", T.th_id],["created_at", T.th_date],["fio_latin", T.th_fio],["email", T.th_email],["phone", T.th_phone],["country", T.th_country],["org_name", T.th_org],["stream", T.th_stream]];
    var html = "<tr>";
    cols.forEach(function(c){{
      html += '<th data-sort="' + c[0] + '" data-label="' + c[1] + '">' + c[1] + "</th>";
    }});
    html += "</tr>";
    head.innerHTML = html;
  }}
  function loadMeta(seq){{
    var form = state.form;
    seq = seq || loadSeq;
    api("/admin/api/meta?form=" + form).then(function(m){{
      if (seq !== loadSeq || state.form !== form) return;
      fillSelect("f-stream", m.streams, T.stream);
      fillSelect("f-country", m.countries, T.country);
      if (form !== "info") fillSelect("f-gender", m.genders, T.gender);
    }}).catch(function(){{}});
  }}
  function fillSelect(id, items, label){{
    var el = document.getElementById(id);
    var cur = el.value;
    ignoreFilterChange = true;
    el.innerHTML = "";
    var o0 = document.createElement("option");
    o0.value = ""; o0.textContent = label + ": " + T.all;
    el.appendChild(o0);
    (items || []).forEach(function(v){{
      var o = document.createElement("option");
      o.value = v; o.textContent = v; el.appendChild(o);
    }});
    el.value = cur;
    if (el.value !== cur) el.value = "";
    ignoreFilterChange = false;
  }}
  function loadList(seq){{
    seq = seq || loadSeq;
    var form = state.form;
    var info = form === "info";
    document.querySelectorAll("th[data-sort]").forEach(function(th){{
      var key = th.getAttribute("data-sort");
      var base = th.getAttribute("data-label") || th.textContent.replace(/ [\\u25B2\\u25BC]$/, "");
      th.setAttribute("data-label", base);
      var mark = "";
      if (state.sort === key) mark = state.order === "asc" ? " \\u25B2" : " \\u25BC";
      th.textContent = base + mark;
    }});
    var url = info ? "/admin/api/participants?" : "/admin/api/applications?";
    api(url + qs()).then(function(data){{
      if (seq !== loadSeq || state.form !== form) return;
      var tb = document.getElementById("tbody");
      tb.innerHTML = "";
      document.getElementById("count-line").textContent = (data.total || 0) + " " + (info ? T.count_info : T.count);
      document.getElementById("page-line").textContent = data.page + " / " + data.pages;
      document.getElementById("prev-btn").disabled = data.page <= 1;
      document.getElementById("next-btn").disabled = data.page >= data.pages;
      if (!data.items.length){{
        var tr = document.createElement("tr");
        tr.innerHTML = '<td colspan="8">' + (info ? T.empty_info : T.empty) + "</td>";
        tb.appendChild(tr);
        return;
      }}
      data.items.forEach(function(it){{
        var tr = document.createElement("tr");
        tr.className = "row";
        if (info) {{
          tr.innerHTML =
            "<td>" + it.id + "</td>" +
            "<td>" + fmtDate(it.created_at) + "</td>" +
            "<td><b>" + esc(it.fio_latin||"") + "</b></td>" +
            "<td>" + esc(it.meal_type||"") + "</td>" +
            "<td>" + esc(it.depart_country||"") + "</td>" +
            "<td>" + esc(it.depart_city||"") + "</td>" +
            "<td>" + esc(it.visa_needed||"") + "</td>" +
            "<td>" + esc(it.stream||"") + "</td>";
        }} else {{
          tr.innerHTML =
            "<td>" + it.id + "</td>" +
            "<td>" + fmtDate(it.created_at) + "</td>" +
            "<td><b>" + esc(it.fio_latin||"") + "</b><br><span style='color:#7a7368'>" + esc(it.fio_ru||"") + "</span></td>" +
            "<td>" + esc(it.email||"") + "</td>" +
            "<td>" + esc(it.phone||"") + "</td>" +
            "<td>" + esc(it.country||"") + "<br>" + esc(it.city||"") + "</td>" +
            "<td>" + esc(it.org_name||"") + "</td>" +
            "<td>" + esc(it.stream||"") + "</td>";
        }}
        tr.addEventListener("click", function(){{ openCard(it.id); }});
        tb.appendChild(tr);
      }});
    }}).catch(function(e){{
      if (seq !== loadSeq) return;
      if (e.message === "auth") showLogin();
    }});
  }}
  function esc(s){{
    return String(s).replace(/[&<>"]/g, function(c){{
      return ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}})[c];
    }});
  }}
  function filenameFrom(r, fallback){{
    var cd = r.headers.get("content-disposition") || "";
    var star = /filename\\*=UTF-8''([^;]+)/i.exec(cd);
    if (star) {{
      try {{ return decodeURIComponent(star[1]); }} catch (e) {{}}
    }}
    var plain = /filename="([^"]+)"/i.exec(cd);
    if (plain) return plain[1];
    return fallback;
  }}
  function saveBlob(url, fallbackName){{
    return fetch(url, {{credentials:"include"}}).then(function(r){{
      var ct = (r.headers.get("content-type") || "").toLowerCase();
      if (!r.ok || ct.indexOf("json") >= 0 || ct.indexOf("text/html") >= 0) {{
        return r.text().then(function(t){{
          var msg = T.err_file;
          try {{
            var j = JSON.parse(t);
            if (j && j.detail) msg = typeof j.detail === "string" ? j.detail : T.err_file;
          }} catch (e) {{}}
          alert(msg);
        }});
      }}
      return r.blob().then(function(blob){{
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = filenameFrom(r, fallbackName);
        document.body.appendChild(a);
        a.click();
        setTimeout(function(){{ URL.revokeObjectURL(a.href); a.remove(); }}, 1500);
      }});
    }}).catch(function(){{ alert(T.err_file); }});
  }}
  function openCard(id){{
    var form = state.form;
    var url = form === "info" ? "/admin/api/participants/" : "/admin/api/applications/";
    api(url + id).then(function(it){{
      if (state.form !== form) return;
      document.getElementById("card-title").textContent = it.fio_latin || ("#" + it.id);
      var labels = form === "info" ? LABELS_INFO : LABELS;
      var skip = {{payload_raw:1, has_portfolio:1, has_consent:1, portfolio_url:1, consent_url:1}};
      var html = "";
      Object.keys(labels).forEach(function(k){{
        if (skip[k]) return;
        html += '<div class="kv"><b>' + esc(labels[k]) + "</b><span>" + esc(fmtVal(it[k])) + "</span></div>";
      }});
      if (form !== "info") {{
        html += '<div class="kv"><b>' + T.files + "</b><span>";
        if (it.has_portfolio) html += '<button class="btn btn-navy" type="button" data-dl="/admin/api/applications/' + id + '/file/portfolio" data-name="portfolio.pdf">' + T.dl_portfolio + "</button> ";
        else html += T.portfolio + ": " + T.no_file + "<br>";
        if (it.has_consent) html += '<button class="btn btn-navy" type="button" data-dl="/admin/api/applications/' + id + '/file/consent" data-name="consent.pdf">' + T.dl_consent + "</button>";
        else html += T.consent + ": " + T.no_file;
        html += "</span></div>";
      }}
      document.getElementById("card-body").innerHTML = html;
      document.getElementById("drawer").classList.add("open");
      document.getElementById("drawer-bg").classList.add("show");
    }});
  }}
  function closeCard(){{
    document.getElementById("drawer").classList.remove("open");
    document.getElementById("drawer-bg").classList.remove("show");
  }}
  document.getElementById("login-btn").onclick = function(){{
    var pwd = document.getElementById("password").value;
    fetch("/admin/api/login", {{
      method:"POST", credentials:"include",
      headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify({{password: pwd}})
    }}).then(function(r){{
      if (!r.ok) throw new Error("bad");
      document.getElementById("login-err").textContent = "";
      showApp();
    }}).catch(function(){{
      document.getElementById("login-err").textContent = T.bad;
    }});
  }};
  document.getElementById("password").addEventListener("keydown", function(e){{
    if (e.key === "Enter") document.getElementById("login-btn").click();
  }});
  document.getElementById("logout-btn").onclick = function(){{
    fetch("/admin/api/logout", {{method:"POST", credentials:"include"}}).finally(showLogin);
  }};
  document.getElementById("excel-btn").onclick = function(){{
    var path = isInfo() ? "/admin/api/participants/export.xlsx?" : "/admin/api/applications/export.xlsx?";
    var name = isInfo() ? "mashuk_uchastniki.xlsx" : "mashuk_zayavki.xlsx";
    saveBlob(path + qs(), name);
  }};
  document.getElementById("consents-btn").onclick = function(){{
    saveBlob("/admin/api/consents.zip?" + qs(), "mashuk_soglasia.zip");
  }};
  document.getElementById("card-body").addEventListener("click", function(e){{
    var b = e.target.closest("[data-dl]");
    if (!b) return;
    saveBlob(b.getAttribute("data-dl"), b.getAttribute("data-name") || "file");
  }});
  document.getElementById("form-apply").onclick = function(){{ setForm("apply"); }};
  document.getElementById("form-info").onclick = function(){{ setForm("info"); }};
  ["f-stream","f-country","f-gender","f-from","f-to"].forEach(function(id){{
    document.getElementById(id).addEventListener("change", function(){{
      if (ignoreFilterChange) return;
      state.page = 1;
      loadList();
    }});
  }});
  var qTimer = null;
  document.getElementById("f-q").addEventListener("input", function(){{
    clearTimeout(qTimer);
    qTimer = setTimeout(function(){{ state.page = 1; loadList(); }}, 350);
  }});
  document.getElementById("f-q").addEventListener("keydown", function(e){{
    if (e.key === "Enter") {{ state.page = 1; loadList(); }}
  }});
  document.getElementById("reset-btn").onclick = function(){{
    document.getElementById("f-q").value = "";
    document.getElementById("f-stream").value = "";
    document.getElementById("f-country").value = "";
    document.getElementById("f-gender").value = "";
    document.getElementById("f-from").value = "";
    document.getElementById("f-to").value = "";
    state.page = 1;
    state.sort = "created_at";
    state.order = "desc";
    loadList();
  }};
  document.getElementById("prev-btn").onclick = function(){{ if (state.page>1){{ state.page--; loadList(); }} }};
  document.getElementById("next-btn").onclick = function(){{ state.page++; loadList(); }};
  document.getElementById("thead").addEventListener("click", function(e){{
    var th = e.target.closest("th[data-sort]");
    if (!th) return;
    var key = th.getAttribute("data-sort");
    if (state.sort === key) state.order = state.order === "asc" ? "desc" : "asc";
    else {{ state.sort = key; state.order = "asc"; }}
    state.page = 1;
    loadList();
  }});
  document.getElementById("close-btn").onclick = closeCard;
  document.getElementById("drawer-bg").onclick = closeCard;
  api("/admin/api/me").then(showApp).catch(showLogin);
}})();
</script>
</body>
</html>
"""

(STATIC / "admin.html").write_text(html, encoding="utf-8")
print("wrote", STATIC / "admin.html", len(html))
