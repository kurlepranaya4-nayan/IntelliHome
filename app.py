import random
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Home IoT Dashboard", page_icon="🏠", layout="wide")

# Session state keeps controls working between Streamlit reruns.
defaults = {
    "Bedroom Light": True,
    "Living Room Light": False,
    "Fan": True,
    "Air Conditioner": False,
    "auto_mode": False,
    "temperature": 25.4,
    "humidity": 58,
    "history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("""
<style>
.stApp { background: #f4f8f6; }
.block-container { padding-top: 1.6rem; }
.hero { background: linear-gradient(110deg,#123f35,#207a65); color: white; padding: 25px 28px; border-radius: 18px; }
.hero h1 { margin: 0; font-size: 2.1rem; }
.hero p { margin: 8px 0 0 0; color: #d9eee7; }
.device { background: white; border: 1px solid #e1ebe6; padding: 17px; border-radius: 15px; }
.small-label { color: #557268; font-size: .88rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🏠 Smart Home Automation</h1>
  <p>Monitor your home, control virtual devices, and explore energy usage.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
left, middle, right = st.columns(3)
on_count = sum(bool(st.session_state[d]) for d in ["Bedroom Light","Living Room Light","Fan","Air Conditioner"])
with left:
    st.metric("Devices online", "4 / 4", "Simulation active")
with middle:
    st.metric("Devices switched on", f"{on_count} / 4")
with right:
    st.metric("Estimated power now", f"{sum(w for d,w in [('Bedroom Light',10),('Living Room Light',12),('Fan',55),('Air Conditioner',900)] if st.session_state[d])} W")

st.subheader("Device controls")
devices = [
    ("Bedroom Light", "💡", "10 W", "Warm lighting for the bedroom"),
    ("Living Room Light", "🛋️", "12 W", "Main living area lighting"),
    ("Fan", "🌀", "55 W", "Virtual ceiling fan"),
    ("Air Conditioner", "❄️", "900 W", "Virtual air conditioner"),
]
cols = st.columns(4)
for col, (name, icon, watt, desc) in zip(cols, devices):
    with col:
        st.markdown('<div class="device">', unsafe_allow_html=True)
        st.markdown(f"### {icon} {name}")
        st.caption(desc)
        st.write(f"Rated power: **{watt}**")
        st.toggle("Power", key=name)
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.subheader("Sensor monitoring")
s1, s2, s3 = st.columns(3)
with s1:
    st.metric("🌡️ Temperature", f"{st.session_state.temperature:.1f} °C", "Simulated sensor")
with s2:
    st.metric("💧 Humidity", f"{st.session_state.humidity}%", "Simulated sensor")
with s3:
    active = "ON" if st.session_state.auto_mode else "OFF"
    st.metric("⚙️ Automation", active, "Rule-based mode")

a, b = st.columns([1, 1])
with a:
    st.markdown("#### Automation rules")
    st.session_state.auto_mode = st.toggle(
        "Enable energy-saving mode",
        value=st.session_state.auto_mode,
        help="Demo rule: when enabled, the AC is switched off if temperature is below 24°C."
    )
    if st.button("Run automation rule", use_container_width=True):
        if st.session_state.auto_mode:
            if st.session_state.temperature < 24:
                st.session_state["Air Conditioner"] = False
                st.success("Rule applied: AC switched OFF because temperature is below 24°C.")
            else:
                st.info("Rule checked: temperature is 24°C or above, so no change was made.")
        else:
            st.warning("Turn on energy-saving mode first.")
with b:
    st.markdown("#### Simulated sensor controls")
    if st.button("Refresh sensor readings", use_container_width=True):
        st.session_state.temperature = round(random.uniform(20, 33), 1)
        st.session_state.humidity = random.randint(35, 75)
        st.rerun()
    st.caption("Readings are randomly generated for demonstration; no physical sensor is connected.")

st.subheader("Energy usage")
watts = sum(w for d,w in [('Bedroom Light',10),('Living Room Light',12),('Fan',55),('Air Conditioner',900)] if st.session_state[d])
hours = st.slider("Assumed daily usage (hours)", 1, 24, 8)
kwh = watts * hours / 1000
cost = kwh * 8  # illustrative rate only
c1, c2 = st.columns(2)
with c1:
    st.metric("Estimated energy for selected devices", f"{kwh:.2f} kWh/day")
with c2:
    st.metric("Illustrative daily cost", f"₹{cost:.2f}", help="Uses an example rate of ₹8/kWh. Actual tariffs vary.")

chart_df = pd.DataFrame({
    "Device": ["Bedroom Light", "Living Room Light", "Fan", "Air Conditioner"],
    "Power (W)": [10 if st.session_state["Bedroom Light"] else 0,
                  12 if st.session_state["Living Room Light"] else 0,
                  55 if st.session_state["Fan"] else 0,
                  900 if st.session_state["Air Conditioner"] else 0]
})
fig = px.bar(chart_df, x="Device", y="Power (W)", color="Device", title="Current estimated power by device")
fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=10,t=55,b=10))
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Last dashboard refresh: {datetime.now().strftime('%d %b %Y, %I:%M:%S %p')} · College project prototype · Devices and sensor values are simulated.")
with st.expander("Project notes for your viva"):
    st.markdown("""
    - **Objective:** Demonstrate a smart-home dashboard that monitors and controls home devices.
    - **Frontend:** Streamlit dashboard with interactive switches, metrics and charts.
    - **Logic:** Python calculates estimated power use and applies a simple automation rule.
    - **IoT simulation:** Device states and sensor readings are simulated in software.
    - **Future scope:** Connect an ESP32, real sensors, an MQTT broker, persistent database storage and user authentication.
    - **Important:** This is a functional simulation prototype, not a real hardware-connected IoT system.
    """)
