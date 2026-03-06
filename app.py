import streamlit as st
import requests
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
    --orange: #F5A623;
    --orange-dim: #d4891a;
    --orange-glow: rgba(245,166,35,0.18);
    --bg: #e8eaf0;
    --surface: #d4d7e0;
    --surface2: #c8ccd8;
    --surface3: #dde0e8;
    --border: #b8bccc;
    --border-bright: #a0a4b8;
    --text: #1e2030;
    --muted: #5a5f78;
    --green: #16a34a;
    --red: #dc2626;
    --sidebar-bg: #2b2d38;
    --sidebar-surface: #23252f;
    --sidebar-border: #3a3c4a;
    --sidebar-text: #e8eaf0;
    --sidebar-muted: #8b8da8;
}

* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background: var(--bg);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* kill ALL default padding */
.block-container {
    padding: 0.5rem 1rem 1rem 1rem !important;
    max-width: 100% !important;
}
.main > div { padding-top: 0 !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 2px solid var(--orange) !important;
    min-width: 290px !important;
    max-width: 290px !important;
}
[data-testid="stSidebar"] > div {
    padding: 0.75rem 1rem 2rem 1rem !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── LOGO ── */
.sb-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: var(--orange);
    letter-spacing: 5px;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.sb-logo span { color: var(--sidebar-text); }
.sb-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.45rem;
    color: var(--sidebar-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--sidebar-border);
}

/* ── SECTION LABELS (no numbers) ── */
.sl {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.48rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--orange);
    margin: 0.85rem 0 0.4rem 0;
}
.sl::before { content:''; display:block; width:10px; height:2px; background:var(--orange); flex-shrink:0; }
.sl::after  { content:''; display:block; flex:1; height:1px; background:var(--sidebar-border); }

/* ── SIDEBAR INPUTS ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: var(--sidebar-muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="stSidebar"] input[type="number"],
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] [data-testid="stTimeInput"] input {
    background: var(--sidebar-surface) !important;
    border: 1px solid var(--sidebar-border) !important;
    border-radius: 4px !important;
    color: var(--sidebar-text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 2px var(--orange-glow) !important;
    outline: none !important;
}

/* ── SLIDER ── */
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: var(--sidebar-border) !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div {
    background: var(--orange) !important;
    box-shadow: 0 0 8px var(--orange-glow) !important;
}

/* ── BUTTON ── */
[data-testid="stSidebar"] .stButton > button {
    background: var(--orange) !important;
    color: #1a1a1a !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.25rem !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--orange-dim) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(245,166,35,0.35) !important;
}

/* ── COORD BOX ── */
.coord-box {
    font-family: 'Space Mono', monospace;
    font-size: 0.54rem;
    color: var(--sidebar-muted);
    padding: 0.4rem 0.6rem;
    background: var(--sidebar-surface);
    border-radius: 3px;
    border: 1px solid var(--sidebar-border);
    line-height: 1.8;
    margin-top: 0.4rem;
}
.coord-box span { color: var(--orange); }

/* ── TIME CTX ── */
.time-ctx {
    font-family: 'Space Mono', monospace;
    font-size: 0.5rem;
    background: rgba(0,0,0,0.15);
    border: 1px solid var(--sidebar-border);
    border-radius: 4px;
    padding: 4px 8px;
    letter-spacing: 1px;
}

/* ── PAX DOTS ── */
.pax-dots { display:flex; gap:5px; flex-wrap:wrap; margin-top:0.3rem; }
.pax-dot {
    width:22px; height:22px; border-radius:50%;
    border:2px solid var(--sidebar-border);
    display:flex; align-items:center; justify-content:center; font-size:0.66rem;
}
.pax-dot.on { border-color:var(--orange); background:var(--orange-glow); }

/* ── STATS ── */
.stats-row { display:grid; grid-template-columns:repeat(3,1fr); gap:0.35rem; margin-top:0.45rem; }
.stat-box {
    background: var(--sidebar-surface);
    border: 1px solid var(--sidebar-border);
    border-radius: 4px; padding:0.4rem; text-align:center;
}
.stat-val { font-family:'Bebas Neue',sans-serif; font-size:0.95rem; color:var(--orange); line-height:1; }
.stat-lbl { font-family:'Space Mono',monospace; font-size:0.38rem; color:var(--sidebar-muted); letter-spacing:2px; text-transform:uppercase; margin-top:1px; }

