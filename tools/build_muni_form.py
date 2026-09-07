# -*- coding: utf-8 -*-
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_apply_form import CSS as APPLY_CSS
from muni_data import DISTRICT_ALIASES, DISTRICTS, REGION_GROUPS
from muni_strings import S

EXTRA_CSS = r"""
#mshk-apply .mshk-apply__shell,#mshk-form .mshk-apply__shell{width:calc(100% - 40px);max-width:860px;margin-left:auto;margin-right:auto}
html.mshk-embed .mshk-apply__shell{width:calc(100% - 32px);max-width:860px}
.mshk-apply__waves--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.mshk-apply__select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,#223f9a 50%),linear-gradient(135deg,#223f9a 50%,transparent 50%);background-position:calc(100% - 18px) calc(50% - 3px),calc(100% - 12px) calc(50% - 3px);background-size:6px 6px,6px 6px;background-repeat:no-repeat;padding-right:36px}
.mshk-apply__combo{position:relative}
.mshk-apply__suggest{margin-top:8px;max-height:240px;overflow:auto;background:#fff;border:1px solid rgba(34,63,154,.18);border-radius:12px;box-shadow:0 10px 28px rgba(34,63,154,.1)}
.mshk-apply__suggest-g{padding:10px 14px 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#a2855f;font-weight:600;font-family:var(--sans)!important}
.mshk-apply__suggest-i{display:block;width:100%;text-align:left;border:0;background:transparent;padding:9px 14px;font-size:14px;line-height:1.35;color:#223f9a;cursor:pointer;font-family:var(--sans)!important}
.mshk-apply__suggest-i:hover,.mshk-apply__suggest-i.is-on{background:rgba(34,63,154,.07)}
.mshk-apply__suggest-empty{padding:12px 14px;font-size:13px;color:rgba(51,45,36,.65);font-family:var(--sans)!important}
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
        "err_snils": S["err_snils"],
        "err_inn": S["err_inn"],
        "err_region": S["err_region"],
        "err_sign": S["err_sign"],
        "err_confirm": S["err_confirm"],
        "err_file": S["err_file"],
        "err_fio_dl": S["err_fio_dl"],
        "ok_sent": S["ok_sent"],
        "err_send": S["err_send"],
        "file_ok": S["file_ok"],
        "done": S["done"],
        "region_empty": S["region_empty"],
    },
    ensure_ascii=True,
)
js_regions = json.dumps(
    [{"title": title, "items": items} for title, items in REGION_GROUPS],
    ensure_ascii=True,
)
js_fo_aliases = json.dumps(DISTRICT_ALIASES, ensure_ascii=True)

JS = r"""
(function(){
  var root = document.getElementById("mshk-form") || document.getElementById("mshk-apply");
  if (!root) return;
  if (window.parent && window.parent !== window) {
    document.documentElement.classList.add("mshk-embed");
  }
  var T = __I18N__;
  var REGION_GROUPS = __REGIONS__;
  var FO_ALIASES = __FO_ALIASES__;
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
      if (name === "federal_district" && v && FO_ALIASES[v]) v = FO_ALIASES[v];
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
    if (inn.value.length === 12) showErr("inn", validInn(inn.value) ? "" : T.err_inn);
  });
  function fold(s){
    return String(s||"").toLowerCase().replace(/ё/g,"е").replace(/[—–−]/g,"-").replace(/\s+/g," ").trim();
  }
  function validEmail(s){
    s = String(s||"").trim();
    if (!s || s.length > 254 || s.indexOf("..") >= 0) return false;
    return /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/.test(s);
  }
  function validSnils(s){
    var d = String(s||"").replace(/\D/g,"");
    if (d.length !== 11 || d === "00000000000") return false;
    if (parseInt(d.slice(0,9), 10) < 1001998) return true;
    var sum = 0, i;
    for (i = 0; i < 9; i++) sum += parseInt(d.charAt(i), 10) * (9 - i);
    var check;
    if (sum < 100) check = sum;
    else if (sum === 100 || sum === 101) check = 0;
    else {
      check = sum % 101;
      if (check === 100) check = 0;
    }
    return check === parseInt(d.slice(9,11), 10);
  }
  function innCtrl(d, coeffs){
    var sum = 0, i;
    for (i = 0; i < coeffs.length; i++) sum += parseInt(d.charAt(i), 10) * coeffs[i];
    return String((sum % 11) % 10);
  }
  function validInn(s){
    var d = String(s||"").replace(/\D/g,"");
    if (d.length !== 12) return false;
    if (/^(\d)\1{11}$/.test(d)) return false;
    return innCtrl(d, [7,2,4,10,3,5,9,4,6,8]) === d.charAt(10)
      && innCtrl(d, [3,7,2,4,10,3,5,9,4,6,8]) === d.charAt(11);
  }
  function allRegions(){
    var out = [];
    REGION_GROUPS.forEach(function(g){ g.items.forEach(function(n){ out.push(n); }); });
    return out;
  }
  function isKnownRegion(name){
    return allRegions().indexOf(name) >= 0;
  }
  function setupRegionSearch(){
    var search = $("#region-search");
    var hidden = $("#region");
    var box = $("#region-suggest");
    if (!search || !hidden || !box) return;
    var active = -1;
    function items(){ return Array.prototype.slice.call(box.querySelectorAll(".mshk-apply__suggest-i")); }
    function highlight(){
      items().forEach(function(btn, i){ btn.classList.toggle("is-on", i === active); });
      var on = items()[active];
      if (on && on.scrollIntoView) try { on.scrollIntoView({block:"nearest"}); } catch (e) {}
    }
    function pick(name){
      hidden.value = name;
      search.value = name;
      box.hidden = true;
      active = -1;
      showErr("region", "");
      scheduleSave();
      notifyHeight();
    }
    function render(q){
      var query = fold(q);
      var html = [];
      var shown = 0;
      REGION_GROUPS.forEach(function(g){
        var hits = g.items.filter(function(n){ return !query || fold(n).indexOf(query) >= 0; });
        if (!hits.length) return;
        html.push('<div class="mshk-apply__suggest-g">' + g.title + "</div>");
        hits.forEach(function(n){
          html.push('<button type="button" class="mshk-apply__suggest-i" data-region="'+n.replace(/"/g,"&quot;")+'">'+n+"</button>");
          shown += 1;
        });
      });
      if (!shown) html.push('<p class="mshk-apply__suggest-empty">'+T.region_empty+"</p>");
      box.innerHTML = html.join("");
      box.hidden = false;
      active = shown ? 0 : -1;
      highlight();
      notifyHeight();
    }
    search.addEventListener("focus", function(){ render(search.value); });
    search.addEventListener("input", function(){
      if (hidden.value && fold(search.value) !== fold(hidden.value)) hidden.value = "";
      render(search.value);
    });
    search.addEventListener("keydown", function(ev){
      var list = items();
      if (ev.key === "ArrowDown") {
        ev.preventDefault();
        if (box.hidden) render(search.value);
        if (list.length) { active = (active + 1) % list.length; highlight(); }
      } else if (ev.key === "ArrowUp") {
        ev.preventDefault();
        if (list.length) { active = (active - 1 + list.length) % list.length; highlight(); }
      } else if (ev.key === "Enter") {
        if (!box.hidden && list[active]) { ev.preventDefault(); pick(list[active].getAttribute("data-region")); }
      } else if (ev.key === "Escape") {
        box.hidden = true; notifyHeight();
      }
    });
    box.addEventListener("mousedown", function(ev){
      var btn = ev.target.closest("[data-region]");
      if (!btn) return;
      ev.preventDefault();
      pick(btn.getAttribute("data-region"));
    });
    search.addEventListener("blur", function(){
      setTimeout(function(){
        box.hidden = true;
        var typed = (search.value || "").trim();
        if (isKnownRegion(typed)) pick(typed);
        else if (hidden.value && isKnownRegion(hidden.value)) search.value = hidden.value;
        else if (typed) { hidden.value = ""; showErr("region", T.err_region); }
        notifyHeight();
      }, 160);
    });
    if (hidden.value && isKnownRegion(hidden.value)) search.value = hidden.value;
    else if (search.value && isKnownRegion(search.value)) hidden.value = search.value;
  }
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
    if (val("region") && !isKnownRegion(val("region"))) { showErr("region", T.err_region); ok = false; }
    if (val("snils") && !validSnils(val("snils"))) { showErr("snils", T.err_snils); ok = false; }
    if (val("inn") && !validInn(val("inn"))) { showErr("inn", T.err_inn); ok = false; }
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
  setupRegionSearch();
  if (snils) snils.addEventListener("blur", function(){
    if (snils.value && !validSnils(snils.value)) showErr("snils", T.err_snils);
    else if (snils.value) showErr("snils", "");
  });
  if (inn) inn.addEventListener("blur", function(){
    if (inn.value && !validInn(inn.value)) showErr("inn", T.err_inn);
    else if (inn.value) showErr("inn", "");
  });
  var emailEl = $("#email");
  if (emailEl) emailEl.addEventListener("blur", function(){
    if (emailEl.value && !validEmail(emailEl.value)) showErr("email", T.err_email);
    else if (emailEl.value) showErr("email", "");
  });
  notifyHeight();
  setTimeout(notifyHeight, 300);
  window.addEventListener("resize", notifyHeight);
})();
"""

JS = (
    JS.replace("__I18N__", js_i18n)
    .replace("__REGIONS__", js_regions)
    .replace("__FO_ALIASES__", js_fo_aliases)
)

DISTRICT_OPTS = [(name, name) for name in DISTRICTS]


def region_field():
    return (
        '<div class="mshk-apply__field mshk-apply__combo" data-field="region">'
        '<label class="mshk-apply__label" for="region-search">'
        + h("region")
        + '</label><input class="mshk-apply__input" id="region-search" type="search" '
        + 'autocomplete="off" placeholder="'
        + eh(S["region_ph"])
        + '"><input type="hidden" id="region" name="region" required>'
        + '<div class="mshk-apply__suggest" id="region-suggest" hidden></div>'
        + '<p class="mshk-apply__hint">'
        + h("region_h")
        + '</p><p class="mshk-apply__err" hidden></p></div>'
    )


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
    html.append(select("federal_district", S["fo"], DISTRICT_OPTS))
    html.append(region_field())
    html.append('<div class="mshk-apply__row">')
    html.append(field("city", S["city"]))
    html.append(field("birth_date", S["birth"], "", "date"))
    html.append("</div>")
    html.append(field("workplace", S["workplace"], "", "text", True, True))
    html.append(field("position", S["position"]))
    html.append('<div class="mshk-apply__row">')
    html.append(field("snils", S["snils"], S["snils_h"], "text", True, False, ' inputmode="numeric" autocomplete="off"'))
    html.append(field("inn", S["inn"], S["inn_h"], "text", True, False, ' inputmode="numeric" autocomplete="off"'))
    html.append("</div>")
    html.append('<div class="mshk-apply__row">')
    html.append(field("phone", S["phone"], "", "tel"))
    html.append(field("email", S["email"], S["email_h"], "email"))
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
