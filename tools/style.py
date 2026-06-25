# CSS base (clonado de la entrega de referencia del usuario, estética propia).
# Sistema editorial cinematográfico oscuro. La variación de color por notebook
# se hace con hue-rotate en el contenedor (ver nbgen.py), no tocando este CSS.
EDU_CSS = r"""<style>
  @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=Archivo+Expanded:wght@600;700;800&display=swap');

  /* ===================================================================
     SISTEMA EDITORIAL CINEMATOGRÁFICO OSCURO
     Paleta fría documental · tipografía display extruida · vidrio esmerilado
     =================================================================== */

  /* ---------- contenedor base ---------- */
  .edu{max-width:1140px;margin:24px auto;font-family:'Archivo',system-ui,sans-serif;
       color:#dde7f2;line-height:1.66;font-size:15px;}
  .edu *{box-sizing:border-box;}

  /* ---------- hoja: panel de vidrio oscuro ---------- */
  .edu-sheet{position:relative;overflow:hidden;border-radius:22px;padding:36px 44px 40px;
     color:#e6eef8;background:linear-gradient(168deg,rgba(17,30,47,.94),rgba(9,16,27,.96));
     border:1px solid rgba(140,180,224,.14);
     box-shadow:0 30px 70px rgba(3,8,18,.55),inset 0 1px 0 rgba(255,255,255,.05);}
  .edu-sheet::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;
     background:linear-gradient(90deg,#1d6fb0,#43c4b0 35%,#7fd4ff 55%,#43c4b0 75%,#1d6fb0);
     background-size:220% 100%;animation:eduBarFlow 7s linear infinite;}
  .edu-sheet::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:0;opacity:.5;
     background:radial-gradient(110% 60% at 88% -10%,rgba(127,212,255,.10),transparent 60%);}
  .edu-sheet>*{position:relative;z-index:1;}

  /* ---------- eyebrow / etiqueta ---------- */
  .edu-eyebrow{display:inline-block;font-family:'Archivo Expanded','Archivo',sans-serif;
     font-size:10.5px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#7fd4ff;
     background:rgba(127,212,255,.08);border:1px solid rgba(127,212,255,.30);
     padding:6px 16px;border-radius:999px;margin-bottom:18px;animation:eduPulse 3.4s ease-in-out infinite;}

  /* ---------- títulos ---------- */
  .edu h2{font-family:'Archivo Expanded','Archivo',sans-serif;color:#f1f7ff;font-size:23px;
     font-weight:800;letter-spacing:.3px;text-transform:uppercase;margin:34px 0 14px;
     padding:6px 0 10px 18px;border-left:4px solid #43c4b0;
     background:linear-gradient(90deg,rgba(67,196,176,.12),transparent 60%);}
  .edu h2:first-child{margin-top:0;}
  .edu h2.alt{border-left-color:#ff8f6b;background:linear-gradient(90deg,rgba(255,143,107,.13),transparent 60%);}
  .edu h3{color:#7fd4ff;font-size:12px;font-weight:700;letter-spacing:1.4px;
     text-transform:uppercase;margin:22px 0 6px;font-family:'Archivo Expanded','Archivo',sans-serif;}
  .edu p{margin:9px 0;color:#cdd9e7;}
  .edu b,.edu strong{color:#ffffff;font-weight:700;}
  .edu i,.edu em{color:#bfe6ff;}
  .edu code{background:rgba(127,212,255,.12);border:1px solid rgba(127,212,255,.26);border-radius:5px;
     padding:1px 7px;font-size:13px;color:#bfe6ff;font-family:ui-monospace,Menlo,monospace;}

  /* ---------- listas con viñeta propia ---------- */
  .edu ul{margin:6px 0;padding-left:2px;list-style:none;}
  .edu ul li{position:relative;padding-left:26px;margin:8px 0;color:#cdd9e7;}
  .edu ul li::before{content:"";position:absolute;left:4px;top:9px;width:8px;height:8px;border-radius:2px;
     background:linear-gradient(135deg,#7fd4ff,#43c4b0);transform:rotate(45deg);box-shadow:0 0 8px rgba(127,212,255,.5);}

  /* ---------- tablas ---------- */
  .edu-tbl{border-collapse:separate;border-spacing:0;width:100%;font-size:14px;margin:16px 0;
     border:1px solid rgba(140,180,224,.16);border-radius:14px;overflow:hidden;
     background:rgba(8,15,26,.45);box-shadow:0 10px 30px rgba(3,8,18,.4);}
  .edu-tbl th{background:linear-gradient(135deg,#103a5e,#1c6aa6);color:#eaf4ff;font-weight:700;
     padding:12px 15px;text-align:left;letter-spacing:.4px;border:none;
     font-family:'Archivo Expanded','Archivo',sans-serif;font-size:12px;text-transform:uppercase;}
  .edu-tbl td{padding:10px 15px;border:none;border-top:1px solid rgba(140,180,224,.10);color:#d4e0ee;}
  .edu-tbl tr:nth-child(even) td{background:rgba(255,255,255,.025);}
  .edu-tbl tr:hover td{background:rgba(127,212,255,.10);}
  .edu-tbl .num,.edu-tbl td.num{text-align:right;font-variant-numeric:tabular-nums;}

  /* ---------- grid de tarjetas ---------- */
  .edu-grid{display:flex;flex-wrap:wrap;gap:16px;margin:16px 0;}
  .edu-card{flex:1 1 220px;border-radius:16px;padding:18px 20px;
     background:linear-gradient(160deg,rgba(24,40,60,.6),rgba(13,23,37,.5));
     border:1px solid rgba(140,180,224,.16);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;}
  .edu-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(3,8,18,.5);border-color:rgba(127,212,255,.4);}
  .edu-card h3{margin:0 0 6px;}
  .edu-card p{margin:0;font-size:14px;color:#aebfd2;line-height:1.5;}

  /* ---------- KPIs / cifras ---------- */
  .edu-kpis{display:flex;flex-wrap:wrap;gap:14px;margin:18px 0;}
  .edu-kpi{flex:1 1 150px;text-align:center;border-radius:16px;padding:18px 14px;
     background:linear-gradient(165deg,rgba(20,38,58,.7),rgba(10,18,30,.6));
     border:1px solid rgba(140,180,224,.18);box-shadow:inset 0 1px 0 rgba(255,255,255,.05);}
  .edu-kpi .v{font-size:30px;font-weight:800;color:#7fd4ff;line-height:1;
     font-family:'Archivo Expanded','Archivo',sans-serif;text-shadow:0 0 22px rgba(127,212,255,.4);}
  .edu-kpi .l{font-size:10.5px;text-transform:uppercase;letter-spacing:1.2px;color:#8ea3ba;margin-top:8px;}

  /* ---------- callouts ---------- */
  .edu-note,.edu-warn,.edu-ok{border-radius:14px;padding:15px 20px;margin:16px 0;font-size:14px;
     line-height:1.62;border:1px solid;border-left-width:4px;backdrop-filter:blur(4px);}
  .edu-note{background:rgba(47,159,224,.10);border-color:rgba(127,212,255,.26);border-left-color:#7fd4ff;color:#cfe7fb;}
  .edu-warn{background:rgba(255,160,90,.10);border-color:rgba(255,180,110,.30);border-left-color:#ff9f5c;color:#ffd9b8;}
  .edu-ok{background:rgba(67,196,176,.10);border-color:rgba(90,220,190,.30);border-left-color:#43c4b0;color:#bff0e4;}
  .edu-note b,.edu-warn b,.edu-ok b{color:#fff;}

  /* ---------- spans destacados ---------- */
  .edu .hl{color:#7fd4ff;font-weight:700;} .edu .ok{color:#5ce0b5;font-weight:700;}
  .edu .warn{color:#ff9f5c;font-weight:700;}

  /* ---------- caption / pie ---------- */
  .edu-cap{font-size:12.5px;color:#8295ab;margin-top:12px;}
  .edu-foot{font-size:12.5px;color:#8295ab;margin-top:22px;border-top:1px dashed rgba(140,180,224,.22);padding-top:14px;}

  /* ---------- referencias ---------- */
  .edu-ref{background:rgba(8,16,28,.5);border:1px solid rgba(140,180,224,.16);border-left:4px solid #7fd4ff;
     border-radius:12px;padding:18px 20px;font-size:13.5px;color:#b9c8da;line-height:1.75;}

  /* ===================================================================
     PORTADA · HERO CINEMATOGRÁFICO
     =================================================================== */
  .edu-portada{max-width:1180px;margin:26px auto;border-radius:26px;overflow:hidden;
     font-family:'Archivo',system-ui,sans-serif;color:#e9f1fb;border:1px solid rgba(120,160,210,.18);
     box-shadow:0 40px 90px rgba(2,6,14,.6);animation:eduBreathe 12s ease-in-out infinite;}

  .edu-cine{position:relative;overflow:hidden;padding:26px 52px 24px 78px;min-height:560px;
     background:
        radial-gradient(60% 42% at 78% 6%,rgba(170,210,255,.20),transparent 55%),
        radial-gradient(80% 60% at 6% 104%,rgba(40,150,140,.20),transparent 60%),
        linear-gradient(180deg,#0c1a2b 0%,#0a1626 42%,#060f1b 100%);
     background-size:130% 130%,100% 100%,100% 100%;animation:eduHeroFlow 20s ease infinite;}

  /* atmósfera: niebla, grano, montañas, estrellas, cometas (todo CSS, sin imágenes externas) */
  .edu-fog{position:absolute;inset:0;z-index:0;pointer-events:none;
     background:radial-gradient(50% 38% at 50% 26%,rgba(150,190,230,.16),transparent 72%);filter:blur(14px);
     animation:eduFog 16s ease-in-out infinite;}
  .edu-grain{position:absolute;inset:0;z-index:2;pointer-events:none;opacity:.32;mix-blend-mode:overlay;
     background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
  .edu-ridge{position:absolute;left:0;right:0;bottom:0;width:100%;height:190px;z-index:1;pointer-events:none;display:block;}
  .edu-stars,.edu-stars2{position:absolute;inset:0;pointer-events:none;z-index:1;}
  .edu-stars{animation:eduTwinkle 4.5s ease-in-out infinite;background-image:
     radial-gradient(1px 1px at 12% 22%,#fff,transparent),radial-gradient(1px 1px at 28% 64%,#fff,transparent),
     radial-gradient(1px 1px at 44% 14%,#fff,transparent),radial-gradient(1px 1px at 63% 38%,#fff,transparent),
     radial-gradient(1px 1px at 82% 33%,#fff,transparent),radial-gradient(1px 1px at 91% 20%,#fff,transparent),
     radial-gradient(1px 1px at 7% 48%,#fff,transparent),radial-gradient(1px 1px at 35% 12%,#fff,transparent);}
  .edu-stars2{animation:eduTwinkle 7s ease-in-out infinite;animation-delay:1.6s;background-image:
     radial-gradient(1.6px 1.6px at 18% 30%,#bfefff,transparent),radial-gradient(1.6px 1.6px at 49% 20%,#ffe9a8,transparent),
     radial-gradient(1.6px 1.6px at 70% 12%,#fff,transparent),radial-gradient(1.6px 1.6px at 88% 28%,#9fe6da,transparent),
     radial-gradient(1.6px 1.6px at 24% 18%,#fff,transparent);}
  .edu-comet{position:absolute;top:14%;left:-15%;width:160px;height:2px;z-index:1;pointer-events:none;
     background:linear-gradient(90deg,transparent,#bfefff,#fff);border-radius:50%;opacity:0;
     box-shadow:0 0 8px #bfefff,0 0 24px rgba(150,210,255,.55);transform:rotate(15deg);
     animation:eduComet 13s linear infinite;}
  .edu-comet.edu-comet2{top:40%;animation-duration:17s;animation-delay:7s;}

  .edu-cine>*{position:relative;z-index:3;}

  /* nav superior */
  .edu-nav{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;
     padding-bottom:8px;border-bottom:1px solid rgba(160,195,235,.12);}
  .edu-logo{font-family:'Archivo Black',sans-serif;font-size:18px;letter-spacing:.5px;color:#fff;}
  .edu-logo span{color:#7fd4ff;font-weight:400;font-family:'Archivo',sans-serif;font-size:13px;margin-left:6px;letter-spacing:1px;}
  .edu-nav nav{display:flex;gap:22px;flex-wrap:wrap;}
  .edu-nav nav a{font-size:12.5px;letter-spacing:.6px;color:#aebfd2;text-decoration:none;text-transform:uppercase;
     font-weight:600;transition:color .15s ease;}
  .edu-nav nav a:hover{color:#fff;}
  .edu-nav nav a.on{color:#7fd4ff;}

  /* etiquetas verticales decorativas (borde izquierdo) */
  .edu-vlabels{position:absolute;left:20px;top:54%;transform:translateY(-50%);z-index:3;
     display:flex;flex-direction:column;gap:30px;}
  .edu-vlabels span{writing-mode:vertical-rl;transform:rotate(180deg);font-size:10px;letter-spacing:3px;
     text-transform:uppercase;color:rgba(174,191,210,.6);font-weight:600;
     font-family:'Archivo Expanded','Archivo',sans-serif;}

  /* layout principal: titular gigante a todo el ancho */
  .edu-cine-grid{margin-top:30px;}
  .edu-kicker{display:inline-block;font-family:'Archivo Expanded','Archivo',sans-serif;font-size:10.5px;
     font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#8fb4d8;margin-bottom:18px;
     padding-left:2px;animation:eduRise .8s cubic-bezier(.2,.7,.2,1) both;}

  .edu-mega{font-family:'Archivo Black',sans-serif;text-transform:uppercase;color:#f6faff;margin:0;
     font-size:clamp(44px,6.6vw,92px);line-height:.9;letter-spacing:-.01em;
     text-shadow:0 1px 0 #c4cfdd,0 2px 0 #aeb9c9,0 3px 0 #99a5b8,0 4px 0 #8593a8,0 5px 0 #74829a,
                 0 12px 22px rgba(0,0,0,.6);animation:eduRise .9s cubic-bezier(.2,.7,.2,1) both;}
  .edu-mega em{display:block;font-style:normal;color:#7fd4ff;
     text-shadow:0 0 30px rgba(127,212,255,.55),0 3px 0 rgba(10,40,70,.5);}

  .edu-lede{max-width:480px;margin:24px 0 0;color:#c4d3e4;font-size:16px;line-height:1.6;
     animation:eduRise .9s cubic-bezier(.2,.7,.2,1) .15s both;}

  .edu-cta{display:inline-flex;align-items:center;gap:12px;margin-top:26px;cursor:pointer;
     padding:14px 26px;border-radius:999px;text-decoration:none;font-weight:700;font-size:14.5px;
     letter-spacing:.4px;color:#06121f;background:linear-gradient(135deg,#aee1ff,#7fd4ff);
     box-shadow:0 14px 34px rgba(127,212,255,.35);transition:transform .18s ease,box-shadow .18s ease;
     animation:eduRise .9s cubic-bezier(.2,.7,.2,1) .3s both;}
  .edu-cta:hover{transform:translateY(-2px);box-shadow:0 18px 42px rgba(127,212,255,.5);}
  .edu-cta span{transition:transform .18s ease;} .edu-cta:hover span{transform:translateX(5px);}

  /* tarjetas glassmorphic en fila horizontal (hallazgos) bajo el titular */
  .edu-floats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:40px;}
  .edu-glass{position:relative;display:flex;flex-direction:column;border-radius:18px;padding:22px 24px;color:#e9f1fb;
     background:linear-gradient(160deg,rgba(22,38,58,.55),rgba(10,18,30,.42));
     backdrop-filter:blur(14px) saturate(130%);-webkit-backdrop-filter:blur(14px) saturate(130%);
     border:1px solid rgba(160,200,240,.18);box-shadow:0 20px 50px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08);
     transition:transform .2s ease,border-color .2s ease;animation:eduRise .9s cubic-bezier(.2,.7,.2,1) both;}
  .edu-floats .edu-glass:nth-child(1){animation-delay:.35s;}
  .edu-floats .edu-glass:nth-child(2){animation-delay:.46s;}
  .edu-floats .edu-glass:nth-child(3){animation-delay:.57s;}
  .edu-glass:hover{transform:translateY(-4px);border-color:rgba(127,212,255,.5);}
  .edu-glass h4{margin:0 0 8px;font-size:17px;font-weight:700;color:#fff;font-family:'Archivo Expanded','Archivo',sans-serif;}
  .edu-glass p{margin:0;font-size:13.5px;line-height:1.55;color:#b6c6d8;}
  .edu-glass-foot{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:16px;gap:10px;}
  .edu-metric{font-size:12px;font-weight:700;color:#7fd4ff;letter-spacing:.3px;}
  .edu-glass-foot a{font-size:12.5px;font-weight:700;color:#fff;text-decoration:none;white-space:nowrap;
     border-bottom:1px solid rgba(127,212,255,.5);padding-bottom:1px;transition:color .15s ease;}
  .edu-glass-foot a:hover{color:#7fd4ff;}

  /* fila de fuentes (logos) */
  .edu-logos{display:flex;align-items:center;gap:26px;flex-wrap:wrap;margin-top:38px;padding-top:18px;
     border-top:1px solid rgba(160,195,235,.12);}
  .edu-logos-label{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:#6f86a0;font-weight:700;}
  .edu-logos>span:not(.edu-logos-label){font-family:'Archivo Expanded','Archivo',sans-serif;font-weight:700;
     font-size:13px;letter-spacing:.5px;color:rgba(190,205,222,.55);transition:color .18s ease;}
  .edu-logos>span:not(.edu-logos-label):hover{color:#cfe0f2;}

  /* franja de metadatos académicos bajo el hero */
  .edu-metastrip{background:linear-gradient(180deg,#0a131f,#0b1422);padding:26px 52px 30px;
     border-top:1px solid rgba(160,195,235,.10);}
  .edu-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:18px;}
  .edu-meta>div{display:flex;flex-direction:column;gap:4px;}
  .edu-meta .k{font-size:10px;letter-spacing:1.8px;text-transform:uppercase;color:#7fd4ff;font-weight:700;
     font-family:'Archivo Expanded','Archivo',sans-serif;}
  .edu-meta .v{font-size:13.5px;color:#cdd9e7;line-height:1.45;}
  .edu-disc{background:rgba(255,170,90,.09);border:1px solid rgba(255,185,120,.28);border-left:4px solid #ff9f5c;
     color:#ffd9b8;border-radius:14px;padding:14px 18px;font-size:12.8px;margin-top:22px;line-height:1.6;}
  .edu-disc b{color:#ffe9d2;}

  @media (max-width:820px){
     .edu-cine{padding:24px 30px 22px;min-height:auto;}
     .edu-floats{grid-template-columns:1fr;gap:14px;margin-top:30px;}
     .edu-vlabels{display:none;}
     .edu-nav nav{gap:14px;} .edu-sheet{padding:26px 22px 30px;}
  }

  /* ===================================================================
     ANIMACIONES
     =================================================================== */
  @keyframes eduBarFlow{0%{background-position:0% 0;}100%{background-position:220% 0;}}
  @keyframes eduPulse{0%,100%{box-shadow:0 0 0 rgba(127,212,255,0);}50%{box-shadow:0 0 16px rgba(127,212,255,.35);}}
  @keyframes eduHeroFlow{0%{background-position:0% 50%,0 0,0 0;}50%{background-position:100% 50%,0 0,0 0;}100%{background-position:0% 50%,0 0,0 0;}}
  @keyframes eduBreathe{0%,100%{box-shadow:0 40px 90px rgba(2,6,14,.6);}50%{box-shadow:0 46px 104px rgba(20,80,110,.5);}}
  @keyframes eduTwinkle{0%,100%{opacity:.35;}50%{opacity:1;}}
  @keyframes eduFog{0%,100%{opacity:.7;transform:translateX(0);}50%{opacity:1;transform:translateX(20px);}}
  @keyframes eduComet{0%{opacity:0;transform:translate(0,0) rotate(15deg);}5%{opacity:.95;}
     22%{opacity:0;transform:translate(1200px,330px) rotate(15deg);}100%{opacity:0;}}
  @keyframes eduRise{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}

  @media (prefers-reduced-motion:reduce){
     .edu-portada,.edu-cine,.edu-fog,.edu-stars,.edu-stars2,.edu-comet,.edu-sheet::before,.edu-eyebrow,
     .edu-kicker,.edu-mega,.edu-lede,.edu-cta,.edu-glass{animation:none!important;}
  }
</style>"""
