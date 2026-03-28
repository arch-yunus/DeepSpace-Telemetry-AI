# 🛰️ DeepSpace-Telemetry-AI: Interstellar-Class Technical Ecosystem

<div align="center">
  <img src="https://img.shields.io/badge/Status-Mission_Ready-success?style=for-the-badge&logo=nasa" alt="Mission Ready">
  <img src="https://img.shields.io/badge/Class-Interstellar-blueviolet?style=for-the-badge&logo=starship" alt="Interstellar Class">
  <img src="https://img.shields.io/badge/Event-TUA_Astrohackathon-0052cc?style=for-the-badge" alt="TUA">
</div>

---

## 🌌 Overview
**DeepSpace-Telemetry-AI** is a state-of-the-art simulation and analysis platform for deep space communication. It bridges the gap between theoretical astrophysics and operational telecommunications, providing a high-fidelity environment for mission planning, signal optimization, and predictive maintenance.

From **Skyfield-driven orbital mechanics** to **CCSDS-standard modulation analysis** and **Optical (Laser) communication modeling**, this ecosystem is designed for the future of humanity's expansion into the solar system and beyond.

---

## 🚀 Core Pillars of Technology

### 📡 1. High-Fidelity Physics Engine
*   **Orbital Precision:** Leverages NASA/JPL DE421 ephemeris for real-time planetary positioning.
*   **Propagation Models:** FSPL, Atmospheric Gas/Rain attenuation (ITU-R P.676), and Ionospheric Scintillation (Nakagami-m).
*   **Solar Interference:** Dynamic Sun-Earth-Probe (SEP) angle noise temperature modeling.

### 💡 2. Next-Gen Communication
*   **RF Standards:** CCSDS-compliant BPSK, QPSK, 8-PSK, and 16-APSK modulation curves.
*   **Optical (Laser) Links:** Photon-counting statistics, pointing jitter analysis, and beam divergence modeling for 1550nm laser links.
*   **Relay Logic:** Multi-hop mission simulation (Lander → Orbiter → DSN).

### 🤖 3. AI & Prediction
*   **SNR Forecasting:** Trend prediction based on solar flux and historic telemetry telemetry.
*   **Anomaly Detection:** 3-Sigma statistical engine to flag signal glitches (Autoencoder-ready).
*   **DSN Integration:** Real-time data ingestion from NASA's Deep Space Network (DSN Now).

---

## 🖥️ Interactive Omega Dashboard
The project features a **Streamlit** dashboard for mission control and analysis.

### Features:
-   **3D Orbit View:** Interactive Plotly visualization of Sun, Earth, Mars, and the communication vector.
-   **Link Budget Analyzer:** Real-time calculations of SNR, BER, and Capacity.
-   **Mission Profiles:** Pre-set scenarios for Mars Transit, Lunar Orbit, and Jupiter Flyby.
-   **DSN Live Status:** Integrated view of active NASA ground stations.

### Quick Start:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Architecture
```text
📦 DeepSpace-Telemetry-AI
 ┣ 📂 src              # Core Engine Modules
 ┃ ┣ 📜 engine.py      # Physics & Modulation (RF/Optical)
 ┃ ┣ 📜 predictor.py   # AI Forecasting & Anomaly Detection
 ┃ ┣ 📜 relay.py       # Multi-hop Relay Logic
 ┃ ┣ 📜 scheduler.py   # DSN Station Allocation
 ┃ ┗ 📜 api_connector.py # NASA DSN Now & SpaceWeather APIs
 ┣ 📂 simulations      # Mission Scenarios
 ┣ 📂 docs             # Technical Reports & Graphics
 ┣ 📜 app.py           # Streamlit Web UI
 ┗ 📜 requirements.txt # System Dependencies
```

---

## 🌗 Mathematical Foundations
The system is built on rigorous academic literature, including:
-   **Friis Transmission Equation** for link budgets.
-   **Nyquist-Shannon** for theoretical channel capacity.
-   **ITU-R P.676** for atmospheric gaseous attenuation.
-   **Nakagami-m** for ionospheric scintillation fading math.

---

## 👨‍💻 Developed by
**Yunus Emre** | Multi-Disciplinary Systems Designer | AI & Space Science Implementation  
Developed specifically for the **TUA Astrohackathon 2026**.

---
<div align="center">
  <i>"Ad Astra Per Aspera"</i>
</div>
