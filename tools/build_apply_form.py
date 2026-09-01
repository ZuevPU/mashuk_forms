# -*- coding: utf-8 -*-
from pathlib import Path
import json
from form_strings import S

ROOT = Path(__file__).resolve().parent.parent


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


def field(name, label, hint="", typ="text", required=True, area=False, extra=""):
    req = " required" if required else ""
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + "</p>") if hint else ""
    lab = '<label class="mshk-apply__label" for="' + name + '">' + eh(label) + "</label>"
    if area:
        ctrl = (
            '<textarea class="mshk-apply__input mshk-apply__area" id="'
            + name
            + '" name="'
            + name
            + '" rows="4"'
            + req
            + extra
            + "></textarea>"
        )
    else:
        ctrl = (
            '<input class="mshk-apply__input" id="'
            + name
            + '" name="'
            + name
            + '" type="'
            + typ
            + '"'
            + req
            + extra
            + ">"
        )
    return (
        '<div class="mshk-apply__field" data-field="'
        + name
        + '">'
        + lab
        + ctrl
        + hid
        + '<p class="mshk-apply__err" hidden></p></div>'
    )


def radios(name, label, options, hint=""):
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + "</p>") if hint else ""
    items = []
    for val, txt in options:
        items.append(
            '<label class="mshk-apply__choice"><input type="radio" name="'
            + name
            + '" value="'
            + eh(val)
            + '" required><span>'
            + eh(txt)
            + "</span></label>"
        )
    return (
        '<fieldset class="mshk-apply__field" data-field="'
        + name
        + '"><legend class="mshk-apply__label">'
        + eh(label)
        + "</legend>"
        + hid
        + '<div class="mshk-apply__choices">'
        + "".join(items)
        + '</div><p class="mshk-apply__err" hidden></p></fieldset>'
    )


def checks(name, label, options, hint="", extra_cls=""):
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + "</p>") if hint else ""
    items = []
    for val, txt in options:
        items.append(
            '<label class="mshk-apply__choice"><input type="checkbox" name="'
            + name
            + '" value="'
            + eh(val)
            + '"><span>'
            + eh(txt)
            + "</span></label>"
        )
    return (
        '<fieldset class="mshk-apply__field '
        + extra_cls
        + '" data-field="'
        + name
        + '"><legend class="mshk-apply__label">'
        + eh(label)
        + "</legend>"
        + hid
        + '<div class="mshk-apply__choices">'
        + "".join(items)
        + '</div><p class="mshk-apply__err" hidden></p></fieldset>'
    )


def file_box(name, label, hint, accept, note_id):
    return (
        '<div class="mshk-apply__field" data-field="'
        + name
        + '"><p class="mshk-apply__label">'
        + eh(label)
        + '</p><p class="mshk-apply__hint">'
        + eh(hint)
        + '</p><label class="mshk-apply__drop"><input type="file" id="'
        + name
        + '" name="'
        + name
        + '" accept="'
        + accept
        + '" hidden><span class="mshk-apply__drop-btn">'
        + h("upload")
        + '</span><span class="mshk-apply__drop-name" id="'
        + note_id
        + '">PDF, max 20 MB</span></label><p class="mshk-apply__err" hidden></p></div>'
    )


