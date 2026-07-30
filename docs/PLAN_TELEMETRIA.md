# Plan: Telemetría Geoespacial con Google Maps

## 1. Concepto — ¿Qué es telemetría aquí?

Telemetría es capturar **eventos de ubicación en el tiempo** para un usuario. Así:

```
[Usuario] ──→ { timestamp, lat, lon, velocidad, evento }
              { timestamp, lat, lon, velocidad, evento }
              { timestamp, lat, lon, velocidad, evento }  ←-historial
```

Cada punto es una **baliza** ( beacon ). Una secuencia de balizas forma una **ruta** o **patrón de movimiento**. Combinado con `user_time_events` puedes responder:

- ¿A qué hora pasó por esta zona?
- ¿Cuánto tiempo estuvo en el punto X?
- ¿Qué ruta tomó entre el origen y el destino?

---

## 2. Arquitectura

```
┌─────────────────┐       ┌───────────────────┐       ┌─────────────────┐
│  Base de Datos   │──────▶│   Streamlit App   │──────▶│  Google Maps JS │
│  SQLite          │       │   (Python)        │       │  (API Key)      │
│  telemetry_log   │       │   folium/folium   │       │  Mapa interactivo│
│  user_geolocation│       │   st.rerun()      │       │  Polilíneas     │
└─────────────────┘       └───────────────────┘       └─────────────────┘
         ▲                                                      │
         │           ┌───────────────────┐                      │
         └───────────│   Simulador/GPS   │◀─────────────────────┘
                     │   (o datos reales)  │   Clic en punto → zoom
                     └───────────────────┘   + detalle
```

---

## 3. Nueva tabla en SQLite

```sql
CREATE TABLE "telemetry_log" (
    "beacon_id"     TEXT NOT NULL PRIMARY KEY,
    "user_id"       TEXT NOT NULL REFERENCES user_identity(user_id),
    "latitude"      REAL NOT NULL,
    "longitude"     REAL NOT NULL,
    "altitude_m"    REAL,
    "speed_kmh"     REAL,
    "heading_deg"   REAL,
    "accuracy_m"    REAL,
    "event_type"    TEXT NOT NULL DEFAULT 'gps_fix',
    "recorded_at"   TEXT NOT NULL,  -- ISO 8601 UTC
    "metadata"      TEXT            -- JSON opcional (batería, red, etc.)
);
```

**Índices:**
- `idx_telemetry_user_time` ON `telemetry_log(user_id, recorded_at)`
- `idx_telemetry_timestamp` ON `telemetry_log(recorded_at)`

**Significado de `event_type`:**
| Tipo | Significado |
|---|---|
| `gps_fix` | Lectura GPS normal |
| `geofence_enter` | Entró a una zona geocercada |
| `geofence_exit` | Salió de una zona |
| `stop` | Detenido por más de N segundos |
| `route_start` | Inicio de ruta |
| `route_end` | Fin de ruta |
| `manual_checkin` | Marcación manual del usuario |

---

## 4. Vistas útiles

```sql
-- Vista: ruta completa de un usuario en orden cronológico
CREATE VIEW view_ruta_usuario AS
SELECT
    t.user_id,
    u.email,
    t.latitude,
    t.longitude,
    t.speed_kmh,
    t.heading_deg,
    t.event_type,
    t.recorded_at
FROM telemetry_log t
JOIN user_identity u ON t.user_id = u.user_id
ORDER BY t.user_id, t.recorded_at;

-- Vista: tiempos de permanencia por punto
CREATE VIEW view_geoestadisticas AS
SELECT
    user_id,
    latitude,
    longitude,
    COUNT(*) as lecturas,
    MIN(recorded_at) as primera_vez,
    MAX(recorded_at) as ultima_vez,
    ROUND(julianday(MAX(recorded_at)) - julianday(MIN(recorded_at)), 4) * 86400 as segundos_en_punto
FROM telemetry_log
GROUP BY user_id, ROUND(latitude, 4), ROUND(longitude, 4);

-- Vista: vista unificada para el mapa (combina ubicación base + telemetría)
CREATE VIEW view_mapa_pasaporte AS
SELECT
    u.user_id,
    u.email,
    g.city_name,
    g.latitude as lat_base,
    g.longitude as lon_base,
    t.latitude as lat_telemetry,
    t.longitude as lon_telemetry,
    t.speed_kmh,
    t.recorded_at,
    t.event_type
FROM user_identity u
LEFT JOIN user_geolocation g ON u.user_id = g.user_id
LEFT JOIN telemetry_log t ON u.user_id = t.user_id;
```

