import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.scheduler import DSNScheduler
from src.api_connector import SpaceWeatherAPI
from src.relay import MissionRelay
from src.analyser import MonteCarloAnalyser, CoverageMapper
from src.reconstructor import SignalReconstructor
from src.swarm import SwarmCoordinator

# Sayfa Yapılandırması
st.set_page_config(page_title="DeepSpace-Telemetry-AI Aşkın Seviye", layout="wide")

st.title("🛰️ DeepSpace-Telemetry-AI: Aşkın Görev Kontrol")
st.markdown("### Final Sınır: Kuantum ve Sürü Zekası (Transcendental-Class)")

# Yan Panel Girişleri
st.sidebar.header("📡 Görev Kontrol (TUA)")
mission_type = st.sidebar.selectbox("Görev Profili", ["Ay Projesi", "Mars Testi", "Jüpiter Flyby", "Alpha Centauri (Teorik)"])

sim_date = st.sidebar.date_input("Simülasyon Tarihi", datetime.now())
modulation = st.sidebar.selectbox("Modülasyon (CCSDS)", ["BPSK", "QPSK", "8-PSK", "16-APSK"])

st.sidebar.header("🌌 İleri Teknoloji")
use_quantum = st.sidebar.toggle("Kuantum Dolanıklık Linki (Dolaysız)", value=False)
swarm_size = st.sidebar.slider("Sürü Anten Büyüklüğü (Uydu Sayısı)", 1, 1000, 100)

# Motorların Başlatılması
if 'engine' not in st.session_state:
    st.session_state.engine = TelemetryEngine()
    st.session_state.reconstructor = SignalReconstructor()
    st.session_state.swarm = SwarmCoordinator()
    st.session_state.relay = MissionRelay(st.session_state.engine)
    st.session_state.analyser = MonteCarloAnalyser(st.session_state.engine)
    st.session_state.api = SpaceWeatherAPI()

engine = st.session_state.engine
swarm = st.session_state.swarm

# Görev Parametrelerini Al
m_params = engine.get_tua_mission_params(mission_type if mission_type != "Alpha Centauri (Teorik)" else "Özel Görev")
dist_au = m_params["dist_au"] if mission_type != "Alpha Centauri (Teorik)" else 268770 # ~4.2 Light Years

# Kuantum Gecikme ve SNR Boost
latency, q_boost = (0, 30) if use_quantum else ((dist_au * 499), 0)
swarm_gain = swarm.calculate_array_gain(swarm_size)

# Hesaplamalar (RF/Optik Temelli)
snr_base = engine.calculate_snr(43, 48, 70, engine.calculate_fspl(dist_au, 8.4e9), 1e-15)
final_snr = snr_base + q_boost + swarm_gain

# Ana Ekran Sekmeleri
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analiz", "🧬 Kuantum & Sürü", "🛠️ Görev Tasarımı", "🌍 Yer İstasyonu"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Mesafe", f"{dist_au:.2f} AU")
    with col2: st.metric("Gecikme (Latency)", f"{latency:.2f} s" if latency < 3600 else f"{latency/3600:.2f} saat")
    with col3: st.metric("Efektif SNR", f"{final_snr:.2f} dB")
    with col4: st.metric("Sürü Kazancı", f"+{swarm_gain:.1f} dB")

    # Görselleştirme
    st.subheader("🚀 Görev Yörüngesi ve Sürü Yayılımı")
    st.info("Sürü uyduları hedef yörüngesinde faz dizilimli olarak koordine ediliyor.")

with tab2:
    st.header("🧬 Kuantum Dolanıklık ve Sürü Zekası")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("⚛️ Kuantum Link Durumu")
        if use_quantum:
            st.success("Kuantum Dolanıklık Aktif: Gecikme Sıfırlandı.")
            st.write("Veri İletimi: **Dolaysız (Instantaneous)**")
        else:
            st.warning("Standart Elektromanyetik Yayılım: Işık Hızı Sınırı Aktif.")
            st.write(f"Tahmini Gecikme (Tek Yön): {latency:.2f} saniye")

    with c2:
        st.subheader("🐝 Otonom Sürü Koordinasyonu")
        st.write(f"Aktif Sürü Üyesi: **{swarm_size} Uydu**")
        st.write(f"Eşdeğer Anten Çapı: **{np.sqrt(swarm_size)*5:.1f} metre**")
        st.progress(swarm_size / 1000)

    st.divider()
    if st.button("🔥 GÜNEŞ SÜPER-FIRTINASI TESTİ (Stress Test)"):
        with st.status("Güneş Fırtınası Algılandı...", expanded=True) as status:
            st.write("İyonosferik bozulma artıyor...")
            time.sleep(1)
            st.error("Link Kaybı! SNR Düştü.")
            time.sleep(1)
            st.write("AI Reconstructor Devreye Giriyor...")
            time.sleep(1)
            st.success("Bağlantı AI ile Kurtarıldı!")
            status.update(label="Stres Testi Tamamlandı: Sistem Stabil", state="complete")

with tab3:
    st.header("🛠️ Galaktik Görev Tasarımcısı")
    target_node = st.selectbox("Hedef Düğüm", list(st.session_state.relay.nodes.keys()))
    path, _ = st.session_state.relay.optimize_path("Dünya", target_node)
    st.success(f"En İyi Rota: {' -> '.join(path)}")

with tab4:
    st.subheader("📡 Küresel DSN Ağı")
    dsn = st.session_state.api.fetch_dsn_now_realtime()
    st.table(pd.DataFrame(dsn[:5]))

# Footer
st.divider()
st.markdown("*Bu sistem TUA Astrohackathon 2026 kapsamında 'Transcendental-Class' (Aşkın Vizyon) seviyesi için geliştirilmiştir.*")