CSS = r"""
@import url("https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap");
html,body{margin:0;padding:0;max-width:100%;overflow-x:hidden;background:#fafafa}
#mshk-apply{--navy:#223f9a;--sky:#54a4db;--stone:#dcdedd;--ink:#332d24;--black:#0a1014;--paper:#fafafa;--white:#fff;--gold:#a2855f;--sans:"Geologica",Verdana,system-ui,sans-serif;--serif:"Noto Serif","Times New Roman",serif;--ease:cubic-bezier(.22,1,.36,1);--pad:clamp(16px,4vw,48px);position:relative;isolation:isolate;overflow:hidden;box-sizing:border-box;width:100%;max-width:100%;margin:0;padding:clamp(28px,5vw,56px) 0 12px;color:var(--ink);background-color:var(--paper);background-image:radial-gradient(ellipse 70% 55% at 8% 12%,rgba(84,164,219,.16),transparent 58%),radial-gradient(ellipse 55% 50% at 92% 8%,rgba(34,63,154,.12),transparent 52%),radial-gradient(ellipse 50% 45% at 78% 88%,rgba(162,133,95,.11),transparent 55%);font-family:var(--sans);-webkit-font-smoothing:antialiased}
#mshk-apply *,#mshk-apply *::before,#mshk-apply *::after,#mshk-form *,#mshk-form *::before,#mshk-form *::after{box-sizing:border-box}
#mshk-apply a,#mshk-form a{color:var(--navy);text-decoration:none}
#mshk-form{--navy:#223f9a;--sky:#54a4db;--stone:#dcdedd;--ink:#332d24;--black:#0a1014;--paper:#fafafa;--white:#fff;--gold:#a2855f;--sans:"Geologica",Verdana,system-ui,sans-serif;--serif:"Noto Serif","Times New Roman",serif;--ease:cubic-bezier(.22,1,.36,1);--pad:clamp(16px,4vw,48px);position:relative;isolation:isolate;overflow:hidden;box-sizing:border-box;width:100%;max-width:100%;margin:0;padding:8px 0 32px;color:var(--ink);background:var(--paper);font-family:var(--sans);-webkit-font-smoothing:antialiased}
#mshk-apply{padding-bottom:12px}
.mshk-apply__geo{position:absolute;border:1px solid rgba(34,63,154,.12);border-radius:50%;pointer-events:none;z-index:0}
.mshk-apply__geo--lg{width:min(58vw,640px);height:min(58vw,640px);top:-18%;right:-8%}
.mshk-apply__geo--sm{width:min(28vw,280px);height:min(28vw,280px);bottom:8%;left:-6%}
.mshk-apply__shell{position:relative;z-index:1;width:calc(100% - var(--pad)*2);max-width:none;margin:0 auto;box-sizing:border-box}
.mshk-apply__title,.mshk-apply__p,.mshk-apply__lead,.mshk-apply__hint,.mshk-apply__choice span,.mshk-apply__chip,.mshk-apply__wave span{overflow-wrap:break-word;word-wrap:break-word}
.mshk-apply__kicker{margin:0 0 12px;font-size:12px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);font-family:var(--sans)!important}
.mshk-apply__title{margin:0 0 18px;font-size:clamp(28px,4.6vw,48px);font-weight:600;line-height:1.08;letter-spacing:-.03em;color:var(--navy);font-family:var(--sans)!important}
.mshk-apply__title span{display:block;font-weight:400;color:var(--ink);font-size:.62em;letter-spacing:-.02em;margin-bottom:8px}
.mshk-apply__lead{margin:0 0 16px;font-family:var(--serif)!important;font-size:clamp(16px,1.4vw,19px);font-style:italic;line-height:1.55;color:var(--ink)}
.mshk-apply__p{margin:0 0 14px;font-size:15px;font-weight:300;line-height:1.65;color:var(--ink);font-family:var(--sans)!important}
.mshk-apply__meta{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:22px 0}
.mshk-apply__chip{padding:12px 14px;background:var(--white);border:1px solid rgba(34,63,154,.1);border-radius:14px;font-size:13px;line-height:1.35;color:var(--navy);font-family:var(--sans)!important}
.mshk-apply__chip--wide{grid-column:1 / -1}
.mshk-apply__waves{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:8px 0 22px}
.mshk-apply__wave{padding:14px 16px;background:var(--white);border-radius:16px;border:1px solid rgba(34,63,154,.08);box-shadow:0 1px 2px rgba(10,16,20,.04)}
.mshk-apply__wave b{display:block;margin:0 0 4px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:500;font-family:var(--sans)!important}
.mshk-apply__wave span{font-size:13px;line-height:1.4;color:var(--ink);font-family:var(--sans)!important}
.mshk-apply__note{margin:0 0 12px;padding:14px 16px;border-left:3px solid var(--gold);background:rgba(162,133,95,.08);border-radius:0 12px 12px 0;font-size:14px;line-height:1.5;font-family:var(--sans)!important}
.mshk-apply__fin{margin:22px 0 28px;padding:22px 22px 8px;background:var(--white);border-radius:20px;border:1px solid rgba(34,63,154,.08)}
.mshk-apply__fin h3{margin:0 0 10px;font-size:16px;color:var(--navy);font-family:var(--sans)!important}
.mshk-apply__fin p,.mshk-apply__fin li{font-size:14px;font-weight:300;line-height:1.55;font-family:var(--sans)!important}
.mshk-apply__fin ul{margin:8px 0 16px;padding:0 0 0 18px}
.mshk-apply__steps{display:flex;gap:8px;margin:0 0 22px;padding:0;list-style:none}
.mshk-apply__steps li{flex:1;height:4px;border-radius:99px;background:rgba(34,63,154,.12)}
.mshk-apply__steps li.is-on{background:var(--navy)}
.mshk-apply__step-label{margin:0 0 18px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--navy);font-family:var(--sans)!important}
.mshk-apply__card{padding:clamp(20px,4vw,32px);background:var(--white);border-radius:24px;border:1px solid rgba(34,63,154,.08);box-shadow:0 10px 40px rgba(34,63,154,.06)}
.mshk-apply__pane[hidden]{display:none!important}
.mshk-apply__label,.mshk-apply__field legend{display:block;margin:0 0 8px;font-size:14px;font-weight:500;color:var(--ink);font-family:var(--sans)!important}
.mshk-apply__field{margin:0 0 18px;padding:0;border:0;min-width:0}
.mshk-apply__hint{margin:8px 0 0;font-size:13px;font-weight:300;line-height:1.45;color:rgba(51,45,36,.65);font-family:var(--sans)!important}
.mshk-apply__err{margin:6px 0 0;font-size:13px;color:#9a2233;font-family:var(--sans)!important}
.mshk-apply__input,.mshk-apply__area{width:100%;padding:12px 14px;border:1px solid rgba(34,63,154,.18);border-radius:12px;background:var(--paper);color:var(--black);font-size:15px;font-family:var(--sans)!important;outline:none;transition:border-color .2s var(--ease),box-shadow .2s var(--ease)}
.mshk-apply__area{min-height:120px;resize:vertical}
.mshk-apply__input:focus,.mshk-apply__area:focus{border-color:var(--navy);box-shadow:0 0 0 4px rgba(34,63,154,.12);background:var(--white)}
.mshk-apply__choices{display:flex;flex-direction:column;gap:8px}
.mshk-apply__choice{display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid rgba(34,63,154,.1);border-radius:12px;cursor:pointer;font-size:14px;line-height:1.4;font-family:var(--sans)!important}
.mshk-apply__choice:hover{border-color:rgba(34,63,154,.28);background:rgba(34,63,154,.03)}
.mshk-apply__choice:has(input:checked){border-color:var(--navy);background:rgba(34,63,154,.06)}
.mshk-apply__choice input{margin-top:3px;accent-color:var(--navy)}
.mshk-apply__row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.mshk-apply__nav{display:flex;justify-content:space-between;gap:12px;margin-top:8px}
.mshk-apply__btn{appearance:none;border:0;cursor:pointer;min-height:48px;padding:0 22px;border-radius:999px;font-size:15px;font-weight:500;font-family:var(--sans)!important;transition:transform .2s var(--ease),background .2s}
.mshk-apply__btn:hover{transform:translateY(-1px)}
.mshk-apply__btn--ghost{background:transparent;color:var(--navy);border:1px solid rgba(34,63,154,.2)}
.mshk-apply__btn--navy{background:var(--navy);color:#fff}
.mshk-apply__btn--gold{background:var(--gold);color:#fff}
.mshk-apply__drop{display:flex;align-items:center;gap:14px;padding:16px;border:1px dashed rgba(34,63,154,.28);border-radius:16px;background:rgba(34,63,154,.03);cursor:pointer}
.mshk-apply__drop-btn{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;background:var(--navy);color:#fff;font-size:14px;font-family:var(--sans)!important}
.mshk-apply__drop-name{font-size:13px;color:rgba(51,45,36,.7);font-family:var(--sans)!important}
.mshk-apply__consent{margin:0 0 20px;padding:18px 18px 8px;border-radius:18px;background:rgba(34,63,154,.05);border:1px solid rgba(34,63,154,.08)}
.mshk-apply__ok{padding:28px;text-align:center}
.mshk-apply__ok h3{margin:0 0 10px;color:var(--navy);font-family:var(--sans)!important}
.mshk-apply__count{margin:6px 0 0;font-size:12px;color:rgba(51,45,36,.55);font-family:var(--sans)!important;text-align:right}
.mshk-apply__links{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 16px}
html.mshk-embed,html.mshk-embed body{width:100%;max-width:100%;height:100%;max-height:100%;overflow:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:manipulation}
html.mshk-embed #mshk-apply,html.mshk-embed #mshk-form{width:100%;max-width:100%;box-sizing:border-box}
html.mshk-embed #mshk-apply{padding:12px 0 8px}
html.mshk-embed #mshk-form{padding:4px 0 24px}
html.mshk-embed .mshk-apply__shell{width:calc(100% - 24px);max-width:none}
html.mshk-embed .mshk-apply__btn,html.mshk-embed .mshk-apply__choice,html.mshk-embed .mshk-apply__input,html.mshk-embed .mshk-apply__drop{touch-action:manipulation;-webkit-tap-highlight-color:rgba(34,63,154,.12)}
@media(max-width:820px){.mshk-apply__meta,.mshk-apply__waves,.mshk-apply__row{grid-template-columns:1fr 1fr}.mshk-apply__shell{width:calc(100% - 16px)}.mshk-apply__geo{display:none}.mshk-apply__card{padding:18px}}
@media(max-width:560px){.mshk-apply__meta,.mshk-apply__waves,.mshk-apply__row{grid-template-columns:1fr}.mshk-apply__nav{flex-direction:column}.mshk-apply__btn{width:100%;max-width:100%}.mshk-apply__title{font-size:26px}.mshk-apply__card{padding:16px;border-radius:18px}}
"""

