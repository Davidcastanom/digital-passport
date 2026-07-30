import streamlit as st
import streamlit.components.v1 as components

IMG_FONDO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366977/fondo_biruor.png"
IMG_LOGO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366976/logo_2_ne0zk5.png"

MODULES = [
    ("01", "🆔", "Identidad Digital", "Perfil maestro del usuario: email, teléfono E.164, ubicación base de ciudad y configuración regional BCP47.", "user_identity · user_geolocation · user_culture_language"),
    ("02", "📦", "Logística Global", "Órdenes de comercio exterior con códigos HS, Incoterms y unidades UN/CEFACT. Trazabilidad producto por producto.", "trade_supply_chain · industry_measurements"),
    ("03", "💰", "Compliance & KYC", "Validación fiscal y bancaria automatizada: NIT, CIIU, IBAN, SWIFT. Listo para integración con entidades financieras.", "user_financials · legal_economic_activity"),
    ("04", "🔐", "Ciberseguridad", "Trazabilidad de accesos con IP, MAC, auditoría de eventos y registro cronológico de cada acción del usuario.", "network_infrastructure · user_time_events · view_auditoria_seguridad"),
    ("05", "📡", "Telemetría GPS", "Rastreo satelital con Google Maps: balizas, rutas por carretera, slider temporal, velocidad y reproducción de trayectos.", "telemetry_log · Google Maps JavaScript API"),
    ("06", "🎓", "Perfil Científico", "Clasificación ISCO-08 (OIT) y publicaciones DOI para validación de credenciales profesionales y académicas.", "health_science_sectorial"),
    ("07", "🏗", "Arquitectura Viva", "ERD generado dinámicamente, explorador de tablas/vistas con DDL, PK/FK, relaciones y exportación CSV.", "sqlite_master · PRAGMA · vistas del sistema"),
    ("08", "🔌", "Integración API", "Perfil de conexión completo exportable a JSON. Un solo endpoint virtual con todos los datos del usuario.", "connection_profile · JSON unificado"),
]

SECTORS = [
    ("🏪", "Marketplace Global", "Vendedores y compradores internacionales verificados."),
    ("🏭", "ERP / Cadena", "Fabricaci&oacute;n, facturaci&oacute;n, inventario y aduana."),
    ("🎓", "Universidad", "Investigadores, publicaciones DOI y perfiles ISCO-08."),
    ("🏦", "FinTech", "KYC automatizado en milisegundos para onboarding."),
    ("🚚", "Logística 3PL", "Rastreo GPS de flotas y validaci&oacute;n de entregas."),
    ("🏛", "Gobierno / Aduana", "Cumplimiento regulatorio y control de fronteras."),
]

def _card_html(num, icon, title, desc, tags):
    return f"""
    <div class="card" onclick="openModal('{num}','{icon}','{title}','{desc}','{tags}')">
      <div class="card-head"><span class="card-num">{num}</span><span class="card-icon">{icon}</span><span class="card-title">{title}</span></div>
      <div class="card-desc">{desc}</div>
      <div class="card-tags">&#9656; {tags}</div>
    </div>"""

