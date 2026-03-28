# 🛰️ DeepSpace-Telemetry-AI: Omega-Class Telemetri Analiz ve Optimizasyon Ekosistemi

![TUA Astrohackathon](https://img.shields.io/badge/Etkinlik-TUA_Astrohackathon-0052cc?style=flat-square)
![Milli Uzay Programı](https://img.shields.io/badge/Hedef-Derin_Uzay_Haberleşmesi-e60000?style=flat-square)
![Sürüm](https://img.shields.io/badge/Sürüm-v2.0.0--omega-purple?style=flat-square)
![Teknoloji](https://img.shields.io/badge/Teknoloji-Skyfield_%7C_CCSDS_%7C_Plotly-2ea44f?style=flat-square)

## 🌌 Proje Hakkında
**DeepSpace-Telemetry-AI**, derin uzay görevlerinde (Mars, Jüpiter ve ötesi) karşılaşılan devasa sinyal bozulumlarını ve gürültü faktörlerini gerçek zamanlı olarak modelleyen, analiz eden ve optimize eden yüksek sadakatli (high-fidelity) bir teknik ekosistemdir.

Bu sistem, sıradan bir simülasyondan öte; **Skyfield** kütüphanesi ile gerçek gezegen ephemeris verilerini kullanarak anlık yörünge geometrisi hesaplar, **CCSDS (Consultative Committee for Space Data Systems)** standartlarında modülasyon performanslarını analiz eder ve etkileşimli 3D arayüzü ile operatörlere bir karar destek mekanizması sunar.

---

## 🛠️ Teknik Kapasite ve Özellikler

### 1. Dinamik Astronomik Geometri (High-Fidelity)
*   **Gerçek Zamanlı Yörünge Verisi:** `skyfield` entegrasyonu ile Dünya ve Mars'ın J2000 koordinatlarındaki anlık konumlarını kullanarak hassas mesafe ($d$) hesaplaması yapar.
*   **Dinamik SEP Açısı:** Sun-Earth-Probe (SEP) açısını anlık hesaplayarak Güneş kavuşumu (Solar Conjunction) dönemlerindeki gürültü sıcaklığını ($T_{sun}$) otomatik belirler.

### 2. CCSDS Standartlarında İletişim Analizi
*   **Gelişmiş Modülasyon Modelleri:** BPSK, QPSK, 8-PSK ve 16-APSK modülasyonları için teorik Bit Error Rate (BER) eğrilerini modeller.
*   **Hata Düzeltme Kodları (FEC):** Reed-Solomon, Turbo ve LDPC kodlarının sağladığı sinyal kazançlarını (Coding Gain) hesaba katarak bağlantı bütçesini (Link Budget) optimize eder.

### 3. Atmosferik ve Uzay Havası Modelleri
*   **ITU-R Uyumlu Atmosferik Kayıp:** Anten yükselim açısı (Elevation) ve yağmur oranına bağlı olarak atmosferik gaz sönümlenmesini ($L_{atmos}$) hesaplar.
*   **İyonosferik Sintilasyon:** Nakagami-m dağılımı ile iyonosferdeki plazma yoğunluklarının yarattığı dalgalanmaları modeller.

---

## 📊 Matematiksel Temeller

### Sinyal-Gürültü Oranı (Total Link Budget)
Sistem, nihai SNR değerini hesaplarken şu denklemi temel alır:
$$SNR_{total} = P_{tx} + G_{tx} + G_{rx} - L_{fspl} - L_{atmos} - L_{scintillation} + G_{fec} - 10\log_{10}(k(T_{sys} + T_{sun})B)$$

### Bit Error Rate (BER) Analizi
Farklı modülasyonlar için hata olasılığını $Q$-fonksiyonu üzerinden hesaplar:
$$P_b \approx \frac{2}{\log_2 M} Q\left(\sqrt{2\frac{E_b}{N_0}}\sin\frac{\pi}{M}\right)$$

---

## 🖥️ İnteraktif Dashboard (Omega UI)

Proje, operasyonel kullanım için profesyonel bir **Streamlit** arayüzü sunar.

### Uygulama Bileşenleri:
-   **3D Orbit View:** Plotly tabanlı 3D sahne üzerinde Güneş, Dünya ve Mars'ın anlık konumları ve haberleşme vektörü.
-   **Real-time Link Budget:** Parametreler değiştikçe (yağmur oranı, modülasyon tipi vb.) anlık güncellenen SNR ve BER metrikleri.
-   **Link Status:** Sinyalin kararlılık durumunu (OPERATIONAL / CRITICAL) belirleyen akıllı uyarı sistemi.

#### Dashboard'u Çalıştırma:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Repository Yapısı
```text
DeepSpace-Telemetry-AI/
├── app.py                      # Omega-Class Etkileşimli Dashboard (Main UI)
├── docs/                       # Teknik raporlar ve analiz grafikleri
│   ├── teorik_fizik_raporu.md  # Detaylı fiziksel modeller dökümanı
│   └── snr_analysis_plot.png   # 30 günlük yörünge analizi çıktısı
├── src/                        # Çekirdek Kütüphane
│   ├── engine.py               # Fizik Motoru (Skyfield & CCSDS Entegrasyonu)
│   ├── predictor.py            # AI Trend Tahminleyici
│   ├── api_connector.py        # Uzay Havası Veri Bağlayıcısı
│   └── scheduler.py            # DSN İstasyon Zamanlayıcısı
├── simulations/                # Senaryo Koşturucular
├── LICENSE                     # MIT
└── requirements.txt            # Bağımlılıklar (Skyfield, Plotly, Streamlit vb.)
```

---

## 🔮 Gelecek Vizyonu
-   **Optical Comm Support:** Ka-Band ötesinde derin uzay lazer haberleşme (Optical Link) modellerinin entegrasyonu.
-   **Multi-Hop Relay Logic:** Mars yörüngesindeki uydular üzerinden (Relay) aktarmalı haberleşme bütçesinin hesaplanması.
-   **Real Space Data:** Deep Space Network (DSN) Now API'sinden anlık gerçek anten verilerinin çekilmesi.

---

## 👨‍💻 Geliştirici
Bu proje, **TUA Astrohackathon 2026** kapsamında geliştirilmiş "Omega-Class" bir sistemdir.

**Contact:** [Yunus Emre] | Multi-Disciplinary Systems Designer | AI & Space Science Implementation
