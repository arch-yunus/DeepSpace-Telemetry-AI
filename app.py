import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.scheduler import DSNScheduler

# Page Config
st.set_page_config(page_title="DeepSpace-Telemetry-AI Omega", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI: Omega Dashboard")
st.markdown("### High-Fidelity Deep Space Communication Simulation")

# Sidebar for Inputs
st.sidebar.header("📡 Mission Control")
sim_date = st.sidebar.date_input("Simulation Date", datetime.now())
modulation = st.sidebar.selectbox("Modulation (CCSDS)", ["BPSK", "QPSK", "8-PSK", "16-APSK"])
fec_type = st.sidebar.selectbox("FEC Coding", ["None", "Reed-Solomon", "Turbo", "LDPC"])

st.sidebar.header("🌍 Ground Segment")
elevation = st.sidebar.slider("Antenna Elevation (Deg)", 5, 90, 45)
rain_rate = st.sidebar.slider("Rain Rate (mm/h)", 0, 50, 0)

# Initialize Engine
engine = TelemetryEngine()
predictor = TelemetryPredictor()
scheduler = DSNScheduler()

# Astronomical Data
dist_au, sep_angle, positions = engine.get_planetary_positions(sim_date.strftime("%Y-%m-%d"))

# Calculations
freq = engine.frequencies["X"]
fspl = engine.calculate_fspl(dist_au, freq)
t_solar = engine.calculate_solar_conjunction_noise(sep_angle)
fec_gain = engine.calculate_fec_gain(fec_type)
atmos_loss = engine.calculate_atmospheric_loss(elevation, rain_rate)

p_tx, g_tx, g_rx = 43, 48, 70
p_noise_thermal = engine.calculate_thermal_noise(25, 1e6)

snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise_thermal, t_solar=t_solar, fec_gain_db=fec_gain, atmos_loss_db=atmos_loss)
ber = engine.calculate_ber(snr, modulation=modulation)

# 3D Visualization
if positions:
    fig = go.Figure()
    # Sun
    fig.add_trace(go.Scatter3d(x=[positions['sun'][0]], y=[positions['sun'][1]], z=[positions['sun'][2]], mode='markers', marker=dict(size=12, color='yellow'), name='Sun'))
    # Earth
    fig.add_trace(go.Scatter3d(x=[positions['earth'][0]], y=[positions['earth'][1]], z=[positions['earth'][2]], mode='markers', marker=dict(size=8, color='blue'), name='Earth'))
    # Mars
    fig.add_trace(go.Scatter3d(x=[positions['mars'][0]], y=[positions['mars'][1]], z=[positions['mars'][2]], mode='markers', marker=dict(size=6, color='red'), name='Mars'))
    # Comm Vector
    fig.add_trace(go.Scatter3d(x=[positions['earth'][0], positions['mars'][0]], y=[positions['earth'][1], positions['mars'][1]], z=[positions['earth'][2], positions['mars'][2]], mode='lines', line=dict(color='white', width=2), name='Comm Link'))
    
    fig.update_layout(title="3D Orbital Geometry (Ecliptic J2000)", scene=dict(bgcolor='black', xaxis=dict(gridcolor='gray'), yaxis=dict(gridcolor='gray'), zaxis=dict(gridcolor='gray')), margin=dict(l=0, r=0, b=0, t=40))
    st.plotly_chart(fig, use_container_width=True)

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Distance", f"{dist_au:.3f} AU")
with col2:
    st.metric("SEP Angle", f"{sep_angle:.2f}°")
with col3:
    st.metric("SNR (RF)", f"{snr:.2f} dB")
with col4:
    opt_snr = engine.calculate_optical_snr(p_tx_watts=10, distance_au=dist_au)
    st.metric("SNR (Optical)", f"{opt_snr:.1f} dB")

# Detailed Analysis
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📋 Link Budget Details")
    st.write(f"**FSPL:** -{fspl:.2f} dB | **Atmos Loss:** -{atmos_loss:.2f} dB")
    st.write(f"**Solar Noise:** +{t_solar:.0f} K | **FEC Gain:** +{fec_gain:.1f} dB")
    if ber > 1e-5:
        st.error("⚠️ CRITICAL: BER is too high for reliable RF comm.")
    else:
        st.success("✅ OPTIMAL: Link conditions are stable.")

with c2:
    st.subheader("📡 NASA DSN Live (Mocked/Feed)")
    dsn_data = api.fetch_dsn_now_realtime()
    for station in dsn_data[:3]:
        st.write(f"**{station['name']}** ({station['type']}): `{station['status']}`")

# AI Insights
st.divider()
st.subheader("🧠 AI Mission Insights")
is_anomaly, z_score = predictor.detect_anomalies([snr-1, snr+1, snr-0.5, snr+0.5, snr-5]) # Simulated drop
if is_anomaly:
    st.warning(f"🚨 ANOMALY DETECTED: Signal drop detected (Z-Score: {z_score:.2f})")
else:
    st.info("AI Analysis: No signal anomalies detected in the last 5 frames.")

st.markdown("""
---
**Note:** This dashboard is a simulation of the core DeepSpace-Telemetry-AI physics engine. 
It accounts for Free Space Path Loss, Solar Conjunction Noise, and Ionospheric Scintillation.
""")