def show():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', sans-serif !important; }
        .main .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer, #MainMenu, .stDeployButton { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        iframe[title="streamlit-iframe-component"] { border: none !important; }
        ::-webkit-scrollbar { display: none; }
    </style>
    """, unsafe_allow_html=True)

    cards_html = ""
    for i in range(0, 8, 4):
        row = "".join(_card_html(*m) for m in MODULES[i:i+4])
        cards_html += f'<div class="grid-4">{row}</div>'

    sectors_html = "".join(
        f'<div class="sec"><div class="sec-icon">{s[0]}</div><div class="sec-title">{s[1]}</div><div class="sec-desc">{s[2]}</div></div>'
        for s in SECTORS
    )

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif;}}
body{{background:#070b24;color:white;overflow-x:hidden;}}
.bg{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;overflow:hidden;}}
.bg img{{width:100%;height:100%;object-fit:cover;filter:blur(4px) brightness(0.5);}}
.overlay{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1;background:linear-gradient(180deg,rgba(7,11,36,0.96) 0%,rgba(7,11,36,0.75) 40%,rgba(7,11,36,0.93) 100%);}}
.content{{position:relative;z-index:2;padding:12px 24px 20px;max-width:1280px;margin:0 auto;min-height:100vh;}}
.header{{display:flex;align-items:center;gap:14px;margin-bottom:4px;}}
.header img{{height:48px;filter:drop-shadow(0 0 20px rgba(0,212,255,0.2));}}
.header span{{color:#00d4ff;font-weight:700;font-size:14px;letter-spacing:4px;text-shadow:0 0 20px rgba(0,212,255,0.3);}}
.hero{{text-align:center;margin:6px auto 10px;max-width:750px;}}
.hero .tag{{color:#00d4ff;font-weight:600;font-size:13px;letter-spacing:4px;text-transform:uppercase;margin-bottom:2px;text-shadow:0 0 30px rgba(0,212,255,0.2);}}
.hero h1{{color:white;font-weight:900;font-size:2.8rem;line-height:1.05;text-shadow:0 2px 40px rgba(0,0,0,0.3);}}
.hero h2{{background:linear-gradient(135deg,#00d4ff,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;font-size:1.5rem;margin-bottom:4px;}}
.hero p{{color:#cbd5e1;font-size:15px;line-height:1.5;text-shadow:0 1px 20px rgba(0,0,0,0.2);}}
.section-label{{display:flex;align-items:center;gap:8px;margin-bottom:6px;}}
.section-label span{{color:#64748b;font-size:11px;font-weight:600;letter-spacing:3px;text-transform:uppercase;}}
.section-label hr{{flex:1;height:1px;border:none;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);}}
.grid-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px;}}
.card{{background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:12px 14px;box-shadow:0 8px 32px rgba(0,0,0,0.2);cursor:pointer;transition:all 0.2s;}}
.card:hover{{border-color:#00d4ff;transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,212,255,0.15);}}
.card-head{{display:flex;align-items:center;gap:8px;margin-bottom:6px;}}
.card-num{{font-size:18px;color:#00d4ff;font-weight:800;}}
.card-icon{{font-size:20px;}}
.card-title{{color:white;font-weight:700;font-size:14px;}}
.card-desc{{color:#94a3b8;font-size:13px;line-height:1.5;margin-bottom:6px;}}
.card-tags{{color:#475569;font-size:11px;}}
.card-tags span{{color:#00d4ff;}}
.grid-sec{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:8px;}}
.sec{{background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:8px 10px;text-align:center;}}
.sec-icon{{font-size:22px;margin-bottom:2px;}}
.sec-title{{color:white;font-size:13px;font-weight:700;}}
.sec-desc{{color:#94a3b8;font-size:11px;line-height:1.3;}}
.summary{{text-align:center;margin:0 auto 8px;max-width:700px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:8px 16px;}}
.summary p{{color:#94a3b8;font-size:12px;line-height:1.4;margin:0;}}
.summary .hl{{color:#00d4ff;}}
.footer{{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:12px;}}
.footer span{{color:#475569;font-size:11px;}}
.footer .d{{color:#00d4ff;}}
.footer .p{{color:#a855f7;}}

.btn-wrap{{text-align:center;margin:0 auto 0;}}
.btn-access{{background:linear-gradient(135deg,#00d4ff,#7c3aed);color:white;border:none;font-weight:800;padding:18px 48px;border-radius:60px;font-size:18px;letter-spacing:2px;box-shadow:0 8px 40px rgba(0,212,255,0.35),0 0 80px rgba(124,58,237,0.15);cursor:pointer;transition:all 0.2s;}}
.btn-access:hover{{transform:scale(1.03);box-shadow:0 12px 60px rgba(0,212,255,0.5),0 0 100px rgba(124,58,237,0.25);}}

.modal{{display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.7);z-index:999;justify-content:center;align-items:center;}}
.modal-box{{background:#0f172a;border:1px solid rgba(0,212,255,0.2);border-radius:20px;padding:28px 32px;max-width:480px;width:90%;box-shadow:0 20px 80px rgba(0,0,0,0.6);position:relative;}}
.modal-close{{position:absolute;top:12px;right:16px;color:#64748b;font-size:24px;cursor:pointer;background:none;border:none;}}
.modal-close:hover{{color:#f87171;}}
.modal-head{{display:flex;align-items:center;gap:10px;margin-bottom:12px;}}
.modal-num{{font-size:24px;color:#00d4ff;font-weight:800;}}
.modal-icon{{font-size:28px;}}
.modal-title{{color:white;font-weight:800;font-size:20px;}}
.modal-desc{{color:#cbd5e1;font-size:15px;line-height:1.6;margin-bottom:14px;}}
.modal-tags{{color:#94a3b8;font-size:13px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);}}
.modal-tags span{{color:#00d4ff;}}

@media(max-width:900px){{.grid-4{{grid-template-columns:repeat(2,1fr);}}.grid-sec{{grid-template-columns:repeat(3,1fr);}}}}
@media(max-width:500px){{.grid-4{{grid-template-columns:1fr;}}.grid-sec{{grid-template-columns:repeat(2,1fr);}}.hero h1{{font-size:1.8rem;}}.hero h2{{font-size:1.1rem;}}.hero p{{font-size:13px;}}.card-desc{{font-size:12px;}}}}
</style>
</head>
<body>
<div class="bg"><img src="{IMG_FONDO}"></div>
<div class="overlay"></div>
<div class="content">
<div class="header"><img src="{IMG_LOGO}"><span>TRADETECH SOLUTIONS</span></div>
<div class="hero">
<div class="tag">Sistema de Identidad Digital y Logística Internacional</div>
<h1>Pasaporte Digital</h1>
<h2>de Comercio Exterior</h2>
<p>El <strong style="color:white;">&ldquo;documento de identidad universal&rdquo;</strong> para usuarios y empresas en el ecosistema digital global. <strong style="color:#00d4ff;">11 tablas &middot; 6 vistas &middot; 8 m&oacute;dulos</strong> en una plataforma integrada.</p>
</div>
<div class="section-label"><span>M&oacute;dulos del Sistema</span><hr></div>
{cards_html}
<div class="section-label"><span>Sectores Objetivo</span><hr></div>
<div class="grid-sec">{sectors_html}</div>
<div class="summary"><p><strong>En resumen:</strong> Cualquier sistema &mdash;ERP, FinTech, aduana, universidad&mdash; puede consultar el perfil completo de un usuario <strong class="hl">(identidad, logística, finanzas, ciencia, telemetría)</strong> en milisegundos desde una sola plataforma.</p></div>
<div class="btn-wrap"><button class="btn-access" onclick="enter()">🌐  ACCEDER AL SISTEMA</button></div>
<div class="footer">
<span><span class="d">&#10022;</span> ISO 639-1 &middot; BCP47 &middot; E.164</span>
<span><span class="p">&#10022;</span> HS Code &middot; Incoterms 2020 &middot; ISCO-08</span>
<span><span class="d">&#10022;</span> UN/CEFACT &middot; SWIFT &middot; IBAN &middot; CIIU</span>
</div>
</div>

<div id="modal" class="modal" onclick="closeModal(event)">
  <div class="modal-box" id="modalBox">
    <button class="modal-close" onclick="closeModal(event)">&times;</button>
    <div class="modal-head">
      <span class="modal-num" id="mNum"></span>
      <span class="modal-icon" id="mIcon"></span>
      <span class="modal-title" id="mTitle"></span>
    </div>
    <div class="modal-desc" id="mDesc"></div>
    <div class="modal-tags"><span>&#9656;</span> Tablas: <span id="mTags"></span></div>
  </div>
</div>

<script>
function openModal(num, icon, title, desc, tags) {{
  document.getElementById('mNum').textContent = num;
  document.getElementById('mIcon').textContent = icon;
  document.getElementById('mTitle').textContent = title;
  document.getElementById('mDesc').textContent = desc;
  document.getElementById('mTags').textContent = tags;
  document.getElementById('modal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}}
function closeModal(e) {{
  if (e.target === e.currentTarget || e.target.classList.contains('modal-close')) {{
    document.getElementById('modal').style.display = 'none';
    document.body.style.overflow = '';
  }}
}}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') {{
    document.getElementById('modal').style.display = 'none';
    document.body.style.overflow = '';
  }}
}});
function enter() {{
  try {{
    window.parent.location.href = window.parent.location.href.split('?')[0] + '?enter=1';
  }} catch(e) {{
    window.location.href = window.location.href.split('?')[0] + '?enter=1';
  }}
}}
</script>
</body>
</html>"""

    components.html(html, height=860, scrolling=False)

    qp = st.query_params
    if "enter" in qp and qp["enter"] == "1":
        st.session_state.landing = False
        st.query_params.clear()
        st.rerun()