consent_path = ROOT / "consent" / "consent-text.txt"
if not consent_path.exists():
    consent_path = ROOT / "consent-text.txt"
consent_raw = consent_path.read_text(encoding="utf-8") if consent_path.exists() else ""
# Keep body from "????????" onward; header is rebuilt in JS.
marker = "\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e, \u0441\u0432\u043e\u0435\u0439 \u0432\u043e\u043b\u0435\u0439"
idx = consent_raw.lower().find(marker[0:10].lower()) if False else consent_raw.find("\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e, \u0441\u0432\u043e\u0435\u0439")
consent_body = consent_raw[idx:].strip() if idx >= 0 else consent_raw
if "____________________" in consent_body:
    consent_body = consent_body.split("____________________")[0].rstrip()

js_i18n = json.dumps(
    {
        "req": S["req"],
        "err_email": S["err_email"],
        "err_msg": S["err_msg"],
        "err_aud": S["err_aud"],
        "err_dir": S["err_dir"],
        "err_500": S["err_500"],
        "err_pdf": S["err_pdf"],
        "err_sign": S["err_sign"],
        "err_confirm": S["err_confirm"],
        "err_file": S["err_file"],
        "ok_local": S["ok_local"],
        "ok_sent": S["ok_sent"],
        "err_send": S["err_send"],
        "chars": S["chars"],
        "file_ok": S["file_ok"],
        "need_fio": S["need_fio"],
        "doc_name": S["doc_name"],
        "sig": S["sig"],
        "dec": S["dec"],
        "title2": S["title2"],
        "consent_title": S["consent_title"],
    },
    ensure_ascii=True,
)

