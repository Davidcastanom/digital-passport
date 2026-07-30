import streamlit as st
import streamlit.components.v1 as components

IMG_FONDO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366977/fondo_biruor.png"
IMG_LOGO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366976/logo_2_ne0zk5.png"

def _card(num, icon, title, desc, tags):
    return f"""
    <div class="mod-card">
        <div class="mod-head"><span class="mod-num">{num}</span><span class="mod-icon">{icon}</span><span class="mod-title">{title}</span></div>
        <div class="mod-desc">{desc}</div>
        <div class="mod-tags"><span class="arr">▸</span> {tags}</div>
    </div>"""

def _sec(icon, title, desc):
    return f"""
    <div class="sec-card">
        <div class="sec-icon">{icon}</div>
        <div class="sec-title">{title}</div>
        <div class="sec-desc">{desc}</div>
    </div>"""

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
    ("🏭", "ERP / Cadena", "Fabricación, facturación, inventario y aduana."),
    ("🎓", "Universidad", "Investigadores, publicaciones DOI y perfiles ISCO-08."),
    ("🏦", "FinTech", "KYC automatizado en milisegundos para onboarding."),
    ("🚚", "Logística 3PL", "Rastreo GPS de flotas y validación de entregas."),
    ("🏛", "Gobierno / Aduana", "Cumplimiento regulatorio y control de fronteras."),
]

HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif;}}
body{{background:#070b24;min-height:100vh;overflow-x:hidden;}}
.bg{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;}}
.bg img{{width:100%;height:100%;object-fit:cover;}}
.bg-overlay{{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1;background:linear-gradient(180deg,rgba(7,11,36,0.92) 0%,rgba(7,11,36,0.6) 40%,rgba(7,11,36,0.88) 100%);}}
.content{{position:relative;z-index:2;max-width:1200px;margin:0 auto;padding:0.8rem 2rem;}}
.header{{display:flex;align-items:center;gap:14px;margin-bottom:0.3rem;}}
.header img{{height:48px;filter:drop-shadow(0 0 20px rgba(0,212,255,0.2));}}
.header span{{color:#00d4ff;font-weight:700;font-size:11px;letter-spacing:4px;text-shadow:0 0 20px rgba(0,212,255,0.3);}}
.hero{{text-align:center;margin:0.5rem auto 0.6rem;max-width:750px;}}
.hero .tag{{color:#00d4ff;font-weight:600;font-size:0.75rem;letter-spacing:6px;text-transform:uppercase;margin-bottom:4px;text-shadow:0 0 30px rgba(0,212,255,0.2);}}
.hero h1{{color:white;font-weight:900;font-size:3rem;line-height:1.05;text-shadow:0 2px 40px rgba(0,0,0,0.3);}}
.hero h2{{background:linear-gradient(135deg,#00d4ff,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;font-size:1.7rem;text-shadow:none;}}
.hero p{{color:#e2e8f0;font-size:0.85rem;line-height:1.5;text-shadow:0 1px 20px rgba(0,0,0,0.2);}}
.section-label{{display:flex;align-items:center;gap:8px;margin-bottom:8px;padding-left:2px;}}
.section-label span{{color:#475569;font-size:0.6rem;font-weight:600;letter-spacing:3px;text-transform:uppercase;}}
.section-label hr{{flex:1;height:1px;border:none;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);}}
.grid-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;}}
.mod-card{{background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem 0.9rem;box-shadow:0 8px 32px rgba(0,0,0,0.2);display:flex;flex-direction:column;}}
.mod-head{{display:flex;align-items:center;gap:8px;margin-bottom:4px;}}
.mod-num{{font-size:1.2rem;color:#00d4ff;font-weight:800;}}
.mod-icon{{font-size:1.2rem;}}
.mod-title{{color:white;font-weight:700;font-size:0.8rem;}}
.mod-desc{{color:#94a3b8;font-size:0.62rem;line-height:1.4;margin-bottom:4px;flex:1;}}
.mod-tags{{color:#475569;font-size:0.5rem;letter-spacing:0.3px;}}
.mod-tags .arr{{color:#00d4ff;}}
.grid-6{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:0.5rem;}}
.sec-card{{background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.7rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);}}
.sec-icon{{font-size:1.3rem;margin-bottom:2px;}}
.sec-title{{color:white;font-size:0.75rem;font-weight:700;}}
.sec-desc{{color:#94a3b8;font-size:0.55rem;line-height:1.3;}}
.summary{{text-align:center;margin:0 auto 0.5rem;max-width:700px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:0.5rem 1rem;}}
.summary p{{color:#94a3b8;font-size:0.65rem;line-height:1.4;margin:0;}}
.summary strong{{color:#e2e8f0;}}
.summary .hl{{color:#00d4ff;}}
.footer{{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:6px;}}
.footer span{{color:#475569;font-size:0.55rem;display:flex;align-items:center;gap:4px;}}
.footer .d{{color:#00d4ff;}}
.footer .p{{color:#a855f7;}}
@media(max-width:900px){{.grid-4{{grid-template-columns:repeat(2,1fr);}}.grid-6{{grid-template-columns:repeat(3,1fr);}}}}
@media(max-width:500px){{.grid-4{{grid-template-columns:1fr;}}.grid-6{{grid-template-columns:repeat(2,1fr);}}.hero h1{{font-size:2rem;}}.hero h2{{font-size:1.2rem;}}}}
</style>
</head>
<body>
<div class="bg"><img src="{IMG_FONDO}"></div>
<div class="bg-overlay"></div>
<div class="content">
<div class="header"><img src="{IMG_LOGO}"><span>TRADETECH SOLUTIONS</span></div>
<div class="hero">
<div class="tag">Sistema de Identidad Digital y Logística Internacional</div>
<h1>Pasaporte Digital</h1>
<h2>de Comercio Exterior</h2>
<p>El <strong style="color:white;">&ldquo;documento de identidad universal&rdquo;</strong> para usuarios y empresas en el ecosistema digital global. <strong style="color:#00d4ff;">11 tablas · 6 vistas · 8 módulos</strong> en una plataforma integrada.</p>
</div>
"""

r1 = "".join(_card(*m) for m in MODULES[:4])
r2 = "".join(_card(*m) for m in MODULES[4:])
HTML += f'<div class="section-label"><span>Módulos del Sistema</span><hr></div><div class="grid-4">{r1}</div><div class="grid-4">{r2}</div>'

secs = "".join(_sec(*s) for s in SECTORS)
HTML += f'<div class="section-label"><span>Sectores Objetivo</span><hr></div><div class="grid-6">{secs}</div>'

HTML += f"""
<div class="summary"><p><strong>En resumen:</strong> Cualquier sistema &mdash;ERP, FinTech, aduana, universidad&mdash; puede consultar el perfil completo de un usuario <strong class="hl">(identidad, logística, finanzas, ciencia, telemetría)</strong> en milisegundos desde una sola plataforma.</p></div>
<div class="footer">
<span><span class="d">&#10022;</span> ISO 639-1 · BCP47 · E.164</span>
<span><span class="p">&#10022;</span> HS Code · Incoterms 2020 · ISCO-08</span>
<span><span class="d">&#10022;</span> UN/CEFACT · SWIFT · IBAN · CIIU</span>
</div>
</div>
</body>
</html>"""


def show():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', sans-serif !important; }
        .stApp { background: transparent !important; }
        .main .block-container { padding: 0.2rem 0.5rem !important; max-width: 100% !important; }
        header, footer, #MainMenu, .stDeployButton { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff, #7c3aed) !important;
            color: white !important; border: none !important; font-weight: 700 !important;
            height: 60px !important; border-radius: 100px !important; font-size: 1.2rem !important;
            box-shadow: 0 8px 40px rgba(0,212,255,0.35), 0 0 80px rgba(124,58,237,0.15) !important;
            letter-spacing: 2px !important;
        }
        .stButton > button:hover { transform: scale(1.02) !important; box-shadow: 0 12px 60px rgba(0,212,255,0.5), 0 0 100px rgba(124,58,237,0.25) !important; }
        ::-webkit-scrollbar { display: none; }
    </style>
    """, unsafe_allow_html=True)

    components.html(HTML, height=640)

    if st.button("🌐  ACCEDER AL SISTEMA", use_container_width=True, type="primary"):
        st.session_state.landing = False
        st.rerun()