---

## 5. Cómo poblar datos de prueba

Estrategia: generar rutas sintéticas realistas usando coordenadas de carreteras/avenidas entre ciudades colombianas.

```
Bogotá    (4.7110, -74.0721)
Medellín  (6.2476, -75.5658)
Cali      (3.4516, -76.5319)

Ruta sintética: Bogotá → Medellín
- 5 puntos intermedios por interpolación lineal + ruido
- velocidad variable (40–110 km/h)
- timestamp cada 30 segundos simulados
- event_type alterna entre 'gps_fix' y 'stop' en puntos de interés
```

Algoritmo de interpolación:

```python
def generar_ruta(origen, destino, pasos=20):
    """Genera N puntos entre origen y destino con variación aleatoria"""
    puntos = []
    for i in range(pasos):
        frac = i / (pasos - 1)
        lat = origen[0] + (destino[0] - origen[0]) * frac + random.uniform(-0.02, 0.02)
        lon = origen[1] + (destino[1] - origen[1]) * frac + random.uniform(-0.02, 0.02)
        velocidad = random.uniform(30, 100)
        puntos.append((lat, lon, velocidad))
    return puntos
```

---

## 6. Visualización en Streamlit

### Opción A — `folium` (recomendada)

```python
import folium
from streamlit_folium import st_folium

m = folium.Map(location=[4.7110, -74.0721], zoom_start=12)

# Puntos de telemetría
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3 + row["speed_kmh"] / 20,
        color="#00d4ff" if row["event_type"] == "gps_fix" else "#a855f7",
        popup=f"{row['recorded_at']} | {row['speed_kmh']:.0f} km/h",
    ).add_to(m)

# Línea de ruta
coords = list(zip(df["latitude"], df["longitude"]))
folium.PolyLine(coords, color="#00d4ff", weight=2, opacity=0.7).add_to(m)

st_folium(m, width=1200, height=600)
```

### Opción B — `st.map` (nativa, menos control)

```python
st.map(df, latitude="latitude", longitude="longitude", size="speed_kmh", color="#00d4ff")
```

### Opción C — Overlay con Google Maps JS mediante `components.html`

Renderiza un HTML con la API de Google Maps, markers y polilíneas. Permite Street View, tráfico en tiempo real, etc.

```python
import streamlit.components.v1 as components
components.html(html_string, height=600)
```

Donde `html_string` contiene JavaScript con la API de Google Maps.

---

## 7. Interactividad: clic en historial → mapa

El flujo es:

```
Usuario selecciona email → sidebar o selectbox
    ↓
Se cargan todas las balizas del usuario ordenadas por tiempo
    ↓
Lista de eventos en un DataFrame expandible
    ↓
Usuario hace clic en una fila (st.dataframe con on_select / st.selectbox con índice)
    ↓
Mapa se centra en ese punto + muestra tooltip con datos
    ↓
Botón "▶ Reproducir ruta" anima los puntos secuencialmente
```

Implementación:

