import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.scheduler import DSNScheduler
from src.api_connector import SpaceWeatherAPI
from src.relay import MissionRelay
from src.analyser import MonteCarloAnalyser, CoverageMapper

# Sayfa Yapılandırması
st.set_page_config(page_title="DeepSpace-Telemetry-AI Galaktik Seviye", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI: Galaktik Görev Kontrol")
st.markdown("### İleri Seviye Derin Uzay Analiz Ekosistemi (Galactic-Class)")

# Yan Panel Girişleri
st.sidebar.header("📡 Görev Kontrol (TUA)")
mission_type = st.sidebar.selectbox("Görev Profili", ["Ay Projesi", "Mars Testi", "Jüpiter Flyby", "Özel Görev"])

sim_date = st.sidebar.date_input("Simülasyon Tarihi", datetime.now())
modulation = st.sidebar.selectbox("Modülasyon (CCSDS)", ["BPSK", "QPSK", "8-PSK", "16-APSK"])
fec_type = st.sidebar.selectbox("Hata Düzeltme (FEC)", ["None", "Reed-Solomon", "Turbo", "LDPC"])

st.sidebar.header("🌍 Yer Segmenti (Türkiye)")
elevation = st.sidebar.slider("Anten Yükselimi (Derece)", 5, 90, 45)
rain_rate = st.sidebar.slider("Yağış Oranı (mm/saat)", 0, 50, 0)

# Motorların Başlatılması
engine = TelemetryEngine()
predictor = TelemetryPredictor()
scheduler = DSNScheduler()
api = SpaceWeatherAPI()
relay = MissionRelay(engine)
analyser = MonteCarloAnalyser(engine)
mapper = CoverageMapper(engine)

# Görev Parametrelerini Al
m_params = engine.get_tua_mission_params(mission_type)

# Astronomik Veriler
dist_au, sep_angle, positions = engine.get_planetary_positions(sim_date.strftime("%Y-%m-%d"))
if mission_type == "Ay Projesi": dist_au = m_params["dist_au"]

# Hesaplamalar
freq = engine.frequencies[m_params["band"]]
fspl = engine.calculate_fspl(dist_au, freq)
t_solar = engine.calculate_solar_conjunction_noise(sep_angle)
fec_gain = engine.calculate_fec_gain(fec_type)
atmos_loss = engine.calculate_atmospheric_loss(elevation, rain_rate)

p_tx, g_tx, g_rx = 43, 48, 70
p_noise_thermal = engine.calculate_thermal_noise(25, 1e6)

snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise_thermal, t_solar=t_solar, fec_gain_db=fec_gain, atmos_loss_db=atmos_loss)
ber = engine.calculate_ber(snr, modulation=modulation)

# Ana Ekran Sekmeleri
tab1, tab2, tab3 = st.tabs(["📊 Standart Analiz", "🧠 İleri Seviye (Galaktik)", "🌍 Yer İstasyonu"])

with tab1:
    # 3D Görselleştirme
    if positions:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[positions['sun'][0]], y=[positions['sun'][1]], z=[positions['sun'][2]], mode='markers', marker=dict(size=12, color='yellow'), name='Güneş'))
        fig.add_trace(go.Scatter3d(x=[positions['earth'][0]], y=[positions['earth'][1]], z=[positions['earth'][2]], mode='markers', marker=dict(size=8, color='blue'), name='Dünya'))
        fig.add_trace(go.Scatter3d(x=[positions['mars'][0]], y=[positions['mars'][1]], z=[positions['mars'][2]], mode='markers', marker=dict(size=6, color='red'), name='Mars'))
        fig.add_trace(go.Scatter3d(x=[positions['earth'][0], positions['mars'][0]], y=[positions['earth'][1], positions['mars'][1]], z=[positions['earth'][2], positions['mars'][2]], mode='lines', line=dict(color='white', width=2), name='Haberleşme Linki'))
        
        fig.update_layout(title="3D Yörünge Geometrisi (J2000)", scene=dict(bgcolor='black'), margin=dict(l=0, r=0, b=0, t=40))
        st.plotly_chart(fig, use_container_width=True)

    # Metrikler
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Mesafe", f"{dist_au:.4f} AU")
    with col2: st.metric("SEP Açısı", f"{sep_angle:.2f}°")
    with col3: st.metric("SNR (RF)", f"{snr:.2f} dB")
    with col4: st.metric("SNR (Optik)", f"{engine.calculate_optical_snr(10, dist_au):.1f} dB")

with tab2:
    st.header("🌌 Galaktik Analiz Araçları")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🎲 Monte Carlo Güven Analizi")
        runs, stats = analyser.run_simulation(snr)
        fig_mc = go.Figure(data=[go.Histogram(x=runs, nbinsx=30, marker_color='cyan')])
        fig_mc.update_layout(title="SNR Dağılımı (%95 Güven)", xaxis_title="SNR (dB)", yaxis_title="Frekans")
        st.plotly_chart(fig_mc, use_container_width=True)
        st.write(f"**Link Kullanılabilirliği:** %{stats['availability']:.2f}")
        st.write(f"**Ortalama SNR:** {stats['mean']:.2f} dB")

    with c2:
        st.subheader("🛤️ Röle Yolu Optimizasyonu (Dijkstra)")
        target = st.selectbox("Hedef Düğüm", ["Deep-Space-Probe", "Mars-Relay", "Lunar-Gateway"])
        path, opt_snr = relay.optimize_path("Dünya", target)
        st.success(f"En İyi Rota: {' -> '.join(path)}")
        st.write(f"Kümülatif Tahmini SNR: {opt_snr:.2f} dB")

with tab3:
    st.subheader("📡 NASA DSN Canlı Durum ve Yer Segmenti")
    dsn_data = api.fetch_dsn_now_realtime()
    for station in dsn_data[:5]:
        st.write(f"**{station['name']}** ({station['type']}): `{station['status']}`")

# Footer
st.divider()
st.markdown("*Bu sistem TUA Astrohackathon 2026 kapsamında en üst seviye teknik yeterlilik (Galactic-Class) için geliştirilmiştir.*")
