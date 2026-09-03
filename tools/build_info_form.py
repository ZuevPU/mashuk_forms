# -*- coding: utf-8 -*-
import json
from pathlib import Path

from form_strings import S as APPLY
from info_strings import S

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
TILDA = ROOT / "tilda"


def C(tag):
    return chr(60) + "/" + tag + chr(62)


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


def h(key):
    return eh(S[key])


def load_css():
    text = (Path(__file__).parent / "build_apply_form.py").read_text(encoding="utf-8")
    start = text.find('CSS = r"""') + len('CSS = r"""')
    end = text.find('"""', start)
    extra = (
        ".mshk-apply__hint{white-space:pre-line}"
        ".mshk-apply__section{margin:8px 0 16px;font-size:18px;font-weight:600;"
        "letter-spacing:.04em;color:var(--navy);font-family:var(--sans)!important}"
    )
    return text[start:end] + extra


def field(name, label, hint="", typ="text", required=True, area=False):
    req = " required" if required else ""
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + C("p")) if hint else ""
    lab = (
        '<label class="mshk-apply__label" for="'
        + name
        + '">'
        + eh(label)
        + C("label")
    )
    if area:
        ctrl = (
            '<textarea class="mshk-apply__input mshk-apply__area" id="'
            + name
            + '" name="'
            + name
            + '" rows="4"'
            + req
            + ">"
            + C("textarea")
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
            + ">"
        )
    return (
        '<div class="mshk-apply__field" data-field="'
        + name
        + '">'
        + lab
        + ctrl
        + hid
        + '<p class="mshk-apply__err" hidden>'
        + C("p")
        + C("div")
    )


def radios(name, label, options, hint="", required=True):
    hid = ('<p class="mshk-apply__hint">' + eh(hint) + C("p")) if hint else ""
    req = " required" if required else ""
    items = []
    for val, txt in options:
        items.append(
            '<label class="mshk-apply__choice"><input type="radio" name="'
            + name
            + '" value="'
            + eh(val)
            + '"'
            + req
            + "><span>"
            + eh(txt)
            + C("span")
            + C("label")
        )
    return (
        '<fieldset class="mshk-apply__field" data-field="'
        + name
        + '"><legend class="mshk-apply__label">'
        + eh(label)
        + C("legend")
        + hid
        + '<div class="mshk-apply__choices">'
        + "".join(items)
        + C("div")
        + '<p class="mshk-apply__err" hidden>'
        + C("p")
        + C("fieldset")
    )


def agree(name, label):
    return (
        '<fieldset class="mshk-apply__field" data-field="'
        + name
        + '"><label class="mshk-apply__choice"><input type="checkbox" id="'
        + name
        + '" name="'
        + name
        + '" value="yes"><span>'
        + eh(label)
        + C("span")
        + C("label")
        + '<p class="mshk-apply__err" hidden>'
        + C("p")
        + C("fieldset")
    )


def nav(back=False, nxt=False, send=False):
    left = "<span>" + C("span")
    if back:
        left = (
            '<button class="mshk-apply__btn mshk-apply__btn--ghost" type="button" data-back>'
            + h("back")
            + C("button")
        )
    right = ""
    if nxt:
        right = (
            '<button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-next>'
            + h("next")
            + C("button")
        )
    if send:
        right = (
            '<button class="mshk-apply__btn mshk-apply__btn--navy" type="button" data-send>'
            + h("send")
            + C("button")
        )
    return '<div class="mshk-apply__nav">' + left + right + C("div")


CSS = load_css()