JS = r"""
(function(){
  var root = document.getElementById("mshk-form") || document.getElementById("mshk-apply");
  if (!root) return;
  if (window.parent && window.parent !== window) {
    document.documentElement.classList.add("mshk-embed");
  }
  function framed(){ return !!(window.parent && window.parent !== window); }
  function scrollFormTop(){
    if (framed()) { window.scrollTo(0, 0); return; }
    try { root.scrollIntoView({behavior:"smooth", block:"start"}); } catch (e) {}
  }
  var T = __I18N__;
  var BODY = __BODY__;
  var ENDPOINT = (window.MSHK_APPLY_ENDPOINT || "/apply").trim();
  var step = 1;
  var panes = root.querySelectorAll(".mshk-apply__pane");
  var bars = root.querySelectorAll(".mshk-apply__steps li");
  function $(sel){ return root.querySelector(sel); }
  function $$(sel){ return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function showErr(field, msg){
    var wrap = root.querySelector('[data-field="'+field+'"]');
    if (!wrap) return false;
    var el = wrap.querySelector(".mshk-apply__err");
    if (el){ el.hidden = !msg; el.textContent = msg || ""; }
    return !msg;
  }
  function val(name){
    var el = root.querySelector('[name="'+name+'"]');
    if (!el) return "";
    if (el.type === "radio") {
      var c = root.querySelector('[name="'+name+'"]:checked');
      return c ? c.value : "";
    }
    return (el.value || "").trim();
  }
  function checked(name){
    return $$('input[name="'+name+'"]:checked').map(function(x){ return x.value; });
  }
  var lastSentH = 0;
  function notifyHeight(){
    try {
      if (!framed()) return;
      var h = 0;
      ["mshk-apply", "mshk-form"].forEach(function(id){
        var el = document.getElementById(id);
        if (el) h += el.offsetHeight || 0;
      });
      if (!h && root) h = root.offsetHeight || 0;
      h = Math.ceil(h + 8);
      if (h < 320) h = 320;
      if (h > 4000) h = 4000;
      if (Math.abs(h - lastSentH) < 4) return;
      lastSentH = h;
      window.parent.postMessage({ type: "mshk-apply-height", height: h }, "*");
    } catch (err) {}
  }
  function go(n){
    step = n;
    panes.forEach(function(p){ p.hidden = p.getAttribute("data-step") != String(n); });
    bars.forEach(function(b,i){ b.classList.toggle("is-on", i < n); });
    scrollFormTop();
    setTimeout(notifyHeight, 50);
    saveDraft();
  }
  function need(name){
    if (!val(name)) { showErr(name, T.req); return false; }
    showErr(name, ""); return true;
  }
  function countArea(id){
    var el = $("#"+id); var out = $("#"+id+"-count");
    if (!el || !out) return;
    out.textContent = el.value.length + " / 500 " + T.chars;
  }
  ["why","coop"].forEach(function(id){
    var el = $("#"+id);
    if (el) el.addEventListener("input", function(){ countArea(id); });
  });
  $$('input[name="directions"]').forEach(function(el){
    el.addEventListener("change", function(){
      if (checked("directions").length > 3) el.checked = false;
    });
  });
  function bindFile(id, pdfOnly){
    var input = $("#"+id);
    if (!input) return;
    input.addEventListener("change", function(){
      var f = input.files && input.files[0];
      var nameEl = $("#"+id+"-name");
      if (!f){ if (nameEl) nameEl.textContent = "PDF, max 20 MB"; return; }
      if (f.size > 20*1024*1024){ alert(T.err_file); input.value=""; return; }
      if (pdfOnly){
        var ok = f.type === "application/pdf" || /\.pdf$/i.test(f.name);
        if (!ok){ alert(T.err_pdf); input.value=""; return; }
      }
      if (nameEl) nameEl.textContent = f.name + " | " + T.file_ok;
      saveDraft();
      saveFiles();
    });
  }
  bindFile("portfolio", true);
  bindFile("consent_file", false);

  var DRAFT_KEY = "mshk-apply-draft-v1";
  var saveTimer = null;
  function collectDraft(){
    var o = {step: step, values: {}, checks: {}};
    $$("input, textarea, select").forEach(function(el){
      if (!el.name) return;
      if (el.type === "file") return;
      if (el.type === "checkbox") {
        if (!o.checks[el.name]) o.checks[el.name] = [];
        if (el.checked) o.checks[el.name].push(el.value);
        return;
      }
      if (el.type === "radio") {
        if (el.checked) o.values[el.name] = el.value;
        return;
      }
      o.values[el.name] = el.value;
    });
    return o;
  }
  function saveDraft(){
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(collectDraft())); } catch (e) {}
  }
  function scheduleSave(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function(){ saveDraft(); }, 250);
  }
  function putFile(input, file){
    if (!input || !file) return;
    try {
      var dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      var nameEl = $("#"+input.id+"-name");
      if (nameEl) nameEl.textContent = file.name + " | " + T.file_ok;
    } catch (e) {}
  }
  function idbOpen(){
    return new Promise(function(res, rej){
      if (!window.indexedDB) { res(null); return; }
      var r = indexedDB.open("mshk-apply", 1);
      r.onupgradeneeded = function(){ r.result.createObjectStore("files"); };
      r.onsuccess = function(){ res(r.result); };
      r.onerror = function(){ res(null); };
    });
  }
  function saveFiles(){
    idbOpen().then(function(db){
      if (!db) return;
      var st = db.transaction("files", "readwrite").objectStore("files");
      var pf = $("#portfolio"); var cf = $("#consent_file");
      st.put(pf && pf.files[0] ? pf.files[0] : null, "portfolio");
      st.put(cf && cf.files[0] ? cf.files[0] : null, "consent_file");
    });
  }
  function loadFiles(){
    return idbOpen().then(function(db){
      if (!db) return {};
      return new Promise(function(res){
        var st = db.transaction("files", "readonly").objectStore("files");
        var out = {}, n = 0;
        ["portfolio","consent_file"].forEach(function(k){
          var g = st.get(k);
          g.onsuccess = function(){ out[k] = g.result; n++; if (n===2) res(out); };
          g.onerror = function(){ n++; if (n===2) res(out); };
        });
      });
    });
  }
  function clearDraft(){
    try { localStorage.removeItem(DRAFT_KEY); } catch (e) {}
    idbOpen().then(function(db){
      if (!db) return;
      db.transaction("files", "readwrite").objectStore("files").clear();
    });
  }
  function restoreDraft(){
    var raw = null;
    try { raw = localStorage.getItem(DRAFT_KEY); } catch (e) {}
    if (!raw) return 1;
    var o;
    try { o = JSON.parse(raw); } catch (e) { return 1; }
    Object.keys(o.values || {}).forEach(function(name){
      var v = o.values[name];
      if (v === undefined || v === null) return;
      var radios = $$('input[type="radio"][name="'+name+'"]');
      if (radios.length) {
        radios.forEach(function(x){ x.checked = x.value === v; });
        return;
      }
      var el = root.querySelector('[name="'+name+'"]');
      if (el && el.type !== "checkbox" && el.type !== "file") el.value = v;
    });
    Object.keys(o.checks || {}).forEach(function(name){
      var set = o.checks[name] || [];
      $$('input[name="'+name+'"]').forEach(function(el){
        if (el.type === "checkbox") el.checked = set.indexOf(el.value) >= 0;
      });
    });
    countArea("why"); countArea("coop");
    var yes = "\u0414\u0430";
    var box = $('[data-field="intl_details"]');
    if (box) box.style.display = val("intl_programs")===yes ? "" : "none";
    box = $('[data-field="ru_details"]');
    if (box) box.style.display = val("ru_programs")===yes ? "" : "none";
    var n = parseInt(o.step, 10);
    return (n >= 1 && n <= 4) ? n : 1;
  }

  function validStep(n){
    var ok = true;
    function req(name){ if (!need(name)) ok = false; }
    if (n===1){
      ["fio_latin","fio_ru","birth_date","gender","country","city","arrival","citizenship","all_citizenships","phone","email"].forEach(req);
      var em = val("email");
      if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) { showErr("email", T.err_email); ok=false; }
      if (!checked("messenger").length) { showErr("messenger", T.err_msg); ok=false; }
      else showErr("messenger","");
      if (checked("messenger").indexOf("\u0414\u0440\u0443\u0433\u043e\u0435")>=0 && !val("messenger_other")) { showErr("messenger_other", T.req); ok=false; }
    }
    if (n===2){
      ["org_name","org_spec","org_location","position","stream"].forEach(req);
      if (!checked("audience").length) { showErr("audience", T.err_aud); ok=false; }
      else showErr("audience","");
    }
    if (n===3){
      ["how_learned","intl_programs","ru_programs","why","coop","mentor"].forEach(req);
      if (val("intl_programs")==="\u0414\u0430" && !val("intl_details")) { showErr("intl_details", T.req); ok=false; }
      if (val("ru_programs")==="\u0414\u0430" && !val("ru_details")) { showErr("ru_details", T.req); ok=false; }
      if (val("why").length < 500) { showErr("why", T.err_500); ok=false; }
      if (val("coop").length < 500) { showErr("coop", T.err_500); ok=false; }
      if (checked("directions").length !== 3) { showErr("directions", T.err_dir); ok=false; }
      else showErr("directions","");
      var pf = $("#portfolio");
      if (!pf || !pf.files || !pf.files[0]) { showErr("portfolio", T.err_pdf); ok=false; }
      else showErr("portfolio","");
    }
    if (n===4){
      var cf = $("#consent_file");
      if (!cf || !cf.files || !cf.files[0]) { showErr("consent_file", T.err_sign); ok=false; }
      else showErr("consent_file","");
      if (!$("#consent_confirm") || !$("#consent_confirm").checked) { showErr("consent_confirm", T.err_confirm); ok=false; }
      else showErr("consent_confirm","");
    }
    return ok;
  }

  root.addEventListener("click", function(e){
    var t = e.target.closest("[data-next],[data-back],[data-download],[data-send]");
    if (!t) return;
    e.preventDefault();
    if (t.hasAttribute("data-next")) { if (validStep(step)) go(step+1); }
    if (t.hasAttribute("data-back")) go(Math.max(1, step-1));
    if (t.hasAttribute("data-download")) downloadDoc();
    if (t.hasAttribute("data-send")) submit();
  });

  $$('input[name="intl_programs"]').forEach(function(el){
    el.addEventListener("change", function(){
      var box = $('[data-field="intl_details"]');
      if (box) box.style.display = val("intl_programs")==="\u0414\u0430" ? "" : "none";
    });
  });
  $$('input[name="ru_programs"]').forEach(function(el){
    el.addEventListener("change", function(){
      var box = $('[data-field="ru_details"]');
      if (box) box.style.display = val("ru_programs")==="\u0414\u0430" ? "" : "none";
    });
  });
  var idBox = $('[data-field="intl_details"]'); if (idBox) idBox.style.display = "none";
  var rdBox = $('[data-field="ru_details"]'); if (rdBox) rdBox.style.display = "none";

  function esc(s){
    return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function downloadDoc(){
    var fio = val("fio_ru") && val("fio_ru") !== "\u043d\u0435\u0442" ? val("fio_ru") : val("fio_latin");
    var addr = val("address") || "____________________";
    var ser = val("passport_series") || "______";
    var num = val("passport_number") || "__________";
    var pdt = val("passport_date") || "__________";
    var pby = val("passport_issued") || "____________________";
    var phone = val("phone") || "____________________";
    var pass = ser + " " + num + ", " + pdt + ", " + pby;
    var header = "\u042f, " + (fio || "____________________") + ", \u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439(-\u0430\u044f) \u043f\u043e \u0430\u0434\u0440\u0435\u0441\u0443: " + addr + ", \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442, \u0443\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u044f\u044e\u0449\u0438\u0439 \u043b\u0438\u0447\u043d\u043e\u0441\u0442\u044c (\u043f\u0430\u0441\u043f\u043e\u0440\u0442) " + pass + ", \u043d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430: " + phone;
    var paras = BODY.split(/\n+/).filter(Boolean).map(function(p){
      return "<p style='margin:0 0 10pt;font-size:12pt;line-height:1.35;text-align:justify;font-family:Times New Roman,serif'>"+esc(p)+"</p>";
    }).join("");
    var html = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word'><head><meta charset='utf-8'><title>"+esc(T.consent_title)+"</title></head><body style='font-family:Times New Roman,serif'>";
    html += "<p style='text-align:right;font-size:12pt'>\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u2116 2</p>";
    html += "<p style='text-align:center;font-size:14pt;font-weight:bold;margin:18pt 0'>"+esc(T.consent_title)+"</p>";
    html += "<p style='margin:0 0 10pt;font-size:12pt;line-height:1.35;text-align:justify;font-family:Times New Roman,serif'>"+esc(header)+"</p>";
    html += paras;
    html += "<p style='margin-top:28pt'>____________________ / "+esc(fio)+" / &nbsp;&nbsp;&nbsp;\u00ab____\u00bb ________ 20__ \u0433.</p>";
    html += "<p style='font-size:10pt'>"+esc(T.sig)+" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "+esc(T.dec)+"</p>";
    html += "</body></html>";
    var blob = new Blob(["\ufeff", html], {type:"application/msword"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = T.doc_name;
    document.body.appendChild(a); a.click(); a.remove();
  }

  function payload(){
    return {
      fio_latin: val("fio_latin"), fio_ru: val("fio_ru"), birth_date: val("birth_date"),
      gender: val("gender"), country: val("country"), city: val("city"), arrival: val("arrival"),
      citizenship: val("citizenship"), all_citizenships: val("all_citizenships"),
      phone: val("phone"), email: val("email"), messenger: checked("messenger"),
      messenger_link: val("messenger_link"), messenger_other: val("messenger_other"),
      org_name: val("org_name"), org_spec: val("org_spec"), org_location: val("org_location"),
      position: val("position"), audience: checked("audience"), audience_other: val("audience_other"),
      stream: val("stream"), how_learned: val("how_learned"),
      intl_programs: val("intl_programs"), intl_details: val("intl_details"),
      ru_programs: val("ru_programs"), ru_details: val("ru_details"),
      why: val("why"), coop: val("coop"), mentor: val("mentor"),
      directions: checked("directions"), directions_other: val("directions_other"),
      address: val("address"), passport_series: val("passport_series"),
      passport_number: val("passport_number"), passport_date: val("passport_date"),
      passport_issued: val("passport_issued"), program: T.title2
    };
  }

  function submit(){
    if (!validStep(4)) return;
    var btn = root.querySelector("[data-send]");
    if (btn) btn.disabled = true;
    var fd = new FormData();
    fd.append("payload", JSON.stringify(payload()));
    var pf = $("#portfolio"); var cf = $("#consent_file");
    if (pf && pf.files[0]) fd.append("portfolio", pf.files[0]);
    if (cf && cf.files[0]) fd.append("consent", cf.files[0]);
    function done(ok, text){
      $$(".mshk-apply__pane").forEach(function(p){ p.hidden = true; });
      var box = $("#mshk-apply-done");
      box.hidden = false;
      box.querySelector("p").textContent = text;
      scrollFormTop();
      setTimeout(notifyHeight, 50);
    }
    fetch(ENDPOINT, {method:"POST", body: fd}).then(function(r){
      if (!r.ok) throw new Error("bad");
      clearDraft();
      done(true, T.ok_sent);
    }).catch(function(){
      if (btn) btn.disabled = false;
      alert(T.err_send);
    });
  }
  root.addEventListener("input", scheduleSave);
  root.addEventListener("change", function(){ saveDraft(); saveFiles(); });
  var startStep = restoreDraft();
  loadFiles().then(function(files){
    if (files) {
      putFile($("#portfolio"), files.portfolio);
      putFile($("#consent_file"), files.consent_file);
    }
    go(startStep);
    notifyHeight();
  }).catch(function(){
    go(startStep);
    notifyHeight();
  });
  window.addEventListener("resize", notifyHeight);
})();
"""