/* ── FARE BOX ── */
.fare-box {
    background: var(--sidebar-surface);
    border: 1px solid var(--orange);
    border-radius: 6px;
    padding:0.8rem; text-align:center; position:relative; overflow:hidden; margin-top:0.5rem;
}
.fare-box::before {
    content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse at center, rgba(245,166,35,0.07) 0%, transparent 70%);
}
.fare-lbl { font-family:'Space Mono',monospace; font-size:0.45rem; letter-spacing:4px; color:var(--sidebar-muted); text-transform:uppercase; }
.fare-amt { font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:var(--orange); line-height:1; text-shadow:0 0 24px rgba(245,166,35,0.4); }
.fare-cur { font-family:'Space Mono',monospace; font-size:0.48rem; color:var(--sidebar-muted); letter-spacing:3px; }
.verdict { display:inline-block; margin-top:0.45rem; padding:3px 12px; border-radius:2px; font-family:'Space Mono',monospace; font-size:0.52rem; letter-spacing:2px; font-weight:700; }
.v-cheap  { background:rgba(22,163,74,0.15);  color:#4ade80; border:1px solid #4ade80; }
.v-mid    { background:rgba(245,166,35,0.15); color:var(--orange); border:1px solid var(--orange); }
.v-pricey { background:rgba(220,38,38,0.15);  color:#f87171; border:1px solid #f87171; }

.tip-total {
    background: rgba(0,0,0,0.2);
    border: 1px solid var(--sidebar-border); border-radius:4px;
    padding:0.4rem 0.65rem; margin-top:0.35rem;
    display:flex; justify-content:space-between; align-items:center;
}
.tip-lbl { font-family:'Space Mono',monospace; font-size:0.45rem; color:var(--sidebar-muted); letter-spacing:2px; text-transform:uppercase; }
.tip-val { font-family:'Bebas Neue',sans-serif; font-size:1.3rem; color:var(--orange); }

/* ── MAIN AREA ── */
.main-title {
    font-family: 'Space Mono', sans-serif;
    font-size: 0.6rem;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

[data-testid="stDeckGlJsonChart"] {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.1) !important;
}

[data-testid="stSidebar"] h3 {
    font-family:'Bebas Neue',sans-serif !important;
    font-size:0.82rem !important;
    color:var(--sidebar-text) !important;
    letter-spacing:2px !important;
    margin: 0 0 0.15rem 0 !important;
}

/* ── MOBILE FIX ── */
/* On mobile, show sidebar content ABOVE the map */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        min-width: 100vw !important;
        max-width: 100vw !important;
        border-right: none !important;
        border-bottom: 2px solid var(--orange) !important;
        position: relative !important;
        height: auto !important;
    }
    [data-testid="stSidebar"] > div {
        height: auto !important;
        overflow: visible !important;
    }
    .block-container {
        padding: 0.5rem !important;
    }
    [data-testid="stDeckGlJsonChart"] {
        height: 400px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">NYC <span>TAXI</span> FARE</div>
    <div class="sb-sub">🟠 Live ML Fare Estimator</div>
    """, unsafe_allow_html=True)

    # WHEN
    st.markdown('<div class="sl">When?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        pickup_date = st.date_input("Date", value=datetime.today())
    with c2:
        pickup_time = st.time_input("Time", value=datetime.now().time())

    hour = pickup_time.hour
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        tctx, tclr = "⚠️ Rush hour", "#f59e0b"
    elif 22 <= hour or hour <= 5:
        tctx, tclr = "🌙 Late night surcharge", "#818cf8"
    else:
        tctx, tclr = "✅ Standard fare period", "#4ade80"
    st.markdown(f'<div class="time-ctx" style="color:{tclr};">{tctx}</div>', unsafe_allow_html=True)

    # WHERE
    st.markdown('<div class="sl">Where to?</div>', unsafe_allow_html=True)
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
<div class="coord-box">
    📍 <span>{pickup_lat:.4f}°N, {abs(pickup_lon):.4f}°W</span><br>
    🏁 <span>{dropoff_lat:.4f}°N, {abs(dropoff_lon):.4f}°W</span><br>
    ~<span>{distance_mi:.1f} mi</span> &nbsp;|&nbsp; ~<span>{est_mins} min</span>
</div>
""", unsafe_allow_html=True)

    # PASSENGERS
    st.markdown('<div class="sl">Passengers</div>', unsafe_allow_html=True)
    passenger_count = st.slider("", min_value=1, max_value=8, value=1)
    dots = '<div class="pax-dots">'
    for i in range(1, 9):
        dots += f'<div class="pax-dot {"on" if i <= passenger_count else ""}">👤</div>'
    dots += '</div>'
    st.markdown(dots, unsafe_allow_html=True)

    # STATS
    rough_min = round(2.50 + distance_mi * 1.75, 2)
    rough_max = round(2.50 + distance_mi * 3.20 + passenger_count * 0.5, 2)
    st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-val">{distance_mi:.1f}</div><div class="stat-lbl">Miles</div></div>
    <div class="stat-box"><div class="stat-val">~{est_mins}</div><div class="stat-lbl">Mins</div></div>
    <div class="stat-box"><div class="stat-val">${rough_min}–{rough_max}</div><div class="stat-lbl">Range</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # BUTTON
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
                r = requests.get("https://taxifare.lewagon.ai/predict", params=params, timeout=10)
            except Exception as e:
                st.error(f"Connection error: {e}")
                st.stop()

        if r.status_code == 200:
            data = r.json()
            pred = data.get("fare", data.get("fare_amount"))
            if pred is not None:
                st.session_state["fare"] = float(pred)
            else:
                st.error(f"Unexpected response: {data}")
        else:
            st.error(f"API Error {r.status_code}")

    # FARE RESULT
    if "fare" in st.session_state:
        fare = st.session_state["fare"]
        if fare < 15:   vcls, vtxt = "v-cheap",  "🟢 GREAT DEAL"
        elif fare < 35: vcls, vtxt = "v-mid",     "🟠 STANDARD FARE"
        else:           vcls, vtxt = "v-pricey",  "🔴 PREMIUM RIDE"

        t15, t20, t25 = fare*.15, fare*.20, fare*.25

        st.markdown(f"""
<div class="fare-box">
    <div class="fare-lbl">Estimated Fare</div>
    <div class="fare-amt">${fare:.2f}</div>
    <div class="fare-cur">USD</div>
    <div><span class="verdict {vcls}">{vtxt}</span></div>
</div>
<div class="stats-row" style="margin-top:0.45rem;">
    <div class="stat-box"><div class="stat-val">${t15:.2f}</div><div class="stat-lbl">15%</div></div>
    <div class="stat-box"><div class="stat-val">${t20:.2f}</div><div class="stat-lbl">20%</div></div>
    <div class="stat-box"><div class="stat-val">${t25:.2f}</div><div class="stat-lbl">25%</div></div>
</div>
<div class="tip-total">
    <div class="tip-lbl">Total w/ 20% tip</div>
    <div class="tip-val">${fare + t20:.2f}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN — MAP
# ─────────────────────────────────────────
st.markdown('<div class="main-title">Route Preview</div>', unsafe_allow_html=True)

arc_layer = pdk.Layer(
    "ArcLayer",
    data=[{"src": [pickup_lon, pickup_lat], "dst": [dropoff_lon, dropoff_lat]}],
    get_source_position="src",
    get_target_position="dst",
    get_source_color=[245, 166, 35, 230],
    get_target_color=[220, 38, 38, 230],
    width_min_pixels=5, width_max_pixels=9,
    great_circle=True,
)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=[
        {"pos": [pickup_lon, pickup_lat],   "col": [245, 166, 35, 240], "lbl": "📍 Pickup"},
        {"pos": [dropoff_lon, dropoff_lat], "col": [220, 38, 38, 240],  "lbl": "🏁 Dropoff"},
    ],
    get_position="pos",
    get_fill_color="col",
    get_radius=80,
    radius_scale=6, radius_min_pixels=8, radius_max_pixels=20,
    pickable=True, stroked=True,
    get_line_color=[255, 255, 255, 100],
    line_width_min_pixels=2,
)

mid_lat = (pickup_lat + dropoff_lat) / 2
mid_lon = (pickup_lon + dropoff_lon) / 2
zoom = 14 if distance_mi < 1 else 13 if distance_mi < 3 else 12 if distance_mi < 8 else 11

deck = pdk.Deck(
    layers=[arc_layer, scatter_layer],
    initial_view_state=pdk.ViewState(
        latitude=mid_lat, longitude=mid_lon,
        zoom=zoom, pitch=45, bearing=0,
    ),
    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    tooltip={"text": "{lbl}"},
)

st.pydeck_chart(deck, use_container_width=True, height=800)
