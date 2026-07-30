import streamlit as st

IMG_FONDO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366977/fondo_biruor.png"
IMG_LOGO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366976/logo_2_ne0zk5.png"

MODULES = [
    ("01", "🆔", "Identidad Digital", "Perfil maestro del usuario: email, teléfono E.164, ubicación base de ciudad y configuración regional BCP47.", "user_identity · user_geolocation · user_culture_language"),
    ("02", "📦", "Logística Global", "Órdenes de comercio exterior con códigos HS, Incoterms y unidades UN/CEFACT. Trazabilidad producto por producto.", "trade_supply_chain · industry_measurements"),
    ("03", "💰", "Compliance & KYC", "Validación fiscal y bancaria automatizada: NIT, CIIU, IBAN, SWIFT. Listo para integración con entidades financieras.", "user_financials · legal_economic_activity"),
    ("04", "🔐", "Ciberseguridad", "Trazabilidad de accesos con IP, MAC, auditoría de eventos y registro cronológico de cada acción del usuario.", "network_infrastructure · user_time_events · view_auditoria_seguridad"),
    ("05", "📡", "Telemetría GPS", "Rastreo satelital con Google Maps: balizas, rutas por carretera, slider temporal, velocidad y reproducción de trayectos.", "telemetry_log · Google Maps JavaScript API"),
    ("06", "🎓", "Perfil Científico", "Clasificación ISCO-08 (OIT) y publicaciones DOI para validación de credenciales profesionales y académicas.", "health_science_sectorial"),
    ("07", "🏗️", "Arquitectura Viva", "ERD generado dinámicamente, explorador de tablas/vistas con DDL, PK/FK, relaciones y exportación CSV.", "sqlite_master · PRAGMA · vistas del sistema"),
    ("08", "🔌", "Integración API", "Perfil de conexión completo exportable a JSON. Un solo endpoint virtual con todos los datos del usuario.", "connection_profile · JSON unificado"),
]