JS = JS.replace("__I18N__", js_i18n).replace("__BODY__", json.dumps(consent_body, ensure_ascii=False))

aud = [
    (S["aud2"], S["aud2"]),
    (S["aud3"], S["aud3"]),
    (S["aud4"], S["aud4"]),
    (S["aud5"], S["aud5"]),
    (S["aud6"], S["aud6"]),
    (S["aud7"], S["aud7"]),
    (S["aud8"], S["aud8"]),
    (S["aud9"], S["aud9"]),
    (S["other"], S["other"]),
]
dirs = [
    (S["dir1"], S["dir1"]),
    (S["dir2"], S["dir2"]),
    (S["dir3"], S["dir3"]),
    (S["dir4"], S["dir4"]),
    (S["dir5"], S["dir5"]),
    (S["dir6"], S["dir6"]),
    (S["dir7"], S["dir7"]),
    (S["dir8"], S["dir8"]),
    (S["dir9"], S["dir9"]),
    (S["dir_other"], S["dir_other"]),
]

html = []
html.append("<!-- Mashuk seminar application. Tilda T123, padding 0, full width.")
html.append("     Set window.MSHK_APPLY_ENDPOINT before this block when the API is ready.")
html.append("     Never put a PostgreSQL password in this HTML. -->")
html.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
html.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
html.append(
    '<link href="https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">'
)
html.append("<style>" + CSS + "</style>")
html.append('<section id="mshk-apply">')
html.append('<div class="mshk-apply__geo mshk-apply__geo--lg"></div>')
html.append('<div class="mshk-apply__geo mshk-apply__geo--sm"></div>')
html.append('<div class="mshk-apply__shell">')
html.append('<p class="mshk-apply__kicker">' + h("kicker") + "</p>")
html.append(
    '<h1 class="mshk-apply__title"><span>'
    + h("title1")
    + "</span>"
    + h("title2")
    + "</h1>"
)
html.append('<p class="mshk-apply__lead">' + h("lead") + "</p>")
html.append('<p class="mshk-apply__p">' + h("p1") + "</p>")
html.append('<p class="mshk-apply__p">' + h("p2") + "</p>")
html.append('<div class="mshk-apply__meta">')
html.append('<div class="mshk-apply__chip">' + h("format") + "</div>")
html.append('<div class="mshk-apply__chip">' + h("lang") + "</div>")
html.append('<div class="mshk-apply__chip mshk-apply__chip--wide">' + h("place") + "</div>")
html.append('<div class="mshk-apply__chip">' + h("age") + "</div>")
html.append("</div>")
html.append('<p class="mshk-apply__step-label">' + h("dates_title") + "</p>")
html.append('<div class="mshk-apply__waves">')
for n, d in (("s1", "s1d"), ("s2", "s2d"), ("s3", "s3d"), ("s4", "s4d")):
    html.append(
        '<div class="mshk-apply__wave"><b>' + h(n) + "</b><span>" + h(d) + "</span></div>"
    )
