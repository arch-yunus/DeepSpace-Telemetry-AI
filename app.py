import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.scheduler import DSNScheduler

# Page Config
st.set_page_config(page_title="DeepSpace-Telemetry-AI Dashboard", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI Dashboard")
st.markdown("### Real-time Deep Space Signal Analysis & Optimization")

# Sidebar for Inputs
st.sidebar.header("Mission Parameters")
dist_au = st.sidebar.slider("Spacecraft Distance (AU)", 0.1, 2.5, 1.52)
sep_angle = st.sidebar.slider("Sun-Earth-Probe (SEP) Angle (Deg)", 0.1, 20.0, 5.0)
band = st.sidebar.selectbox("Frequency Band", ["X", "Ka"])
fec_type = st.sidebar.selectbox("FEC Coding", ["None", "Reed-Solomon", "Turbo", "LDPC"])

# Initialize Engines
engine = TelemetryEngine()
predictor = TelemetryPredictor()
scheduler = DSNScheduler()

# Calculations
freq = engine.frequencies[band]
fspl = engine.calculate_fspl(dist_au, freq)
t_solar = engine.calculate_solar_conjunction_noise(sep_angle)
fec_gain = engine.calculate_fec_gain(fec_type)

p_tx, g_tx, g_rx = 43, 48, 70
p_noise_thermal = engine.calculate_thermal_noise(25, 1e6)

snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise_thermal, t_solar=t_solar, fec_gain_db=fec_gain)
ber = engine.calculate_ber(snr)

# Dashboard Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Signal-to-Noise Ratio (SNR)", f"{snr:.2f} dB", delta=f"{fec_gain} dB FEC Gain")
    
with col2:
    st.metric("Bit Error Rate (BER)", f"{ber:.2e}")
    
with col3:
    station, score = scheduler.get_best_station(random_lon := 45.0, snr) # Mock SC Lon
    st.metric("Optimal Ground Station", station)

# Trend Analysis
st.divider()
st.subheader("📊 24-Hour Predictive Analysis")
pred_snr, confidence = predictor.predict_snr_trend(snr, solar_flux_index=150) # Simulated flux

df_trend = pd.DataFrame({
    "Status": ["Current", "24h Forecast"],
    "SNR (dB)": [snr, pred_snr]
})

st.bar_chart(df_trend.set_index("Status"))
st.info(f"AI Prediction Confidence: {confidence*100:.1f}%")

st.markdown("""
---
**Note:** This dashboard is a simulation of the core DeepSpace-Telemetry-AI physics engine. 
It accounts for Free Space Path Loss, Solar Conjunction Noise, and Ionospheric Scintillation.
""")
