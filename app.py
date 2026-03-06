import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import math
import json
import pydeck as pdk

st.set_page_config(
    page_title="NYC TaxiFare",
    page_icon="🚕",
    layout="centered"
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
    --surface3: #20202c;
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
    padding-top: 0rem !important;
    padding-bottom: 2rem !important;
    max-width: 720px;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    background: var(--yellow);
    margin: -1rem -1rem 0 -1rem;
    padding: 3rem 2.5rem 5rem 2.5rem;
    overflow: hidden;
}

.hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,0,0,0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.12) 1px, transparent 1px);
    background-size: 30px 30px;
}

.hero-badge {
    display: inline-block;
    background: #080808;
    color: var(--yellow);
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 3px;
    padding: 4px 12px;
    border-radius: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 12vw, 7rem);
    color: #080808;
    line-height: 0.85;
    letter-spacing: 3px;
    margin: 0;
    position: relative;
    z-index: 2;
}

.hero-title span {
    color: #fff;
    -webkit-text-stroke: 2px #080808;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #333;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 1rem;
    position: relative;
    z-index: 2;
}

.hero-cab {
    position: absolute;
    right: 2rem;
    bottom: 2rem;
    font-size: 7rem;
    z-index: 2;
    filter: drop-shadow(-4px 4px 0px rgba(0,0,0,0.2));
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(-2deg); }
    50% { transform: translateY(-10px) rotate(2deg); }
}

.hero-wave {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60px;
    background: var(--black);
    clip-path: ellipse(55% 100% at 50% 100%);
    z-index: 3;
}

