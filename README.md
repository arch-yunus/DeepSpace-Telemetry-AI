# 🛰️ DeepSpace-Telemetry-AI: Derin Uzay Sinyal Bozulum ve Gürültü Modeli

![TUA Astrohackathon](https://img.shields.io/badge/Etkinlik-TUA_Astrohackathon-0052cc?style=flat-square)
![Milli Uzay Programı](https://img.shields.io/badge/Hedef-Teorik_Bilimsel_Araştırma-e60000?style=flat-square)
![Sürüm](https://img.shields.io/badge/Sürüm-v1.0.0--beta-orange?style=flat-square)
![Teknoloji](https://img.shields.io/badge/Teknoloji-SciPy_%7C_DSP_%7C_Physics_Engine-2ea44f?style=flat-square)

## 🌌 Yüksek Düzey Özet
**DeepSpace-Telemetry-AI**, derin uzay görevlerindeki (Ay, Mars ve ötesi) uzay araçları ile Dünya'daki yer istasyonları arasındaki telemetri sinyallerinin, uzay havası (Space Weather) koşullarından nasıl etkilendiğini analiz eden ve yapay zeka ile optimize eden teorik bir fizik motorudur.

Sistem; Güneş rüzgarları, Koronal Kütle Atımları (CME), kozmik arka plan ışıması ve Dünya'nın iyonosfer tabakasındaki plazma yoğunluklarının X-Band ve Ka-Band radyo sinyallerinde yarattığı faz kaymalarını ve sintilasyon (scintillation) gürültülerini uzay fiziği denklemleriyle modeller.

---

## 🚀 Araştırma Problemi ve Mühendislik Kısıtları
Derin uzaydan gelen bir sinyal, Dünya'ya ulaşana kadar zorlu bir ortamdan geçer. Karşılaşılan temel sinyal bozulum faktörleri şunlardır:
1. **İyonosferik Gecikme:** Serbest elektronların radyo dalgalarını kırması ve sinyal zarfında hızlı genlik/faz dalgalanmaları yaratması.
2. **Güneş Plazması Girişimi:** Uzay aracının Dünya ve Güneş ile aynı hizaya (Solar Conjunction) geldiği durumlarda artan termal gürültü.
3. **Serbest Uzay Yol Kaybı (FSPL):** Sinyalin kat ettiği devasa mesafeye bağlı olarak enerjisinin ters kare yasasına göre sönümlenmesi.

Bu model, iletişim kopukluklarını önceden tahmin etme ve Sinyal-Gürültü Oranını (SNR) maksimize edecek algoritmik bir Karar Destek mekanizması sunar.

---

## 🛠️ Teorik Çerçeve ve Fiziksel Denklemler
Projenin çekirdek simülasyon motoru, aşağıdaki temel astrofizik ve telekomünikasyon denklemlerini kullanarak anlık gürültü profilleri üretir:

### 1. İyonosferik Gecikme Modeli
Radyo sinyalinin iyonosferden geçerken maruz kaldığı grup gecikmesi ($\Delta\tau$), Toplam Elektron İçeriği (TEC - Total Electron Content) ve sinyal frekansına ($f$) bağlıdır:

$$\Delta\tau = \frac{40.3 \times TEC}{c \cdot f^2}$$

*(Model, $c$ ışık hızını sabit alarak NOAA'dan çekilen anlık TEC verilerini bu formüle besler.)*

### 2. Termal Gürültü ve Güneş Plazma Modeli
Alıcı antenin sistem sıcaklığına ($T_s$) ve Güneş'ten gelen arka plan gürültüsüne bağlı olarak oluşan termal gürültü gücü ($P_N$) Nyquist teoremine göre hesaplanır:

$$P_N = k_B \cdot T_s \cdot B$$

*($k_B$: Boltzmann sabiti, $B$: Alıcının bant genişliği)*

### 3. Friis İletim Denklemi
Uzay aracından iletilen gücün ($P_t$), mesafeye ($d$) ve anten kazançlarına ($G_t, G_r$) göre yer istasyonuna ulaştığındaki son değeri:

$$P_r = P_t \cdot G_t \cdot G_r \left(\frac{\lambda}{4\pi d}\right)^2$$

### 4. Toplam Sinyal-Gürültü Oranı (SNR)
Sistem, tüm bozucu etkileri birleştirerek nihai iletişim kalitesini desibel (dB) cinsinden sürekli optimize eder:

$$SNR_{dB} = 10 \log_{10} \left( \frac{P_r}{P_N + P_{cme} + P_{iono}} \right)$$

---

## 🏗️ Sistem Mimarisi ve Veri Hattı
1. **Uzay Havası Veri Entegrasyonu:** NASA (SDO) ve NOAA API'leri üzerinden anlık Güneş lekesi aktivitesi ve TEC haritaları sisteme çekilir.
2. **Fizik Motoru (DSP & Physics):** Gelen veriler, matematiksel modellere sokularak sinyal zayıflama matrisleri oluşturulur.
3. **Makine Öğrenmesi ile Tahmin:** Geçmiş bozulum verileri eğitilerek, gelecekteki olası sinyal kesintilerini önceden tahmin eden zaman serisi algoritmaları (Time-Series AI) çalıştırılır.

---

## 📂 Depo Yapısı (Repository Structure)

```text
DeepSpace-Telemetry-AI/
├── app.py                      # Streamlit Interactive Dashboard
├── docs/                       # Teorik raporlar ve grafikler
├── data/                       # Tarihsel CME ve TEC veri setleri
├── src/                        # Çekirdek motor ve modüller
│   ├── engine.py               # BER/FEC modelleri ve fiziksel denklemler
│   ├── predictor.py            # AI SNR Tahminleyici
│   ├── api_connector.py        # Dış veri entegrasyonu
│   └── scheduler.py            # DSN İstasyon Seçici (Multi-node)
├── simulations/                # Simülasyon senaryoları
│   ├── run_simulation.py      # Temel simülasyon
│   └── trajectory_sim.py      # 30 günlük görev simülasyonu
├── LICENSE                     # MIT Lisansı
├── requirements.txt            # Bağımlılıklar
└── README.md                   # Proje ana belgesi
```

---

## 💻 Kurulum ve Simülasyon
Geliştirilen sistemi yerel ortamınızda çalıştırmak için:

### 1. Etkileşimli Dashboard (Önerilen)
Gerçek zamanlı parametre analizi için:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. Yörünge Simülasyonu
30 günlük bir transiti analiz etmek ve grafik üretmek için:
```bash
python simulations/trajectory_sim.py
```

---

## 🌓 Proje Özellikleri (+Phase 3)
- **Hata Oranı (BER) Analizi:** BPSK/QPSK modülasyonları için teorik Bit Error Rate hesaplaması.
- **FEC Kazancı:** Reed-Solomon, Turbo ve LDPC kodlama tekniklerinin sinyal üzerindeki iyileştirici etkisi.
- **Akıllı DSN Zamanlayıcı:** Uzay aracının konumuna göre en uygun yer istasyonunun (Goldstone, Madrid, Canberra) otomatik seçimi.
- **Yapay Zeka Destekli Tahmin:** Güneş akısı verileriyle SNR düşüşlerini önceden raporlama.

---

## 🔮 Gelecek Vizyonu
- [ ] Derin uzay optik haberleşmesinde (Lazer iletişimi) atmosferik türbülansın yaratacağı foton sağılımlarını hesaplayacak modellerin sisteme entegrasyonu.
- [ ] Çoklu yer istasyonu dizilimleri kullanılarak sinyal bozulumunun interferometri teknikleriyle filtrelenmesi.

---

## 👨‍💻 Geliştirici
Bu proje, **TUA Astrohackathon** etkinliği kapsamında geliştirilmiştir.

**Tasarım ve Araştırma:** Multi-Disciplinary Systems Designer | Solopreneur | AI & Industrial Optimization