SECTORS = [
    ("🏪", "Marketplace Global", "Vendedores y compradores internacionales verificados."),
    ("🏭", "ERP / Cadena", "Fabricación, facturación, inventario y aduana."),
    ("🎓", "Universidad", "Investigadores, publicaciones DOI y perfiles ISCO-08."),
    ("🏦", "FinTech", "KYC automatizado en milisegundos para onboarding."),
    ("🚚", "Logística 3PL", "Rastreo GPS de flotas y validación de entregas."),
    ("🏛️", "Gobierno / Aduana", "Cumplimiento regulatorio y control de fronteras."),
]

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

    modules_rows = ""
    for i in range(0, 8, 4):
        row_mods = MODULES[i:i+4]
        cards = ""
        for num, icon, title, desc, tags in row_mods:
            cards += f"""
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem 0.9rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);display:flex;flex-direction:column;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="font-size:1.2rem;color:#00d4ff;font-weight:800;">{num}</span>
                    <span style="font-size:1.2rem;">{icon}</span>
                    <span style="color:white;font-weight:700;font-size:0.8rem;">{title}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.62rem;line-height:1.4;margin-bottom:4px;flex:1;">{desc}</div>
                <div style="color:#475569;font-size:0.5rem;letter-spacing:0.3px;"><span style="color:#00d4ff;">▸</span> {tags}</div>
            </div>"""
        modules_rows += f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;">{cards}</div>'

    sectors_cards = ""
    for icon, title, desc in SECTORS:
        sectors_cards += f"""
        <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.7rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);">
            <div style="font-size:1.3rem;margin-bottom:2px;">{icon}</div>
            <div style="color:white;font-size:0.75rem;font-weight:700;">{title}</div>
            <div style="color:#94a3b8;font-size:0.55rem;line-height:1.3;">{desc}</div>
        </div>"""

    st.markdown(f"""
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-2;">
        <img src="{IMG_FONDO}" style="width:100%;height:100%;object-fit:cover;">
    </div>
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
        background:linear-gradient(180deg,rgba(7,11,36,0.92) 0%,rgba(7,11,36,0.6) 40%,rgba(7,11,36,0.88) 100%);">
    </div>
    <div style="padding:0.8rem 2rem;max-width:1200px;margin:0 auto;">

        <!-- Header -->
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:0.3rem;">
            <img src="{IMG_LOGO}" style="height:48px;width:auto;filter:drop-shadow(0 0 20px rgba(0,212,255,0.2));">
            <span style="color:#00d4ff;font-weight:700;font-size:11px;letter-spacing:4px;text-shadow:0 0 20px rgba(0,212,255,0.3);">TRADETECH SOLUTIONS</span>
        </div>

        <!-- Hero -->
        <div style="text-align:center;margin:0.5rem auto 0.6rem auto;max-width:750px;">
            <div style="color:#00d4ff;font-weight:600;font-size:0.75rem;letter-spacing:6px;text-transform:uppercase;margin-bottom:4px;text-shadow:0 0 30px rgba(0,212,255,0.2);">Sistema de Identidad Digital y Logística Internacional</div>
            <h1 style="color:white;font-weight:900;font-size:3rem;margin:0;line-height:1.05;text-shadow:0 2px 40px rgba(0,0,0,0.3);">Pasaporte Digital</h1>
            <h2 style="background:linear-gradient(135deg,#00d4ff,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:900;font-size:1.7rem;margin:0 0 0.3rem 0;text-shadow:none;">de Comercio Exterior</h2>
            <p style="color:#e2e8f0;font-size:0.85rem;line-height:1.5;margin:0;text-shadow:0 1px 20px rgba(0,0,0,0.2);">El <strong style="color:white;">"documento de identidad universal"</strong> para usuarios y empresas en el ecosistema digital global. <strong style="color:#00d4ff;">11 tablas · 6 vistas · 8 módulos</strong> en una plataforma integrada.</p>
        </div>

        <!-- Módulos (8 cards en 2 filas de 4) -->
        <div style="margin-bottom:0.6rem;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;padding-left:2px;">
                <span style="color:#475569;font-size:0.6rem;font-weight:600;letter-spacing:3px;text-transform:uppercase;">Módulos del Sistema</span>
                <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);"></div>
            </div>
            {modules_rows}
        </div>

        <!-- Sectores -->
        <div style="margin-bottom:0.5rem;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;padding-left:2px;">
                <span style="color:#475569;font-size:0.6rem;font-weight:600;letter-spacing:3px;text-transform:uppercase;">Sectores Objetivo</span>
                <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);"></div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">{sectors_cards}</div>
        </div>

        <!-- Resumen -->
        <div style="text-align:center;margin:0 auto 0.5rem auto;max-width:700px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:0.5rem 1rem;">
            <p style="color:#94a3b8;font-size:0.65rem;line-height:1.4;margin:0;">
            💡 <strong style="color:#e2e8f0;">En resumen:</strong> Cualquier sistema —ERP, FinTech, aduana, universidad— puede consultar el perfil completo de un usuario <strong style="color:#00d4ff;">(identidad, logística, finanzas, ciencia, telemetría)</strong> en milisegundos desde una sola plataforma.
            </p>
        </div>

        <div style="max-width:380px;margin:0 auto;">
    """, unsafe_allow_html=True)

    if st.button("🌐  ACCEDER AL SISTEMA", use_container_width=True, type="primary"):
        st.session_state.landing = False
        st.rerun()

    st.markdown(f"""
        </div>
        <div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:6px;">
            <span style="color:#475569;font-size:0.55rem;display:flex;align-items:center;gap:4px;"><span style="color:#00d4ff;">✦</span> ISO 639-1 · BCP47 · E.164</span>
            <span style="color:#475569;font-size:0.55rem;display:flex;align-items:center;gap:4px;"><span style="color:#a855f7;">✦</span> HS Code · Incoterms 2020 · ISCO-08</span>
            <span style="color:#475569;font-size:0.55rem;display:flex;align-items:center;gap:4px;"><span style="color:#00d4ff;">✦</span> UN/CEFACT · SWIFT · IBAN · CIIU</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