```python
# Paso 1: seleccionar usuario
email = st.selectbox("Usuario", emails)
df = get_telemetry(email)  # DataFrame con todas las balizas

# Paso 2: timeline con slider
idx = st.slider("Línea de tiempo", 0, len(df) - 1, 0)
punto = df.iloc[idx]

# Paso 3: mapa actualizado
m = folium.Map(location=[punto["latitude"], punto["longitude"]], zoom_start=14)
folium.Marker(
    location=[punto["latitude"], punto["longitude"]],
    popup=f"⏱ {punto['recorded_at']}<br>🚗 {punto['speed_kmh']:.0f} km/h",
    icon=folium.Icon(color="cyan", icon="circle")
).add_to(m)

# Paso 4: dibujar toda la ruta atrás
coords = list(zip(df.iloc[:idx+1]["latitude"], df.iloc[:idx+1]["longitude"]))
folium.PolyLine(coords, color="#00d4ff", weight=2).add_to(m)

st_folium(m, width=1200, height=500)

# Paso 5: botón reproducción
if st.button("▶ Reproducir ruta completa"):
    for i in range(len(df)):
        # Actualizar slider y rerun
        st.session_state.slider_idx = i
        time.sleep(0.5)
        st.rerun()
```

---

## 8. Cálculo de métricas de telemetría

| Métrica | Fórmula | Utilidad |
|---|---|---|
| Velocidad media | `AVG(speed_kmh)` | Saber ritmo de viaje |
| Distancia total | Suma Haversine entre puntos consecutivos | KMs recorridos |
| Tiempo en ruta | `MAX(recorded_at) - MIN(recorded_at)` | Duración del trayecto |
| Tiempo detenido | Suma de intervalos donde speed=0 | Tiempo en espera |
| Zonas frecuentes | Cluster de coordenadas (DBSCAN) | Lugares recurrentes |
| Geocerca violada | Punto fuera del polígono esperado | Alerta de seguridad |

**Fórmula Haversine para distancia entre dos coordenadas:**

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
```

---

## 9. Conexión con otros sistemas externos

| Sistema | Qué envía | Qué recibe |
|---|---|---|
| Google Maps API | Coordenadas → geocoder reverso | Dirección + lugar |
| OpenStreetMap (OSRM) | Ruta de puntos | Tiempo estimado de viaje |
| ERP (SAP, etc.) | user_id + orden | Validar que entrega llegó a destino |
| Aduanas | beacon en punto fronterizo | Liberar mercancía |
| FinTech | Geocerca de sucursal | Notificar pago cerca de sucursal |

---

## 10. Roadmap de implementación

```
Fase 1 (ahora)
  ├── Crear tabla telemetry_log
  ├── Generar datos sintéticos de ruta (30 usuarios)
  └── Mostrar mapa estático con folium

Fase 2 (interactividad)
  ├── Slider de timeline
  ├── Clic en historial → centra mapa
  └── Métricas de ruta (distancia, velocidad, tiempo)

Fase 3 (Google Maps)
  ├── API Key de Google Maps Platform
  ├── Componente HTML con JS Maps API
  ├── Street View en puntos
  └── Capa de tráfico en tiempo real

Fase 4 (tiempo real)
  ├── WebSocket o polling cada N segundos
  ├── st.rerun() automático
  └── Alerta si usuario se desvía de ruta esperada

Fase 5 (Machine Learning)
  ├── Cluster de zonas frecuentes (DBSCAN)
  ├── Predicción de próxima ubicación
  └── Detección de anomalías (coordenadas fuera de patrón)
```

---

## 11. Stack de librerías

| Librería | Para qué |
|---|---|
| `folium` + `streamlit-folium` | Mapas interactivos |
| `geopy` | Geocodificación reversa |
| `numpy` | Cálculos de rutas sintéticas |
| `scikit-learn` | Clustering DBSCAN para zonas frecuentes |
| `streamlit-components` | HTML personalizado con Google Maps JS |
| `haversine` | Cálculo de distancias |

---

## Resumen visual del flujo completo

```
         ┌────────────┐
         │  Usuario   │
         │  (email)   │
         └─────┬──────┘
               │
               ▼
     ┌─────────────────┐
     │  telemetry_log  │◄──── Simulador GPS o datos reales
     │  + user_geo     │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │   Google Maps   │
     │   API / folium   │
     └────────┬────────┘
              │
    ┌─────────▼──────────┐
    │  Mapa en Streamlit  │
    │  • Puntos           │
    │  • Ruta (polilínea) │
    │  • Tooltips         │
    │  • Timeline slider  │
    └─────────────────────┘
```

¿Quieres que empiece a implementar Fase 1?
