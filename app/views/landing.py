import streamlit as st

IMG_FONDO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366977/fondo_biruor.png"
IMG_LOGO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366976/logo_2_ne0zk5.png"

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

    st.markdown(f"""
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-2;">
        <img src="{IMG_FONDO}" style="width:100%;height:100%;object-fit:cover;">
    </div>
    <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;
        background:linear-gradient(180deg,rgba(7,11,36,0.92) 0%,rgba(7,11,36,0.6) 40%,rgba(7,11,36,0.88) 100%);">
    </div>
    <div style="padding:1rem 2rem;max-width:1200px;margin:0 auto;">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:0.5rem;">
            <img src="{IMG_LOGO}" style="height:52px;width:auto;filter:drop-shadow(0 0 20px rgba(0,212,255,0.2));">
            <span style="color:#00d4ff;font-weight:700;font-size:12px;letter-spacing:4px;text-shadow:0 0 20px rgba(0,212,255,0.3);">TRADETECH SOLUTIONS</span>
        </div>
        <div style="text-align:center;margin:0.8rem auto 0.8rem auto;max-width:750px;">
            <div style="color:#00d4ff;font-weight:600;font-size:0.85rem;letter-spacing:6px;text-transform:uppercase;margin-bottom:4px;text-shadow:0 0 30px rgba(0,212,255,0.2);">Sistema de Identidad Digital y Logística Internacional</div>
            <h1 style="color:white;font-weight:900;font-size:3.5rem;margin:0;line-height:1.05;text-shadow:0 2px 40px rgba(0,0,0,0.3);">Telemetriamaps</h1>
            <h2 style="background:linear-gradient(135deg,#00d4ff,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:900;font-size:2rem;margin:0 0 0.5rem 0;text-shadow:none;">de Comercio Exterior</h2>
            <p style="color:#e2e8f0;font-size:1rem;line-height:1.6;margin:0;text-shadow:0 1px 20px rgba(0,0,0,0.2);">Imagínalo como el <strong style="color:white;">"documento de identidad universal"</strong> de un usuario o empresa dentro de un ecosistema digital integrado. Resuelve <strong style="color:#00d4ff;">5 grandes problemas operativos</strong> en una sola plataforma.</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:0.8rem;">
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:1.3rem;color:#00d4ff;font-weight:800;margin-bottom:4px;text-shadow:0 0 20px rgba(0,212,255,0.2);">01</div>
                <div style="color:white;font-weight:700;font-size:0.85rem;margin-bottom:2px;">Identidad Unificada</div>
                <div style="color:#94a3b8;font-size:0.65rem;line-height:1.4;"><span style="color:#f87171;">▸</span> Datos dispersos.<br><span style="color:#34d399;">▸</span> <em style="color:#e2e8f0;">view_pasaporte_digital_usuario</em> unifica todo.</div>
            </div>
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:1.3rem;color:#00d4ff;font-weight:800;margin-bottom:4px;text-shadow:0 0 20px rgba(0,212,255,0.2);">02</div>
                <div style="color:white;font-weight:700;font-size:0.85rem;margin-bottom:2px;">Logística Internacional</div>
                <div style="color:#94a3b8;font-size:0.65rem;line-height:1.4;"><span style="color:#f87171;">▸</span> Cruce comprador-aduana.<br><span style="color:#34d399;">▸</span> HS Code + Incoterm + medidas.</div>
            </div>
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:1.3rem;color:#00d4ff;font-weight:800;margin-bottom:4px;text-shadow:0 0 20px rgba(0,212,255,0.2);">03</div>
                <div style="color:white;font-weight:700;font-size:0.85rem;margin-bottom:2px;">Ciberseguridad</div>
                <div style="color:#94a3b8;font-size:0.65rem;line-height:1.4;"><span style="color:#f87171;">▸</span> Fraudes y accesos.<br><span style="color:#34d399;">▸</span> IP + eventos + geolocalización.</div>
            </div>
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:1.3rem;color:#00d4ff;font-weight:800;margin-bottom:4px;text-shadow:0 0 20px rgba(0,212,255,0.2);">04</div>
                <div style="color:white;font-weight:700;font-size:0.85rem;margin-bottom:2px;">Compliance & KYC</div>
                <div style="color:#94a3b8;font-size:0.65rem;line-height:1.4;"><span style="color:#f87171;">▸</span> Validación fiscal.<br><span style="color:#34d399;">▸</span> NIT + CIIU + IBAN + SWIFT.</div>
            </div>
            <div style="background:linear-gradient(145deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:1.3rem;color:#00d4ff;font-weight:800;margin-bottom:4px;text-shadow:0 0 20px rgba(0,212,255,0.2);">05</div>
                <div style="color:white;font-weight:700;font-size:0.85rem;margin-bottom:2px;">Perfil Científico</div>
                <div style="color:#94a3b8;font-size:0.65rem;line-height:1.4;"><span style="color:#f87171;">▸</span> Validar credenciales.<br><span style="color:#34d399;">▸</span> ISCO-08 + DOI.</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:0.8rem;">
            <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.8rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);">
                <div style="font-size:1.5rem;margin-bottom:2px;">🏪</div>
                <div style="color:white;font-size:0.85rem;font-weight:700;">Marketplace Global</div>
                <div style="color:#94a3b8;font-size:0.6rem;line-height:1.4;">Vendedores y compradores internacionales.</div>
            </div>
            <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.8rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);">
                <div style="font-size:1.5rem;margin-bottom:2px;">🏭</div>
                <div style="color:white;font-size:0.85rem;font-weight:700;">ERP / Cadena</div>
                <div style="color:#94a3b8;font-size:0.6rem;line-height:1.4;">Fabricación, facturación y aduana.</div>
            </div>
            <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.8rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);">
                <div style="font-size:1.5rem;margin-bottom:2px;">🎓</div>
                <div style="color:white;font-size:0.85rem;font-weight:700;">Universidad</div>
                <div style="color:#94a3b8;font-size:0.6rem;line-height:1.4;">Investigadores, DOI e ISCO-08.</div>
            </div>
            <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));border:1px solid rgba(0,212,255,0.12);border-radius:14px;padding:0.8rem 1rem;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,0.15);">
                <div style="font-size:1.5rem;margin-bottom:2px;">🏦</div>
                <div style="color:white;font-size:0.85rem;font-weight:700;">FinTech</div>
                <div style="color:#94a3b8;font-size:0.6rem;line-height:1.4;">KYC automatizado en milisegundos.</div>
            </div>
        </div>
        <div style="text-align:center;margin:0 auto 0.6rem auto;max-width:700px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:0.6rem 1rem;">
            <p style="color:#94a3b8;font-size:0.7rem;line-height:1.5;margin:0;">
            💡 <strong style="color:#e2e8f0;">En resumen:</strong> Cualquier software moderno puede consultar la información de un usuario desde el frente que necesite <strong style="color:#00d4ff;">(Financiero, Logístico, Ciberseguridad o Identidad)</strong> en milisegundos.
            </p>
        </div>
        <div style="max-width:380px;margin:0 auto;">
    """, unsafe_allow_html=True)

    if st.button("🌐  ACCEDER AL SISTEMA", use_container_width=True, type="primary"):
        st.session_state.landing = False
        st.rerun()

    st.markdown(f"""
        </div>
        <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin-top:6px;">
            <span style="color:#475569;font-size:0.6rem;display:flex;align-items:center;gap:4px;"><span style="color:#00d4ff;">✦</span> ISO 639-1 · BCP47 · E.164</span>
            <span style="color:#475569;font-size:0.6rem;display:flex;align-items:center;gap:4px;"><span style="color:#a855f7;">✦</span> HS Code · Incoterms · ISCO-08</span>
            <span style="color:#475569;font-size:0.6rem;display:flex;align-items:center;gap:4px;"><span style="color:#00d4ff;">✦</span> UN/CEFACT · SWIFT · IBAN · CIIU</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
