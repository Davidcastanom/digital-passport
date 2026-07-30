# Telemetriamaps

Sistema de identidad digital y logística internacional con telemetría geoespacial y Google Maps.

## 🌐 Demo

Próximamente en Streamlit Community Cloud.

## 📋 Requisitos

- Python 3.10+
- API Key de Google Maps (Maps JavaScript API habilitada)

## 🚀 Inicio rápido

### Local

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/telemetriamaps.git
cd telemetriamaps

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
# O doble clic en INICIAR.bat
```

### Windows (sin Python)

Ejecutar `dist/PasaporteDigital.exe` (versión portable, requiere antivirus exception).

## 🏗️ Estructura del proyecto

```
telemetriamaps/
├── app/
│   ├── main.py              # Punto de entrada
│   ├── views/               # Páginas de la app
│   │   ├── landing.py
│   │   ├── dashboard.py
│   │   ├── telemetry.py     # Mapa + Google Maps
│   │   └── ...              # 11 vistas en total
│   ├── database/            # Capa de datos
│   │   └── connection.py
│   ├── utils/               # Utilidades
│   │   ├── config.py        # .env + secrets
│   │   └── helpers.py
│   └── assets/              # CSS / JS estáticos
├── scripts/                 # Utilidades CLI
├── data/                    # Base de datos SQLite
├── .env                     # API Key (gitignorado)
├── .env.example             # Template
├── requirements.txt
└── README.md
```

## 🗺️ Funcionalidades principales

| Módulo | Descripción |
|---|---|
| Identidad | Registro unificado con UUID, email, ubicación e idioma |
| Financiero | IBAN, SWIFT, NIT, código CIIU |
| Comercio | HS Code, Incoterms, UN/CEFACT |
| Red | IPv4, MAC, geolocalización |
| Ciencia | ISCO-08, DOI |
| Telemetría | Google Maps, rutas, timeline, reproducción |
| Auditoría | Eventos por usuario, triggers automáticos |

## 🔐 Seguridad

- API Key vía `.env` (nunca en el código)
- `.gitignore` excluye `.env` y `*.db`
- Para Streamlit Cloud: usar **Secrets** (no `.env`)

## 📦 Despliegue

Ver `docs/DEPLOY.md`.

## 📄 Licencia

MIT
