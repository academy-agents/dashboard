# ---------------------------------------------------------------------------
# HTML / CSS / JS  (served as a single self-contained page)
# This file is Claude generated. Expect shenanigans.
# ---------------------------------------------------------------------------
# ruff: noqa: E501

from __future__ import annotations

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AGENT MONITOR</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <style>
    :root {
      font-size: 18px;
      --cyan:    #00e5ff;
      --blue:    #0066ff;
      --green:   #00ff88;
      --red:     #ff1744;
      --yellow:  #ffdd00;
      --orange:  #ff6d00;
      --bg:      #000810;
      --card-bg: rgba(0,14,38,0.88);
      --border:  rgba(0,229,255,0.32);
      --dim:     rgba(0,229,255,0.52);
    }
    [data-theme="light"] {
      --cyan:    #0055cc;
      --blue:    #0044aa;
      --green:   #007740;
      --red:     #cc0022;
      --yellow:  #b87800;
      --orange:  #b85000;
      --bg:      #eef2f7;
      --card-bg: rgba(255,255,255,0.92);
      --border:  rgba(0,80,200,0.28);
      --dim:     rgba(0,50,140,0.58);
    }
    [data-theme="light"] body { background:var(--bg); color:var(--cyan); }
    [data-theme="light"] body::before {
      background-image:
        linear-gradient(rgba(0,80,200,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,80,200,.055) 1px, transparent 1px);
    }
    [data-theme="light"] body::after {
      background: repeating-linear-gradient(
        0deg, transparent, transparent 3px,
        rgba(0,0,0,.025) 3px, rgba(0,0,0,.025) 4px
      );
    }
    [data-theme="light"] #vig {
      background: radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(200,218,240,.6) 100%);
    }
    [data-theme="light"] header  { background:rgba(224,234,248,.96); border-bottom-color:var(--border); }
    [data-theme="light"] footer  { background:rgba(218,230,246,.97); border-top-color:var(--border); color:rgba(0,50,140,.42); }
    [data-theme="light"] footer span { color:var(--cyan); }
    [data-theme="light"] #log-stream {
      background:rgba(240,246,255,.9);
      border-color:var(--border);
      scrollbar-color:rgba(0,80,200,.28) transparent;
    }
    [data-theme="light"] #log-stream::-webkit-scrollbar-thumb { background:rgba(0,80,200,.28); }
    [data-theme="light"] .log-ts  { color:rgba(0,50,140,.38); }
    [data-theme="light"] .log-src { color:rgba(0,50,140,.6); }
    [data-theme="light"] .log-msg { color:rgba(20,40,90,.82); }
    [data-theme="light"] .lvl-TRACE     { color:rgba(0,50,140,.22); }
    [data-theme="light"] .lvl-DEBUG     { color:rgba(0,80,200,.38); }
    [data-theme="light"] .lvl-INFO      { color:var(--cyan); }
    [data-theme="light"] .lvl-WARNING   { color:var(--yellow); }
    [data-theme="light"] .lvl-ERROR     { color:var(--orange); }
    [data-theme="light"] .lvl-EXCEPTION { color:var(--orange); }
    [data-theme="light"] .lvl-CRITICAL  { color:var(--red); font-weight:bold; }
    [data-theme="light"] .agent-card { background:var(--card-bg); border-color:var(--border); }
    [data-theme="light"] .agent-card::before,
    [data-theme="light"] .agent-card::after { border-color:var(--cyan); }
    [data-theme="light"] .agent-card.live {
      border-color:rgba(0,80,200,.42);
      box-shadow:0 0 22px rgba(0,80,200,.06), inset 0 0 22px rgba(0,80,200,.025);
    }
    [data-theme="light"] .card-hdr { border-bottom-color:rgba(0,80,200,.12); }
    [data-theme="light"] .agent-sub { color:rgba(0,50,140,.35); }
    [data-theme="light"] .track  { background:rgba(0,80,200,.1); }
    [data-theme="light"] .no-stats { color:rgba(0,80,200,.3); }
    [data-theme="light"] .gpu-hdr  { color:rgba(0,80,200,.38); }
    [data-theme="light"] .sh-title { color:var(--dim); }
    [data-theme="light"] .sh-line  { background:linear-gradient(to right,var(--border),transparent); }
    [data-theme="light"] .tab-btn  { border-color:rgba(0,80,200,.22); color:var(--dim); }
    [data-theme="light"] .tab-btn:hover  { border-color:var(--cyan); color:var(--cyan); background:rgba(0,80,200,.05); }
    [data-theme="light"] .tab-btn.active { border-color:var(--cyan); color:var(--cyan); background:rgba(0,80,200,.1);
      box-shadow:0 0 16px rgba(0,80,200,.12),inset 0 0 16px rgba(0,80,200,.04); }
    [data-theme="light"] .hud { color:var(--dim); }
    [data-theme="light"] .hud-val { color:var(--cyan); }
    [data-theme="light"] .btn  { border-color:rgba(0,80,200,.28); color:var(--dim); }
    [data-theme="light"] .btn:hover     { border-color:var(--cyan); color:var(--cyan); background:rgba(0,80,200,.05); }
    [data-theme="light"] .btn.is-active { border-color:var(--cyan); color:var(--cyan); background:rgba(0,80,200,.09); }
    [data-theme="light"] .log-info { color:var(--dim); }
    [data-theme="light"] .empty-agents { color:rgba(0,80,200,.22); }
    [data-theme="light"] #modal-wrap { background:rgba(190,215,240,.78); }
    [data-theme="light"] .modal { background:rgba(242,248,255,.98); border-color:var(--cyan);
      box-shadow:0 0 0 1px rgba(0,80,200,.1),0 0 45px rgba(0,80,200,.14),0 0 90px rgba(0,64,200,.08); }
    [data-theme="light"] .modal::before { border-color:var(--cyan); }
    [data-theme="light"] .modal::after  { border-color:var(--cyan); }
    [data-theme="light"] .modal-from { color:var(--dim); }
    [data-theme="light"] .modal-from strong { color:var(--cyan); }
    [data-theme="light"] .modal-body { border-color:var(--border); background:rgba(0,80,200,.03); color:rgba(20,40,90,.88); }
    [data-theme="light"] .modal-tag { color:var(--yellow); text-shadow:0 0 10px rgba(180,120,0,.4); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      font-family: 'Share Tech Mono','Courier New',monospace;
      background: var(--bg);
      color: var(--cyan);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* ── Animated grid bg ── */
    body::before {
      content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
      background-image:
        linear-gradient(rgba(0,100,255,.065) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,100,255,.065) 1px, transparent 1px);
      background-size: 48px 48px;
      animation: gridDrift 28s linear infinite;
    }
    @keyframes gridDrift { to { background-position: 48px 48px; } }

    /* ── CRT scanlines ── */
    body::after {
      content:''; position:fixed; inset:0; z-index:1; pointer-events:none;
      background: repeating-linear-gradient(
        0deg, transparent, transparent 3px,
        rgba(0,0,0,.09) 3px, rgba(0,0,0,.09) 4px
      );
    }

    /* ── Radial vignette ── */
    #vig {
      position:fixed; inset:0; z-index:2; pointer-events:none;
      background: radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,14,.72) 100%);
    }

    #app { position:relative; z-index:10; min-height:100vh; display:flex; flex-direction:column; }

    /* ════════════════════════════════════════════════
       HEADER
    ════════════════════════════════════════════════ */
    header {
      display:flex; align-items:center; justify-content:space-between;
      gap:18px; padding:11px 26px;
      background: rgba(0,4,18,.93);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(10px);
      position:sticky; top:0; z-index:50;
    }
    .logo {
      display:flex; align-items:center; gap:10px;
      font-size:1.05rem; letter-spacing:.38em;
      text-shadow: 0 0 18px var(--cyan), 0 0 36px rgba(0,102,255,.6);
      white-space:nowrap; flex-shrink:0; user-select:none;
    }
    .logo img { flex-shrink:0; width:36px; height:36px; object-fit:contain; }
    @keyframes hexSpin { to { transform:rotate(360deg); } }

    /* Tabs */
    nav { display:flex; gap:3px; }
    .tab-btn {
      padding:6px 20px;
      background:transparent;
      border:1px solid rgba(0,229,255,.22);
      color:var(--dim);
      font-family:inherit; font-size:.72rem; letter-spacing:.28em;
      cursor:pointer; text-transform:uppercase;
      transition:all .18s;
      clip-path:polygon(10px 0%,100% 0%,calc(100% - 10px) 100%,0% 100%);
    }
    .tab-btn:hover { border-color:var(--cyan); color:var(--cyan); background:rgba(0,229,255,.05); }
    .tab-btn.active {
      border-color:var(--cyan); color:var(--cyan);
      background:rgba(0,229,255,.1);
      box-shadow: 0 0 16px rgba(0,229,255,.14), inset 0 0 16px rgba(0,229,255,.04);
    }

    /* HUD */
    .hud { display:flex; gap:18px; font-size:.66rem; letter-spacing:.15em; color:var(--dim); flex-shrink:0; }
    .hud-item { display:flex; gap:5px; align-items:center; }
    .hud-val { color:var(--cyan); }
    #conn-dot {
      width:7px; height:7px; border-radius:50%;
      background:var(--yellow); box-shadow:0 0 6px var(--yellow);
      transition:all .4s;
    }
    #conn-dot.live { background:var(--green); box-shadow:0 0 10px var(--green); animation:pulse 2s ease-in-out infinite; }
    #conn-dot.dead { background:var(--red);   box-shadow:0 0 8px var(--red);   animation:none; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

    /* ════════════════════════════════════════════════
       MAIN
    ════════════════════════════════════════════════ */
    main { padding:26px 30px 88px; flex:1; }
    .panel { display:none; }
    .panel.active { display:block; }

    .sh { display:flex; align-items:center; gap:14px; margin-bottom:22px; }
    .sh-title { font-size:.68rem; letter-spacing:.45em; text-transform:uppercase; color:var(--dim); white-space:nowrap; }
    .sh-line   { flex:1; height:1px; background:linear-gradient(to right,var(--border),transparent); }

    /* ── Agent grid ── */
    .agents-grid {
      display:grid;
      grid-template-columns:repeat(auto-fill,minmax(295px,1fr));
      gap:22px;
    }
    .empty-agents { grid-column:1/-1; text-align:center; padding:90px 20px; color:rgba(0,229,255,.18); }
    .empty-agents h2 { font-size:.95rem; letter-spacing:.45em; margin-bottom:10px; }
    .empty-agents  p { font-size:.7rem;  letter-spacing:.25em; }

    /* Agent card */
    .agent-card {
      background:var(--card-bg);
      border:1px solid var(--border);
      padding:18px; position:relative;
      backdrop-filter:blur(4px);
      animation:cardIn .35s ease-out;
      transition:border-color .4s, box-shadow .4s;
      cursor:pointer;
    }
    .agent-card.live {
      border-color:rgba(0,229,255,.44);
      box-shadow:0 0 26px rgba(0,229,255,.06), inset 0 0 26px rgba(0,229,255,.025);
    }
    @keyframes cardIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

    /* Corner brackets */
    .agent-card::before,.agent-card::after { content:''; position:absolute; width:14px; height:14px; }
    .agent-card::before { top:-1px;    left:-1px;   border-top:2px solid var(--cyan);    border-left:2px solid var(--cyan); }
    .agent-card::after  { bottom:-1px; right:-1px;  border-bottom:2px solid var(--cyan); border-right:2px solid var(--cyan); }

    .card-hdr {
      display:flex; justify-content:space-between; align-items:flex-start;
      margin-bottom:15px; padding-bottom:11px;
      border-bottom:1px solid rgba(0,229,255,.1);
    }
    .agent-name { font-size:.92rem; letter-spacing:.14em; text-transform:uppercase; }
    .agent-sub  { font-size:.58rem; color:rgba(0,229,255,.28); letter-spacing:.15em; margin-top:3px; }
    .badge      { display:flex; align-items:center; gap:5px; font-size:.62rem; letter-spacing:.15em; }
    .sdot            { width:7px; height:7px; border-radius:50%; }
    .sdot.active     { background:var(--green);  box-shadow:0 0 8px var(--green);  animation:pulse 2s ease-in-out infinite; }
    .sdot.waiting    { background:var(--yellow); box-shadow:0 0 8px var(--yellow); animation:pulse 2s ease-in-out infinite; }
    .sdot.terminated { background:var(--red);    box-shadow:0 0 6px var(--red);    animation:none; }
    .sdot.missing    { background:var(--yellow); box-shadow:0 0 5px var(--yellow); animation:none; opacity:.45; }
    .power-btn {
      background:transparent;
      border:1px solid rgba(255,23,68,.35);
      color:rgba(255,23,68,.55);
      font-size:.9rem; line-height:1;
      width:27px; height:27px;
      cursor:pointer;
      display:flex; align-items:center; justify-content:center;
      transition:all .18s;
      margin-left:8px;
      flex-shrink:0;
    }
    .power-btn:hover {
      border-color:var(--red); color:var(--red);
      background:rgba(255,23,68,.08);
      box-shadow:0 0 12px rgba(255,23,68,.22);
    }

    /* Stat bars */
    .stat { margin-bottom:12px; }
    .stat-meta {
      display:flex; justify-content:space-between;
      font-size:.66rem; color:var(--dim); margin-bottom:5px; letter-spacing:.1em;
    }
    .stat-val { color:var(--cyan); }
    .track { height:3px; background:rgba(0,229,255,.08); border-radius:2px; overflow:hidden; }
    .fill { height:100%; border-radius:2px; transition:width .6s ease,background .5s ease,box-shadow .5s ease; }
    .fill.lo { background:var(--green);  box-shadow:0 0 6px var(--green); }
    .fill.md { background:var(--yellow); box-shadow:0 0 6px var(--yellow); }
    .fill.hi { background:var(--red);    box-shadow:0 0 8px var(--red); }

    .gpu-hdr    { font-size:.62rem; color:rgba(0,229,255,.3); letter-spacing:.25em; margin:14px 0 8px; }
    .no-stats   { text-align:center; color:rgba(0,229,255,.22); font-size:.68rem; letter-spacing:.2em; padding:18px 0; }

    /* ── Log stream ── */
    .log-toolbar { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
    .log-info    { font-size:.66rem; letter-spacing:.15em; color:var(--dim); }
    .log-actions { display:flex; gap:7px; }

    .btn {
      background:transparent;
      border:1px solid rgba(0,229,255,.28);
      color:var(--dim);
      font-family:inherit; font-size:.63rem; letter-spacing:.15em;
      padding:4px 13px; cursor:pointer; text-transform:uppercase;
      transition:all .18s;
    }
    .btn:hover          { border-color:var(--cyan); color:var(--cyan); background:rgba(0,229,255,.05); }
    .btn.is-active      { border-color:var(--cyan); color:var(--cyan); background:rgba(0,229,255,.09); }

    #log-stream {
      height:calc(100vh - 215px);
      overflow-y:scroll;
      background:rgba(0,2,12,.82);
      border:1px solid rgba(0,229,255,.16);
      padding:11px 13px;
      font-size:.71rem; line-height:1.9;
      scrollbar-width:thin;
      scrollbar-color:rgba(0,229,255,.28) transparent;
    }
    #log-stream::-webkit-scrollbar       { width:3px; }
    #log-stream::-webkit-scrollbar-thumb { background:rgba(0,229,255,.28); border-radius:2px; }

    .log-row {
      display:flex; gap:10px; overflow:hidden;
      animation:logIn .14s ease-out;
    }
    @keyframes logIn { from{opacity:0;transform:translateX(-5px)} to{opacity:1;transform:translateX(0)} }
    .log-ts  { color:rgba(0,229,255,.33); min-width:66px; flex-shrink:0; }
    .log-lvl { min-width:54px; flex-shrink:0; font-weight:bold; }
    .log-src { color:rgba(0,229,255,.58); min-width:130px; flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .log-msg { color:rgba(185,220,255,.82); flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

    .lvl-TRACE     { color:rgba(0,229,255,.2); }
    .lvl-DEBUG     { color:rgba(0,229,255,.42); }
    .lvl-INFO      { color:var(--cyan); }
    .lvl-WARNING   { color:var(--yellow); text-shadow:0 0 6px rgba(255,221,0,.35); }
    .lvl-ERROR     { color:var(--orange); text-shadow:0 0 6px rgba(255,109,0,.4); }
    .lvl-EXCEPTION { color:var(--orange); text-shadow:0 0 6px rgba(255,109,0,.4); }
    .lvl-CRITICAL  { color:var(--red); text-shadow:0 0 10px var(--red), 0 0 20px rgba(255,23,68,.4); font-weight:bold; }

    /* ── Prompt modal ── */
    #modal-wrap {
      position:fixed; inset:0; z-index:200;
      display:flex; align-items:center; justify-content:center;
      background:rgba(0,4,18,.83);
      backdrop-filter:blur(7px);
      animation:fadeIn .2s ease;
    }
    #modal-wrap.hidden { display:none; }
    @keyframes fadeIn { from{opacity:0} to{opacity:1} }

    .modal {
      background:rgba(0,10,32,.97);
      border:1px solid var(--cyan);
      padding:28px 30px;
      width:510px; max-width:92vw;
      position:relative;
      box-shadow:
        0 0 0 1px rgba(0,229,255,.12),
        0 0 55px rgba(0,229,255,.17),
        0 0 110px rgba(0,64,255,.11);
      animation:modalIn .24s ease;
    }
    @keyframes modalIn { from{opacity:0;transform:scale(.96)} to{opacity:1;transform:scale(1)} }
    .modal::before { content:''; position:absolute; top:-1px;    left:-1px;   width:18px; height:18px; border-top:2px solid var(--cyan);    border-left:2px solid var(--cyan); }
    .modal::after  { content:''; position:absolute; bottom:-1px; right:-1px;  width:18px; height:18px; border-bottom:2px solid var(--cyan); border-right:2px solid var(--cyan); }

    .modal-tag  { font-size:.63rem; letter-spacing:.4em; color:var(--yellow); text-shadow:0 0 12px var(--yellow); margin-bottom:6px; }
    .modal-from { font-size:.7rem; color:var(--dim); letter-spacing:.2em; margin-bottom:18px; }
    .modal-from strong { color:var(--cyan); }
    .modal-body {
      font-size:.86rem; line-height:1.65;
      color:rgba(200,228,255,.9);
      padding:14px 16px;
      border:1px solid rgba(0,229,255,.1);
      background:rgba(0,229,255,.025);
      margin-bottom:22px;
      white-space:pre-wrap; word-break:break-word;
    }
    .modal-actions { display:flex; justify-content:flex-end; gap:9px; }
    .btn-primary {
      border-color:var(--cyan); color:var(--cyan);
      background:rgba(0,229,255,.08);
      box-shadow:0 0 13px rgba(0,229,255,.11);
    }
    .btn-primary:hover { background:rgba(0,229,255,.14); box-shadow:0 0 22px rgba(0,229,255,.24); }
    .modal-responses {
      display:flex; flex-wrap:wrap; gap:9px;
      margin-bottom:22px;
    }
    .btn-response {
      border-color:rgba(0,229,255,.42); color:var(--cyan);
      background:rgba(0,229,255,.05);
      box-shadow:0 0 8px rgba(0,229,255,.08);
      flex:1; min-width:120px;
      padding:8px 16px;
      text-align:center; white-space:normal; word-break:break-word;
    }
    .btn-response:hover {
      border-color:var(--cyan); background:rgba(0,229,255,.13);
      box-shadow:0 0 18px rgba(0,229,255,.22);
    }
    [data-theme="light"] .btn-response {
      border-color:rgba(0,80,200,.38); color:var(--cyan);
      background:rgba(0,80,200,.05);
    }
    [data-theme="light"] .btn-response:hover {
      border-color:var(--cyan); background:rgba(0,80,200,.11);
    }

    /* ── Map panel ── */
    #map {
      height: calc(100vh - 258px);
      border: 1px solid var(--border);
      background: #060d18;
    }
    /* Leaflet popup theme */
    .leaflet-popup-content-wrapper {
      background: rgba(0,10,32,.97);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      border-radius: 0;
      font-family: 'Share Tech Mono','Courier New',monospace;
      font-size: .74rem;
      box-shadow: 0 0 22px rgba(0,229,255,.18);
    }
    .leaflet-popup-tip { background: rgba(0,10,32,.97); }
    .leaflet-popup-close-button { color: var(--cyan) !important; }
    .map-popup-name  { font-size:.85rem; letter-spacing:.14em; text-transform:uppercase; color:var(--cyan); margin-bottom:6px; }
    .map-popup-row   { display:flex; gap:8px; margin:3px 0; color:rgba(0,229,255,.7); letter-spacing:.1em; }
    .map-popup-label { color:rgba(0,229,255,.38); min-width:60px; }
    .map-legend {
      position:absolute; bottom:36px; right:12px; z-index:1000;
      background:rgba(0,10,32,.88);
      border:1px solid var(--border);
      padding:10px 14px;
      font-family:'Share Tech Mono','Courier New',monospace;
      font-size:.62rem; letter-spacing:.18em;
      color:var(--dim);
    }
    .legend-item { display:flex; align-items:center; gap:8px; margin:4px 0; }
    .legend-dot  { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
    [data-theme="light"] #map { background:#dce8f5; }
    [data-theme="light"] .leaflet-popup-content-wrapper {
      background: rgba(242,248,255,.98); color: var(--cyan);
      border-color: var(--cyan);
    }
    [data-theme="light"] .leaflet-popup-tip { background: rgba(242,248,255,.98); }
    [data-theme="light"] .map-legend { background:rgba(240,246,255,.92); border-color:var(--border); }

    /* ── Agent connection lines ── */
    .map-conn-line {
      stroke-dasharray: 10 7;
      animation: mapConnFlow 1.4s linear infinite;
    }
    .map-conn-line.active {
      stroke-dasharray: 10 7;
      animation: mapConnFlow .7s linear infinite;
      filter: drop-shadow(0 0 3px #00e5ff);
    }
    @keyframes mapConnFlow { to { stroke-dashoffset: -34; } }
    [data-theme="light"] .map-conn-line { stroke: rgba(0,80,200,.45) !important; }
    [data-theme="light"] .map-conn-line.active { stroke: rgba(0,80,200,.8) !important; filter: drop-shadow(0 0 3px rgba(0,80,200,.5)); }

    /* ── Ticker footer ── */
    footer {
      position:fixed; bottom:0; left:0; right:0; z-index:30;
      background:rgba(0,4,18,.94);
      border-top:1px solid rgba(0,229,255,.16);
      padding:5px 26px;
      display:flex; gap:24px; align-items:center;
      font-size:.6rem; letter-spacing:.17em;
      color:rgba(0,229,255,.32);
      backdrop-filter:blur(5px);
    }
    footer span { color:var(--cyan); }
    .fsep { color:rgba(0,229,255,.14); }
  </style>
</head>
<body>
<div id="vig"></div>
<div id="app">

  <!-- ══ HEADER ═══════════════════════════════════════════════════════════ -->
  <header>
    <div class="logo">
      <img src="__BASE_URL__/assets/modcon_logo.png" alt="logo">
      AGENT MONITOR
    </div>

    <nav>
      <button class="tab-btn active" data-tab="dashboard" onclick="switchTab(this)">DASHBOARD</button>
      <button class="tab-btn"        data-tab="logs"      onclick="switchTab(this)">LOGS</button>
      <button class="tab-btn"        data-tab="map"       onclick="switchTab(this)">MAP</button>
    </nav>

    <div class="hud">
      <div class="hud-item">
        <div id="conn-dot"></div>
        <span id="conn-lbl" style="color:var(--dim)">CONNECTING</span>
      </div>
      <div class="hud-item">AGENTS <span class="hud-val" id="h-agents">0</span></div>
      <div class="hud-item">EVENTS <span class="hud-val" id="h-events">0</span></div>
      <div class="hud-item" id="h-time"></div>
    </div>
    <button class="btn" id="theme-btn" onclick="toggleTheme()" title="Toggle light / dark mode" style="padding:4px 10px;font-size:.78rem;flex-shrink:0;">◐</button>
  </header>

  <!-- ══ MAIN ══════════════════════════════════════════════════════════════ -->
  <main>

    <!-- DASHBOARD panel -->
    <div id="panel-dashboard" class="panel active">
      <div class="sh">
        <div class="sh-title">CONNECTED AGENTS</div>
        <div class="sh-line"></div>
      </div>
      <div id="agents-grid" class="agents-grid">
        <div class="empty-agents" id="empty-agents">
          <h2>NO AGENTS ONLINE</h2>
          <p>AWAITING CONNECTIONS...</p>
        </div>
      </div>
    </div>

    <!-- LOGS panel -->
    <div id="panel-logs" class="panel">
      <div class="log-toolbar">
        <div class="log-info">BUFFER&nbsp;<span id="log-buf-n" style="color:var(--cyan)">0</span>&nbsp;ENTRIES</div>
        <div class="log-actions">
          <button class="btn is-active" id="scroll-btn" onclick="toggleScroll()">AUTO-SCROLL ON</button>
          <button class="btn" onclick="clearLogs()">CLEAR</button>
        </div>
      </div>
      <div id="log-stream"></div>
    </div>

    <!-- MAP panel -->
    <div id="panel-map" class="panel">
      <div class="log-toolbar" style="margin-bottom:10px;">
        <div class="log-info">AGENT LOCATIONS</div>
        <div class="log-actions">
          <button class="btn"           id="map-view-world" onclick="setMapView('world')">WORLD</button>
          <button class="btn is-active" id="map-view-us"    onclick="setMapView('us')">US</button>
        </div>
      </div>
      <div id="map"></div>
    </div>

  </main>
</div>

<!-- ══ PROMPT MODAL ══════════════════════════════════════════════════════ -->
<div id="modal-wrap" class="hidden">
  <div class="modal">
    <div class="modal-tag">⚡&nbsp;&nbsp;USER INPUT REQUIRED</div>
    <div class="modal-from">FROM:&nbsp;<strong id="modal-agent"></strong></div>
    <div id="modal-body" class="modal-body"></div>
    <div id="modal-responses" class="modal-responses"></div>
    <div id="modal-actions" class="modal-actions">
      <button class="btn btn-primary" onclick="dismissPrompt()">ACKNOWLEDGE</button>
    </div>
  </div>
</div>

<!-- ══ FOOTER TICKER ═════════════════════════════════════════════════════ -->
<footer>
  <span>AGENT MONITOR</span>
  <span class="fsep">|</span>
  <span>PROTOCOL <span>ACADEMY-SSE</span></span>
  <span class="fsep">|</span>
  <span>UPTIME <span id="f-uptime">00:00:00</span></span>
  <span class="fsep">|</span>
  <span id="f-time"></span>
</footer>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
'use strict';

// ── State ────────────────────────────────────────────────────────────────
const agents = {};
let autoScroll = true;
let logBufN   = 0;
let eventN    = 0;
let pendingPrompts  = [];
let currentPromptId = null;
const t0 = Date.now();

// ── SSE ──────────────────────────────────────────────────────────────────
const es = new EventSource('__BASE_URL__/events');

es.addEventListener('init', e => {
  const s = JSON.parse(e.data);
  s.logs.forEach(appendLog);
  Object.entries(s.agents).forEach(([n, d]) => {
    Object.assign(agents[n] || (agents[n] = {}), d, { agent: n });
    upsertCard(n, agents[n]);
    if (d.geo?.lat) _upsertMapMarker({ ...agents[n], agent: n });
  });
  s.prompts.forEach(p => pendingPrompts.push(p));
  if (pendingPrompts.length && !currentPromptId) showNextPrompt();
  updateHud();
});

es.addEventListener('log', e => {
  appendLog(JSON.parse(e.data)); eventN++; updateHud();
});

es.addEventListener('stats', e => {
  const d = JSON.parse(e.data);
  Object.assign(agents[d.agent] || (agents[d.agent] = {}), d);
  upsertCard(d.agent, agents[d.agent]);
  eventN++; updateHud();
});

es.addEventListener('agent_connected', e => {
  const d = JSON.parse(e.data);
  if (!agents[d.agent]) {
    agents[d.agent] = { last_seen: Date.now() / 1000 };
    upsertCard(d.agent, agents[d.agent]);
  }
  eventN++; updateHud();
});

es.addEventListener('prompt', e => {
  const d = JSON.parse(e.data);
  pendingPrompts.push(d);
  if (!currentPromptId) showNextPrompt();
  eventN++;
});

es.onopen = () => {
  const dot = document.getElementById('conn-dot');
  const lbl = document.getElementById('conn-lbl');
  dot.className = 'live';
  lbl.textContent = 'LIVE';
  lbl.style.color = 'var(--green)';
};
es.onerror = () => {
  const dot = document.getElementById('conn-dot');
  const lbl = document.getElementById('conn-lbl');
  dot.className = 'dead';
  lbl.textContent = 'RECONNECTING';
  lbl.style.color = 'var(--red)';
};

// ── Tab switching ─────────────────────────────────────────────────────────
function switchTab(btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('panel-' + btn.dataset.tab).classList.add('active');
}

// ── Agent cards ───────────────────────────────────────────────────────────
const _STATUS_MAP = {
  'ACTIVE':     { cls: 'active',     color: 'var(--green)',  label: 'ACTIVE'     },
  'WAITING':    { cls: 'waiting',    color: 'var(--yellow)', label: 'WAITING'    },
  'MISSING':    { cls: 'missing',    color: 'var(--yellow)', label: 'MISSING'    },
  'TERMINATED': { cls: 'terminated', color: 'var(--red)',    label: 'TERMINATED' },
};

function buildStatusBadge(status) {
  const s = _STATUS_MAP[status] || _STATUS_MAP['ACTIVE'];
  return `<div class="badge"><div class="sdot ${s.cls}"></div><span style="color:${s.color};font-size:.62rem;letter-spacing:.15em">${s.label}</span></div>`;
}

function upsertCard(name, data) {
  document.getElementById('empty-agents')?.remove();

  const safeId = 'card-' + name.replace(/[^a-zA-Z0-9_-]/g, '_');
  let card = document.getElementById(safeId);
  if (!card) {
    card = document.createElement('div');
    card.id = safeId;
    card.className = 'agent-card live';
    document.getElementById('agents-grid').appendChild(card);
  }

  Object.assign(agents[name] || (agents[name] = {}), data);
  const d = agents[name];
  const hasStats = d.cpu_percent !== undefined;

  card.innerHTML = `
    <div class="card-hdr">
      <div>
        <div class="agent-name">${x(d.agent_name || name)}</div>
        <div class="agent-sub">${x(String(name).slice(0, 22))}</div>
      </div>
      <div style="display:flex;align-items:center">
        ${buildStatusBadge(d.status)}
        <button class="power-btn" onclick="event.stopPropagation();shutdownAgent('${x(name)}')" title="Shutdown agent">⏻</button>
      </div>
    </div>
    ${hasStats ? buildStats(d) : '<div class="no-stats">AWAITING STATS...</div>'}
  `;
  card.onclick = () => { window.location = '__BASE_URL__/agent/' + encodeURIComponent(name); };
}

function buildStats(d) {
  const cpu    = d.cpu_percent    ?? 0;
  const memRss = d.memory_rss_mb  ?? 0;
  const memPct = Math.min(memRss / (32 * 1024) * 100, 100);  // 32 GB ref
  const gpus   = d.gpu ?? [];

  let h = statBar('CPU',     cpu.toFixed(1),    '%',  cpu);
  h    += statBar('MEM RSS', memRss.toFixed(0),  'MB', memPct);

  if (gpus.length) {
    h += '<div class="gpu-hdr">GPU DEVICES</div>';
    gpus.forEach((g, i) => {
      h += statBar(`GPU ${i} UTIL`, g.utilization_percent.toFixed(1), '%', g.utilization_percent);
      const gmp = g.memory_total_mb > 0 ? g.memory_used_mb / g.memory_total_mb * 100 : 0;
      h += statBar(`GPU ${i} MEM`,  g.memory_used_mb.toFixed(0),      'MB', gmp);
    });
  } else {
    h += '<div class="gpu-hdr" style="color:rgba(0,229,255,.18)">NO GPU DETECTED</div>';
  }
  return h;
}

function statBar(label, val, unit, pct) {
  pct = Math.min(Math.max(pct, 0), 100);
  const cls = pct < 60 ? 'lo' : pct < 85 ? 'md' : 'hi';
  return `
    <div class="stat">
      <div class="stat-meta"><span>${label}</span><span class="stat-val">${val}${unit}</span></div>
      <div class="track"><div class="fill ${cls}" style="width:${pct.toFixed(1)}%"></div></div>
    </div>`;
}

// ── Log stream ────────────────────────────────────────────────────────────
function appendLog(entry) {
  const stream = document.getElementById('log-stream');
  const row    = document.createElement('div');
  row.className = 'log-row';
  const lvl = (entry.level || 'INFO').split(':').pop().trim().toUpperCase();
  row.innerHTML = `
    <span class="log-ts">${x(entry.ts || '--:--:--')}</span>
    <span class="log-lvl lvl-${lvl}">${lvl.padEnd(9)}</span>
    <span class="log-src">${x((entry.agent_name || 'unknown').substring(0, 20))}${entry.agent_id ? '[' + x(String(entry.agent_id).substring(0, 4)) + ']' : ''}</span>
    <span class="log-msg">${x(entry.message || '')}</span>
  `;
  stream.appendChild(row);
  logBufN++;
  document.getElementById('log-buf-n').textContent = logBufN;
  while (stream.children.length > 600) stream.removeChild(stream.firstChild);
  if (autoScroll) stream.scrollTop = stream.scrollHeight;
}

function toggleScroll() {
  autoScroll = !autoScroll;
  const btn = document.getElementById('scroll-btn');
  btn.textContent = 'AUTO-SCROLL ' + (autoScroll ? 'ON' : 'OFF');
  btn.classList.toggle('is-active', autoScroll);
  if (autoScroll) document.getElementById('log-stream').scrollTop = 1e9;
}

function clearLogs() {
  document.getElementById('log-stream').innerHTML = '';
  logBufN = 0;
  document.getElementById('log-buf-n').textContent = '0';
}

// ── Prompt modal ──────────────────────────────────────────────────────────
function showNextPrompt() {
  if (!pendingPrompts.length) {
    document.getElementById('modal-wrap').classList.add('hidden');
    currentPromptId = null;
    return;
  }
  const p = pendingPrompts[0];
  currentPromptId = p.id;
  document.getElementById('modal-agent').textContent = p.agent;
  document.getElementById('modal-body').textContent  = p.prompt;

  const responsesEl = document.getElementById('modal-responses');
  const actionsEl   = document.getElementById('modal-actions');
  responsesEl.innerHTML = '';
  actionsEl.innerHTML   = '';

  if (p.responses && p.responses.length > 0) {
    p.responses.forEach(r => {
      const btn = document.createElement('button');
      btn.className   = 'btn btn-response';
      btn.textContent = r;
      btn.addEventListener('click', () => selectResponse(r));
      responsesEl.appendChild(btn);
    });
  } else {
    const ack = document.createElement('button');
    ack.className   = 'btn btn-primary';
    ack.textContent = 'ACKNOWLEDGE';
    ack.addEventListener('click', dismissPrompt);
    actionsEl.appendChild(ack);
  }

  document.getElementById('modal-wrap').classList.remove('hidden');
}

function selectResponse(response) {
  if (!currentPromptId) return;
  fetch('__BASE_URL__/respond/' + encodeURIComponent(currentPromptId), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ response }),
  });
  pendingPrompts = pendingPrompts.filter(p => p.id !== currentPromptId);
  showNextPrompt();
}

