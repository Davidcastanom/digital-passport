import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
from app.database.connection import get_conn
from app.utils.config import get_api_key

def show():
    API_KEY = get_api_key()

    if "route_history" not in st.session_state:
        st.session_state.route_history = []
    if "current_coords" not in st.session_state:
        st.session_state.current_coords = []

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

    if not st.session_state.active_user_id:
        st.warning("Selecciona un usuario en la barra lateral primero.")
        if st.button("→ Registrar primer usuario"):
            st.session_state.nav_to_register = True
            st.rerun()
        return

    uid = st.session_state.active_user_id
    email = st.session_state.active_user_email

    from app.database.seed import generate_beacons

    col_gen, col_num = st.columns([1, 3])
    with col_gen:
        gen_click = st.button("🔄 Generar balizas", type="primary")
    with col_num:
        num_beacons = st.number_input("Cantidad", min_value=5, max_value=200, value=30, step=5, label_visibility="collapsed")
    if gen_click:
        if st.session_state.current_coords:
            st.session_state.route_history.append(st.session_state.current_coords)
        with st.spinner("Generando balizas GPS..."):
            conn_gen = get_conn()
            generate_beacons(conn_gen, uid, num_beacons=int(num_beacons))
            conn_gen.close()
        st.rerun()

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

    coords = [{"lat": r["latitude"], "lng": r["longitude"], "spd": r["speed_kmh"], "hdg": r["heading_deg"], "evt": r["event_type"], "ts": str(r["recorded_at"])} for _, r in df.iterrows()]
    coords_json = json.dumps(coords)
    st.session_state.current_coords = coords

    history_json = json.dumps(st.session_state.route_history)

    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin:0; padding:0; background:#0f172a; }}
            #map {{ width:100%; height:440px; }}
            .controls {{ padding:10px 12px 6px; background:#0f172a; }}
            .slider-container {{ display:flex; align-items:center; gap:12px; }}
            .slider-container input {{ flex:1; accent-color:#00d4ff; }}
            .slider-container span {{ color:#94a3b8; font-size:13px; font-family:'Segoe UI',sans-serif; min-width:80px; }}
            .metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; padding:0 12px 8px; }}
            .metric {{ background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:6px 10px; text-align:center; }}
            .metric .val {{ color:white; font-size:18px; font-weight:700; font-family:'Segoe UI',sans-serif; }}
            .metric .lbl {{ color:#64748b; font-size:10px; font-family:'Segoe UI',sans-serif; }}
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
        <div class="controls">
            <div class="slider-container">
                <span id="lblIndex">1 / 1</span>
                <input type="range" id="timeline" min="0" max="0" value="0" oninput="onSlider(this.value)">
                <span id="lblTime">-</span>
            </div>
        </div>
        <div class="metrics" id="metrics">
            <div class="metric"><div class="val" id="mSpeed">-</div><div class="lbl">Velocidad</div></div>
            <div class="metric"><div class="val" id="mHeading">-</div><div class="lbl">Dirección</div></div>
            <div class="metric"><div class="val" id="mEvent">-</div><div class="lbl">Evento</div></div>
            <div class="metric"><div class="val" id="mTime">-</div><div class="lbl">Hora</div></div>
        </div>
        <script>
        var data = {coords_json};
        var history = {history_json};
        var markerCurrent = null, infoWindow = null, map = null;
        var allMarkers = [];
        var routeRenderers = [];

        function addRoadRoute(waypoints, color, opacity, weight) {{
            if (waypoints.length < 2) return;
            var origin = waypoints[0];
            var dest = waypoints[waypoints.length - 1];
            var mids = waypoints.slice(1, -1).map(function(p) {{
                return {{ location: new google.maps.LatLng(p.lat, p.lng), stopover: false }};
            }});
            var renderer = new google.maps.DirectionsRenderer({{
                map: map, preserveViewport: true, suppressMarkers: true,
                polylineOptions: {{ strokeColor: color, strokeOpacity: opacity, strokeWeight: weight }}
            }});
            routeRenderers.push(renderer);
            new google.maps.DirectionsService().route({{
                origin: origin, destination: dest, waypoints: mids,
                travelMode: google.maps.TravelMode.DRIVING
            }}, function(result, status) {{
                if (status === google.maps.DirectionsStatus.OK) {{
                    renderer.setDirections(result);
                }} else {{
                    addPolyline(waypoints, color, 0.6, weight);
                    if (status === google.maps.DirectionsStatus.REQUEST_DENIED) {{
                        var banner = document.createElement('div');
                        banner.style.cssText = 'position:absolute;top:8px;left:50%;transform:translateX(-50%);background:#7c2d12;color:#fdba74;padding:8px 14px;border-radius:8px;font-family:sans-serif;font-size:12px;z-index:10;box-shadow:0 4px 20px rgba(0,0,0,0.5);';
                        banner.innerHTML = 'Ruta por carretera no disponible — habilita la <strong>Directions API</strong> en Google Cloud Console.';
                        banner.onclick = function() {{ window.open('https://console.cloud.google.com/apis/library/directions-backend.googleapis.com', '_blank'); }};
                        banner.style.cursor = 'pointer';
                        document.getElementById('map').parentElement.appendChild(banner);
                    }}
                }}
            }});
        }}

        function addPolyline(pts, color, opacity, weight) {{
            if (pts.length < 2) return;
            var path = pts.map(function(p) {{ return {{ lat: p.lat, lng: p.lng }}; }});
            new google.maps.Polyline({{
                path: path, map: map,
                strokeColor: color, strokeOpacity: opacity, strokeWeight: weight
            }});
        }}

        function updateView(idx) {{
            if (!data || data.length === 0) return;
            var p = data[idx];
            document.getElementById('lblIndex').textContent = (idx+1) + ' / ' + data.length;
            document.getElementById('lblTime').textContent = p.ts ? p.ts.slice(-8) : '-';
            document.getElementById('mSpeed').textContent = p.spd.toFixed(0) + ' km/h';
            document.getElementById('mHeading').textContent = (p.hdg || 0).toFixed(0) + '°';
            document.getElementById('mEvent').textContent = p.evt ? p.evt.replace(/_/g,' ') : 'gps fix';
            document.getElementById('mTime').textContent = p.ts ? p.ts.slice(-8) : '-';

            if (markerCurrent) markerCurrent.setMap(null);
            if (infoWindow) infoWindow.close();
            markerCurrent = new google.maps.Marker({{
                position: {{ lat: p.lat, lng: p.lng }}, map: map,
                icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 10, fillColor: "#a855f7", fillOpacity: 1, strokeColor: "#ffffff", strokeWeight: 2 }}
            }});
            infoWindow = new google.maps.InfoWindow({{
                content: '<div class="info-box"><strong>📍 Punto ' + (idx+1) + ' / ' + data.length + '</strong><br>🚗 Velocidad: <strong>' + p.spd + ' km/h</strong><br>🕐 ' + (p.ts || '-') + '</div>',
                position: {{ lat: p.lat, lng: p.lng }}
            }});
            infoWindow.open(map);
        }}

        function onSlider(val) {{
            var idx = parseInt(val);
            updateView(idx);
        }}

        function initMap() {{
            if (typeof google === 'undefined' || !google.maps) {{
                document.getElementById('map').innerHTML = '<div style="padding:40px;text-align:center;color:#f87171;font-family:sans-serif;"><h3>❌ Google Maps no pudo cargarse</h3><p>Verifica la API Key</p></div>';
                return;
            }}
            if (!data || data.length === 0) return;

            document.getElementById('timeline').max = data.length - 1;
            document.getElementById('lblIndex').textContent = '1 / ' + data.length;

            var bounds = new google.maps.LatLngBounds();
            map = new google.maps.Map(document.getElementById('map'), {{
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
                allMarkers.push(new google.maps.Marker({{
                    position: {{ lat: p.lat, lng: p.lng }}, map: map,
                    icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: size, fillColor: color, fillOpacity: 0.7, strokeColor: '#ffffff', strokeWeight: 1 }},
                    title: (i+1) + '. ' + p.spd + ' km/h'
                }}));
                bounds.extend(new google.maps.LatLng(p.lat, p.lng));
            }});

            new google.maps.Marker({{
                position: {{ lat: data[0].lat, lng: data[0].lng }}, map: map,
                icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#34d399", fillOpacity: 1, strokeColor: "#fff", strokeWeight: 2 }}, title: "Inicio"
            }});
            if (data.length > 1) {{
                new google.maps.Marker({{
                    position: {{ lat: data[data.length-1].lat, lng: data[data.length-1].lng }}, map: map,
                    icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#f87171", fillOpacity: 1, strokeColor: "#fff", strokeWeight: 2 }}, title: "Fin"
                }});
            }}

            map.fitBounds(bounds);
            updateView(0);

            // Historical routes — dim polylines (no Directions API to save quota)
            var numHistory = history.length;
            history.forEach(function(route, i) {{
                var opacity = 0.15 + (i / numHistory) * 0.25;
                addPolyline(route, '#00d4ff', opacity, 2);
            }});

            // Current route — road route via Directions API with waypoints
            addRoadRoute(data, '#00d4ff', 1.0, 4);
        }}
        </script>
        <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initMap&loading=async" async defer></script>
    </body>
    </html>
    """
    components.html(map_html, height=580)

    with st.expander("📊 Ver tabla de balizas"):
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            st.download_button("📦 Descargar JSON", df.to_json(orient="records").encode("utf-8"), "telemetria.json", "application/json")
