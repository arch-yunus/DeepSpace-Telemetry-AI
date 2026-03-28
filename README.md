# 🛰️ DeepSpace-Telemetry-AI: Galaktik Haberleşme Ekosistemi

<div align="center">
  <img src="https://img.shields.io/badge/Durum-G%C3%B6reve_Haz%C4%B1r-success?style=for-the-badge&logo=nasa" alt="Göreve Hazır">
  <img src="https://img.shields.io/badge/S%C4%B1n%C4%B1f-Galactic_Class-gold?style=for-the-badge" alt="Galactic Class">
  <img src="https://img.shields.io/badge/Etkinlik-TUA_Astrohackathon-0052cc?style=for-the-badge" alt="TUA">
</div>

---

## 🌌 Genel Bakış (Galactic-Class)
**DeepSpace-Telemetry-AI**, Türkiye'nin uzay vizyonunu yıldızlararası seviyeye taşıyan, akademik derinlikli bir haberleşme simülasyon ve analiz ekosistemidir. Bu platform, yalnızca link bütçesi hesaplamakla kalmaz; olasılıksal risk analizi, rota optimizasyonu ve fiziksel anomali tespiti yaparak görev kontrol ekiplerine stratejik karar desteği sunar.

Sistem, **Master-Class** temelleri üzerine inşa edilen **Galactic-Class** genişlemesiyle; Dijkstra tabanlı röle ağları ve Monte Carlo yöntemli güvenilirlik modellerini içermektedir.

---

## 🚀 Zirve Seviye Teknik Özellikler

### 🛤️ 1. Dijkstra Rota Optimizasyonu (Relay Optimization)
*   **Akıllı Ağ:** Dünya'dan derin uzay sondasına kadar olan yolda (Moon-Gateway, Mars-Relay düğümleri üzerinden) en yüksek kümülatif SNR değerini sunan rotayı otomatik belirler.
*   **Dinamik Rota:** Düğümlerin konumuna göre anlık olarak en verimli haberleşme yolunu hesaplar.

### 🎲 2. Monte Carlo Güven Analizi (Statistical Reliability)
*   **1000+ Senaryo:** Atmosferik türbülans, güneş gürültüsü ve iyonosferik bozulmaları olasılıksal motorla simüle eder.
*   **Link Kullanılabilirliği:** Haberleşmenin hangi oranda (örneğin %99.9) kesintisiz devam edebileceğini istatistiksel olarak raporlar.

### 📡 3. Çok Disiplinli Fizik Motoru (RF & Optik)
*   **Lazer (Optik):** 1550nm lazer linkleri için foton istatistikleri ve yönelim hatası analizi.
*   **RF S-Band/X/Ka:** CCSDS uyumlu modülasyonlar (BPSK'dan 16-APSK'ya) ve ITU-R sönümleme modelleri.
*   **NASA DSN Entegrasyonu:** NASA'nın "DSN Now" servisinden alınan canlı verilerle operasyonel uyumluluk.

---

## 🖥️ Galactic Görev Kontrol Dashboard
Yenilenen **Streamlit** arayüzü, üç ana uzmanlık sekmesi sunar:
-   **📊 Standart Analiz:** 3D yörünge mekaniği ve temel link metrikleri.
-   **🧠 Galaktik Analiz Araçları:** Monte Carlo Histogramları ve Dijkstra Rota sonuçları.
-   **🌍 Yer Segmenti:** NASA DSN canlı istasyon durumu ve atmosferik kayıplar.

---

## 📂 Mimari Yapı
```text
📦 DeepSpace-Telemetry-AI
 ┣ 📂 src               # Çekirdek Kütüphane
 ┃ ┣ 📜 engine.py       # Fizik Motoru (RF/Optik)
 ┃ ┣ 📜 analyser.py     # Monte Carlo & Isı Haritaları
 ┃ ┣ 📜 relay.py        # Dijkstra Rota Optimizasyonu
 ┃ ┣ 📜 predictor.py    # AI Anomali Tespiti
 ┃ ┗ 📜 api_connector.py # NASA/DSN Canlı Entegrasyon
 ┣ 📂 docs              # Teknik Dokümantasyon
 ┃ ┗ 📜 akademik_teknik_rapor.md # Matematiksel Modeller Raporu
 ┣ 📜 app.py            # Galactic-Class Dashboard
 ┗ 📜 requirements.txt  # Bağımlılıklar
```

---

## 👨‍💻 Geliştirici
**Yunus Emre** | **TUA Astrohackathon 2026** kapsamında Türk Uzay Programı'nın teknik mükemmeliyet hedefleri doğrultusunda geliştirilmiştir.

---
<div align="center">
  <i>"Gözümüz Yükseklerde, Yolumuz Yıldızlar arası!"</i>
</div>