html.append("</div>")
html.append('<div class="mshk-apply__note">' + h("note_dates") + "</div>")
html.append('<div class="mshk-apply__note">' + h("note_apply") + "</div>")
html.append('<div class="mshk-apply__note">' + h("note_email") + "</div>")
html.append('<div class="mshk-apply__fin"><h3>' + h("finance_title") + "</h3>")
html.append("<p>" + h("finance_fee") + "</p><ul>")
html.append("<li>" + h("fin1") + "</li><li>" + h("fin2") + "</li><li>" + h("fin3") + "</li>")
html.append("</ul></div>")
html.append('<div class="mshk-apply__note">' + h("legal") + "</div>")

intro = "\n".join(html) + "\n</div></section>"

form_parts = []
form_parts.append("<!-- Mashuk seminar FORM. Paste as the NEXT T123 block, padding 0, full width. -->")
form_parts.append('<section id="mshk-form">')
form_parts.append('<div class="mshk-apply__shell">')
form_parts.append('<form class="mshk-apply__card" autocomplete="off" novalidate>')
form_parts.append('<ul class="mshk-apply__steps" aria-hidden="true"><li class="is-on"></li><li></li><li></li><li></li></ul>')
html = form_parts

# step 1
html.append('<div class="mshk-apply__pane" data-step="1">')
html.append('<p class="mshk-apply__step-label">1 / 4 - ' + h("sec_general") + "</p>")
html.append(field("fio_latin", S["fio"], S["fio_h"]))
html.append(field("fio_ru", S["fio_ru"], S["fio_ru_h"]))
html.append('<div class="mshk-apply__row">')
html.append(field("birth_date", S["birth"], "", "date"))
html.append(
    radios("gender", S["gender"], [(S["male"], S["male"]), (S["female"], S["female"])])
)
html.append("</div>")
html.append('<div class="mshk-apply__row">')
html.append(field("country", S["country"]))
html.append(field("city", S["city"]))
html.append("</div>")
html.append(field("arrival", S["arrival"], "", "text", True, True))
html.append('<div class="mshk-apply__row">')
html.append(field("citizenship", S["citizenship"]))
html.append(field("all_citizenships", S["all_cit"], S["all_cit_h"], "text", True, True))
html.append("</div>")
html.append('<div class="mshk-apply__row">')
html.append(field("phone", S["phone"], "", "tel"))
html.append(field("email", S["email"], "", "email"))
html.append("</div>")
html.append(
    checks(
        "messenger",
        S["messenger"],
        [("Telegram", "Telegram"), ("WhatsApp", "WhatsApp"), ("MAX", "MAX"), (S["other"], S["other"])],
    )
)
html.append(field("messenger_other", S["msg_other"], "", "text", False))
html.append(field("messenger_link", S["msg_link"], "", "text", False))
html.append(
    '<div class="mshk-apply__nav"><span></span><button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-next>'
    + h("next")
    + "</button></div></div>"
)