function dismissPrompt() {
  if (!currentPromptId) return;
  fetch('__BASE_URL__/dismiss/' + encodeURIComponent(currentPromptId), { method: 'POST' });
  pendingPrompts = pendingPrompts.filter(p => p.id !== currentPromptId);
  showNextPrompt();
}

// ── Shutdown agent ────────────────────────────────────────────────────────
function shutdownAgent(name) {
  fetch('__BASE_URL__/shutdown/' + encodeURIComponent(name), { method: 'POST' });
  const safeId = 'card-' + name.replace(/[^a-zA-Z0-9_-]/g, '_');
  const card = document.getElementById(safeId);
  if (card) { card.style.opacity = '0.4'; card.style.pointerEvents = 'none'; }
}

// ── HUD + clock ───────────────────────────────────────────────────────────
function updateHud() {
  document.getElementById('h-agents').textContent = Object.keys(agents).length;
  document.getElementById('h-events').textContent = eventN;
}

function pad2(n) { return String(n).padStart(2,'0'); }

setInterval(() => {
  const now = new Date();
  document.getElementById('h-time').textContent = now.toTimeString().slice(0, 8);

  const secs = Math.floor((Date.now() - t0) / 1000);
  const h = pad2(Math.floor(secs / 3600));
  const m = pad2(Math.floor((secs % 3600) / 60));
  const s = pad2(secs % 60);
  document.getElementById('f-uptime').textContent = `${h}:${m}:${s}`;
  document.getElementById('f-time').textContent   = 'UTC ' + now.toUTCString().slice(17, 25);
}, 1000);

