# 🛰️ DeepSpace-Telemetry-AI: Milli Uzay Teknolojileri Ekosistemi

<div align="center">
  <img src="https://img.shields.io/badge/Durum-G%C3%B6reve_Haz%C4%B1r-success?style=for-the-badge&logo=nasa" alt="Göreve Hazır">
  <img src="https://img.shields.io/badge/S%C4%B1n%C4%B1f-Milli_Vizyon-red?style=for-the-badge" alt="Milli Vizyon">
  <img src="https://img.shields.io/badge/Etkinlik-TUA_Astrohackathon-0052cc?style=for-the-badge" alt="TUA">
</div>

---

## 🌌 Genel Bakış
**DeepSpace-Telemetry-AI**, Türkiye'nin derin uzay hedefleri (Ay Projesi, Mars ve ötesi) için haberleşme linklerini yüksek sadakatle modelleyen, analiz eden ve yapay zeka ile optimize eden yerli bir simülasyon platformudur.

Bu ekosistem, teorik astrofizik verilerini operasyonel telekomünikasyon standartlarıyla birleştirerek; **Skyfield tabanlı yörünge mekaniği**, **CCSDS standartlarında modülasyon analizi** ve **Lazer (Optik) haberleşme modelleme** yeteneklerini tek bir platformda sunar.

---

## 🚀 Temel Teknoloji Sütunları

### 📡 1. Yüksek Hassasiyetli Fizik Motoru
*   **Yörünge Hassasiyeti:** NASA/JPL DE421 ephemeris verileri kullanılarak Dünya ve hedef gezegen konumları anlık hesaplanır.
*   **Yayılım Modelleri:** FSPL, Atmosferik Gaz/Yağmur sönümlenmesi (ITU-R P.676) ve İyonosferik Sintilasyon (Nakagami-m).
*   **Güneş Girişimi:** Sun-Earth-Probe (SEP) açısına bağlı dinamik gürültü sıcaklığı modellemesi.

### 💡 2. İleri Seviye Haberleşme Modelleri
*   **RF Standartları:** CCSDS uyumlu BPSK, QPSK, 8-PSK ve 16-APSK modülasyon performans analizleri.
*   **Optik (Lazer) Bağlantılar:** 1550nm lazer linkleri için foton sayma istatistikleri ve yönelim hatası (jitter) analizleri.
*   **Milli Görev Profilleri:** TUA Ay Projesi ve derin uzay testleri için özelleştirilmiş parametreler.

### 🤖 3. Yapay Zeka ve Tahminleme
*   **SNR Tahmini:** Güneş akısı ve geçmiş verilere dayalı sinyal kalitesi trend analizi.
*   **Anomali Tespiti:** Sinyaldeki ani düşüşleri ve fiziksel tutarsızlıkları 3-Sigma motoru ile yakalama.
*   **Canlı Veri:** NASA Deep Space Network (DSN Now) üzerinden anlık istasyon durumu entegrasyonu.

---

## 🖥️ İnteraktif Milli Vizyon Dashboard
Proje, görev kontrol personeli için profesyonel bir **Streamlit** arayüzü sunar.

### Özellikler:
-   **3D Yörünge Görünümü:** Sun, Dünya ve hedef gezegenlerin anlık konumları ve haberleşme vektörü.
-   **Link Bütçesi Analizörü:** SNR, BER ve Kapasite değerlerinin gerçek zamanlı hesaplanması.
-   **TUA Görev Profilleri:** Ay Projesi, Mars Testi ve Jüpiter Flyby senaryoları.
-   **DSN Canlı Durum:** Aktif yer istasyonlarının anlık çalışma durumları.

### Hızlı Başlangıç:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Mimari Yapı
```text
📦 DeepSpace-Telemetry-AI
 ┣ 📂 src              # Çekirdek Kütüphane
 ┃ ┣ 📜 engine.py      # Fizik ve Modülasyon (RF/Optik)
 ┃ ┣ 📜 predictor.py   # AI Tahmin ve Anomali Tespiti
 ┃ ┣ 📜 relay.py       # Çok Sıçramalı Röle Mantığı
 ┃ ┣ 📜 scheduler.py   # DSN İstasyon Atayıcı
 ┃ ┗ 📜 api_connector.py # NASA DSN ve Uzay Havası API'leri
 ┣ 📂 simulations      # Görev Senaryoları
 ┣ 📂 docs             # Teknik Raporlar ve Grafikler
 ┣ 📜 app.py           # Streamlit Milli Vizyon Dashboard
 ┗ 📜 requirements.txt # Sistem Bağımlılıkları
```

---

## 👨‍💻 Geliştirici
**Yunus Emre** | Çok Disiplinli Sistem Tasarımcısı | Yapay Zeka ve Uzay Bilimleri Uygulayıcısı  
**TUA Astrohackathon 2026** kapsamında Türk Uzay Programı vizyonu için geliştirilmiştir.

---
<div align="center">
  <i>"İstikbal Göklerdedir!"</i>
</div>
