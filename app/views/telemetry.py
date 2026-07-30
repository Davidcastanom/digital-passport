import streamlit as st
import pandas as pd
import json
import math
import time
import streamlit.components.v1 as components
from datetime import datetime
from app.database.connection import get_conn
from app.utils.config import get_api_key
from app.utils.helpers import haversine

def show():
    API_KEY = get_api_key()

    col_titulo, col_help = st.columns([0.92, 0.08])
    with col_titulo:
        st.title("Telemetría y Mapas en Tiempo Real")
        st.markdown("Visualiza rutas, patrones de movimiento y tiempos de permanencia con Google Maps.")
    with col_help:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        with st.popover("❔", use_container_width=True):
            st.markdown("""
            ### 📡 ¿Qué es Telemetría?
            Cada **baliza** es una foto del usuario en un instante: `{timestamp, lat, lon, velocidad, rumbo}`.
            Una secuencia de balizas forma una **ruta**.
            ---
            ### 🗺️ El Mapa
            | Elemento | Significado |
            |---|---|
            | 🟣 Círculo | **Punto actual** del slider |
            | 🔵 Línea | **Ruta por carretera** |
            | 🟢 Marcador | **Inicio** del trayecto |
            | 🔴 Marcador | **Fin** del trayecto |
            | 💬 Ventana | Velocidad y hora del punto |
            ---
            ### ⏱️ Línea de Tiempo
            Mueve el slider para **viajar en el tiempo**: el mapa se centra en cada punto histórico.
            ---
            ### ▶️ Reproducir Ruta
            Recorre todos los puntos actualizando el slider cada 0.3s.
            """)

    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()

    if users_df.empty:
        st.warning("No hay usuarios registrados.")
        return

    user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
    email = st.selectbox("Selecciona un usuario", options=list(user_options.keys()), key="telemetry_user")
    uid = user_options[email]

    conn = get_conn()
    df = pd.read_sql("""
        SELECT latitude, longitude, speed_kmh, heading_deg, event_type, recorded_at
        FROM telemetry_log WHERE user_id = ?
        ORDER BY recorded_at
    """, conn, params=[uid])
    conn.close()

    if df.empty:
        st.warning("Este usuario no tiene datos de telemetría.")
        return

    idx = st.slider("Línea de tiempo", 0, len(df) - 1, len(df) - 1, key="tl_idx")
    punto = df.iloc[idx]

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Velocidad", f"{punto['speed_kmh']:.0f} km/h")
    with col2: st.metric("Dirección", f"{punto['heading_deg']:.0f}°")
    with col3: st.metric("Evento", punto["event_type"].replace("_", " ").title())
    with col4: st.metric("Hora", punto["recorded_at"][-8:] if punto["recorded_at"] else "-")

    dist_total = sum(haversine(df.iloc[i-1]["latitude"], df.iloc[i-1]["longitude"],
                                df.iloc[i]["latitude"], df.iloc[i]["longitude"])
                     for i in range(1, len(df)))
    avg_speed = df["speed_kmh"].mean()
    total_time = "—"
    if len(df) >= 2 and df.iloc[0]["recorded_at"] and df.iloc[-1]["recorded_at"]:
        t0 = datetime.fromisoformat(df.iloc[0]["recorded_at"])
        t1 = datetime.fromisoformat(df.iloc[-1]["recorded_at"])
        total_time = str(t1 - t0).split(".")[0]

    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Distancia total", f"{dist_total:.1f} km")
    mcol2.metric("Velocidad media", f"{avg_speed:.0f} km/h")
    mcol3.metric("Duración", total_time)

    coords_json = json.dumps([{"lat": r["latitude"], "lng": r["longitude"], "spd": r["speed_kmh"], "ts": str(r["recorded_at"])} for _, r in df.iterrows()])

    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin:0; padding:0; }}
            #map {{ width:100%; height:550px; }}
            .info-box {{
                background: rgba(7,11,36,0.92); color: white;
                padding: 10px 16px; border-radius: 8px;
                font-family: 'Segoe UI', sans-serif; font-size: 13px;
                border-left: 3px solid #00d4ff;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                max-width: 280px;
            }}
            .info-box strong {{ color: #00d4ff; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
        var telemetryData = {coords_json};
        var currentIndex = {idx};
        function initMap() {{
            if (typeof google === 'undefined' || !google.maps) {{
                document.getElementById('map').innerHTML = '<div style="padding:40px;text-align:center;color:#f87171;font-family:sans-serif;"><h3>❌ Google Maps no pudo cargarse</h3><p>Verifica la API Key en .env</p></div>';
                return;
            }}
            var data = telemetryData;
            var idx = currentIndex;
            if (!data || data.length === 0) return;

            var bounds = new google.maps.LatLngBounds();
            var map = new google.maps.Map(document.getElementById('map'), {{
                mapTypeId: 'roadmap',
                styles: [
                    {{ "elementType": "geometry", "stylers": [{{ "color": "#242f3e" }}] }},
                    {{ "elementType": "labels.text.stroke", "stylers": [{{ "color": "#242f3e" }}] }},
                    {{ "elementType": "labels.text.fill", "stylers": [{{ "color": "#746855" }}] }},
                    {{ "featureType": "road", "elementType": "geometry", "stylers": [{{ "color": "#38414e" }}] }},
                    {{ "featureType": "water", "elementType": "geometry", "stylers": [{{ "color": "#17263c" }}] }},
                    {{ "featureType": "road", "elementType": "labels.text.fill", "stylers": [{{ "color": "#9ca5b3" }}] }}
                ]
            }});

            data.forEach(function(p, i) {{
                var size = Math.max(3, Math.min(8, p.spd / 15));
                var color = p.spd > 50 ? '#00d4ff' : (p.spd > 10 ? '#fbbf24' : '#ef4444');
                new google.maps.Marker({{
                    position: {{ lat: p.lat, lng: p.lng }},
                    map: map,
                    icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: size, fillColor: color, fillOpacity: 0.7, strokeColor: '#ffffff', strokeWeight: 1 }},
                    title: (i+1) + '. ' + p.spd + ' km/h'
                }});
            }});

            new google.maps.Marker({{
                position: {{ lat: data[idx].lat, lng: data[idx].lng }},
                map: map,
                title: 'Vel: ' + data[idx].spd + ' km/h',
                icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 10, fillColor: "#a855f7", fillOpacity: 1, strokeColor: "#ffffff", strokeWeight: 2 }}
            }});

            var info = new google.maps.InfoWindow({{
                content: '<div class="info-box"><strong>📍 Punto ' + (idx + 1) + ' / ' + data.length + '</strong><br>🚗 Velocidad: <strong>' + data[idx].spd + ' km/h</strong><br>🕐 ' + (data[idx].ts || '-') + '</div>',
                position: {{ lat: data[idx].lat, lng: data[idx].lng }}
            }});
            info.open(map);

            new google.maps.Marker({{
                position: {{ lat: data[0].lat, lng: data[0].lng }},
                map: map, icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#34d399", fillOpacity: 1, strokeColor: "#fff", strokeWeight: 2 }},
                title: "Inicio"
            }});
            if (data.length > 1) {{
                new google.maps.Marker({{
                    position: {{ lat: data[data.length-1].lat, lng: data[data.length-1].lng }},
                    map: map, icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#f87171", fillOpacity: 1, strokeColor: "#fff", strokeWeight: 2 }},
                    title: "Fin"
                }});
            }}

            data.forEach(function(p) {{ bounds.extend(new google.maps.LatLng(p.lat, p.lng)); }});
            map.fitBounds(bounds);

            var directionsService = new google.maps.DirectionsService();
            var directionsRenderer = new google.maps.DirectionsRenderer({{
                map: map, polylineOptions: {{ strokeColor: "#00d4ff", strokeOpacity: 0.9, strokeWeight: 4 }},
                suppressMarkers: true, preserveViewport: true
            }});
            directionsService.route({{
                origin: {{ lat: data[0].lat, lng: data[0].lng }},
                destination: {{ lat: data[data.length-1].lat, lng: data[data.length-1].lng }},
                travelMode: google.maps.TravelMode.DRIVING
            }}, function(result, status) {{
                if (status === google.maps.DirectionsStatus.OK) {{
                    directionsRenderer.setDirections(result);
                    var leg = document.createElement('div');
                    leg.innerHTML = '<div style="background:rgba(7,11,36,0.9);color:white;padding:6px 12px;border-radius:6px;font-family:sans-serif;font-size:12px;border-left:3px solid #00d4ff;">🛣️ Ruta por carretera</div>';
                    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(leg);
                }}
            }});
            var leg2 = document.createElement('div');
            leg2.innerHTML = '<div style="background:rgba(7,11,36,0.9);color:white;padding:6px 12px;border-radius:6px;font-family:sans-serif;font-size:12px;margin-top:4px;border-left:3px solid #00d4ff;">⚪ Balizas (tamaño = velocidad)</div>';
            map.controls[google.maps.ControlPosition.TOP_RIGHT].push(leg2);
        }}
        </script>
        <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initMap" async defer></script>
    </body>
    </html>
    """
    components.html(map_html, height=570)

    with st.expander("📊 Ver tabla de balizas"):
        st.dataframe(df, use_container_width=True)

    if st.button("▶ Reproducir ruta"):
        placeholder = st.empty()
        for i in range(len(df)):
            st.session_state.tl_idx = i
            placeholder.info(f"Punto {i+1}/{len(df)} — {df.iloc[i]['speed_kmh']:.0f} km/h")
            st.rerun()
            time.sleep(0.3)
