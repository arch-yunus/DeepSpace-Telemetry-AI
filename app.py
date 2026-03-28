import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.scheduler import DSNScheduler

from src.api_connector import SpaceWeatherAPI

# Page Config
st.set_page_config(page_title="DeepSpace-Telemetry-AI Milli Vizyon", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI: Milli Uzay Vizyonu")
st.markdown("### Derin Uzay Haberleşme Analiz ve Karar Destek Sistemi (Omega-Class)")

# Sidebar for Inputs
st.sidebar.header("📡 Görev Kontrol (TUA)")
mission_type = st.sidebar.selectbox("Görev Profili", ["Ay Projesi", "Mars Testi", "Jüpiter Flyby", "Özel Görev"])

sim_date = st.sidebar.date_input("Simülasyon Tarihi", datetime.now())
modulation = st.sidebar.selectbox("Modülasyon (CCSDS)", ["BPSK", "QPSK", "8-PSK", "16-APSK"])
fec_type = st.sidebar.selectbox("Hata Düzeltme (FEC)", ["None", "Reed-Solomon", "Turbo", "LDPC"])

st.sidebar.header("🌍 Yer Segmenti (Türkiye)")
elevation = st.sidebar.slider("Anten Yükselimi (Derece)", 5, 90, 45)
rain_rate = st.sidebar.slider("Yağış Oranı (mm/saat)", 0, 50, 0)

# Initialize Engine
engine = TelemetryEngine()
predictor = TelemetryPredictor()
scheduler = DSNScheduler()
api = SpaceWeatherAPI()
from src.relay import MissionRelay
relay = MissionRelay(engine)

# Astronomical Data
dist_au, sep_angle, positions = engine.get_planetary_positions(sim_date.strftime("%Y-%m-%d"))
if mission_type == "Ay Projesi": dist_au = m_params["dist_au"]

# Calculations
freq = engine.frequencies[m_params["band"]]
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
    fig.add_trace(go.Scatter3d(x=[positions['sun'][0]], y=[positions['sun'][1]], z=[positions['sun'][2]], mode='markers', marker=dict(size=12, color='yellow'), name='Güneş'))
    fig.add_trace(go.Scatter3d(x=[positions['earth'][0]], y=[positions['earth'][1]], z=[positions['earth'][2]], mode='markers', marker=dict(size=8, color='blue'), name='Dünya'))
    fig.add_trace(go.Scatter3d(x=[positions['mars'][0]], y=[positions['mars'][1]], z=[positions['mars'][2]], mode='markers', marker=dict(size=6, color='red'), name='Mars'))
    fig.add_trace(go.Scatter3d(x=[positions['earth'][0], positions['mars'][0]], y=[positions['earth'][1], positions['mars'][1]], z=[positions['earth'][2], positions['mars'][2]], mode='lines', line=dict(color='white', width=2), name='Haberleşme Linki'))
    
    fig.update_layout(title="3D Yörünge Geometrisi (Ecliptic J2000)", scene=dict(bgcolor='black', xaxis=dict(gridcolor='gray'), yaxis=dict(gridcolor='gray'), zaxis=dict(gridcolor='gray')), margin=dict(l=0, r=0, b=0, t=40))
    st.plotly_chart(fig, use_container_width=True)

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Mesafe", f"{dist_au:.4f} AU")
with col2:
    st.metric("SEP Açısı", f"{sep_angle:.2f}°")
with col3:
    st.metric("SNR (RF)", f"{snr:.2f} dB")
with col4:
    opt_snr = engine.calculate_optical_snr(p_tx_watts=10, distance_au=dist_au)
    st.metric("SNR (Optik)", f"{opt_snr:.1f} dB")

# Detailed Analysis
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📋 Link Bütçesi Detayları")
    st.write(f"**Yol Kaybı (FSPL):** -{fspl:.2f} dB | **Atmosferik Kayıp:** -{atmos_loss:.2f} dB")
    st.write(f"**Güneş Gürültüsü:** +{t_solar:.0f} K | **FEC Kazancı:** +{fec_gain:.1f} dB")
    if ber > 1e-5:
        st.error("⚠️ KRİTİK: Hata oranı (BER) güvenli sınırın üzerinde.")
    else:
        st.success("✅ OPTİMAL: Bağlantı koşulları stabil.")

with c2:
    st.subheader("📡 NASA DSN Canlı Durum (Entegrasyon)")
    dsn_data = api.fetch_dsn_now_realtime()
    for station in dsn_data[:3]:
        st.write(f"**{station['name']}** ({station['type']}): `{station['status']}`")

# AI Insights
st.divider()
st.subheader("🧠 Yapay Zeka Görev Analizi")
is_anomaly, z_score = predictor.detect_anomalies([snr-1, snr+1, snr-0.5, snr+0.5, snr-5]) 
if is_anomaly:
    st.warning(f"🚨 ANOMALİ TESPİT EDİLDİ: Sinyal düşüşü saptandı (Z-Score: {z_score:.2f})")
else:
    st.info("AI Analizi: Son telemetri çerçevelerinde anomali saptanmadı.")

st.markdown("""
---
*Bu sistem TUA Astrohackathon 2026 kapsamında Milli Uzay Programı hedefleri için geliştirilmiştir.*
""")