/* ── TICKER ── */
.ticker {
    background: #080808;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 8px 0;
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 2rem;
}
.ticker-inner {
    display: inline-block;
    animation: ticker 20s linear infinite;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--yellow);
    letter-spacing: 2px;
}
@keyframes ticker {
    0% { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

/* ── SECTION LABELS ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--yellow);
    margin: 2rem 0 0.75rem 0;
}
.section-label::before {
    content: '';
    display: block;
    width: 24px;
    height: 2px;
    background: var(--yellow);
}
.section-label::after {
    content: '';
    display: block;
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── CARDS ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--yellow), transparent);
}

/* ── INPUTS ── */
label, .stSlider label, [data-testid="stWidgetLabel"] {
    color: #9999bb !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
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
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
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
    font-size: 1.6rem !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.4s;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    background: var(--yellow-dim) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(247,201,72,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── HEADINGS ── */
h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    color: var(--text) !important;
    letter-spacing: 2px !important;
    margin-bottom: 0.5rem !important;
}

/* ── MAP ── */
[data-testid="stDeckGlJsonChart"], iframe, [data-testid="stMap"] {
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

/* ── FARE RESULT ── */
.fare-result {
    background: #08080f;
    border: 1px solid var(--yellow);
    border-radius: 6px;
    padding: 2rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.4s ease;
}
.fare-result::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(247,201,72,0.07) 0%, transparent 70%);
}
.fare-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.fare-amount {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: var(--yellow);
    line-height: 1;
    text-shadow: 0 0 40px rgba(247,201,72,0.5);
    letter-spacing: 3px;
}
.fare-currency {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.25rem;
    letter-spacing: 3px;
}
.fare-verdict {
    display: inline-block;
    margin-top: 1.25rem;
    padding: 6px 20px;
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    font-weight: 700;
}
.verdict-cheap { background: rgba(57,255,20,0.15); color: var(--green); border: 1px solid var(--green); }
.verdict-mid   { background: rgba(247,201,72,0.15); color: var(--yellow); border: 1px solid var(--yellow); }
.verdict-pricey { background: rgba(255,57,57,0.15); color: var(--red); border: 1px solid var(--red); }

/* ── STATS ROW ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-top: 1rem;
}
.stat-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.75rem;
    text-align: center;
}
.stat-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--yellow);
    line-height: 1;
}
.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.5rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── PASSENGER DOTS ── */
.pax-dots {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-top: 0.5rem;
}
.pax-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    border: 2px solid var(--border-bright);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    transition: all 0.2s;
}
.pax-dot.active {
    border-color: var(--yellow);
    background: var(--yellow-glow);
    box-shadow: 0 0 8px var(--yellow-glow);
}

/* ── COORDINATE DISPLAY ── */
.coord-display {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    padding: 0.5rem;
    background: var(--surface2);
    border-radius: 3px;
    margin-top: 0.5rem;
    border: 1px solid var(--border);
}
.coord-display span { color: var(--yellow); }

/* ── ANIMATIONS ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.pulse { animation: pulse 1.5s ease-in-out infinite; }

/* ── FOOTER ── */
.nyc-footer {
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: var(--muted);
    letter-spacing: 2px;
    padding: 2rem 0 1rem 0;
    text-transform: uppercase;
}
.nyc-footer a { color: var(--yellow); text-decoration: none; }

/* ── SPINNER ── */
[data-testid="stSpinner"] { color: var(--yellow) !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero-wrap">
    <div class="hero-grid"></div>
    <div class="hero-badge">🟡 Live Fare Estimator</div>
    <div class="hero-title">NYC<br><span>TAXI</span><br>FARE</div>
    <div class="hero-sub">// Predict your ride · New York City · Real-time ML model</div>
    <div class="hero-cab">🚕</div>
    <div class="hero-wave"></div>
</div>
""", unsafe_allow_html=True)

# ── TICKER ──
st.markdown("""
<div class="ticker">
    <div class="ticker-inner">
        🚕 MANHATTAN → BROOKLYN · FROM $12 &nbsp;&nbsp;&nbsp;
        🌃 LATE NIGHT SURCHARGE ACTIVE AFTER 8PM &nbsp;&nbsp;&nbsp;
        ✈️ JFK FLAT RATE: $52 &nbsp;&nbsp;&nbsp;
        🏙️ RUSH HOUR: MON–FRI 4PM–8PM &nbsp;&nbsp;&nbsp;
        💳 CREDIT CARD ACCEPTED IN ALL CABS &nbsp;&nbsp;&nbsp;
        🚦 BASE FARE: $3.00 + $0.70/5th MILE &nbsp;&nbsp;&nbsp;
    </div>
</div>
""", unsafe_allow_html=True)


# ── DATE & TIME ──
st.markdown('<div class="section-label">01 &nbsp; When are you riding?</div>', unsafe_allow_html=True)
with st.container():
    col_date, col_time = st.columns(2)
    with col_date:
        pickup_date = st.date_input("Pickup date", value=datetime.today())
    with col_time:
        pickup_time = st.time_input("Pickup time", value=datetime.now().time())

# Hour-based context
hour = pickup_time.hour
if 7 <= hour <= 9 or 17 <= hour <= 19:
    time_context = "⚠️ Rush hour — expect higher fares & longer ride times"
    context_color = "#ff9900"
elif 22 <= hour or hour <= 5:
    time_context = "🌙 Late night surcharge applies after 8PM"
    context_color = "#8888ff"
else:
    time_context = "✅ Standard fare period"
    context_color = "#39ff14"

st.markdown(f"""
<div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:{context_color};
     background: rgba(255,255,255,0.03); border: 1px solid #222; border-radius:4px;
     padding: 8px 12px; margin-bottom:0.5rem; letter-spacing:1.5px;">
    {time_context}
</div>
""", unsafe_allow_html=True)


# ── COORDINATES ──
st.markdown('<div class="section-label">02 &nbsp; Where to?</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📍 Pickup")
    pickup_lon = st.number_input("Longitude", value=-73.985428, key="plon", format="%.6f")
    pickup_lat = st.number_input("Latitude", value=40.748817, key="plat", format="%.6f")
with col2:
    st.markdown("### 🏁 Dropoff")
    dropoff_lon = st.number_input("Longitude", value=-73.960000, key="dlon", format="%.6f")
    dropoff_lat = st.number_input("Latitude", value=40.760000, key="dlat", format="%.6f")

# Live distance calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

distance_mi = haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
est_mins = int(distance_mi * 3.5 + 5)

st.markdown(f"""
<div class="coord-display">
    📍 <span>{pickup_lat:.4f}°N, {abs(pickup_lon):.4f}°W</span>
    &nbsp;→&nbsp;
    🏁 <span>{dropoff_lat:.4f}°N, {abs(dropoff_lon):.4f}°W</span>
    &nbsp;|&nbsp; ~<span>{distance_mi:.1f} mi</span>
    &nbsp;|&nbsp; ~<span>{est_mins} min</span>
</div>
""", unsafe_allow_html=True)


# ── PASSENGERS ──
st.markdown('<div class="section-label">03 &nbsp; Passengers</div>', unsafe_allow_html=True)
passenger_count = st.slider("", min_value=1, max_value=8, value=1)

dots_html = '<div class="pax-dots">'
for i in range(1, 9):
    cls = "pax-dot active" if i <= passenger_count else "pax-dot"
    dots_html += f'<div class="{cls}">👤</div>'
dots_html += '</div>'
st.markdown(dots_html, unsafe_allow_html=True)


# ── MAP (pydeck arc) ──
st.markdown('<div class="section-label">04 &nbsp; Route preview</div>', unsafe_allow_html=True)

arc_data = [{
    "sourcePosition": [pickup_lon, pickup_lat],
    "targetPosition": [dropoff_lon, dropoff_lat],
}]

scatter_data = [
    {"position": [pickup_lon, pickup_lat],   "color": [247, 201, 72, 220],  "radius": 80, "label": "📍 Pickup"},
    {"position": [dropoff_lon, dropoff_lat], "color": [255, 80, 80, 220],   "radius": 80, "label": "🏁 Dropoff"},
]

arc_layer = pdk.Layer(
    "ArcLayer",
    data=arc_data,
    get_source_position="sourcePosition",
    get_target_position="targetPosition",
    get_source_color=[247, 201, 72, 220],
    get_target_color=[255, 80, 80, 220],
    auto_highlight=True,
    width_min_pixels=4,
    width_max_pixels=8,
    great_circle=True,
)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=scatter_data,
    get_position="position",
    get_fill_color="color",
    get_radius="radius",
    radius_scale=6,
    radius_min_pixels=8,
    radius_max_pixels=20,
    pickable=True,
    stroked=True,
    get_line_color=[255, 255, 255, 80],
    line_width_min_pixels=2,
)

mid_lat = (pickup_lat + dropoff_lat) / 2
mid_lon = (pickup_lon + dropoff_lon) / 2

# Auto zoom based on distance
if distance_mi < 1:
    zoom = 14
elif distance_mi < 3:
    zoom = 13
elif distance_mi < 8:
    zoom = 12
else:
    zoom = 11

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=zoom,
    pitch=45,
    bearing=0,
)

deck = pdk.Deck(
    layers=[arc_layer, scatter_layer],
    initial_view_state=view_state,
    map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    tooltip={"text": "{label}"},
)

st.pydeck_chart(deck, use_container_width=True)


# ── STATS PREVIEW ──
rough_min = round(2.50 + distance_mi * 1.75, 2)
rough_max = round(2.50 + distance_mi * 3.20 + (passenger_count * 0.5), 2)

st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-val">{distance_mi:.1f}</div>
        <div class="stat-lbl">Miles</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">~{est_mins}</div>
        <div class="stat-lbl">Est. Mins</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">${rough_min}–{rough_max}</div>
        <div class="stat-lbl">Range</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── CALCULATE ──
url = "https://taxifare.lewagon.ai/predict"

if st.button("🚕  CALCULATE MY FARE"):
    params = {
        "pickup_datetime": f"{pickup_date} {pickup_time}",
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
    }

    with st.spinner("🚕  Hailing the algorithm..."):
        try:
            response = requests.get(url, params=params, timeout=10)
        except Exception as e:
            st.error(f"Connection error: {e}")
            st.stop()

    if response.status_code == 200:
        data = response.json()
        prediction = data.get("fare", data.get("fare_amount", None))
        if prediction is not None:
            fare = float(prediction)

            if fare < 15:
                verdict_cls = "verdict-cheap"
                verdict_txt = "🟢 GREAT DEAL"
            elif fare < 35:
                verdict_cls = "verdict-mid"
                verdict_txt = "🟡 STANDARD FARE"
            else:
                verdict_cls = "verdict-pricey"
                verdict_txt = "🔴 PREMIUM RIDE"

            tip_15 = fare * 0.15
            tip_20 = fare * 0.20
            tip_25 = fare * 0.25

            st.markdown(f"""
<div class="fare-result">
    <div class="fare-label">Estimated Fare</div>
    <div class="fare-amount">${fare:.2f}</div>
    <div class="fare-currency">UNITED STATES DOLLARS</div>
    <div><span class="fare-verdict {verdict_cls}">{verdict_txt}</span></div>
</div>
""", unsafe_allow_html=True)

            st.markdown('<div class="section-label">Tip calculator</div>', unsafe_allow_html=True)
            st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-val">${tip_15:.2f}</div>
        <div class="stat-lbl">15% Tip</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">${tip_20:.2f}</div>
        <div class="stat-lbl">20% Tip</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">${tip_25:.2f}</div>
        <div class="stat-lbl">25% Tip</div>
    </div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div style="background:var(--surface2); border:1px solid var(--border); border-radius:4px;
     padding:1rem; margin-top:0.75rem; display:flex; justify-content:space-between;
     align-items:center;">
    <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:var(--muted);
         letter-spacing:2px; text-transform:uppercase;">
        Total w/ 20% tip
    </div>
    <div style="font-family:'Bebas Neue',sans-serif; font-size:2rem; color:var(--yellow);">
        ${fare + tip_20:.2f}
    </div>
</div>
""", unsafe_allow_html=True)

        else:
            st.error(f"Unexpected API response: {data}")
    else:
        st.error(f"API Error {response.status_code}: {response.text}")


# ── FOOTER ──
st.markdown("""
<div class="nyc-footer">
    NYC TaxiFare · Powered by <a href="#">Le Wagon</a> · ML Model by TaxiFare API<br>
    Not affiliated with NYC TLC · For estimation purposes only
</div>
""", unsafe_allow_html=True)