// ── Escape HTML ───────────────────────────────────────────────────────────
function x(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Theme toggle ──────────────────────────────────────────────────────────
function toggleTheme() {
  const html = document.documentElement;
  const btn  = document.getElementById('theme-btn');
  if (html.dataset.theme === 'light') {
    delete html.dataset.theme;
    btn.textContent = '◐';
    localStorage.setItem('theme', 'dark');
  } else {
    html.dataset.theme = 'light';
    btn.textContent = '◑';
    localStorage.setItem('theme', 'light');
  }
}

(function () {
  if (localStorage.getItem('theme') === 'light') {
    document.documentElement.dataset.theme = 'light';
    const btn = document.getElementById('theme-btn');
    if (btn) btn.textContent = '◑';
  }
})();

// ── MAP ───────────────────────────────────────────────────────────────────
let _map = null;
let _darkTiles, _lightTiles;
const _markers = {};   // agent_name → { marker, data }

// Facility logo table: { patterns, logo, label }
// Patterns are matched against the agent's fqdn (lowercase).
// logos are served from /assets/.
function _makeIcon(d) {
  if (!d.logo_url) return null;
  return L.icon({
    iconUrl: d.logo_url,
    iconSize: [45, 45],
    iconAnchor: [22, 22],
    popupAnchor: [0, -25],
    className: 'map-facility-icon',
  });
}

function _agentColor(name) {
  // Deterministic colour from agent name so each agent has a stable hue.
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffff;
  const hue = (h % 360);
  return `hsl(${hue},85%,58%)`;
}

function _popupHtml(d) {
  const row = (label, val) => val
    ? `<div class="map-popup-row"><span class="map-popup-label">${label}</span><span>${x(String(val))}</span></div>`
    : '';
  return `
    <div class="map-popup-name">${x(d.agent_name || d.agent || '?')}</div>
    ${row('ID', d.agent)}
    ${row('FQDN',    d.fqdn)}
    ${row('CITY',    d.geo?.city)}
    ${row('COUNTRY', d.geo?.country)}
    ${row('ORG',     d.geo?.org)}
    ${row('CPU',     d.cpu)}
    ${row('OS',      d.os)}
    ${row('ARCH',    d.arch)}
    ${row('PYTHON',  d.python_version)}
  `;
}

const MAP_VIEWS = {
  world: { center: [20,    0], zoom: 2 },
  us:    { center: [38,  -97], zoom: 4 },
};
let _currentMapView = 'us';

function _ensureMap() {
  if (_map) return;
  const dark  = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
  const light = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
  const attr  = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>';

  const v = MAP_VIEWS[_currentMapView];
  _map = L.map('map', { zoomControl: true, attributionControl: true }).setView(v.center, v.zoom);
  _darkTiles  = L.tileLayer(dark,  { attribution: attr, maxZoom: 19 });
  _lightTiles = L.tileLayer(light, { attribution: attr, maxZoom: 19 });
  const isLight = document.documentElement.dataset.theme === 'light';
  (isLight ? _lightTiles : _darkTiles).addTo(_map);
}

function setMapView(view) {
  _currentMapView = view;
  // Update button states
  document.getElementById('map-view-world').classList.toggle('is-active', view === 'world');
  document.getElementById('map-view-us').classList.toggle('is-active', view === 'us');
  if (!_map) return;
  const v = MAP_VIEWS[view];
  _map.flyTo(v.center, v.zoom, { duration: 0.8 });
}

function _upsertMapMarker(d) {
  if (!d.geo?.lat || !d.geo?.lon) return;
  _ensureMap();
  const uid         = d.agent;                        // stable unique key (uid)
  const displayName = d.agent_name || uid || '?';     // human-readable label
  const lat  = d.geo.lat, lon = d.geo.lon;
  const icon = _makeIcon(d);
  const popup = _popupHtml(d);

  if (_markers[uid]) {
    _markers[uid].marker.setLatLng([lat, lon]).setPopupContent(popup);
    _markers[uid].data = d;
    return;
  }

  let marker;
  if (icon) {
    marker = L.marker([lat, lon], { icon }).bindPopup(popup);
  } else {
    const color = _agentColor(displayName);
    marker = L.circleMarker([lat, lon], {
      radius: 10, color, fillColor: color, fillOpacity: 0.75, weight: 2,
    }).bindPopup(popup);
  }
  marker.addTo(_map);
  _markers[uid] = { marker, data: d };
}

// ── Agent connection lines ─────────────────────────────────────────────────
const _lines = {};  // 'agentA||agentB' → { line, timer }

function _lineKey(a, b) { return [a, b].sort().join('||'); }

// Draw (or refresh) a passive idle line between two agents.
function _connectAgents(nameA, nameB) {
  if (!_map) return;
  const dA = agents[nameA], dB = agents[nameB];
  if (!dA?.geo?.lat || !dB?.geo?.lat) return;
  const key  = _lineKey(nameA, nameB);
  const latlngs = [[dA.geo.lat, dA.geo.lon], [dB.geo.lat, dB.geo.lon]];
  if (_lines[key]) {
    _lines[key].line.setLatLngs(latlngs);
    return;
  }
  const line = L.polyline(latlngs, {
    color: '#00e5ff', weight: 1.5, opacity: 0.35,
    className: 'map-conn-line',
  }).addTo(_map);
  _lines[key] = { line, timer: null };
}

// Draw idle lines between every pair of geo-located agents.
// TODO: replace with event-driven calls to showConnection() once
//       agent-agent communication events are wired up.
function _drawAllConnections() {
  const geo = Object.keys(agents).filter(n => agents[n]?.geo?.lat);
  for (let i = 0; i < geo.length; i++) {
    for (let j = i + 1; j < geo.length; j++) {
      _connectAgents(geo[i], geo[j]);
    }
  }
}

// Public API — call this from a future agent-agent communication SSE event.
// The line brightens and speeds up for `durationMs` ms, then reverts to idle.
function showConnection(nameA, nameB, durationMs = 2500) {
  _connectAgents(nameA, nameB);
  const key  = _lineKey(nameA, nameB);
  const entry = _lines[key];
  if (!entry) return;
  entry.line.setStyle({ opacity: 0.85, weight: 2.5 });
  entry.line.getElement()?.classList.add('active');
  clearTimeout(entry.timer);
  entry.timer = setTimeout(() => {
    entry.line.setStyle({ opacity: 0.35, weight: 1.5 });
    entry.line.getElement()?.classList.remove('active');
  }, durationMs);
}

// Handle registration event (full agent data, geo may be null initially)
es.addEventListener('registration', e => {
  const d = JSON.parse(e.data);
  Object.assign(agents[d.agent] || (agents[d.agent] = {}), d);
  upsertCard(d.agent, agents[d.agent]);
  _upsertMapMarker(d);
  _drawAllConnections();
  eventN++; updateHud();
});

es.addEventListener('status', e => {
  const d = JSON.parse(e.data);
  Object.assign(agents[d.agent] || (agents[d.agent] = {}), d);
  upsertCard(d.agent, agents[d.agent]);
  eventN++; updateHud();
});

// Swap tile layer when theme is toggled
const _origToggleTheme = toggleTheme;
toggleTheme = function () {
  _origToggleTheme();
  if (!_map) return;
  const isLight = document.documentElement.dataset.theme === 'light';
  if (isLight) { _map.removeLayer(_darkTiles);  _lightTiles.addTo(_map); }
  else          { _map.removeLayer(_lightTiles); _darkTiles.addTo(_map); }
};

// Invalidate map size when the MAP tab is activated (Leaflet needs this)
const _origSwitchTab = switchTab;
switchTab = function (btn) {
  _origSwitchTab(btn);
  if (btn.dataset.tab === 'map') {
    _ensureMap();
    setTimeout(() => _map.invalidateSize(), 50);
    // Re-render all agents with geo onto the map
    Object.entries(agents).forEach(([name, d]) => {
      if (d.geo?.lat) _upsertMapMarker({ ...d, agent: name });
    });
    _drawAllConnections();
  }
};
</script>
</body>
</html>
"""

_DETAIL_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AGENT DETAIL</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    :root {
      --cyan:#00e5ff; --green:#00ff88; --red:#ff1744; --yellow:#ffdd00;
      --bg:#000810; --card-bg:rgba(0,14,38,0.88); --border:rgba(0,229,255,0.32); --dim:rgba(0,229,255,0.52);
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:'Share Tech Mono','Courier New',monospace; background:var(--bg); color:var(--cyan); min-height:100vh; padding:28px 36px 72px; }
    body::before {
      content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
      background-image:linear-gradient(rgba(0,100,255,.065) 1px,transparent 1px),linear-gradient(90deg,rgba(0,100,255,.065) 1px,transparent 1px);
      background-size:48px 48px; animation:gridDrift 28s linear infinite;
    }
    @keyframes gridDrift { to { background-position:48px 48px; } }
    .page { position:relative; z-index:10; max-width:960px; margin:0 auto; }
    a.back { display:inline-flex; align-items:center; gap:8px; font-size:.7rem; letter-spacing:.28em; color:var(--dim); text-decoration:none; margin-bottom:30px; transition:color .18s; }
    a.back:hover { color:var(--cyan); }
    h1 { font-size:1.3rem; letter-spacing:.2em; text-transform:uppercase; text-shadow:0 0 18px var(--cyan); margin-bottom:5px; }
    .sub { font-size:.6rem; color:rgba(0,229,255,.32); letter-spacing:.15em; margin-bottom:38px; }
    .section { margin-bottom:38px; }
    .sh { display:flex; align-items:center; gap:14px; margin-bottom:16px; }
    .sh-title { font-size:.66rem; letter-spacing:.45em; text-transform:uppercase; color:var(--dim); white-space:nowrap; }
    .sh-line { flex:1; height:1px; background:linear-gradient(to right,var(--border),transparent); }
    table { width:100%; border-collapse:collapse; font-size:.75rem; }
    th { text-align:left; color:rgba(0,229,255,.36); letter-spacing:.2em; font-size:.62rem; padding:7px 12px; border-bottom:1px solid rgba(0,229,255,.1); font-weight:normal; }
    td { padding:9px 12px; border-bottom:1px solid rgba(0,229,255,.06); color:rgba(185,220,255,.85); vertical-align:top; }
    #hw-table td:first-child { color:var(--dim); white-space:nowrap; width:130px; }
    .tag { display:inline-block; padding:2px 8px; font-size:.58rem; letter-spacing:.15em; border:1px solid rgba(0,229,255,.28); color:var(--dim); margin:1px 2px 1px 0; }
    .param-block { font-size:.65rem; }
    .param-name { color:var(--cyan); }
    .param-type { color:rgba(0,229,255,.44); }
    .no-data { color:rgba(0,229,255,.24); font-size:.72rem; letter-spacing:.2em; padding:18px 0; }
    .communicates { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; margin-bottom:22px; }
    .comm-tag { padding:4px 14px; border:1px solid rgba(0,229,255,.3); font-size:.65rem; letter-spacing:.15em; color:var(--cyan); }
    td.desc { white-space:pre-line; max-width:300px; }
    .topbar { display:flex; justify-content:space-between; align-items:center; margin-bottom:30px; }
    .topbar a.back { margin-bottom:0; }
    .btn-theme { background:transparent; border:1px solid rgba(0,229,255,.28); color:var(--dim); font-family:inherit; font-size:.78rem; padding:4px 10px; cursor:pointer; transition:all .18s; }
    .btn-theme:hover { border-color:var(--cyan); color:var(--cyan); background:rgba(0,229,255,.05); }
    [data-theme="light"] { --cyan:#0055cc; --green:#007740; --red:#cc0022; --yellow:#b87800; --bg:#eef2f7; --border:rgba(0,80,200,0.28); --dim:rgba(0,50,140,0.58); }
    [data-theme="light"] body { background:var(--bg); color:var(--cyan); }
    [data-theme="light"] body::before { background-image:linear-gradient(rgba(0,80,200,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(0,80,200,.055) 1px,transparent 1px); }
    [data-theme="light"] th { color:rgba(0,50,140,.38); border-bottom-color:rgba(0,80,200,.12); }
    [data-theme="light"] td { color:rgba(20,40,90,.82); border-bottom-color:rgba(0,80,200,.07); }
    [data-theme="light"] #hw-table td:first-child { color:var(--dim); }
    [data-theme="light"] .param-type { color:rgba(0,50,140,.45); }
    [data-theme="light"] .no-data { color:rgba(0,80,200,.25); }
    [data-theme="light"] .btn-theme { border-color:rgba(0,80,200,.28); color:var(--dim); }
    [data-theme="light"] .btn-theme:hover { border-color:var(--cyan); color:var(--cyan); background:rgba(0,80,200,.05); }
  </style>
</head>
<body>
<div class="page">
  <div class="topbar">
    <a href="__BASE_URL__/" class="back">← DASHBOARD</a>
    <button class="btn-theme" id="theme-btn" onclick="toggleTheme()">◐</button>
  </div>
  <h1 id="agent-name">LOADING...</h1>
  <div class="sub" id="agent-sub"></div>

  <div class="section">
    <div class="sh"><div class="sh-title">HARDWARE</div><div class="sh-line"></div></div>
    <table id="hw-table"><tbody></tbody></table>
  </div>

  <div class="section">
    <div class="sh"><div class="sh-title">SKILLS</div><div class="sh-line"></div></div>
    <div id="skills-content"></div>
  </div>
</div>
<script>
'use strict';
function x(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

const agentId = decodeURIComponent(window.location.pathname.split('/').pop());
fetch('__BASE_URL__/api/agent/' + encodeURIComponent(agentId))
  .then(r => r.ok ? r.json() : Promise.reject(r.status))
  .then(render)
  .catch(() => { document.getElementById('agent-name').textContent = 'AGENT NOT FOUND'; });

function render(d) {
  document.title = (d.agent_name || agentId) + ' — AGENT DETAIL';
  document.getElementById('agent-name').textContent = (d.agent_name || agentId).toUpperCase();
  document.getElementById('agent-sub').textContent = agentId;

  const geo = d.geo || {};
  const hw = [
    ['FQDN',     d.fqdn],
    ['CPU',      d.cpu],
    ['OS',       d.os ? (d.os + (d.arch ? '  ' + d.arch : '')) : null],
    ['PYTHON',   d.python_version],
    ['LOCATION', geo.city ? [geo.city, geo.country].filter(Boolean).join(', ') : null],
    ['ORG',      geo.org],
  ];
  const tbody = document.querySelector('#hw-table tbody');
  hw.forEach(([label, val]) => {
    if (!val) return;
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>' + x(label) + '</td><td>' + x(val) + '</td>';
    tbody.appendChild(tr);
  });

  renderSkills(d.agent_card);
}

function renderSkills(card) {
  const el = document.getElementById('skills-content');
  if (!card) { el.innerHTML = '<div class="no-data">NO AGENT CARD AVAILABLE</div>'; return; }

  if (card.x_communicates_with && card.x_communicates_with.length) {
    const tags = card.x_communicates_with.map(a => '<span class="comm-tag">' + x(a) + '</span>').join('');
    el.innerHTML += '<div style="font-size:.64rem;letter-spacing:.2em;color:var(--dim)">COMMUNICATES WITH<div class="communicates">' + tags + '</div></div>';
  }

  const skills = card.skills || [];
  if (!skills.length) { el.innerHTML += '<div class="no-data">NO SKILLS DEFINED</div>'; return; }

  let t = '<table><thead><tr><th>NAME</th><th>TYPE</th><th>DESCRIPTION</th><th>PARAMETERS</th></tr></thead><tbody>';
  skills.forEach(s => {
    const tags = (s.tags || []).map(t => '<span class="tag">' + x(t) + '</span>').join('');
    const params = Object.entries(s.x_parameters || {})
      .map(([k, v]) => '<div class="param-block"><span class="param-name">' + x(k) + '</span> <span class="param-type">' + x(v) + '</span></div>')
      .join('') || '<span style="opacity:.3">—</span>';
    t += '<tr><td>' + x(s.name) + '</td><td>' + tags + '</td><td class="desc">' + x(s.description || '') + '</td><td>' + params + '</td></tr>';
  });
  t += '</tbody></table>';
  el.innerHTML += t;
}

function toggleTheme() {
  const html = document.documentElement;
  const btn  = document.getElementById('theme-btn');
  if (html.dataset.theme === 'light') {
    delete html.dataset.theme;
    btn.textContent = '◐';
    localStorage.setItem('theme', 'dark');
  } else {
    html.dataset.theme = 'light';
    btn.textContent = '◑';
    localStorage.setItem('theme', 'light');
  }
}

(function () {
  if (localStorage.getItem('theme') === 'light') {
    document.documentElement.dataset.theme = 'light';
    const btn = document.getElementById('theme-btn');
    if (btn) btn.textContent = '◑';
  }
})();
</script>
</body>
</html>"""


def agent_detail_page(base_url: str = '') -> str:
    """Return the agent detail page HTML with base_url substituted."""
    return _DETAIL_HTML.replace('__BASE_URL__', base_url)
