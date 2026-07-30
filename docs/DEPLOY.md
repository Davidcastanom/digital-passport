# Guía de despliegue — Streamlit Community Cloud

Gratuito, HTTPS incluido, despliegue automático desde GitHub.

---

## 1. Subir a GitHub

```bash
# En la carpeta del proyecto:
git init
git add .
git commit -m "MVP Telemetriamaps"
```

Crear un repo en https://github.com/new (público o privado)

```bash
git remote add origin https://github.com/tu-usuario/telemetriamaps.git
git branch -M main
git push -u origin main
```

> ⚠️ Verifica que `.env` NO esté en `git add` (debe estar en `.gitignore`)

---

## 2. Configurar en Streamlit Cloud

1. Ir a https://streamlit.io/cloud
2. Iniciar sesión con tu cuenta de GitHub
3. Click **"New app"**
4. Elegir: `tu-usuario/telemetriamaps`
5. Branch: `main`
6. Main file: `app/main.py`
7. Click **"Deploy"**

---

## 3. Configurar Secrets (API Key)

1. En la app ya desplegada, ir a ⚙️ **Settings** → **Secrets**
2. Pegar:

```toml
MAPS_API_KEY = "AIzaSyCqtyEUSvwEZ_86jBJo1oaZTqlsz7XmUWw"
```

3. Click **Save**
4. La app se reinicia automáticamente con la key cargada

---

## 4. Restringir la API Key (seguridad)

En https://console.cloud.google.com/apis/credentials:

1. Click en tu API Key
2. En **"Restricciones de aplicación"** → `HTTP referrers (sitios web)`
3. Agregar:

```
localhost:8501
*.streamlit.app
```

4. Abajo en **"Restricciones de API"** → `Restringir clave` → solo **Maps JavaScript API**
5. Guardar

---

## 5. Actualizar la app

Cada vez que hagas:

```bash
git add .
git commit -m "mensaje"
git push
```

Streamlit Cloud detecta el cambio y redepliega solo.

---

## URL final

```
https://tu-usuario-telemetriamaps.streamlit.app
```

Comparte ese enlace con quien quieras.