js_i18n = json.dumps(
    {"req": S["req"], "ok_sent": S["ok_sent"], "err_send": S["err_send"]},
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
  var ENDPOINT = (window.MSHK_INFO_ENDPOINT || "/info").trim();
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
    if (el.type === "checkbox") return el.checked ? (el.value || "yes") : "";
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
  var DRAFT_KEY = "mshk-info-draft-v6";
  var saveTimer = null;
  function collectDraft(){
    var o = {step: step, values: {}, checks: {}};
    $$("input, textarea, select").forEach(function(el){
      if (!el.name) return;
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
  function clearDraft(){
    try { localStorage.removeItem(DRAFT_KEY); } catch (e) {}
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
      if (el && el.type !== "checkbox") el.value = v;
    });
    Object.keys(o.checks || {}).forEach(function(name){
      var set = o.checks[name] || [];
      $$('input[name="'+name+'"]').forEach(function(el){
        if (el.type === "checkbox") el.checked = set.indexOf(el.value) >= 0;
      });
    });
    var n = parseInt(o.step, 10);
    return (n >= 1 && n <= 6) ? n : 1;
  }
  function syncOtherCit(){
    var yes = "\u0414\u0430";
    var box = $('[data-field="other_citizenships_detail"]');
    if (box) box.style.display = val("other_citizenships")===yes ? "" : "none";
  }
  function syncIdOther(){
    var other = "\u0414\u0440\u0443\u0433\u043e\u0435";
    var box = $('[data-field="id_doc_type_other"]');
    if (box) box.style.display = val("id_doc_type")===other ? "" : "none";
  }
  function syncVisaStatus(){
    var no = "\u041d\u0435\u0442";
    var box = $('[data-field="visa_status"]');
    if (box) box.style.display = val("visa_current")===no ? "" : "none";
  }
  function syncHealth(){
    var yes = "\u0414\u0430";
    var other = "\u0414\u0440\u0443\u0433\u043e\u0435";
    var a = $('[data-field="allergies_detail"]');
    if (a) a.style.display = val("allergies")===yes ? "" : "none";
    var h = $('[data-field="health_conditions_detail"]');
    if (h) h.style.display = val("health_conditions")===yes ? "" : "none";
    var m = $('[data-field="meal_type_other"]');
    if (m) m.style.display = val("meal_type")===other ? "" : "none";
  }
  var STEP1 = ["fio_latin","gender","citizenship","other_citizenships"];
  var STEP2 = [
    "id_doc_type","id_doc_series","id_doc_number","id_doc_issued",
    "id_doc_valid_to","id_doc_issuer","entry_doc_name",
    "entry_doc_series","entry_doc_number","entry_doc_issued",
    "entry_doc_valid_to","entry_doc_issuer"
  ];
  var STEP3 = ["stream","depart_country","depart_city","return_ticket","baggage"];
  var STEP4 = ["visa_needed","visa_current"];
  var STEP5 = ["allergies","health_conditions","meal_type"];
  var STEP6 = ["agree_participate","agree_notice","agree_truth","agree_extra_docs","agree_refusal","agree_logistics_city","agree_logistics_change","agree_logistics_fixed"];
  function validStep(n){
    var ok = true;
    function req(name){ if (!need(name)) ok = false; }
    if (n===1) {
      STEP1.forEach(req);
      if (val("other_citizenships")==="\u0414\u0430") req("other_citizenships_detail");
    }
    if (n===2) {
      STEP2.forEach(req);
      if (val("id_doc_type")==="\u0414\u0440\u0443\u0433\u043e\u0435") req("id_doc_type_other");
    }
    if (n===3) STEP3.forEach(req);
    if (n===4) {
      STEP4.forEach(req);
      if (val("visa_current")==="\u041d\u0435\u0442") req("visa_status");
    }
    if (n===5) {
      STEP5.forEach(req);
      if (val("allergies")==="\u0414\u0430") req("allergies_detail");
      if (val("health_conditions")==="\u0414\u0430") req("health_conditions_detail");
      if (val("meal_type")==="\u0414\u0440\u0443\u0433\u043e\u0435") req("meal_type_other");
    }
    if (n===6) STEP6.forEach(req);
    return ok;
  }
  function payload(){
    return {
      fio_latin: val("fio_latin"),
      gender: val("gender"),
      citizenship: val("citizenship"),
      other_citizenships: val("other_citizenships"),
      other_citizenships_detail: val("other_citizenships")==="\u0414\u0430" ? val("other_citizenships_detail") : "",
      health_limits: val("health_conditions")==="\u0414\u0430" ? val("health_conditions_detail") : val("health_conditions"),
      allergies: val("allergies"),
      allergies_detail: val("allergies")==="\u0414\u0430" ? val("allergies_detail") : "",
      health_conditions: val("health_conditions"),
      health_conditions_detail: val("health_conditions")==="\u0414\u0430" ? val("health_conditions_detail") : "",
      meal_type: val("meal_type"),
      meal_type_other: val("meal_type")==="\u0414\u0440\u0443\u0433\u043e\u0435" ? val("meal_type_other") : "",
      id_doc_type: val("id_doc_type"),
      id_doc_type_other: val("id_doc_type")==="\u0414\u0440\u0443\u0433\u043e\u0435" ? val("id_doc_type_other") : "",
      id_doc_series: val("id_doc_series"),
      id_doc_number: val("id_doc_number"),
      id_doc_issued: val("id_doc_issued"),
      id_doc_valid_to: val("id_doc_valid_to"),
      id_doc_issuer: val("id_doc_issuer"),
      entry_doc_name: val("entry_doc_name"),
      entry_doc_series: val("entry_doc_series"),
      entry_doc_number: val("entry_doc_number"),
      entry_doc_issued: val("entry_doc_issued"),
      entry_doc_valid_to: val("entry_doc_valid_to"),
      entry_doc_issuer: val("entry_doc_issuer"),
      stream: val("stream"),
      depart_country: val("depart_country"),
      depart_city: val("depart_city"),
      return_ticket: val("return_ticket"),
      baggage: val("baggage"),
      visa_needed: val("visa_needed"),
      visa_current: val("visa_current"),
      visa_status: val("visa_current")==="\u041d\u0435\u0442" ? val("visa_status") : "",
      agree_participate: !!$("#agree_participate") && $("#agree_participate").checked,
      agree_notice: !!$("#agree_notice") && $("#agree_notice").checked,
      agree_truth: !!$("#agree_truth") && $("#agree_truth").checked,
      agree_extra_docs: !!$("#agree_extra_docs") && $("#agree_extra_docs").checked,
      agree_refusal: !!$("#agree_refusal") && $("#agree_refusal").checked,
      agree_logistics_city: !!$("#agree_logistics_city") && $("#agree_logistics_city").checked,
      agree_logistics_fixed: !!$("#agree_logistics_fixed") && $("#agree_logistics_fixed").checked,
      agree_logistics_change: !!$("#agree_logistics_change") && $("#agree_logistics_change").checked
    };
  }
  function submit(){
    if (!validStep(6)) return;
    var btn = root.querySelector("[data-send]");
    if (btn) btn.disabled = true;
    function done(text){
      $$(".mshk-apply__pane").forEach(function(p){ p.hidden = true; });
      var box = $("#mshk-apply-done");
      box.hidden = false;
      box.querySelector("p").textContent = text;
      scrollFormTop();
      setTimeout(notifyHeight, 50);
    }
    fetch(ENDPOINT, {
      method:"POST",
      headers: {"Content-Type":"application/json","Accept":"application/json"},
      body: JSON.stringify(payload())
    }).then(function(r){
      if (!r.ok) throw new Error("bad");
      clearDraft();
      done(T.ok_sent);
    }).catch(function(){
      if (btn) btn.disabled = false;
      alert(T.err_send);
    });
  }
  function focusFirstError(){
    var pane = root.querySelector(".mshk-apply__pane:not([hidden])") || root;
    var err = null;
    var list = pane.querySelectorAll(".mshk-apply__err");
    for (var i = 0; i < list.length; i++) {
      if (!list[i].hidden && list[i].textContent) { err = list[i]; break; }
    }
    if (!err) return;
    var wrap = err.closest(".mshk-apply__field") || err;
    try { wrap.scrollIntoView({behavior:"smooth", block:"center"}); } catch (e) { wrap.scrollIntoView(); }
  }
  root.addEventListener("click", function(e){
    var t = e.target.closest("[data-next],[data-back],[data-send]");
    if (!t) return;
    e.preventDefault();
    if (t.hasAttribute("data-next")) { if (validStep(step)) go(step+1); else focusFirstError(); }
    if (t.hasAttribute("data-back")) go(Math.max(1, step-1));
    if (t.hasAttribute("data-send")) submit();
  });
  root.addEventListener("input", scheduleSave);
  root.addEventListener("change", function(){ saveDraft(); syncOtherCit(); syncIdOther(); syncVisaStatus(); syncHealth(); });
  $$('input[name="other_citizenships"]').forEach(function(el){
    el.addEventListener("change", syncOtherCit);
  });
  $$('input[name="id_doc_type"]').forEach(function(el){
    el.addEventListener("change", syncIdOther);
  });
  $$('input[name="visa_current"]').forEach(function(el){
    el.addEventListener("change", syncVisaStatus);
  });
  $$('input[name="allergies"], input[name="health_conditions"], input[name="meal_type"]').forEach(function(el){
    el.addEventListener("change", syncHealth);
  });
  var ocBox = $('[data-field="other_citizenships_detail"]');
  if (ocBox) ocBox.style.display = "none";
  var idOtherBox = $('[data-field="id_doc_type_other"]');
  if (idOtherBox) idOtherBox.style.display = "none";
  var visaStatusBox = $('[data-field="visa_status"]');
  if (visaStatusBox) visaStatusBox.style.display = "none";
  ["allergies_detail","health_conditions_detail","meal_type_other"].forEach(function(name){
    var box = $('[data-field="'+name+'"]');
    if (box) box.style.display = "none";
  });
  var start = restoreDraft();
  syncOtherCit();
  syncIdOther();
  syncVisaStatus();
  syncHealth();
  go(start);
  notifyHeight();
  window.addEventListener("resize", notifyHeight);
})();
"""

JS = JS.replace("__I18N__", js_i18n)

parts = []
parts.append('<section id="mshk-apply">')
parts.append('<div class="mshk-apply__geo mshk-apply__geo--lg">' + C("div"))
parts.append('<div class="mshk-apply__geo mshk-apply__geo--sm">' + C("div"))
parts.append('<div class="mshk-apply__shell">')
parts.append('<p class="mshk-apply__kicker">' + h("kicker") + C("p"))
parts.append(
    '<h1 class="mshk-apply__title"><span>'
    + h("title1")
    + C("span")
    + h("title2")
    + C("h1")
)
parts.append('<p class="mshk-apply__lead">' + h("hello") + C("p"))
parts.append('<p class="mshk-apply__p">' + h("lead") + C("p"))
parts.append('<p class="mshk-apply__p">' + h("need") + C("p"))
parts.append(C("div") + C("section"))

form = []
form.append('<section id="mshk-form">')
form.append('<div class="mshk-apply__shell">')
form.append('<form class="mshk-apply__card" autocomplete="off" novalidate>')
form.append(
    '<ul class="mshk-apply__steps" aria-hidden="true"><li class="is-on">'
    + C("li")
    + "<li>"
    + C("li")
    + "<li>"
    + C("li")
    + "<li>"
    + C("li")
    + "<li>"
    + C("li")
    + "<li>"
    + C("li")
    + C("ul")
)

form.append('<div class="mshk-apply__pane" data-step="1">')
form.append('<p class="mshk-apply__section">' + h("sec_general") + C("p"))
form.append(field("fio_latin", S["fio"], S["fio_h"]))
form.append(radios("gender", S["gender"], [(S["male"], S["male"]), (S["female"], S["female"])]))
form.append(field("citizenship", S["citizenship"], "", "text", True, True))
form.append(
    radios(
        "other_citizenships",
        S["other_cit_q"],
        [(S["yes"], S["yes"]), (S["no"], S["no"])],
    )
)
form.append(field("other_citizenships_detail", S["other_cit_h"], "", "text", False, True))
form.append(nav(back=False, nxt=True))
form.append(C("div"))

form.append('<div class="mshk-apply__pane" data-step="2" hidden>')
form.append('<p class="mshk-apply__section">' + h("sec_id") + C("p"))
form.append(
    radios(
        "id_doc_type",
        S["id_type"],
        [(S["id1"], S["id1"]), (S["id2"], S["id2"]), (S["id3"], S["id3"]), (S["id4"], S["id4"])],
    )
)
form.append(field("id_doc_type_other", S["id_other"], "", "text", False))
form.append(field("id_doc_series", S["series"], S["series_h"]))
form.append(field("id_doc_number", S["number"]))
form.append(field("id_doc_issued", S["issued"], "", "date"))
form.append(field("id_doc_valid_to", S["valid"], S["valid_h"]))
form.append(field("id_doc_issuer", S["issuer"], "", "text", True, True))
form.append(field("entry_doc_name", S["entry"]))
form.append(field("entry_doc_series", S["series"], S["series_h"]))
form.append(field("entry_doc_number", S["number"]))
form.append(field("entry_doc_issued", S["issued"], "", "date"))
form.append(field("entry_doc_valid_to", S["valid"], S["valid_h"]))
form.append(field("entry_doc_issuer", S["issuer"], "", "text", True, True))
form.append(nav(back=True, nxt=True))
form.append(C("div"))

form.append('<div class="mshk-apply__pane" data-step="3" hidden>')
form.append('<p class="mshk-apply__step-label">3 / 6 \u2014 ' + h("st2") + C("p"))
form.append('<p class="mshk-apply__section">' + h("sec_route") + C("p"))
form.append(
    radios(
        "stream",
        S["stream"],
        [
            (APPLY["s1opt"], APPLY["s1opt"]),
            (APPLY["s2opt"], APPLY["s2opt"]),
            (APPLY["s3opt"], APPLY["s3opt"]),
            (APPLY["s4opt"], APPLY["s4opt"]),
        ],
        S["stream_h"],
    )
)
form.append('<div class="mshk-apply__row">')
form.append(field("depart_country", S["depart_country"]))
form.append(field("depart_city", S["depart_city"]))
form.append(C("div"))
form.append(radios("return_ticket", S["return"], [(S["yes"], S["yes"]), (S["no"], S["no"])]))
form.append(
    radios("baggage", S["baggage"], [(S["bag_yes"], S["bag_yes"]), (S["bag_no"], S["bag_no"])])
)
form.append(nav(back=True, nxt=True))
form.append(C("div"))

form.append('<div class="mshk-apply__pane" data-step="4" hidden>')
form.append('<p class="mshk-apply__section">' + h("sec_visa") + C("p"))
form.append(
    radios(
        "visa_needed",
        S["visa"],
        [(S["yes"], S["yes"]), (S["visa_no"], S["visa_no"])],
        S["visa_h"],
    )
)
form.append(
    radios(
        "visa_current",
        S["visa_current"],
        [(S["visa_current_yes"], S["visa_current_yes"]), (S["no"], S["no"])],
    )
)
form.append(
    radios(
        "visa_status",
        S["visa_status"],
        [
            (S["visa_st1"], S["visa_st1"]),
            (S["visa_st2"], S["visa_st2"]),
            (S["visa_st3"], S["visa_st3"]),
        ],
        "",
        False,
    )
)
form.append(nav(back=True, nxt=True))
form.append(C("div"))

form.append('<div class="mshk-apply__pane" data-step="5" hidden>')
form.append('<p class="mshk-apply__section">' + h("sec_health") + C("p"))
form.append(radios("allergies", S["allergy"], [(S["yes"], S["yes"]), (S["no"], S["no"])]))
form.append(field("allergies_detail", S["yes_detail"], "", "text", False, True))
form.append(
    radios("health_conditions", S["health_cond"], [(S["yes"], S["yes"]), (S["no"], S["no"])])
)
form.append(field("health_conditions_detail", S["yes_detail"], "", "text", False, True))
form.append(
    radios(
        "meal_type",
        S["meal"],
        [(S["meal1"], S["meal1"]), (S["meal2"], S["meal2"]), (S["meal3"], S["meal3"])],
    )
)
form.append(field("meal_type_other", S["meal_other"], "", "text", False))
form.append(nav(back=True, nxt=True))
form.append(C("div"))

form.append('<div class="mshk-apply__pane" data-step="6" hidden>')
form.append('<p class="mshk-apply__section">' + h("sec_resp") + C("p"))
form.append('<p class="mshk-apply__hint" style="margin-bottom:16px">' + h("resp_h") + C("p"))
form.append(agree("agree_participate", S["a1"]))
form.append(agree("agree_notice", S["a2"]))
form.append(agree("agree_truth", S["a3"]))
form.append(agree("agree_extra_docs", S["a4"]))
form.append(agree("agree_refusal", S["a5"]))
form.append(agree("agree_logistics_city", S["a6"]))
form.append(agree("agree_logistics_change", S["a8"]))
form.append(agree("agree_logistics_fixed", S["a7"]))
form.append(nav(back=True, send=True))
form.append(C("div"))

form.append(
    '<div class="mshk-apply__ok" id="mshk-apply-done" hidden><h3>'
    + h("done")
    + C("h3")
    + "<p>"
    + C("p")
    + C("div")
)
form.append(C("form") + C("div") + C("section"))

combined = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;1,400&display=swap" rel="stylesheet">'
    "<style>"
    + CSS
    + C("style")
    + "\n".join(parts)
    + "\n"
    + "\n".join(form)
    + "\n<script>"
    + JS
    + C("script")
)

preview = (
    "<!DOCTYPE html>\n"
    '<html lang="ru">\n'
    "<head>\n"
    '  <meta charset="utf-8">\n'
    '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "  <title>"
    + eh(S["title1"])
    + C("title")
    + "\n  <style>html,body{margin:0;padding:0;height:auto;min-height:0;max-width:100%;overflow-x:hidden;background:#fafafa}"
    + C("style")
    + "\n"
    + C("head")
    + "\n<body>\n"
    + combined
    + "\n"
    + C("body")
    + "\n"
    + C("html")
    + "\n"
)

STATIC.mkdir(parents=True, exist_ok=True)
TILDA.mkdir(parents=True, exist_ok=True)
(STATIC / "info.html").write_text(preview, encoding="utf-8")
(TILDA / "preview-info.html").write_text(preview, encoding="utf-8")
print("wrote", STATIC / "info.html", len(preview))
