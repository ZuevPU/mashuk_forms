# -*- coding: utf-8 -*-
"""Tilda T123 iframe snippets. ASCII only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TILDA = ROOT / "tilda"

SCRIPT = r"""
(function () {
  var clip = document.getElementById("__CLIP__");
  var frame = document.getElementById("__FRAME__");
  if (!clip || !frame) return;
  var old = document.getElementById("__OLD__");
  if (old) old.style.cssText = "display:none!important;height:0!important;overflow:hidden!important";
  var lastH = 0;
  var busy = 0;
  function recOf(el) {
    var n = el;
    for (var i = 0; i < 16 && n; i++) {
      var id = n.id ? String(n.id) : "";
      var cn = n.className ? String(n.className) : "";
      if (id.indexOf("rec") === 0 || cn.indexOf("t-rec") !== -1) return n;
      n = n.parentElement;
    }
    return el.parentElement;
  }
  function bleed() {
    var rec = recOf(clip);
    var n = clip;
    for (var i = 0; i < 24 && n && n !== document.body; i++) {
      n.style.setProperty("width", "100%", "important");
      n.style.setProperty("max-width", "none", "important");
      n.style.setProperty("padding-left", "0px", "important");
      n.style.setProperty("padding-right", "0px", "important");
      n.style.setProperty("margin-left", "0px", "important");
      n.style.setProperty("margin-right", "0px", "important");
      n.style.setProperty("box-sizing", "border-box", "important");
      var cn = n.className ? String(n.className) : "";
      if (n === rec || cn.indexOf("t-rec") !== -1) break;
      n = n.parentElement;
    }
    if (rec && rec.style) {
      rec.style.setProperty("width", "100vw", "important");
      rec.style.setProperty("max-width", "100vw", "important");
      rec.style.setProperty("margin-left", "calc(50% - 50vw)", "important");
      rec.style.setProperty("margin-right", "calc(50% - 50vw)", "important");
      rec.style.setProperty("padding-left", "0px", "important");
      rec.style.setProperty("padding-right", "0px", "important");
      rec.style.setProperty("left", "0px", "important");
      rec.style.setProperty("overflow", "hidden", "important");
      rec.style.setProperty("padding-bottom", "0px", "important");
    }
  }
  function cap() {
    var vh = window.innerHeight || 640;
    var rec = recOf(clip);
    var top = 0;
    try {
      if (rec) top = rec.getBoundingClientRect().top;
    } catch (e) {}
    var remain = Math.round(vh - Math.max(0, top) - 2);
    return Math.max(480, remain);
  }
  function pin() {
    if (busy) return;
    busy = 1;
    bleed();
    var h = cap();
    if (!(lastH && Math.abs(h - lastH) < 8)) {
      lastH = h;
      var px = h + "px";
      clip.style.cssText = "box-sizing:border-box;width:100%;max-width:none;height:" + px + ";max-height:" + px + ";min-height:" + px + ";overflow:hidden;background:#fafafa;line-height:normal;margin:0;padding:0;";
      frame.style.cssText = "display:block;width:100%;max-width:none;height:" + px + ";max-height:" + px + ";border:0;background:#fafafa;pointer-events:auto;touch-action:manipulation;margin:0;padding:0;";
      frame.setAttribute("scrolling", "yes");
      var rec = recOf(clip);
      if (rec && rec.style) {
        rec.style.setProperty("min-height", "0px", "important");
        rec.style.setProperty("max-height", (h + 8) + "px", "important");
      }
    }
    busy = 0;
  }
  pin();
  setTimeout(pin, 200);
  setTimeout(pin, 800);
  window.addEventListener("orientationchange", function () {
    lastH = 0;
    setTimeout(pin, 300);
  });
  window.addEventListener("resize", function () {
    lastH = 0;
    pin();
  });
})();
"""


def block(kind):
    if kind == "apply":
        clip, frame = "mshk-a-clip", "mshk-a-frame"
        src = "https://zuevpu-mashuk-forms-e759.twc1.net/"
        title = "Mashuk apply"
        old = "mshk-apply-wrap"
        page = "seminar application"
    else:
        clip, frame = "mshk-i-clip", "mshk-i-frame"
        src = "https://zuevpu-mashuk-forms-e759.twc1.net/info"
        title = "Mashuk participant data"
        old = "mshk-info-wrap"
        page = "participant data"
    js = SCRIPT.replace("__CLIP__", clip).replace("__FRAME__", frame).replace("__OLD__", old)
    return (
        "<!-- Tilda T123, padding 0, full width.\n"
        "     Page: " + page + ". DELETE the old iframe block, then paste this.\n"
        "     Record: Stretch / full width. Height: 0 / Auto. -->\n"
        '<div id="' + clip + '" style="box-sizing:border-box;width:100%;max-width:none;'
        'height:100vh;overflow:hidden;background:#fafafa;margin:0;padding:0;">\n'
        '  <iframe id="' + frame + '" src="' + src + '" title="' + title + '" '
        'loading="eager" scrolling="yes" allow="clipboard-write" '
        'style="display:block;width:100%;max-width:none;height:100vh;border:0;'
        'background:#fafafa;pointer-events:auto;touch-action:manipulation;'
        'margin:0;padding:0;"></iframe>\n'
        "</div>\n"
        "<script>" + js + "</script>\n"
    )


def main():
    TILDA.mkdir(parents=True, exist_ok=True)
    apply_html = block("apply")
    info_html = block("info")
    (TILDA / "tilda-iframe-block.html").write_text(apply_html, encoding="utf-8")
    (TILDA / "tilda-iframe-info.html").write_text(info_html, encoding="utf-8")
    print("wrote", TILDA / "tilda-iframe-block.html", len(apply_html))
    print("wrote", TILDA / "tilda-iframe-info.html", len(info_html))


if __name__ == "__main__":
    main()
