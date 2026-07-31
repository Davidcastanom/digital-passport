# Pasaporte Digital

Sistema de identidad digital y logística internacional con telemetría geoespacial, Google Maps, y validación de datos en tiempo real.

## 🌐 Demo

[https://digital-passport.streamlit.app](https://digital-passport.streamlit.app)

## 📋 Requisitos

- Python 3.10+
- API Key de Google Maps (Maps JavaScript API + Directions API habilitadas)

## 🚀 Inicio rápido

### Local

```bash
# 1. Clonar
git clone https://github.com/Davidcastanom/digital-passport.git
cd digital-passport

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API Key
cp .env.example .env
# Editar .env: pegar tu MAPS_API_KEY

# 5. Ejecutar
streamlit run app/main.py
```

### Windows (sin Python)

Ejecutar `dist/PasaporteDigital.exe` (versión portable).

## 🧪 Tests

```bash
python -m pytest tests/ -v
```

## 🏗️ Estructura del proyecto

```
digital-passport/
├── app/
│   ├── main.py                 # Punto de entrada + CSS global + navegación agrupada
│   ├── views/                  # 11 vistas funcionales
│   │   ├── landing.py          # Hero + 8 módulos + modal expandible + fallback CDN
│   │   ├── dashboard.py        # Métricas + barra de progreso del pasaporte
│   │   ├── register.py         # Registro con validación de email/E.164
│   │   ├── finances.py         # IBAN validado + datos fiscales
│   │   ├── trade.py            # HS Code + Incoterms + UN/CEFACT
│   │   ├── network.py          # IPv4 + MAC validados
│   │   ├── science.py          # ISCO-08 + DOI
│   │   ├── architecture.py     # ERD dinámico, DDL, relaciones
│   │   ├── records.py          # Explorador con export CSV + JSON
│   │   ├── connection_profile.py # Perfil completo exportable a JSON
│   │   ├── telemetry.py        # Google Maps + rutas + fallback polyline
│   │   └── audit.py            # Eventos de seguridad + export JSON
│   ├── database/
│   │   ├── connection.py       # Conexión + validate_table_name() + VIEWS_LIST
│   │   ├── schema.py           # get_key_info() (PRAGMA PK/FK)
│   │   └── seed.py             # generate_beacons() + CITIES
│   ├── utils/
│   │   ├── config.py           # .env + secrets + project root detection
│   │   ├── validators.py       # 9 validadores (email, E.164, IPv4, MAC, IBAN, ISCO-08, DOI, HS Code, Incoterm)
│   │   ├── id_gen.py           # gen_id() con UUID
│   │   ├── geo.py              # haversine()
│   │   ├── ui.py               # style_keys() (PK/FK emojis)
│   │   └── helpers.py          # Shims retrocompatibles
│   └── assets/
├── tests/
│   ├── test_validators.py      # 9 validadores, casos positivos/negativos
│   ├── test_db.py              # Tablas, whitelist SQL, PK/FK reales
│   ├── test_config.py          # Resolución de rutas y .env
│   └── test_seed.py            # Generación de balizas en DB temporal
├── .streamlit/
│   └── config.toml             # Tema oscuro (#070b24 / #0f172a / #00d4ff)
├── scripts/
├── data/
├── .env                        # API Key (gitignorado)
├── .env.example
├── requirements.txt
└── README.md
```

## 🗺️ Funcionalidades

| Módulo | Descripción | Validación |
|--------|-------------|------------|
| Identidad | UUID, email, E.164, ubicación, BCP47 | Email + E.164 |
| Financiero | IBAN, SWIFT, NIT, CIIU | IBAN (formato) |
| Comercio | HS Code, Incoterms 2020, UN/CEFACT | HS Code + Incoterm |
| Red | IPv4, MAC | IPv4 + MAC |
| Ciencia | ISCO-08 (OIT), DOI | ISCO-08 + DOI |
| Telemetría | Google Maps, rutas por carretera, slider, reproducción | — |
| Auditoría | Eventos por usuario, triggers automáticos | — |
| Arquitectura | ERD dinámico, DDL, PK/FK, export CSV/JSON | — |

## 🔐 Seguridad

- API Key vía `.env` o Streamlit Secrets (nunca en código)
- `validate_table_name()` contra whitelist previene SQL injection en SQL dinámico
- Validación de formato en todos los campos de entrada (IBAN, email, IP, MAC, ISCO-08, DOI, HS Code, Incoterm)
- `_get_project_root()` con soporte para `sys.frozen` (PyInstaller) + fallback CWD
- `.gitignore` excluye `.env`, `*.bak`, `__pycache__/`

## 🎨 UX

- Tema oscuro unificado (config.toml + CSS global)
- Navegación agrupada en 3 categorías (Gestión / Datos del Perfil / Exploración)
- Selector de usuario persistente en sidebar (evita elegir 8 veces)
- Barra de progreso de completitud del pasaporte en Dashboard
- Empty states con navegación directa a registro
- Spinners en todas las operaciones de base de datos
- Tooltips contextuales en campos técnicos
- Landing page con 8 módulos, modal expandible, glassmorphism, fallback si el CDN falla

## 📦 Despliegue

Ver `docs/DEPLOY.md`.

Para Streamlit Cloud: configurar `MAPS_API_KEY` en **Secrets** (Settings → Secrets).

## ⚠️ Notas de mantenimiento

- `st.components.v1.html` (landing + telemetry) y `use_container_width` (14 usos) están deprecados en Streamlit 1.60; aún funcionan, migrarlos a `st.html`/`width='stretch'` en una próxima versión.
- La DB `Esquema Relacional Global_David.db` está versionada en git para desplegar con datos en Streamlit Cloud.

## 📄 Licencia

MIT
