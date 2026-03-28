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
from src.reconstructor import SignalReconstructor

# Sayfa Yapılandırması
st.set_page_config(page_title="DeepSpace-Telemetry-AI Evrensel Seviye", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI: Evrensel Görev Kontrol")
st.markdown("### Sonsuz Vizyon Derin Uzay Analiz Ekosistemi (Universal-Class)")

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
if 'engine' not in st.session_state:
    st.session_state.engine = TelemetryEngine()
    st.session_state.reconstructor = SignalReconstructor()
    st.session_state.predictor = TelemetryPredictor()
    st.session_state.scheduler = DSNScheduler()
    st.session_state.api = SpaceWeatherAPI()
    st.session_state.relay = MissionRelay(st.session_state.engine)
    st.session_state.analyser = MonteCarloAnalyser(st.session_state.engine)
    st.session_state.mapper = CoverageMapper(st.session_state.engine)

engine = st.session_state.engine
reconstructor = st.session_state.reconstructor

# Görev Parametrelerini Al
m_params = engine.get_tua_mission_params(mission_type)

# Bant Seçimi (Multispectral Genişleme)
band = st.sidebar.selectbox("Haberleşme Bandı", list(engine.frequencies.keys()), index=1)

# Astronomik Veriler
dist_au, sep_angle, positions = engine.get_planetary_positions(sim_date.strftime("%Y-%m-%d"))
if mission_type == "Ay Projesi": dist_au = m_params["dist_au"]

# Hesaplamalar
freq = engine.frequencies[band]
fspl = engine.calculate_fspl(dist_au, freq)
t_solar = engine.calculate_solar_conjunction_noise(sep_angle)
fec_gain = engine.calculate_fec_gain(fec_type)
atmos_loss = engine.calculate_atmospheric_loss(elevation, rain_rate)

p_tx, g_tx, g_rx = 43, 48, 70
p_noise_thermal = engine.calculate_thermal_noise(25, 1e6)

snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise_thermal, t_solar=t_solar, fec_gain_db=fec_gain, atmos_loss_db=atmos_loss)
ber = engine.calculate_ber(snr, modulation=modulation)

# Ana Ekran Sekmeleri
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analiz", "🧠 Galaktik/Evrensel", "🛠️ Görev Tasarımcısı", "🌍 Yer İstasyonu"])

with tab1:
    # 3D Görselleştirme
    if positions:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=[positions['sun'][0]], y=[positions['sun'][1]], z=[positions['sun'][2]], mode='markers', marker=dict(size=12, color='yellow'), name='Güneş'))
        fig.add_trace(go.Scatter3d(x=[positions['earth'][0]], y=[positions['earth'][1]], z=[positions['earth'][2]], mode='markers', marker=dict(size=8, color='blue'), name='Dünya'))
        fig.add_trace(go.Scatter3d(x=[positions['mars'][0]], y=[positions['mars'][1]], z=[positions['mars'][2]], mode='markers', marker=dict(size=6, color='red'), name='Mars'))
        # Ek düğümleri çiz
        for name, node in st.session_state.relay.nodes.items():
            if name not in ["Dünya", "Mars-Relay"]:
                fig.add_trace(go.Scatter3d(x=[node['pos']], y=[0], z=[0], mode='markers', marker=dict(size=5, color='cyan'), name=name))

        fig.add_trace(go.Scatter3d(x=[positions['earth'][0], positions['mars'][0]], y=[positions['earth'][1], positions['mars'][1]], z=[positions['earth'][2], positions['mars'][2]], mode='lines', line=dict(color='white', width=2), name='Ana Link'))
        
        fig.update_layout(title="3D Sistem Geometrisi ve Link Durumu", scene=dict(bgcolor='black'), margin=dict(l=0, r=0, b=0, t=40))
        st.plotly_chart(fig, use_container_width=True)

    # Metrikler
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Mesafe", f"{dist_au:.4f} AU")
    with col2: st.metric("Frekans", f"{freq/1e9:.2f} GHz")
    with col3: st.metric("SNR (Aktif)", f"{snr:.2f} dB")
    with col4: st.metric("Hata Oranı (BER)", f"{ber:.1e}")

with tab2:
    st.header("🌌 Evrensel Analiz ve AI Onarım")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🤖 AI Sinyal Onarımı (Denoising)")
        if snr < 10:
            st.warning(f"Sinyal Zayıf ({snr:.2f} dB). AI Onarımı öneriliyor.")
            if st.button("AI Onarımı Başlat"):
                recon = reconstructor.reconstruct_fragment(snr)
                st.success(f"Onarım Başarılı! Efektif SNR: {recon['effective_snr']:.2f} dB (+{recon['recovery_gain']:.1f} dB Kazanç)")
                st.info(f"Yapay Zeka Kalite Skoru: %{recon['quality_score']*100:.1f}")
        else:
            st.success("Sinyal kalitesi optimal. AI onarımı şu an gerekli değil.")

    with c2:
        st.subheader("🎲 Monte Carlo Link Güvenilirliği")
        runs, stats = st.session_state.analyser.run_simulation(snr)
        fig_mc = go.Figure(data=[go.Histogram(x=runs, nbinsx=30, marker_color='gold')])
        fig_mc.update_layout(title="SNR Dağılım Analizi", xaxis_title="SNR (dB)", yaxis_title="Frekans")
        st.plotly_chart(fig_mc, use_container_width=True)
        st.write(f"**Sistem Kullanılabilirliği:** %{stats['availability']:.2f}")

with tab3:
    st.header("🛠️ Galaktik Görev Tasarımcısı")
    st.info("Sisteme dinamik olarak yeni röle istasyonları ekleyin.")
    new_node_name = st.text_input("Düğüm Adı", "Yeni-Relay-1")
    new_node_pos = st.number_input("Pozisyon (AU)", value=2.5, step=0.1)
    if st.button("Düğüm Ekle"):
        st.session_state.relay.nodes[new_node_name] = {"type": "Custom", "pos": new_node_pos}
        st.success(f"{new_node_name} sisteme eklendi!")
    
    st.divider()
    st.subheader("🛤️ Rota Optimizasyonu (Dijkstra)")
    target = st.selectbox("Varış Hedefi", list(st.session_state.relay.nodes.keys()))
    path, opt_snr = st.session_state.relay.optimize_path("Dünya", target)
    st.code(" -> ".join(path), language="text")
    st.write(f"Kümülatif Tahmini Link SNR: **{opt_snr:.2f} dB**")

with tab4:
    st.subheader("📡 Küresel Yer İstasyonu Ağı")
    dsn_data = st.session_state.api.fetch_dsn_now_realtime()
    for station in dsn_data[:6]:
        st.write(f"**{station['name']}** ({station['type']}): `{station['status']}`")

# Footer
st.divider()
st.markdown("*Bu sistem TUA Astrohackathon 2026 kapsamında 'Universal-Class' (Sonsuz Vizyon) seviyesi için geliştirilmiştir.*")
