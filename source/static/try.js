/* MyPowerfulNotes: the Try it page. A small copy of the app's page, pens and scale drawing, in the browser only.
   Page units: an A4 page is 840 × 1188 (4 units to the millimetre). Nothing is saved or sent anywhere. */
(function () {
  "use strict";

  var PW = 840, PH = 1188, U = 4;               // page size and units per mm on the page
  var INK = "#1E242B", ACCENT = "#0E6E66", DIM = "#4F7C93", GUIDE = "#6FA8DC", PART = "#2E7D32", FLAG = "#E8710A";
  var WIDTHS = { pen: [2.2, 3.6, 6], fine: [2, 3.2, 5], hl: [18, 26, 36] };
  var DASHES = { "": [], dash: [16, 8], dot: [2, 7], dashdot: [16, 6, 2, 6] };

  var $ = function (id) { return document.getElementById(id); };
  var app = $("app"), cv = $("cv"), ctx = cv.getContext("2d"), sheet = $("sheet"), desk = $("desk");

  // ---------------------------------------------------------------------------------------------------------------
  // The document
  // ---------------------------------------------------------------------------------------------------------------
  function newPage(paper) { return { paper: paper || "Ruled", strokes: [], texts: [], flags: [], drawing: null, cut: null }; }
  var doc = { pages: [newPage("Ruled")], cur: 0 };
  var state = { tool: "pen", colour: "#111111", width: 1, fit: "page", mode: "line", dash: "",
                show: { lengths: true, measures: true, parts: true } };
  var undoStack = [], redoStack = [];
  var page = function () { return doc.pages[doc.cur]; };

  function snapshot() {
    undoStack.push(JSON.stringify(doc));
    if (undoStack.length > 60) undoStack.shift();
    redoStack = [];
  }
  function undo() {
    if (!undoStack.length) return;
    redoStack.push(JSON.stringify(doc));
    doc = JSON.parse(undoStack.pop());
    cad.sel = null; cad.chain = null;
    refreshAll();
  }
  function redo() {
    if (!redoStack.length) return;
    undoStack.push(JSON.stringify(doc));
    doc = JSON.parse(redoStack.pop());
    refreshAll();
  }

  // A starter page, so there's something to look at.
  (function seed() {
    var p = page();
    p.texts.push({ x: 120, y: 150, text: "Try it", size: 34, bold: true });
    p.texts.push({ x: 120, y: 214, text: "Write here with the pen, then try the highlighter,", size: 19 });
    p.texts.push({ x: 120, y: 246, text: "a flag, or the scale drawing tool.", size: 19 });
  })();

  // ---------------------------------------------------------------------------------------------------------------
  // Layout: fit the page into the desk
  // ---------------------------------------------------------------------------------------------------------------
  var scale = 1, dpr = 1;
  function layout() {
    var dw = desk.clientWidth - 32, dh = desk.clientHeight - 32;
    if (dw <= 0 || dh <= 0) return;
    scale = state.fit === "page" ? Math.min(dw / PW, dh / PH) : dw / PW;
    scale = Math.max(scale, 0.2);
    var w = Math.round(PW * scale), h = Math.round(PH * scale);
    dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    sheet.style.width = w + "px"; sheet.style.height = h + "px";
    cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    cv.style.width = w + "px"; cv.style.height = h + "px";
    render();
  }

  // ---------------------------------------------------------------------------------------------------------------
  // Drawing the page
  // ---------------------------------------------------------------------------------------------------------------
  function line(c, x1, y1, x2, y2) { c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke(); }

  function drawPaper(c, kind) {
    c.fillStyle = "#FFFFFF"; c.fillRect(0, 0, PW, PH);
    c.lineWidth = 1; c.strokeStyle = "#D6E1EC";
    var x, y;
    if (kind === "Ruled" || kind === "Cornell") {
      var left = kind === "Cornell" ? 230 : 40, top = kind === "Cornell" ? 150 : 150, bottom = kind === "Cornell" ? PH - 260 : PH - 50;
      for (y = top; y <= bottom; y += 32) line(c, left, y, PW - 40, y);
      c.strokeStyle = kind === "Cornell" ? "#9DB3C8" : "#E8B4B4"; c.lineWidth = 1.4;
      if (kind === "Ruled") line(c, 110, 20, 110, PH - 20);
      else { line(c, 30, 110, PW - 30, 110); line(c, 210, 110, 210, PH - 230); line(c, 30, PH - 230, PW - 30, PH - 230); }
    } else if (kind === "Grid" || kind === "Three views") {
      c.strokeStyle = "#E3EAF1";
      for (x = 20; x <= PW - 20; x += 20) line(c, x, 20, x, PH - 20);
      for (y = 20; y <= PH - 20; y += 20) line(c, 20, y, PW - 20, y);
      if (kind === "Three views") {
        c.strokeStyle = "#9DB3C8"; c.lineWidth = 1.6;
        line(c, PW / 2, 20, PW / 2, PH - 20); line(c, 20, PH / 2, PW - 20, PH / 2);
        c.fillStyle = "#7F95AB"; c.font = "600 18px Inter, sans-serif";
        c.fillText("Plan", 32, 46); c.fillText("Front", 32, PH / 2 + 28); c.fillText("Side", PW / 2 + 12, PH / 2 + 28);
      }
    } else if (kind === "Dots") {
      c.fillStyle = "#B9C5D2";
      for (x = 30; x <= PW - 30; x += 24) for (y = 30; y <= PH - 30; y += 24) { c.beginPath(); c.arc(x, y, 1.3, 0, 7); c.fill(); }
    } else if (kind === "Isometric") {
      c.strokeStyle = "#E3EAF1"; var s = 28, k = Math.tan(Math.PI / 6);
      for (x = -PH; x <= PW + PH; x += s / k / 2) {
        line(c, x, 0, x + PH / k, PH); line(c, x, 0, x - PH / k, PH);
      }
      for (x = 0; x <= PW; x += s / k / 2) line(c, x, 0, x, PH);
    }
    // the page's date, as in the app
    c.fillStyle = "#8A939C"; c.font = "17px Inter, sans-serif"; c.textAlign = "right";
    c.fillText(today, PW - 40, 60); c.textAlign = "left";
  }
  var today = new Date().toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" });

  function drawStroke(c, s) {
    var p = s.pts;
    if (!p.length) return;
    c.lineCap = "round"; c.lineJoin = "round";
    if (s.tool === "hl") {
      c.save(); c.globalAlpha = 0.38; c.strokeStyle = s.colour === "#111111" ? "#FFD400" : s.colour; c.lineWidth = s.w;
      c.lineCap = "butt"; c.beginPath(); c.moveTo(p[0][0], p[0][1]);
      for (var i = 1; i < p.length; i++) c.lineTo(p[i][0], p[i][1]);
      c.stroke(); c.restore(); return;
    }
    c.strokeStyle = s.colour; c.fillStyle = s.colour;
    if (p.length === 1) { c.beginPath(); c.arc(p[0][0], p[0][1], s.w / 2, 0, 7); c.fill(); return; }
    if (s.tool === "fine") {
      c.lineWidth = s.w; c.beginPath(); c.moveTo(p[0][0], p[0][1]);
      for (var j = 1; j < p.length - 1; j++) {
        var mx = (p[j][0] + p[j + 1][0]) / 2, my = (p[j][1] + p[j + 1][1]) / 2;
        c.quadraticCurveTo(p[j][0], p[j][1], mx, my);
      }
      c.lineTo(p[p.length - 1][0], p[p.length - 1][1]); c.stroke(); return;
    }
    for (var k = 1; k < p.length; k++) penSegment(c, s, p[k - 1], p[k]);
  }
  function penSegment(c, s, a, b) {
    c.lineWidth = s.w * (0.35 + 1.3 * ((a[2] + b[2]) / 2));
    c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke();
  }

  function drawTexts(c, p) {
    p.texts.forEach(function (t) {
      c.fillStyle = t.colour || INK;
      c.font = (t.bold ? "600 " : "") + t.size + "px Inter, 'Segoe UI', sans-serif";
      String(t.text).split("\n").forEach(function (ln, i) { c.fillText(ln, t.x, t.y + i * t.size * 1.35); });
    });
  }

  function drawFlags(c, p) {
    p.flags.forEach(function (f) {
      c.save(); c.strokeStyle = f.done ? "#2E7D32" : FLAG; c.lineWidth = 1.6; c.setLineDash([6, 4]);
      c.strokeRect(f.x, f.y, f.w, f.h); c.restore();
      c.fillStyle = f.done ? "#2E7D32" : FLAG;
      c.fillRect(f.x - 4, f.y - 26, 2.4, 26);
      c.beginPath(); c.moveTo(f.x - 2, f.y - 26); c.lineTo(f.x + 14, f.y - 20); c.lineTo(f.x - 2, f.y - 14); c.fill();
    });
  }

  // ---- Scale drawing ----
  function realMm(units, d) { return units / U * d.scale; }
  function fmtLen(mm) {
    var units = $("cadUnits").value;
    if (units === "m") return (mm / 1000).toFixed(mm >= 10000 ? 2 : 3).replace(/0+$/, "").replace(/\.$/, "") + " m";
    return String(Math.round(mm));
  }
  function len(l) { return Math.hypot(l.x2 - l.x1, l.y2 - l.y1); }

  function drawDrawing(c, d, live) {
    c.save();
    c.fillStyle = "#FFFFFF"; c.fillRect(d.x, d.y, d.w, d.h);
    c.beginPath(); c.rect(d.x, d.y, d.w, d.h); c.clip();
    // grid every 100 mm real, finer at large scales
    var step = 100 / d.scale * U; while (step < 14) step *= 5; while (step > 80) step /= 2;
    c.strokeStyle = "#EEF2F6"; c.lineWidth = 1;
    for (var gx = d.x; gx <= d.x + d.w; gx += step) line(c, gx, d.y, gx, d.y + d.h);
    for (var gy = d.y; gy <= d.y + d.h; gy += step) line(c, d.x, gy, d.x + d.w, gy);
    // guides
    c.strokeStyle = GUIDE; c.lineWidth = 1.4; c.setLineDash([2, 6]);
    d.guides.forEach(function (g) { line(c, g.x1, g.y1, g.x2, g.y2); });
    c.setLineDash([]);
    // parts fill
    if (state.show.parts) d.parts.forEach(function (pt) {
      var r = rectById(d, pt.rect); if (!r) return;
      c.fillStyle = "rgba(46,125,50,0.05)"; c.fillRect(r.x, r.y, r.w, r.h);
    });
    // lines
    d.lines.forEach(function (l) {
      var sel = cad.sel === l.id;
      if (sel) { c.strokeStyle = "rgba(14,110,102,0.3)"; c.lineWidth = 9; c.setLineDash([]); line(c, l.x1, l.y1, l.x2, l.y2); }
      c.strokeStyle = INK; c.lineWidth = 2.4; c.lineCap = "round"; c.setLineDash(DASHES[l.dash || ""]);
      line(c, l.x1, l.y1, l.x2, l.y2); c.setLineDash([]);
      if (state.show.lengths && len(l) > 30) lengthLabel(c, l, d);
      if (sel) [[l.x1, l.y1], [l.x2, l.y2]].forEach(function (h) {
        c.fillStyle = "#fff"; c.strokeStyle = ACCENT; c.lineWidth = 2.4;
        c.beginPath(); c.arc(h[0], h[1], 7, 0, 7); c.fill(); c.stroke();
      });
    });
    if (state.show.measures) d.measures.forEach(function (m) { dimension(c, m, d); });
    if (state.show.parts) d.parts.forEach(function (pt) {
      var r = rectById(d, pt.rect); if (!r) return;
      pill(c, r.x + r.w / 2, r.y + r.h / 2, pt.qty > 1 ? pt.name + " ×" + pt.qty : pt.name);
    });
    if (live) live(c);
    c.restore();
    c.strokeStyle = "#9AA6B2"; c.lineWidth = 1.4; c.strokeRect(d.x, d.y, d.w, d.h);
    c.fillStyle = "#5C6670"; c.font = "16px Inter, sans-serif";
    c.fillText("1:" + d.scale, d.x + 8, d.y + d.h + 22);
  }
  function lengthLabel(c, l, d) {
    var mx = (l.x1 + l.x2) / 2, my = (l.y1 + l.y2) / 2, ang = Math.atan2(l.y2 - l.y1, l.x2 - l.x1);
    if (ang > Math.PI / 2 || ang <= -Math.PI / 2) ang += Math.PI;
    c.save(); c.translate(mx, my); c.rotate(ang);
    c.fillStyle = DIM; c.font = "500 15px Inter, sans-serif"; c.textAlign = "center";
    c.fillText(fmtLen(realMm(len(l), d)), 0, -8); c.restore();
  }
  function dimension(c, m, d) {
    var dx = m.x2 - m.x1, dy = m.y2 - m.y1, L = Math.hypot(dx, dy); if (L < 1) return;
    var nx = dy / L, ny = -dx / L, o = m.off;
    var ax = m.x1 + nx * o, ay = m.y1 + ny * o, bx = m.x2 + nx * o, by = m.y2 + ny * o;
    c.strokeStyle = DIM; c.lineWidth = 1.2;
    var sg = o >= 0 ? 1 : -1;
    line(c, m.x1 + nx * 6 * sg, m.y1 + ny * 6 * sg, ax + nx * 8 * sg, ay + ny * 8 * sg);
    line(c, m.x2 + nx * 6 * sg, m.y2 + ny * 6 * sg, bx + nx * 8 * sg, by + ny * 8 * sg);
    line(c, ax, ay, bx, by);
    var ux = dx / L, uy = dy / L;
    [[ax, ay, 1], [bx, by, -1]].forEach(function (e) {
      c.beginPath(); c.moveTo(e[0] + (ux * 12 + nx * 4) * e[2], e[1] + (uy * 12 + ny * 4) * e[2]);
      c.lineTo(e[0], e[1]); c.lineTo(e[0] + (ux * 12 - nx * 4) * e[2], e[1] + (uy * 12 - ny * 4) * e[2]); c.stroke();
    });
    var ang = Math.atan2(dy, dx); if (ang > Math.PI / 2 || ang <= -Math.PI / 2) ang += Math.PI;
    var label = fmtLen(realMm(L, d));
    c.save(); c.translate((ax + bx) / 2, (ay + by) / 2); c.rotate(ang);
    c.font = "500 15px Inter, sans-serif"; var tw = c.measureText(label).width + 10;
    c.fillStyle = "#fff"; c.fillRect(-tw / 2, -10, tw, 20);
    c.fillStyle = DIM; c.textAlign = "center"; c.fillText(label, 0, 5); c.restore();
  }
  function pill(c, x, y, label) {
    c.font = "500 14px Inter, sans-serif"; var w = c.measureText(label).width + 18;
    c.fillStyle = "#fff"; c.strokeStyle = "#9CCBA3"; c.lineWidth = 1.2;
    roundRect(c, x - w / 2, y - 12, w, 24, 12); c.fill(); c.stroke();
    c.fillStyle = PART; c.textAlign = "center"; c.fillText(label, x, y + 5); c.textAlign = "left";
  }
  function roundRect(c, x, y, w, h, r) {
    c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath();
  }
  function rectById(d, id) { for (var i = 0; i < d.rects.length; i++) if (d.rects[i].id === id) return d.rects[i]; return null; }

  // ---- Cut list pages ----
  function drawCut(c, cut) {
    var x = 70, y = 110;
    c.fillStyle = INK; c.font = "600 34px Inter, sans-serif"; c.fillText(cut.first ? "Cut list" : "Cut list (continued)", x, y);
    c.fillStyle = "#5C6670"; c.font = "16px Inter, sans-serif";
    c.fillText(cut.note, x, y + 30);
    y += 78;
    if (cut.table) {
      c.fillStyle = INK; c.font = "600 22px Inter, sans-serif"; c.fillText(cut.material, x, y);
      c.fillStyle = "#5C6670"; c.font = "15px Inter, sans-serif";
      c.fillText("18 mm thick, sheets 2400 × 1200, 3.2 mm kerf, 10 mm trimmed off each edge.", x, y + 24);
      y += 46;
      var cols = [300, 70, 120, 120], heads = ["Part", "Qty", "Length", "Width"];
      c.fillStyle = "#EEF0EE"; c.fillRect(x, y, 610, 32);
      var rows = [heads].concat(cut.table.map(function (r) { return [r.name, String(r.qty), String(r.L), String(r.W)]; }));
      rows.forEach(function (row, ri) {
        var cx = x;
        row.forEach(function (cell, ci) {
          c.fillStyle = INK; c.font = (ri === 0 ? "600 " : "") + "16px Inter, sans-serif";
          c.textAlign = ci === 0 ? "left" : "right";
          c.fillText(cell, ci === 0 ? cx + 10 : cx + cols[ci] - 12, y + ri * 32 + 21);
          cx += cols[ci];
        });
        c.textAlign = "left"; c.strokeStyle = "#D8DCDF"; c.lineWidth = 1; line(c, x, y + (ri + 1) * 32, x + 610, y + (ri + 1) * 32);
      });
      y += rows.length * 32 + 34;
      c.fillStyle = INK; c.font = "16px Inter, sans-serif";
      c.fillText(cut.summary, x, y); y += 40;
    }
    cut.sheets.forEach(function (sh) {
      c.fillStyle = INK; c.font = "600 18px Inter, sans-serif";
      c.fillText("Sheet " + sh.n + " of " + cut.total + ", " + sh.used + "% used", x, y); y += 16;
      var k = 700 / 2400, h = 1200 * k;
      c.fillStyle = "#F4EBDD"; c.fillRect(x, y, 700, h); c.strokeStyle = "#9A8A72"; c.lineWidth = 1.2; c.strokeRect(x, y, 700, h);
      c.setLineDash([3, 3]); c.strokeStyle = "#C9B99E"; c.strokeRect(x + 10 * k, y + 10 * k, 700 - 20 * k, h - 20 * k); c.setLineDash([]);
      sh.parts.forEach(function (pp) {
        var rx = x + pp.x * k, ry = y + pp.y * k, rw = pp.w * k, rh = pp.h * k;
        c.fillStyle = "#fff"; c.fillRect(rx, ry, rw, rh); c.strokeStyle = INK; c.lineWidth = 1.2; c.strokeRect(rx, ry, rw, rh);
        c.font = "500 " + (rw > 90 ? 13 : 11) + "px Inter, sans-serif"; c.fillStyle = INK; c.textAlign = "center";
        if (rw > 40 && rh > 18) c.fillText(pp.name, rx + rw / 2, ry + rh / 2 + (rh > 40 ? -2 : 4));
        if (rw > 60 && rh > 40) { c.fillStyle = "#5C6670"; c.font = "11px Inter, sans-serif"; c.fillText(Math.round(pp.L) + " × " + Math.round(pp.W), rx + rw / 2, ry + rh / 2 + 14); }
        c.textAlign = "left";
      });
      y += h + 44;
    });
  }

  function renderPage(c, p, live) {
    drawPaper(c, p.cut ? "Blank" : p.paper);
    if (p.cut) drawCut(c, p.cut);
    p.strokes.forEach(function (s) { if (s.tool === "hl") drawStroke(c, s); });
    if (p.drawing) drawDrawing(c, p.drawing, live && live.cad);
    drawTexts(c, p);
    p.strokes.forEach(function (s) { if (s.tool !== "hl") drawStroke(c, s); });
    drawFlags(c, p);
    if (live && live.page) live.page(c);
  }

  var liveDraw = null;
  function render() {
    ctx.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0);
    renderPage(ctx, page(), liveDraw);
  }

  // ---------------------------------------------------------------------------------------------------------------
  // Thumbnails, page count and actions
  // ---------------------------------------------------------------------------------------------------------------
  function thumbs() {
    var host = $("pages"); host.textContent = "";
    var head = document.createElement("div"); head.className = "pages-head"; head.textContent = "Pages"; host.appendChild(head);
    doc.pages.forEach(function (p, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "thumb" + (i === doc.cur ? " on" : "");
      b.setAttribute("aria-label", "Page " + (i + 1)); if (i === doc.cur) b.setAttribute("aria-current", "page");
      var t = document.createElement("canvas"); t.width = 84; t.height = 119;
      var c = t.getContext("2d"); c.setTransform(84 / PW, 0, 0, 119 / PH, 0, 0); renderPage(c, p);
      var n = document.createElement("span"); n.textContent = i + 1;
      b.appendChild(n); b.appendChild(t);
      b.addEventListener("click", function () { go(i); });
      host.appendChild(b);
    });
  }
  function counts() {
    $("pageCount").textContent = (doc.cur + 1) + " / " + doc.pages.length;
    $("pageTitle").textContent = page().cut ? "Cut list" : "Page " + (doc.cur + 1);
  }
  function actions() {
    var list = $("actionList"); list.textContent = "";
    var n = 0;
    doc.pages.forEach(function (p, pi) {
      p.flags.forEach(function (f) {
        n++;
        var li = document.createElement("li");
        var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = !!f.done; cb.setAttribute("aria-label", "Done: " + f.text);
        cb.addEventListener("change", function () { snapshot(); f.done = cb.checked; refreshAll(); });
        var b = document.createElement("button"); b.type = "button";
        var t = document.createElement("strong"); t.textContent = f.text || "Action";
        var w = document.createElement("small"); w.textContent = "Page " + (pi + 1) + (f.done ? " · done" : "");
        b.appendChild(t); b.appendChild(w);
        b.addEventListener("click", function () { go(pi); });
        if (f.done) li.className = "done";
        li.appendChild(cb); li.appendChild(b); list.appendChild(li);
      });
    });
    $("actionEmpty").hidden = n > 0;
  }
  function refreshAll() {
    if (doc.cur >= doc.pages.length) doc.cur = doc.pages.length - 1;
    counts(); thumbs(); actions(); cadUi(); render();
  }
  function go(i) {
    if (i < 0 || i >= doc.pages.length) return;
    finishText(); cad.chain = null; cad.sel = null; cad.task = ""; doc.cur = i; refreshAll();
  }

  // ---------------------------------------------------------------------------------------------------------------
  // Toolbar
  // ---------------------------------------------------------------------------------------------------------------
  function pressed(sel, attr, val) {
    app.querySelectorAll(sel).forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute(attr) === String(val))); });
  }
  var HINTS = {
    pen: "Pen: write on the page. A pen or stylus gives pressure.", fine: "Fineliner: an even line, good for sketches and labels.",
    hl: "Highlighter: drag across writing. It goes under the ink.", eraser: "Eraser: touch a stroke to rub it out.",
    text: "Text: tap the page and type. Tap outside the box to finish.", flag: "Flag: drag a box across a line of writing, then say what the action is.",
    draw: "Scale drawing: drag a box on the page for the drawing."
  };
  function setTool(t) {
    finishText(); state.tool = t; cad.chain = null; cad.task = "";
    pressed("[data-tool]", "data-tool", t);
    $("cadbar").hidden = !(t === "draw" && page().drawing);
    hint(t === "draw" && page().drawing ? cadHint() : HINTS[t]);
    cv.style.cursor = t === "text" ? "text" : "crosshair";
    render(); placeBar();
  }
  function hint(s) { $("hint").textContent = s; }

  app.querySelectorAll("[data-tool]").forEach(function (b) { b.addEventListener("click", function () { setTool(b.dataset.tool); }); });
  app.querySelectorAll("[data-colour]").forEach(function (b) {
    b.firstChild.style.background = b.dataset.colour;
    b.addEventListener("click", function () { state.colour = b.dataset.colour; pressed("[data-colour]", "data-colour", state.colour); });
  });
  app.querySelectorAll("[data-width]").forEach(function (b) {
    b.addEventListener("click", function () { state.width = +b.dataset.width; pressed("[data-width]", "data-width", state.width); });
  });
  app.querySelectorAll("[data-act]").forEach(function (b) {
    b.addEventListener("click", function () {
      var a = b.dataset.act;
      if (a === "undo") undo();
      else if (a === "redo") redo();
      else if (a === "prev") go(doc.cur - 1);
      else if (a === "next") go(doc.cur + 1);
      else if (a === "add") { snapshot(); doc.pages.splice(doc.cur + 1, 0, newPage(page().cut ? "Ruled" : page().paper)); go(doc.cur + 1); }
      else if (a === "actions") { var h = !$("actions").hidden; $("actions").hidden = h; b.setAttribute("aria-pressed", String(!h)); setTimeout(layout, 0); }
      else if (a === "pages") { var on = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", String(on)); app.classList.toggle("no-pages", !on); setTimeout(layout, 0); }
      else if (a === "fit") { state.fit = state.fit === "page" ? "width" : "page"; layout(); }
    });
  });

  $("actionsClose").addEventListener("click", function () {
    $("actions").hidden = true; app.querySelector('[data-act="actions"]').setAttribute("aria-pressed", "false"); setTimeout(layout, 0);
  });

  // menus
  var openMenu = null;
  function closeMenu() { if (openMenu) { openMenu.hidden = true; openMenu = null; } }
  app.querySelectorAll("[data-menu]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var m = $(b.dataset.menu);
      if (openMenu === m) { closeMenu(); return; }
      closeMenu(); m.hidden = false; openMenu = m;
      var ar = app.getBoundingClientRect(), br = b.getBoundingClientRect();
      var left = Math.min(br.left - ar.left, ar.width - m.offsetWidth - 8);
      m.style.left = Math.max(8, left) + "px"; m.style.top = (br.bottom - ar.top + 4) + "px";
    });
  });
  document.addEventListener("click", function (e) { if (openMenu && !openMenu.contains(e.target)) closeMenu(); });
  $("showMenu").addEventListener("click", function (e) { e.stopPropagation(); });
  app.querySelectorAll("[data-paper]").forEach(function (b) {
    b.addEventListener("click", function () {
      closeMenu(); if (page().cut) { hint("A cut list page keeps its own layout."); return; }
      snapshot(); page().paper = b.dataset.paper; refreshAll();
    });
  });

  // ---------------------------------------------------------------------------------------------------------------
  // Pointer input
  // ---------------------------------------------------------------------------------------------------------------
  function pt(e) { var r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / scale, (e.clientY - r.top) / scale]; }
  var active = null;   // the stroke, box or drag in progress

  cv.addEventListener("pointerdown", function (e) {
    if (e.button !== undefined && e.button > 0) { if (state.tool === "draw") { cad.chain = null; render(); } return; }
    closeMenu();
    var p = pt(e), t = state.tool;
    if (t === "text") { e.preventDefault(); startText(p); return; }
    cv.setPointerCapture(e.pointerId);
    if (t === "pen" || t === "fine" || t === "hl") {
      var pr = e.pointerType === "pen" ? (e.pressure || 0.5) : 0.5;
      active = { kind: "stroke", s: { tool: t, colour: state.colour, w: WIDTHS[t][state.width], pts: [[p[0], p[1], pr]] } };
      if (t === "hl") active.s.colour = state.colour === "#111111" ? "#FFD400" : state.colour;
    } else if (t === "eraser") { snapshot(); active = { kind: "erase", any: false }; erase(p); }
    else if (t === "flag") { active = { kind: "box", a: p, b: p, then: "flag" }; }
    else if (t === "draw") cadDown(p, e);
  });
  cv.addEventListener("pointermove", function (e) {
    var p = pt(e);
    if (!active) { if (state.tool === "draw") cadHover(p); return; }
    if (active.kind === "stroke") {
      var evs = e.getCoalescedEvents ? e.getCoalescedEvents() : [e];
      if (!evs.length) evs = [e];
      ctx.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0);
      evs.forEach(function (ev) {
        var q = pt(ev), s = active.s, last = s.pts[s.pts.length - 1];
        if (Math.hypot(q[0] - last[0], q[1] - last[1]) < 0.8) return;
        var pr = ev.pointerType === "pen" ? (ev.pressure || 0.5) : 0.5;
        var np = [q[0], q[1], pr]; s.pts.push(np);
        if (s.tool === "pen") { ctx.strokeStyle = s.colour; ctx.lineCap = "round"; penSegment(ctx, s, last, np); }
      });
      if (active.s.tool !== "pen") { liveDraw = { page: function (c) { drawStroke(c, active.s); } }; render(); liveDraw = null; }
    } else if (active.kind === "erase") erase(p);
    else if (active.kind === "box") {
      active.b = p;
      var a = active.a;
      liveDraw = { page: function (c) { c.save(); c.setLineDash([6, 4]); c.strokeStyle = active.then === "flag" ? FLAG : ACCENT; c.lineWidth = 1.6;
        c.strokeRect(Math.min(a[0], p[0]), Math.min(a[1], p[1]), Math.abs(p[0] - a[0]), Math.abs(p[1] - a[1])); c.restore(); } };
      render(); liveDraw = null;
    } else if (active.kind === "cad") cadMove(p);
  });
  function up(e) {
    if (!active) return;
    var a = active; active = null;
    if (a.kind === "stroke") { snapshot(); page().strokes.push(a.s); afterChange(); }
    else if (a.kind === "erase") { if (!a.any) undoStack.pop(); afterChange(); }
    else if (a.kind === "box") {
      var x = Math.min(a.a[0], a.b[0]), y = Math.min(a.a[1], a.b[1]), w = Math.abs(a.b[0] - a.a[0]), h = Math.abs(a.b[1] - a.a[1]);
      if (a.then === "flag") {
        if (w < 20 || h < 12) { render(); hint("Drag a box across a line of writing to flag it."); return; }
        var f = { x: x, y: y, w: w, h: h, text: "", done: false };
        ask("What's the action?", "", function (v) { snapshot(); f.text = v || "Action"; page().flags.push(f); afterChange(); hint("Flagged. It's in the Actions list."); }, render);
      } else if (a.then === "frame") {
        if (w < 80 || h < 80) { render(); hint("Drag a bigger box for the drawing."); return; }
        snapshot();
        page().drawing = { x: x, y: y, w: w, h: h, scale: +$("cadScale").value, lines: [], rects: [], measures: [], parts: [], guides: [], next: 1 };
        afterChange(); setTool("draw");
      }
    }
  }
  cv.addEventListener("pointerup", up);
  cv.addEventListener("pointercancel", function () { active = null; render(); });
  cv.addEventListener("contextmenu", function (e) { if (state.tool === "draw") e.preventDefault(); });

  function afterChange() { render(); thumbs(); actions(); counts(); }

  function erase(p) {
    var pg = page(), r = 10 + WIDTHS.pen[state.width] * 2, before = pg.strokes.length;
    pg.strokes = pg.strokes.filter(function (s) {
      return !s.pts.some(function (q) { return Math.hypot(q[0] - p[0], q[1] - p[1]) < r + s.w / 2; });
    });
    var nf = pg.flags.length;
    pg.flags = pg.flags.filter(function (f) { return !(p[0] > f.x - 20 && p[0] < f.x + 16 && p[1] > f.y - 30 && p[1] < f.y); });
    pg.texts = pg.texts.filter(function (t) {
      var w = String(t.text).split("\n").reduce(function (m, l) { return Math.max(m, l.length); }, 0) * t.size * 0.55;
      var h = String(t.text).split("\n").length * t.size * 1.35;
      return !(p[0] > t.x && p[0] < t.x + w && p[1] > t.y - t.size && p[1] < t.y - t.size + h);
    });
    if (pg.strokes.length !== before || pg.flags.length !== nf) active && (active.any = true);
    render();
  }

  // ---- text boxes ----
  var editing = null;
  function startText(p) {
    finishText();
    var ta = document.createElement("textarea"); ta.className = "page-text"; ta.setAttribute("aria-label", "Text");
    var size = 19;
    ta.style.left = (p[0] * scale) + "px"; ta.style.top = ((p[1] - size) * scale) + "px";
    ta.style.fontSize = (size * scale) + "px"; ta.style.width = Math.min(520, PW - p[0] - 20) * scale + "px";
    sheet.appendChild(ta); ta.focus();
    editing = { ta: ta, x: p[0], y: p[1], size: size, colour: state.colour === "#FFD400" ? INK : state.colour };
    ta.addEventListener("blur", finishText);
    ta.addEventListener("keydown", function (e) { if (e.key === "Escape") { e.stopPropagation(); finishText(); } });
  }
  function finishText() {
    if (!editing) return;
    var ed = editing; editing = null;
    var v = ed.ta.value.replace(/\s+$/, "");
    ed.ta.remove();
    if (v) { snapshot(); page().texts.push({ x: ed.x, y: ed.y, text: v, size: ed.size, colour: ed.colour }); afterChange(); }
  }

  // ---- the ask box ----
  var asking = null;
  function ask(label, value, ok, cancel) {
    $("askLabel").textContent = label; $("askInput").value = value; $("ask").hidden = false;
    asking = { ok: ok, cancel: cancel }; setTimeout(function () { $("askInput").focus(); $("askInput").select(); }, 0);
  }
  $("ask").addEventListener("submit", function (e) {
    e.preventDefault(); var a = asking; asking = null; $("ask").hidden = true; if (a) a.ok($("askInput").value.trim());
  });
  $("askCancel").addEventListener("click", function () { var a = asking; asking = null; $("ask").hidden = true; if (a && a.cancel) a.cancel(); });

  // ---------------------------------------------------------------------------------------------------------------
  // Scale drawing
  // ---------------------------------------------------------------------------------------------------------------
  var cad = { chain: null, sel: null, hover: null, task: "", measureA: null };

  function cadHint() {
    if (cad.task === "part") return "Make a part: tap inside a rectangle. Esc stops.";
    if (cad.task === "drawers") return "Plan drawers: tap inside the opening the drawers go in. Esc stops.";
    if (cad.task === "thirds" || cad.task === "golden") return "Proportion guides: tap inside the shape to divide, or anywhere else for the whole drawing.";
    return {
      line: "Draw lines: click where a line starts, then click each corner. Lines snap to ends and to square. Esc or double-click stops.",
      rect: "Rectangle: drag from one corner to the other.",
      select: "Select: tap a line. Type a length and press Edit to change it, or Delete.",
      measure: cad.measureA ? "Measure: now tap the second point." : "Measure: tap the first point. Points snap to the ends of lines."
    }[state.mode];
  }
  function cadUi() {
    var d = page().drawing;
    $("cadbar").hidden = !(state.tool === "draw" && d);
    if (d) $("cadScale").value = String(d.scale);
    pressed("[data-mode]", "data-mode", state.mode);
    $("ltSample").dataset.dash = state.dash;
    placeBar();
  }
  app.querySelectorAll("[data-mode]").forEach(function (b) {
    b.addEventListener("click", function () { state.mode = b.dataset.mode; cad.chain = null; cad.measureA = null; cad.task = ""; cadUi(); hint(cadHint()); render(); });
  });
  $("cadScale").addEventListener("change", function () { var d = page().drawing; if (!d) return; snapshot(); d.scale = +this.value; afterChange(); });
  $("cadUnits").addEventListener("change", render);
  app.querySelectorAll("[data-dash]").forEach(function (b) {
    if (b.tagName !== "BUTTON") return;
    b.addEventListener("click", function () {
      closeMenu(); state.dash = b.dataset.dash; cadUi();
      var d = page().drawing, l = d && lineById(d, cad.sel);
      if (l) { snapshot(); l.dash = state.dash; afterChange(); }
    });
  });
  ["Lengths", "Measures", "Parts"].forEach(function (k) {
    $("show" + k).addEventListener("change", function () { state.show[k.toLowerCase()] = this.checked; render(); });
  });
  function lineById(d, id) { if (!d) return null; for (var i = 0; i < d.lines.length; i++) if (d.lines[i].id === id) return d.lines[i]; return null; }

  function snap(p, d, from) {
    var best = null, bd = 12 / scale;
    d.lines.forEach(function (l) {
      [[l.x1, l.y1], [l.x2, l.y2]].forEach(function (q) { var dd = Math.hypot(q[0] - p[0], q[1] - p[1]); if (dd < bd) { bd = dd; best = q; } });
    });
    if (best) return { p: [best[0], best[1]], end: true };
    var x = p[0], y = p[1];
    if (from) {
      var ang = Math.atan2(y - from[1], x - from[0]), L = Math.hypot(x - from[0], y - from[1]);
      var step = Math.PI / 12, a2 = Math.round(ang / step) * step;
      if (Math.abs(a2 - ang) < 0.06) { x = from[0] + Math.cos(a2) * L; y = from[1] + Math.sin(a2) * L; }
      // whole millimetres, real size
      var mm = Math.round(realMm(Math.hypot(x - from[0], y - from[1]), d)), u = mm / d.scale * U, a3 = Math.atan2(y - from[1], x - from[0]);
      x = from[0] + Math.cos(a3) * u; y = from[1] + Math.sin(a3) * u;
    }
    return { p: [x, y], end: false };
  }
  function inside(d, p) { return p[0] >= d.x && p[0] <= d.x + d.w && p[1] >= d.y && p[1] <= d.y + d.h; }
  function addLine(d, a, b, dash) {
    var l = { id: d.next++, x1: a[0], y1: a[1], x2: b[0], y2: b[1], dash: dash === undefined ? state.dash : dash };
    d.lines.push(l); return l;
  }

  function cadDown(p, e) {
    var d = page().drawing;
    if (!d) { active = { kind: "box", a: p, b: p, then: "frame" }; return; }
    if (!inside(d, p)) { if (cad.chain) { cad.chain = null; render(); } return; }
    if (cad.task) { cadTask(p, d); return; }
    if (state.mode === "line") {
      var s = snap(p, d, cad.chain);
      if (!cad.chain) { cad.chain = s.p; render(); return; }
      if (Math.hypot(s.p[0] - cad.chain[0], s.p[1] - cad.chain[1]) < 2) { cad.chain = null; render(); return; }
      snapshot(); var l = addLine(d, cad.chain, s.p); cad.sel = null;
      cad.chain = s.end && closesLoop(d, s.p) ? null : s.p;
      afterChange();
      $("cadLen").value = fmtLen(realMm(len(l), d)).replace(" m", "");
    } else if (state.mode === "rect") {
      active = { kind: "cad", a: snap(p, d).p, b: snap(p, d).p };
    } else if (state.mode === "select") {
      cad.sel = nearestLine(d, p);
      var sl = lineById(d, cad.sel);
      if (sl) { $("cadLen").value = String(Math.round(realMm(len(sl), d))); $("cadAng").value = String(Math.round(-Math.atan2(sl.y2 - sl.y1, sl.x2 - sl.x1) * 180 / Math.PI)); }
      render();
    } else if (state.mode === "measure") {
      var q = snap(p, d).p;
      if (!cad.measureA) { cad.measureA = q; hint(cadHint()); render(); return; }
      snapshot(); d.measures.push({ x1: cad.measureA[0], y1: cad.measureA[1], x2: q[0], y2: q[1], off: 8 * U });
      cad.measureA = null; afterChange(); hint("Measured. Show or hide measurements with the eye button.");
      setTimeout(function () { hint(cadHint()); }, 2400);
    }
  }
  function closesLoop(d, p) {
    var n = 0; d.lines.forEach(function (l) { if ((Math.abs(l.x1 - p[0]) < 0.5 && Math.abs(l.y1 - p[1]) < 0.5) || (Math.abs(l.x2 - p[0]) < 0.5 && Math.abs(l.y2 - p[1]) < 0.5)) n++; });
    return n >= 2;
  }
  function cadMove(p) {
    var d = page().drawing; active.b = snap(p, d).p;
    var a = active.a, b = active.b;
    liveDraw = { cad: function (c) {
      c.strokeStyle = ACCENT; c.lineWidth = 2; c.setLineDash([8, 5]);
      c.strokeRect(Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])); c.setLineDash([]);
      c.fillStyle = DIM; c.font = "500 15px Inter, sans-serif";
      c.fillText(fmtLen(realMm(Math.abs(b[0] - a[0]), d)) + " × " + fmtLen(realMm(Math.abs(b[1] - a[1]), d)), Math.max(a[0], b[0]) + 8, Math.max(a[1], b[1]) + 18);
    } };
    render(); liveDraw = null;
  }
  // Rectangles finish here; everything else goes to up().
  var origUp = up;
  cv.removeEventListener("pointerup", up);
  cv.addEventListener("pointerup", function (e) {
    if (active && active.kind === "cad") {
      var d = page().drawing, a = active.a, b = snap(pt(e), d).p; active = null;
      var x = Math.min(a[0], b[0]), y = Math.min(a[1], b[1]), w = Math.abs(b[0] - a[0]), h = Math.abs(b[1] - a[1]);
      if (w < 6 || h < 6) { render(); return; }
      snapshot(); makeRect(d, x, y, w, h); afterChange();
      return;
    }
    origUp(e);
  });
  function makeRect(d, x, y, w, h, dash) {
    var ids = [addLine(d, [x, y], [x + w, y], dash).id, addLine(d, [x + w, y], [x + w, y + h], dash).id,
               addLine(d, [x + w, y + h], [x, y + h], dash).id, addLine(d, [x, y + h], [x, y], dash).id];
    var r = { id: d.next++, x: x, y: y, w: w, h: h, lines: ids }; d.rects.push(r); return r;
  }
  function nearestLine(d, p) {
    var best = null, bd = 12 / scale;
    d.lines.forEach(function (l) {
      var dx = l.x2 - l.x1, dy = l.y2 - l.y1, L2 = dx * dx + dy * dy || 1;
      var t = Math.max(0, Math.min(1, ((p[0] - l.x1) * dx + (p[1] - l.y1) * dy) / L2));
      var dd = Math.hypot(p[0] - (l.x1 + t * dx), p[1] - (l.y1 + t * dy));
      if (dd < bd) { bd = dd; best = l.id; }
    });
    return best;
  }
  function cadHover(p) {
    var d = page().drawing; if (!d || !inside(d, p)) return;
    if (state.mode === "line" && cad.chain && !cad.task) {
      var s = snap(p, d, cad.chain), a = cad.chain, b = s.p;
      liveDraw = { cad: function (c) {
        c.strokeStyle = ACCENT; c.lineWidth = 2; c.setLineDash(DASHES[state.dash].length ? DASHES[state.dash] : [8, 5]); line(c, a[0], a[1], b[0], b[1]); c.setLineDash([]);
        if (s.end) { c.strokeStyle = ACCENT; c.beginPath(); c.arc(b[0], b[1], 8, 0, 7); c.stroke(); }
        var mm = realMm(Math.hypot(b[0] - a[0], b[1] - a[1]), d), ang = Math.round(-Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI);
        c.fillStyle = ACCENT; c.font = "500 15px Inter, sans-serif"; c.fillText(fmtLen(mm) + "  " + ang + "°", b[0] + 12, b[1] - 12);
      } };
      render(); liveDraw = null;
    } else if ((state.mode === "measure" && cad.measureA) || state.mode === "line") {
      var q = snap(p, d).p, ma = cad.measureA;
      liveDraw = { cad: function (c) {
        c.strokeStyle = ACCENT; c.lineWidth = 1.6; c.beginPath(); c.arc(q[0], q[1], 6, 0, 7); c.stroke();
        if (ma) { c.setLineDash([4, 4]); line(c, ma[0], ma[1], q[0], q[1]); c.setLineDash([]); c.fillStyle = ACCENT; c.font = "500 15px Inter, sans-serif";
          c.fillText(fmtLen(realMm(Math.hypot(q[0] - ma[0], q[1] - ma[1]), d)), q[0] + 10, q[1] - 10); }
      } };
      render(); liveDraw = null;
    }
  }

  function num(v) { var n = parseFloat(String(v).replace(",", ".")); return isFinite(n) ? n : NaN; }
  function typedMm() { var v = num($("cadLen").value); return $("cadUnits").value === "m" ? v * 1000 : v; }
  $("cadAdd").addEventListener("click", function () {
    var d = page().drawing; if (!d) return;
    var mm = typedMm(), ang = num($("cadAng").value) || 0;
    if (!(mm > 0)) { hint("Type a length first, such as 600."); return; }
    var a = cad.chain || (d.lines.length ? [d.lines[d.lines.length - 1].x2, d.lines[d.lines.length - 1].y2] : [d.x + 40, d.y + d.h - 40]);
    var u = mm / d.scale * U, r = -ang * Math.PI / 180;
    snapshot(); addLine(d, a, [a[0] + Math.cos(r) * u, a[1] + Math.sin(r) * u]);
    cad.chain = [a[0] + Math.cos(r) * u, a[1] + Math.sin(r) * u]; afterChange();
  });
  $("cadEdit").addEventListener("click", function () {
    var d = page().drawing, l = lineById(d, cad.sel); if (!l) { hint("Select a line first."); return; }
    var mm = typedMm(); if (!(mm > 0)) { hint("Type the new length."); return; }
    var u = mm / d.scale * U, L = len(l) || 1, ox = l.x2, oy = l.y2;
    snapshot();
    l.x2 = l.x1 + (l.x2 - l.x1) / L * u; l.y2 = l.y1 + (l.y2 - l.y1) / L * u;
    // lines joined at the moved end follow it
    d.lines.forEach(function (o) {
      if (o === l) return;
      if (Math.abs(o.x1 - ox) < 0.5 && Math.abs(o.y1 - oy) < 0.5) { o.x1 = l.x2; o.y1 = l.y2; }
      if (Math.abs(o.x2 - ox) < 0.5 && Math.abs(o.y2 - oy) < 0.5) { o.x2 = l.x2; o.y2 = l.y2; }
    });
    d.rects = d.rects.filter(function (r) { return r.lines.indexOf(l.id) < 0; });
    afterChange(); hint("Length changed. The joined line followed.");
  });
  $("cadDel").addEventListener("click", function () {
    var d = page().drawing, l = lineById(d, cad.sel); if (!l) { hint("Select a line first."); return; }
    snapshot(); d.lines = d.lines.filter(function (o) { return o !== l; });
    var gone = d.rects.filter(function (r) { return r.lines.indexOf(l.id) >= 0; }).map(function (r) { return r.id; });
    d.rects = d.rects.filter(function (r) { return gone.indexOf(r.id) < 0; });
    d.parts = d.parts.filter(function (p) { return gone.indexOf(p.rect) < 0; });
    cad.sel = null; afterChange();
  });
  [$("cadLen"), $("cadAng")].forEach(function (i) {
    i.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); (cad.sel && state.mode === "select" ? $("cadEdit") : $("cadAdd")).click(); } });
  });

  // ---- woodwork ----
  function rectAt(d, p) {
    var hits = d.rects.filter(function (r) { return p[0] > r.x && p[0] < r.x + r.w && p[1] > r.y && p[1] < r.y + r.h; });
    hits.sort(function (a, b) { return a.w * a.h - b.w * b.h; });
    return hits[0] || null;
  }
  app.querySelectorAll("[data-wood]").forEach(function (b) {
    b.addEventListener("click", function () {
      closeMenu(); var d = page().drawing, w = b.dataset.wood;
      if (w === "cutlist") { cutList(); return; }
      if (!d) { hint("Make a scale drawing first: pick the drawing tool and drag a box on the page."); return; }
      if (w === "noguides") { snapshot(); d.guides = []; afterChange(); hint("Guides removed."); return; }
      cad.task = w; cad.chain = null; hint(cadHint());
    });
  });
  function cadTask(p, d) {
    var t = cad.task, r = rectAt(d, p);
    if (t === "thirds" || t === "golden") {
      var box = r || { x: d.x, y: d.y, w: d.w, h: d.h }, fr = t === "thirds" ? [1 / 3, 2 / 3] : [0.382, 0.618];
      snapshot();
      fr.forEach(function (f) {
        d.guides.push({ x1: box.x + box.w * f, y1: box.y, x2: box.x + box.w * f, y2: box.y + box.h });
        d.guides.push({ x1: box.x, y1: box.y + box.h * f, x2: box.x + box.w, y2: box.y + box.h * f });
      });
      cad.task = ""; afterChange(); hint(t === "thirds" ? "Thirds added. Remove them from the Woodwork menu." : "Golden ratio sections (0.382 and 0.618 of each side) added.");
      return;
    }
    if (!r) { hint("That point isn't inside a rectangle. Draw one with the rectangle button and tap inside it."); return; }
    if (t === "part") {
      var existing = d.parts.filter(function (x) { return x.rect === r.id; })[0];
      ask("Part name, such as Side or Top. Add ×2 for two.", existing ? existing.name + (existing.qty > 1 ? " ×" + existing.qty : "") : "Part " + (d.parts.length + 1), function (v) {
        var m = /^(.*?)\s*[×x]\s*(\d+)$/.exec(v), name = (m ? m[1] : v) || "Part", qty = m ? Math.max(1, +m[2]) : 1;
        snapshot();
        if (existing) { existing.name = name; existing.qty = qty; } else d.parts.push({ rect: r.id, name: name, qty: qty });
        afterChange();
        hint(name + ": " + Math.round(realMm(r.w, d)) + " × " + Math.round(realMm(r.h, d)) + " in 18 mm birch plywood. Tap another shape, or Esc.");
      });
    } else if (t === "drawers") {
      ask("How many drawers?", "3", function (v) {
        var n = Math.max(1, Math.min(8, parseInt(v, 10) || 3)), gap = 3 / d.scale * U;
        var total = r.h - gap * (n + 1), sizes = [], sum = 0, i;
        for (i = 0; i < n; i++) { sizes.push(1 + i * 0.25); sum += 1 + i * 0.25; }   // graduated, smallest at the top
        snapshot();
        var y = r.y + gap;
        for (i = 0; i < n; i++) {
          var h = total * sizes[i] / sum, fr = makeRect(d, r.x + gap, y, r.w - 2 * gap, h, "");
          d.parts.push({ rect: fr.id, name: "Drawer front " + (i + 1), qty: 1 });
          y += h + gap;
        }
        cad.task = ""; afterChange();
        hint(n + " drawer fronts with 3 mm gaps. In the app, the planner also sizes the boxes from the depth and your runners.");
      });
    }
  }
  function cutList() {
    var parts = [];
    doc.pages.forEach(function (p) {
      var d = p.drawing; if (!d) return;
      d.parts.forEach(function (pt) {
        var r = rectById(d, pt.rect); if (!r) return;
        var a = Math.round(realMm(r.w, d)), b = Math.round(realMm(r.h, d));
        parts.push({ name: pt.name, qty: pt.qty, L: Math.max(a, b), W: Math.min(a, b) });
      });
    });
    if (!parts.length) { hint("There are no parts yet. Use Make a part, or Plan drawers, first."); return; }
    // group identical parts
    var rows = [];
    parts.forEach(function (p) {
      var same = rows.filter(function (r) { return r.name === p.name && r.L === p.L && r.W === p.W; })[0];
      if (same) same.qty += p.qty; else rows.push({ name: p.name, qty: p.qty, L: p.L, W: p.W });
    });
    var sheets = pack(rows);
    var area = 0; rows.forEach(function (r) { area += r.L * r.W * r.qty; });
    var used = Math.round(area / (sheets.length * 2400 * 1200) * 100);
    var date = new Date().toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" });
    var note = "From the drawings in this notebook, " + date + ". Sizes in mm, length first.";
    var pagesOut = [], first = { cut: { first: true, note: note, material: "18 mm birch plywood", table: rows,
      summary: sheets.length + " sheet" + (sheets.length > 1 ? "s" : "") + ", " + used + "% used (the layouts follow).", sheets: [], total: sheets.length } };
    var room = 1188 - (188 + 46 + (rows.length + 1) * 32 + 74) - 40, cur = first;
    pagesOut.push(first);
    sheets.forEach(function (sh, i) {
      var need = 16 + 350 + 44;
      if (room < need) { cur = { cut: { first: false, note: note, sheets: [], total: sheets.length } }; pagesOut.push(cur); room = 1188 - 188 - 40; }
      sh.n = i + 1; cur.cut.sheets.push(sh); room -= need;
    });
    snapshot();
    pagesOut.forEach(function (o, i) { var np = newPage("Blank"); np.cut = o.cut; doc.pages.splice(doc.cur + 1 + i, 0, np); });
    go(doc.cur + 1); setTool("pen");
    hint("Cut list made as a new page after the drawing. Write on it like any page.");
  }
  // Shelf packing on 2400 × 1200 sheets, 10 mm trim, 3.2 mm kerf, length along the grain (turned only if it won't fit).
  function pack(rows) {
    var SL = 2380, SW = 1180, K = 3.2, items = [];
    rows.forEach(function (r) { for (var i = 0; i < r.qty; i++) items.push({ name: r.name, L: r.L, W: r.W }); });
    items.sort(function (a, b) { return b.W - a.W || b.L - a.L; });
    var sheets = [];
    function place(it) {
      var w = it.L, h = it.W;
      if (w > SL && h <= SL && w <= SW) { w = it.W; h = it.L; }
      for (var s = 0; s < sheets.length; s++) {
        var sh = sheets[s];
        for (var j = 0; j < sh.shelves.length; j++) {
          var f = sh.shelves[j];
          if (h <= f.h && f.x + w <= SL) { sh.parts.push({ x: 10 + f.x, y: 10 + f.y, w: w, h: h, name: it.name, L: it.L, W: it.W }); f.x += w + K; return; }
        }
        if (sh.top + h <= SW) {
          var nf = { x: w + K, y: sh.top, h: h }; sh.shelves.push(nf);
          sh.parts.push({ x: 10, y: 10 + sh.top, w: w, h: h, name: it.name, L: it.L, W: it.W }); sh.top += h + K; return;
        }
      }
      var ns = { shelves: [{ x: w + K, y: 0, h: h }], top: h + K, parts: [{ x: 10, y: 10, w: w, h: h, name: it.name, L: it.L, W: it.W }] };
      sheets.push(ns);
    }
    items.forEach(function (it) { if (Math.min(it.L, it.W) <= SW && Math.max(it.L, it.W) <= SL) place(it); });
    sheets.forEach(function (sh) {
      var a = 0; sh.parts.forEach(function (p) { a += p.w * p.h; }); sh.used = Math.round(a / (2400 * 1200) * 100);
      delete sh.shelves; delete sh.top;
    });
    return sheets;
  }

  // ---- floating drawing bar (Windows) ----
  var floatPos = null;
  $("cadDock").addEventListener("click", function () {
    var bar = $("cadbar"), f = !bar.classList.contains("floating");
    bar.classList.toggle("floating", f);
    if (f && !floatPos) floatPos = { x: 60, y: 110 };
    placeBar(); setTimeout(layout, 0);
  });
  function placeBar() {
    var bar = $("cadbar");
    if (bar.classList.contains("floating") && floatPos) { bar.style.left = floatPos.x + "px"; bar.style.top = floatPos.y + "px"; }
    else { bar.style.left = ""; bar.style.top = ""; }
  }
  $("cadGrip").addEventListener("pointerdown", function (e) {
    if (!$("cadbar").classList.contains("floating")) return;
    e.preventDefault(); this.setPointerCapture(e.pointerId);
    var ar = app.getBoundingClientRect(), start = { x: e.clientX, y: e.clientY, fx: floatPos.x, fy: floatPos.y };
    var mv = function (ev) {
      floatPos.x = Math.max(0, Math.min(ar.width - 120, start.fx + ev.clientX - start.x));
      floatPos.y = Math.max(0, Math.min(ar.height - 60, start.fy + ev.clientY - start.y)); placeBar();
    };
    var stop = function () { $("cadGrip").removeEventListener("pointermove", mv); $("cadGrip").removeEventListener("pointerup", stop); };
    this.addEventListener("pointermove", mv); this.addEventListener("pointerup", stop);
  });

  // ---------------------------------------------------------------------------------------------------------------
  // Keys, devices, start
  // ---------------------------------------------------------------------------------------------------------------
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input, textarea, select")) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); e.shiftKey ? redo() : undo(); }
    else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") { e.preventDefault(); redo(); }
    else if (e.key === "Escape") { cad.chain = null; cad.measureA = null; cad.task = ""; closeMenu(); if (state.tool === "draw" && page().drawing) hint(cadHint()); render(); }
    else if (e.key === "PageDown") go(doc.cur + 1);
    else if (e.key === "PageUp") go(doc.cur - 1);
    else if ((e.key === "Delete" || e.key === "Backspace") && cad.sel) $("cadDel").click();
  });

  function setDevice(dv) {
    app.dataset.device = dv;
    document.querySelectorAll(".device-switch [data-device]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.device === dv)); });
    if (dv !== "windows") { $("cadbar").classList.remove("floating"); placeBar(); }
    state.fit = "page";
    setTimeout(layout, 0);
  }
  document.querySelectorAll(".device-switch [data-device]").forEach(function (b) {
    b.addEventListener("click", function () { setDevice(b.dataset.device); });
  });
  if (window.ResizeObserver) new ResizeObserver(function () { layout(); }).observe(desk);
  else window.addEventListener("resize", layout);

  pressed("[data-colour]", "data-colour", state.colour);
  pressed("[data-width]", "data-width", state.width);
  if (window.matchMedia && window.matchMedia("(max-width: 700px)").matches) setDevice("phone");
  else if (window.matchMedia && window.matchMedia("(max-width: 1100px)").matches) setDevice("tablet");
  setTool("pen");
  refreshAll();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(render);
})();
