# -*- coding: utf-8 -*-
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_apply_form import CSS as APPLY_CSS
from muni_strings import S

ROOT = Path(__file__).resolve().parent.parent

EXTRA_CSS = r"""
#mshk-apply .mshk-apply__shell,#mshk-form .mshk-apply__shell{width:calc(100% - 40px);max-width:860px;margin-left:auto;margin-right:auto}
html.mshk-embed .mshk-apply__shell{width:calc(100% - 32px);max-width:860px}
.mshk-apply__waves--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.mshk-apply__select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,#223f9a 50%),linear-gradient(135deg,#223f9a 50%,transparent 50%);background-position:calc(100% - 18px) calc(50% - 3px),calc(100% - 12px) calc(50% - 3px);background-size:6px 6px,6px 6px;background-repeat:no-repeat;padding-right:36px}
.mshk-apply__dl{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 16px}
.mshk-apply__dl .mshk-apply__btn{width:100%;text-align:center}
.mshk-apply__section{margin:8px 0 22px;padding-top:8px;border-top:1px solid rgba(34,63,154,.08)}
.mshk-apply__section:first-child{border-top:0;padding-top:0}
@media(max-width:820px){#mshk-apply .mshk-apply__shell,#mshk-form .mshk-apply__shell,html.mshk-embed .mshk-apply__shell{width:calc(100% - 24px);max-width:860px}}
@media(max-width:560px){.mshk-apply__dl{grid-template-columns:1fr}.mshk-apply__waves--2{grid-template-columns:1fr}#mshk-apply .mshk-apply__shell,#mshk-form .mshk-apply__shell,html.mshk-embed .mshk-apply__shell{width:calc(100% - 16px)}}
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
            + '" rows="3"'
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


def radios(name, label, options):
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
        + '<div class="mshk-apply__choices">'
        + "".join(items)
        + '</div><p class="mshk-apply__err" hidden></p></fieldset>'
    )


def select(name, label, options, hint=""):
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + "</p>") if hint else ""
    opts = ['<option value="" selected disabled></option>']
    for val, txt in options:
        opts.append('<option value="' + eh(val) + '">' + eh(txt) + "</option>")
    return (
        '<div class="mshk-apply__field" data-field="'
        + name
        + '"><label class="mshk-apply__label" for="'
        + name
        + '">'
        + eh(label)
        + '</label><select class="mshk-apply__input mshk-apply__select" id="'
        + name
        + '" name="'
        + name
        + '" required>'
        + "".join(opts)
        + "</select>"
        + hid
        + '<p class="mshk-apply__err" hidden></p></div>'
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
        + '"><span class="mshk-apply__drop-btn">'
        + h("upload")
        + '</span><span class="mshk-apply__drop-name" id="'
        + note_id
        + '">PDF / JPG / PNG</span></label><p class="mshk-apply__err" hidden></p></div>'
    )


js_i18n = json.dumps(
    {
        "req": S["req"],
        "err_email": S["err_email"],
        "err_sign": S["err_sign"],
        "err_confirm": S["err_confirm"],
        "err_file": S["err_file"],
        "err_fio_dl": S["err_fio_dl"],
        "ok_sent": S["ok_sent"],
        "err_send": S["err_send"],
        "file_ok": S["file_ok"],
        "done": S["done"],
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
  var T = __I18N__;
  var ENDPOINT = (window.MSHK_MUNI_ENDPOINT || "/muni").trim();
  function $(sel){ return root.querySelector(sel); }
  function $$(sel){ return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function framed(){ return !!(window.parent && window.parent !== window); }
  function showErr(field, msg){
    var wrap = root.querySelector('[data-field="'+field+'"]');
    if (!wrap) return false;
    var el = wrap.querySelector(".mshk-apply__err");
    if (el){ el.hidden = !msg; el.textContent = msg || ""; }
    if (msg) wrap.classList.add("is-invalid");
    else wrap.classList.remove("is-invalid");
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
      if (h > 8000) h = 8000;
      if (Math.abs(h - lastSentH) < 4) return;
      lastSentH = h;
      window.parent.postMessage({ type: "mshk-apply-height", height: h }, "*");
    } catch (err) {}
  }
  function need(name){
    if (!val(name)) { showErr(name, T.req); return false; }
    showErr(name, ""); return true;
  }
  var picked = {};
  function getFile(id){
    var input = $("#"+id);
    if (input && input.files && input.files[0]) {
      picked[id] = input.files[0];
      return input.files[0];
    }
    return picked[id] || null;
  }
  function markFile(id, f){
    var nameEl = $("#"+id+"-name");
    if (!nameEl) return;
    nameEl.textContent = f ? (f.name + " | " + T.file_ok) : "PDF / JPG / PNG";
  }
  var input = $("#consent_file");
  if (input) input.addEventListener("change", function(){
    var f = input.files && input.files[0];
    if (!f){ if (picked.consent_file) markFile("consent_file", picked.consent_file); return; }
    if (f.size > 20*1024*1024){ alert(T.err_file); input.value=""; picked.consent_file=null; markFile("consent_file", null); return; }
    picked.consent_file = f;
    markFile("consent_file", f);
    showErr("consent_file", "");
    saveDraft();
  });
  var DRAFT_KEY = "mshk-muni-draft-v1";
  var saveTimer = null;
  function collectDraft(){
    var o = {values: {}};
    $$("input, textarea, select").forEach(function(el){
      if (!el.name || el.type === "file") return;
      if (el.type === "checkbox") { o.values[el.name] = !!el.checked; return; }
      if (el.type === "radio") { if (el.checked) o.values[el.name] = el.value; return; }
      o.values[el.name] = el.value;
    });
    return o;
  }
  function saveDraft(){
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(collectDraft())); } catch (e) {}
  }
  function scheduleSave(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveDraft, 250);
  }
  function restoreDraft(){
    var raw;
    try { raw = localStorage.getItem(DRAFT_KEY); } catch (e) { return; }
    if (!raw) return;
    var o;
    try { o = JSON.parse(raw); } catch (e) { return; }
    var values = (o && o.values) || {};
    Object.keys(values).forEach(function(name){
      var els = $$('[name="'+name+'"]');
      if (!els.length) return;
      var v = values[name];
      els.forEach(function(el){
        if (el.type === "checkbox") el.checked = !!v;
        else if (el.type === "radio") el.checked = el.value === v;
        else el.value = v;
      });
    });
  }
  $$("input, textarea, select").forEach(function(el){
    if (el.type === "file") return;
    el.addEventListener("input", scheduleSave);
    el.addEventListener("change", scheduleSave);
  });
  function fmtSnils(v){
    var d = String(v||"").replace(/\D/g,"").slice(0,11);
    var a = d.slice(0,3), b = d.slice(3,6), c = d.slice(6,9), e = d.slice(9,11);
    var out = a;
    if (b) out += "-" + b;
    if (c) out += "-" + c;
    if (e) out += " " + e;
    return out;
  }
  var snils = $("#snils");
  if (snils) snils.addEventListener("input", function(){
    var start = snils.selectionStart;
    var before = snils.value;
    snils.value = fmtSnils(snils.value);
    if (document.activeElement === snils) {
      try { snils.setSelectionRange(snils.value.length, snils.value.length); } catch (e) {}
    }
    if (before !== snils.value) scheduleSave();
  });
  var inn = $("#inn");
  if (inn) inn.addEventListener("input", function(){
    inn.value = String(inn.value||"").replace(/\D/g,"").slice(0,12);
  });
  function consentPayload(){
    return {
      fio: val("fio"),
      address: val("address"),
      phone: val("phone"),
      email: val("email"),
      passport_series: val("passport_series"),
      passport_number: val("passport_number"),
      passport_issued: val("passport_issued"),
      snils: val("snils"),
      inn: val("inn"),
      region: val("region"),
      workplace: val("workplace")
    };
  }
  function saveBlob(blob, name){
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }
  var blankBtn = $("[data-blank]");
  if (blankBtn) blankBtn.addEventListener("click", function(){
    fetch("/muni/consent.pdf").then(function(r){
      if (!r.ok) throw new Error("bad");
      return r.blob();
    }).then(function(b){ saveBlob(b, "Soglasie_uchastnika.pdf"); }).catch(function(){
      alert(T.err_send);
    });
  });
  var fillBtn = $("[data-filled]");
  if (fillBtn) fillBtn.addEventListener("click", function(){
    if (!val("fio")) { showErr("fio", T.err_fio_dl); alert(T.err_fio_dl); return; }
    showErr("fio", "");
    fetch("/muni/consent.pdf", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(consentPayload())
    }).then(function(r){
      if (!r.ok) throw new Error("bad");
      return r.blob();
    }).then(function(b){
      var name = "Soglasie_" + val("fio").replace(/\s+/g, "_").slice(0,40) + ".pdf";
      saveBlob(b, name);
    }).catch(function(){ alert(T.err_send); });
  });
  function validEmail(s){ return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s); }
  function collect(){
    return {
      fio: val("fio"),
      federal_district: val("federal_district"),
      region: val("region"),
      city: val("city"),
      workplace: val("workplace"),
      position: val("position"),
      birth_date: val("birth_date"),
      snils: val("snils"),
      inn: val("inn"),
      phone: val("phone"),
      email: val("email"),
      stream: val("stream"),
      address: val("address"),
      passport_series: val("passport_series"),
      passport_number: val("passport_number"),
      passport_issued: val("passport_issued")
    };
  }
  function validate(){
    var ok = true;
    ["fio","federal_district","region","city","workplace","position","birth_date","snils","inn","phone","email","stream"].forEach(function(n){
      if (!need(n)) ok = false;
    });
    if (val("email") && !validEmail(val("email"))) { showErr("email", T.err_email); ok = false; }
    if (!getFile("consent_file")) { showErr("consent_file", T.err_sign); ok = false; }
    if (!$("#consent_confirm") || !$("#consent_confirm").checked) { showErr("consent_confirm", T.err_confirm); ok = false; }
    else showErr("consent_confirm", "");
    return ok;
  }
  var sendBtn = $("[data-send]");
  if (sendBtn) sendBtn.addEventListener("click", function(){
    if (!validate()) {
      var bad = root.querySelector(".is-invalid");
      if (bad) try { bad.scrollIntoView({behavior:"smooth", block:"center"}); } catch (e) {}
      return;
    }
    sendBtn.disabled = true;
    var fd = new FormData();
    fd.append("payload", JSON.stringify(collect()));
    fd.append("consent", getFile("consent_file"));
    fetch(ENDPOINT, { method:"POST", body: fd }).then(function(r){
      if (!r.ok) throw new Error("bad");
      return r.json();
    }).then(function(){
      var form = root.querySelector("form");
      var done = $("#mshk-apply-done");
      if (form) form.hidden = true;
      if (done){ done.hidden = false; done.querySelector("p").textContent = T.ok_sent; }
      try { localStorage.removeItem(DRAFT_KEY); } catch (e) {}
      if (framed()) window.scrollTo(0,0);
      notifyHeight();
    }).catch(function(){
      sendBtn.disabled = false;
      alert(T.err_send);
    });
  });
  restoreDraft();
  notifyHeight();
  setTimeout(notifyHeight, 300);
  window.addEventListener("resize", notifyHeight);
})();
""".replace("__I18N__", js_i18n)

