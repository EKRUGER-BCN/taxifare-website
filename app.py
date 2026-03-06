import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import math
import pydeck as pdk

st.set_page_config(
    page_title="NYC TaxiFare",
    page_icon="🚕",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --yellow: #F7C948;
    --yellow-dim: #c9a030;
    --yellow-glow: rgba(247,201,72,0.15);
    --black: #0a0a0f;
    --surface: #13131a;
    --surface2: #1a1a24;
    --border: #2e2e3e;
    --border-bright: #44445a;
    --text: #f0f0f0;
    --muted: #8888aa;
    --green: #39ff14;
    --red: #ff3939;
}

* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background-color: var(--black);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOPBAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--black);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: var(--yellow);
    letter-spacing: 4px;
    line-height: 1;
}
.topbar-logo span { color: #fff; }
.topbar-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
}
.topbar-ticker {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: var(--yellow);
    letter-spacing: 2px;
    overflow: hidden;
    white-space: nowrap;
    max-width: 340px;
}

/* ── SECTION LABELS ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--yellow);
    margin: 1.25rem 0 0.6rem 0;
}
.section-label:first-child { margin-top: 0; }
.section-label::before {
    content: '';
    display: block;
    width: 16px;
    height: 2px;
    background: var(--yellow);
    flex-shrink: 0;
}
.section-label::after {
    content: '';
    display: block;
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── INPUTS ── */
label, [data-testid="stWidgetLabel"] {
    color: #9999bb !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.58rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
input[type="number"], input[type="text"],
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 4px !important;
    color: var(--yellow) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}
input:focus {
    border-color: var(--yellow) !important;
    box-shadow: 0 0 0 3px var(--yellow-glow) !important;
    outline: none !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] > div > div > div {
    background: var(--border-bright) !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--yellow) !important;
    box-shadow: 0 0 12px var(--yellow-glow) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: var(--yellow) !important;
    color: #080808 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.4rem !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: var(--yellow-dim) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(247,201,72,0.3) !important;
}

/* ── COORDINATE DISPLAY ── */
.coord-display {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted);
    padding: 0.5rem 0.6rem;
    background: var(--surface2);
    border-radius: 3px;
    margin-top: 0.5rem;
    border: 1px solid var(--border);
    line-height: 1.8;
}
.coord-display span { color: var(--yellow); }

/* ── TIME CONTEXT ── */
.time-ctx {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid #222;
    border-radius: 4px;
    padding: 6px 10px;
    margin-bottom: 0.25rem;
    letter-spacing: 1px;
}

/* ── PAX DOTS ── */
.pax-dots {
    display: flex;
    gap: 6px;
    align-items: center;
    margin-top: 0.4rem;
    flex-wrap: wrap;
}
.pax-dot {
    width: 26px; height: 26px;
    border-radius: 50%;
    border: 2px solid var(--border-bright);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
}
.pax-dot.active {
    border-color: var(--yellow);
    background: var(--yellow-glow);
    box-shadow: 0 0 6px var(--yellow-glow);
}

/* ── STATS ROW ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-top: 0.75rem;
}
.stat-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.6rem;
    text-align: center;
}
.stat-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    color: var(--yellow);
    line-height: 1;
}
.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.48rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── FARE RESULT ── */
.fare-result {
    background: #08080f;
    border: 1px solid var(--yellow);
    border-radius: 6px;
    padding: 1.25rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-top: 0.75rem;
}
.fare-result::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(247,201,72,0.07) 0%, transparent 70%);
}
.fare-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
}
.fare-amount {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    color: var(--yellow);
    line-height: 1;
    text-shadow: 0 0 40px rgba(247,201,72,0.5);
    letter-spacing: 3px;
}
.fare-currency {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 3px;
}
.fare-verdict {
    display: inline-block;
    margin-top: 0.75rem;
    padding: 4px 16px;
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2px;
    font-weight: 700;
}
.verdict-cheap  { background: rgba(57,255,20,0.15);  color: var(--green);  border: 1px solid var(--green); }
.verdict-mid    { background: rgba(247,201,72,0.15); color: var(--yellow); border: 1px solid var(--yellow); }
.verdict-pricey { background: rgba(255,57,57,0.15);  color: var(--red);    border: 1px solid var(--red); }

/* ── MAP ── */
[data-testid="stDeckGlJsonChart"] {
    border-radius: 0 !important;
    border: none !important;
}