# step 2
html.append('<div class="mshk-apply__pane" data-step="2" hidden>')
html.append('<p class="mshk-apply__step-label">2 / 4 - ' + h("sec_org") + "</p>")
html.append(field("org_name", S["org_name"], "", "text", True, True))
html.append(field("org_spec", S["org_spec"], "", "text", True, True))
html.append(field("org_location", S["org_loc"], "", "text", True, True))
html.append(field("position", S["position"], "", "text", True, True))
html.append(checks("audience", S["audience"], aud))
html.append(field("audience_other", S["aud_other"], "", "text", False))
html.append(
    radios(
        "stream",
        S["stream"],
        [
            (S["s1opt"], S["s1opt"]),
            (S["s2opt"], S["s2opt"]),
            (S["s3opt"], S["s3opt"]),
            (S["s4opt"], S["s4opt"]),
        ],
        S["stream_h"],
    )
)
html.append(
    '<div class="mshk-apply__nav"><button class="mshk-apply__btn mshk-apply__btn--ghost" type="button" data-back>'
    + h("back")
    + '</button><button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-next>'
    + h("next")
    + "</button></div></div>"
)

# step 3
html.append('<div class="mshk-apply__pane" data-step="3" hidden>')
html.append('<p class="mshk-apply__step-label">3 / 4 - ' + h("sec_self") + "</p>")
html.append(field("how_learned", S["how"]))
html.append(
    radios("intl_programs", S["intl"], [(S["yes"], S["yes"]), (S["no"], S["no"])])
)
html.append(field("intl_details", S["intl_d"], "", "text", False, True))
html.append(radios("ru_programs", S["ru"], [(S["yes"], S["yes"]), (S["no"], S["no"])]))
html.append(field("ru_details", S["ru_d"], "", "text", False, True))
why = field("why", S["why"], S["min500"], "text", True, True)
why = why.replace("</textarea>", "</textarea>" + '<p class="mshk-apply__count" id="why-count">0 / 500 ' + h("chars") + "</p>")
html.append(why)
coop = field("coop", S["coop"], S["min500"], "text", True, True)
coop = coop.replace("</textarea>", "</textarea>" + '<p class="mshk-apply__count" id="coop-count">0 / 500 ' + h("chars") + "</p>")
html.append(coop)
html.append(field("mentor", S["mentor"], "", "text", True, True))
html.append(checks("directions", S["dirs"], dirs, S["dirs"]))
html.append(field("directions_other", S["dir_other_h"], "", "text", False))
html.append(file_box("portfolio", S["portfolio"], S["portfolio_h"], "application/pdf,.pdf", "portfolio-name"))
html.append(
    '<div class="mshk-apply__nav"><button class="mshk-apply__btn mshk-apply__btn--ghost" type="button" data-back>'
    + h("back")
    + '</button><button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-next>'
    + h("next")
    + "</button></div></div>"
)