DISTRICTS = [
    ("ЦФО", "ЦФО"),
    ("СЗФО", "СЗФО"),
    ("ЮФО", "ЮФО"),
    ("СКФО", "СКФО"),
    ("ПФО", "ПФО"),
    ("УФО", "УФО"),
    ("СФО", "СФО"),
    ("ДФО", "ДФО"),
]


def main():
    css = APPLY_CSS + EXTRA_CSS
    html = []
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
    html.append('<p class="mshk-apply__p">' + h("about") + "</p>")
    html.append('<p class="mshk-apply__p">' + h("about2") + "</p>")
    html.append('<div class="mshk-apply__meta">')
    html.append('<div class="mshk-apply__chip">' + h("format") + "</div>")
    html.append('<div class="mshk-apply__chip">' + h("age") + "</div>")
    html.append('<div class="mshk-apply__chip mshk-apply__chip--wide">' + h("place") + "</div>")
    html.append("</div>")
    html.append('<p class="mshk-apply__step-label">' + h("dates_title") + "</p>")
    html.append('<div class="mshk-apply__waves mshk-apply__waves--2">')
    for n, d in (("s1", "s1d"), ("s2", "s2d")):
        html.append(
            '<div class="mshk-apply__wave"><b>' + h(n) + "</b><span>" + h(d) + "</span></div>"
        )
    html.append("</div>")
    html.append('<div class="mshk-apply__fin"><h3>' + h("finance_title") + "</h3>")
    html.append("<p>" + h("finance_fee") + "</p><ul>")
    html.append("<li>" + h("fin1") + "</li><li>" + h("fin2") + "</li>")
    html.append("</ul></div>")
    html.append("</div></section>")

    html.append('<section id="mshk-form">')
    html.append('<div class="mshk-apply__shell">')
    html.append('<form class="mshk-apply__card" autocomplete="off" novalidate>')
    html.append('<div class="mshk-apply__section">')
    html.append('<p class="mshk-apply__step-label">' + h("sec_general") + "</p>")
    html.append(field("fio", S["fio"], S["fio_h"]))
    html.append('<div class="mshk-apply__row">')
    html.append(select("federal_district", S["fo"], DISTRICTS, S["fo_h"]))
    html.append(field("region", S["region"]))
    html.append("</div>")
    html.append('<div class="mshk-apply__row">')
    html.append(field("city", S["city"]))
    html.append(field("birth_date", S["birth"], "", "date"))
    html.append("</div>")
    html.append(field("workplace", S["workplace"], "", "text", True, True))
    html.append(field("position", S["position"]))
    html.append('<div class="mshk-apply__row">')
    html.append(field("snils", S["snils"], S["snils_h"], "text", True, False, ' inputmode="numeric" autocomplete="off"'))
    html.append(field("inn", S["inn"], "", "text", True, False, ' inputmode="numeric" autocomplete="off"'))
    html.append("</div>")
    html.append('<div class="mshk-apply__row">')
    html.append(field("phone", S["phone"], "", "tel"))
    html.append(field("email", S["email"], "", "email"))
    html.append("</div>")
    html.append(
        radios(
            "stream",
            S["stream"],
            [(S["s1opt"], S["s1opt"]), (S["s2opt"], S["s2opt"])],
        )
    )
    html.append("</div>")

    html.append('<div class="mshk-apply__section">')
    html.append('<div class="mshk-apply__consent">')
    html.append('<p class="mshk-apply__kicker">' + h("consent_kicker") + "</p>")
    html.append('<p class="mshk-apply__p" style="font-weight:500">' + h("consent_title") + "</p>")
    html.append('<p class="mshk-apply__p">' + h("consent_intro") + "</p>")
    html.append("</div>")
    html.append('<p class="mshk-apply__hint" style="margin-bottom:14px">' + h("pass_opt") + "</p>")
    html.append(field("address", S["addr"], S["addr_h"], "text", False, True))
    html.append('<div class="mshk-apply__row">')
    html.append(field("passport_series", S["pass_ser"], "", "text", False))
    html.append(field("passport_number", S["pass_num"], "", "text", False))
    html.append("</div>")
    html.append(field("passport_issued", S["pass_by"], "", "text", False))
    html.append('<div class="mshk-apply__dl">')
    html.append(
        '<button class="mshk-apply__btn mshk-apply__btn--ghost" type="button" data-blank>'
        + h("dl_blank")
        + "</button>"
    )
    html.append(
        '<button class="mshk-apply__btn mshk-apply__btn--gold" type="button" data-filled>'
        + h("dl_filled")
        + "</button>"
    )
    html.append("</div>")
    html.append(
        file_box(
            "consent_file",
            S["signed"],
            S["signed_h"],
            "application/pdf,image/jpeg,image/png,.pdf,.jpg,.jpeg,.png,.doc,.docx",
            "consent_file-name",
        )
    )
    html.append(
        '<fieldset class="mshk-apply__field" data-field="consent_confirm"><label class="mshk-apply__choice"><input type="checkbox" id="consent_confirm" name="consent_confirm" required><span>'
        + h("confirm")
        + '</span></label><p class="mshk-apply__err" hidden></p></fieldset>'
    )
    html.append("</div>")
    html.append(
        '<div class="mshk-apply__nav"><span></span><button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-send>'
        + h("send")
        + "</button></div>"
    )
    html.append("</form>")
    html.append(
        '<div class="mshk-apply__ok mshk-apply__card" id="mshk-apply-done" hidden><h3>'
        + h("done")
        + "</h3><p></p></div>"
    )
    html.append("</div></section>")
    html.append("<script>" + JS + "</script>")

    body = "\n".join(html)
    page = (
        "<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + h("title2") + "</title>\n"
        "<style>html,body{margin:0;padding:0;height:auto;min-height:0;max-width:100%;overflow-x:hidden;background:#fafafa}</style>\n"
        "<style>" + css + "</style>\n"
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    static_dir = ROOT / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    (static_dir / "muni.html").write_text(page, encoding="utf-8")
    tilda = ROOT / "tilda"
    tilda.mkdir(parents=True, exist_ok=True)
    (tilda / "tilda-muni-block.html").write_text(page, encoding="utf-8")
    print("wrote", static_dir / "muni.html", len(page))


if __name__ == "__main__":
    main()