h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    color: var(--text) !important;
    letter-spacing: 2px !important;
    margin-bottom: 0.3rem !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1rem 0 !important;
}

[data-testid="stSpinner"] { color: var(--yellow) !important; }

/* left col scrollable */
[data-testid="column"]:first-child {
    background: var(--surface);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    max-height: calc(100vh - 52px);
    padding: 1.25rem 1.25rem 2rem 1.25rem !important;
}

[data-testid="column"]:last-child {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ──
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">NYC <span>TAXI</span> FARE</div>
    <div class="topbar-ticker">
        🚕 MANHATTAN→BROOKLYN FROM $12 &nbsp;·&nbsp;
        ✈️ JFK FLAT RATE $52 &nbsp;·&nbsp;
        🌃 LATE NIGHT SURCHARGE AFTER 8PM
    </div>
    <div class="topbar-badge">🟡 Live ML Estimator</div>
</div>
""", unsafe_allow_html=True)

# ── HELPER ──
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# ── TWO COLUMNS ──
left, right = st.columns([1.1, 1.9])

with left:
    # 01 — DATE & TIME
    st.markdown('<div class="section-label">01 &nbsp; When?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        pickup_date = st.date_input("Date", value=datetime.today())
    with c2:
        pickup_time = st.time_input("Time", value=datetime.now().time())

    hour = pickup_time.hour
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        time_context, ctx_color = "⚠️ Rush hour — higher fares", "#ff9900"
    elif 22 <= hour or hour <= 5:
        time_context, ctx_color = "🌙 Late night surcharge active", "#8888ff"
    else:
        time_context, ctx_color = "✅ Standard fare period", "#39ff14"

    st.markdown(f'<div class="time-ctx" style="color:{ctx_color};">{time_context}</div>', unsafe_allow_html=True)

    # 02 — COORDINATES
    st.markdown('<div class="section-label">02 &nbsp; Where to?</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.markdown("### 📍 Pickup")
        pickup_lon = st.number_input("Longitude", value=-73.985428, key="plon", format="%.6f")
        pickup_lat = st.number_input("Latitude",  value=40.748817,  key="plat", format="%.6f")
    with cb:
        st.markdown("### 🏁 Dropoff")
        dropoff_lon = st.number_input("Longitude", value=-73.960000, key="dlon", format="%.6f")
        dropoff_lat = st.number_input("Latitude",  value=40.760000,  key="dlat", format="%.6f")

    distance_mi = haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
    est_mins = int(distance_mi * 3.5 + 5)

    st.markdown(f"""
<div class="coord-display">
    📍 <span>{pickup_lat:.4f}°N, {abs(pickup_lon):.4f}°W</span><br>
    🏁 <span>{dropoff_lat:.4f}°N, {abs(dropoff_lon):.4f}°W</span><br>
    ~<span>{distance_mi:.1f} mi</span> &nbsp;|&nbsp; ~<span>{est_mins} min</span>
</div>
""", unsafe_allow_html=True)

    # 03 — PASSENGERS
    st.markdown('<div class="section-label">03 &nbsp; Passengers</div>', unsafe_allow_html=True)
    passenger_count = st.slider("", min_value=1, max_value=8, value=1)
    dots_html = '<div class="pax-dots">'
    for i in range(1, 9):
        cls = "pax-dot active" if i <= passenger_count else "pax-dot"
        dots_html += f'<div class="{cls}">👤</div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

    # STATS
    rough_min = round(2.50 + distance_mi * 1.75, 2)
    rough_max = round(2.50 + distance_mi * 3.20 + passenger_count * 0.5, 2)
    st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-val">{distance_mi:.1f}</div><div class="stat-lbl">Miles</div></div>
    <div class="stat-box"><div class="stat-val">~{est_mins}</div><div class="stat-lbl">Est. Mins</div></div>
    <div class="stat-box"><div class="stat-val">${rough_min}–{rough_max}</div><div class="stat-lbl">Range</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── BUTTON ──
    url = "https://taxifare.lewagon.ai/predict"
    if st.button("🚕  CALCULATE MY FARE"):
        params = {
            "pickup_datetime":   f"{pickup_date} {pickup_time}",
            "pickup_longitude":  pickup_lon,
            "pickup_latitude":   pickup_lat,
            "dropoff_longitude": dropoff_lon,
            "dropoff_latitude":  dropoff_lat,
            "passenger_count":   passenger_count,
        }
        with st.spinner("Hailing the algorithm..."):
            try:
                response = requests.get(url, params=params, timeout=10)
            except Exception as e:
                st.error(f"Connection error: {e}")
                st.stop()

        if response.status_code == 200:
            data = response.json()
            prediction = data.get("fare", data.get("fare_amount", None))
            if prediction is not None:
                st.session_state["fare"] = float(prediction)
            else:
                st.error(f"Unexpected response: {data}")
        else:
            st.error(f"API Error {response.status_code}")

    # ── FARE RESULT ──
    if "fare" in st.session_state:
        fare = st.session_state["fare"]
        if fare < 15:
            verdict_cls, verdict_txt = "verdict-cheap",  "🟢 GREAT DEAL"
        elif fare < 35:
            verdict_cls, verdict_txt = "verdict-mid",    "🟡 STANDARD FARE"
        else:
            verdict_cls, verdict_txt = "verdict-pricey", "🔴 PREMIUM RIDE"

        tip_15 = fare * 0.15
        tip_20 = fare * 0.20
        tip_25 = fare * 0.25

        st.markdown(f"""
<div class="fare-result">
    <div class="fare-label">Estimated Fare</div>
    <div class="fare-amount">${fare:.2f}</div>
    <div class="fare-currency">USD</div>
    <div><span class="fare-verdict {verdict_cls}">{verdict_txt}</span></div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:0.75rem;">Tip</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-val">${tip_15:.2f}</div><div class="stat-lbl">15%</div></div>
    <div class="stat-box"><div class="stat-val">${tip_20:.2f}</div><div class="stat-lbl">20%</div></div>
    <div class="stat-box"><div class="stat-val">${tip_25:.2f}</div><div class="stat-lbl">25%</div></div>
</div>
<div style="background:var(--surface2); border:1px solid var(--border); border-radius:4px;
     padding:0.75rem 1rem; margin-top:0.5rem; display:flex; justify-content:space-between; align-items:center;">
    <div style="font-family:'Space Mono',monospace; font-size:0.55rem; color:var(--muted); letter-spacing:2px; text-transform:uppercase;">
        Total w/ 20% tip
    </div>
    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:var(--yellow);">
        ${fare + tip_20:.2f}
    </div>
</div>
""", unsafe_allow_html=True)

# ── RIGHT: MAP ──
with right:
    arc_data = [{"sourcePosition": [pickup_lon, pickup_lat], "targetPosition": [dropoff_lon, dropoff_lat]}]
    scatter_data = [
        {"position": [pickup_lon, pickup_lat],   "color": [247, 201, 72, 220], "radius": 80, "label": "📍 Pickup"},
        {"position": [dropoff_lon, dropoff_lat], "color": [255, 80, 80, 220],  "radius": 80, "label": "🏁 Dropoff"},
    ]

    arc_layer = pdk.Layer(
        "ArcLayer", data=arc_data,
        get_source_position="sourcePosition",
        get_target_position="targetPosition",
        get_source_color=[247, 201, 72, 220],
        get_target_color=[255, 80, 80, 220],
        width_min_pixels=4, width_max_pixels=8,
        great_circle=True,
    )
    scatter_layer = pdk.Layer(
        "ScatterplotLayer", data=scatter_data,
        get_position="position",
        get_fill_color="color",
        get_radius="radius",
        radius_scale=6, radius_min_pixels=8, radius_max_pixels=20,
        pickable=True, stroked=True,
        get_line_color=[255, 255, 255, 80],
        line_width_min_pixels=2,
    )

    mid_lat = (pickup_lat + dropoff_lat) / 2
    mid_lon = (pickup_lon + dropoff_lon) / 2
    zoom = 14 if distance_mi < 1 else 13 if distance_mi < 3 else 12 if distance_mi < 8 else 11

    view_state = pdk.ViewState(
        latitude=mid_lat, longitude=mid_lon,
        zoom=zoom, pitch=45, bearing=0,
    )

    deck = pdk.Deck(
        layers=[arc_layer, scatter_layer],
        initial_view_state=view_state,
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        tooltip={"text": "{label}"},
    )

    st.pydeck_chart(deck, use_container_width=True, height=900)