# step 4
html.append('<div class="mshk-apply__pane" data-step="4" hidden>')
html.append('<p class="mshk-apply__step-label">4 / 4 - ' + h("sec_docs") + "</p>")
html.append('<div class="mshk-apply__consent">')
html.append('<p class="mshk-apply__kicker">' + h("consent_kicker") + "</p>")
html.append('<p class="mshk-apply__p" style="font-weight:500">' + h("consent_title") + "</p>")
html.append('<p class="mshk-apply__p">' + h("consent_intro") + "</p>")
html.append("</div>")
html.append(field("address", S["addr"], S["pass_opt"], "text", False, True))
html.append('<div class="mshk-apply__row">')
html.append(field("passport_series", S["pass_ser"], S["pass_opt"], "text", False))
html.append(field("passport_number", S["pass_num"], S["pass_opt"], "text", False))
html.append("</div>")
html.append('<div class="mshk-apply__row">')
html.append(field("passport_date", S["pass_date"], S["pass_opt"], "date", False))
html.append(field("passport_issued", S["pass_by"], S["pass_opt"], "text", False))
html.append("</div>")
html.append('<div class="mshk-apply__links">')
html.append(
    '<button class="mshk-apply__btn mshk-apply__btn--gold" type="button" data-download>'
    + h("download")
    + "</button>"
)
html.append(
    '<a class="mshk-apply__btn mshk-apply__btn--ghost" style="display:inline-flex;align-items:center" href="/consent-template" target="_blank" rel="noopener">'
    + h("blank")
    + "</a>"
)
html.append("</div>")
html.append('<p class="mshk-apply__hint" style="margin-bottom:16px">' + h("download_h") + "</p>")
html.append(
    file_box(
        "consent_file",
        S["signed"],
        S["download_h"],
        "application/pdf,image/jpeg,image/png,.pdf,.jpg,.jpeg,.png,.doc,.docx",
        "consent_file-name",
    )
)
html.append(
    '<fieldset class="mshk-apply__field" data-field="consent_confirm"><label class="mshk-apply__choice"><input type="checkbox" id="consent_confirm" name="consent_confirm" required><span>'
    + h("confirm")
    + '</span></label><p class="mshk-apply__err" hidden></p></fieldset>'
)
html.append(
    '<div class="mshk-apply__nav"><button class="mshk-apply__btn mshk-apply__btn--ghost" type="button" data-back>'
    + h("back")
    + '</button><button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-send>'
    + h("send")
    + "</button></div></div>"
)

html.append(
    '<div class="mshk-apply__ok" id="mshk-apply-done" hidden><h3>'
    + eh("\u0413\u043e\u0442\u043e\u0432\u043e")
    + "</h3><p></p></div>"
)
html.append("</form></div></section>")
form_html = "\n".join(html)
script_html = (
    "<!-- Mashuk seminar SCRIPT. Paste as the THIRD T123 block, padding 0. -->\n"
    "<script>" + JS + "</script>"
)

tilda = ROOT / "tilda"
tilda.mkdir(parents=True, exist_ok=True)
(tilda / "tilda-apply-1-intro.html").write_text(intro, encoding="utf-8")
(tilda / "tilda-apply-2-form.html").write_text(form_html, encoding="utf-8")
(tilda / "tilda-apply-3-script.html").write_text(script_html, encoding="utf-8")
combined = intro + "\n" + form_html + "\n" + script_html
(tilda / "tilda-apply-block.html").write_text(combined, encoding="utf-8")

preview = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%s</title>
  <style>html,body{margin:0;padding:0;height:auto;min-height:0;max-width:100%%;overflow-x:hidden;background:#fafafa}</style>
</head>
<body>
%s
</body>
</html>
""" % (eh(S["title2"]), combined)
(tilda / "preview-apply.html").write_text(preview, encoding="utf-8")
static_dir = ROOT / "static"
static_dir.mkdir(parents=True, exist_ok=True)
(static_dir / "index.html").write_text(preview, encoding="utf-8")
print("intro", len(intro))
print("form", len(form_html))
print("script", len(script_html))
print("combined", len(combined))
print("static", static_dir / "index.html")
