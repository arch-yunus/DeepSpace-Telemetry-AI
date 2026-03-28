# 📑 DeepSpace-Telemetry-AI: Omega-Class Teknik Gelişim Raporu

## 1. Yüksek Sadakatli Yörünge Geometrisi
Projenin Phase 4 (Omega) aşamasında, statik mesafe tahminleri yerine gerçek zamanlı astronomik hesaplamalar getirilmiştir.
- **Skyfield & DE421 Ephemeris:** NASA/JPL tarafından sağlanan DE421 ephemeris verileri kullanılarak Dünya, Ay, Güneş ve Mars konumları J2000 eylemsizlik çerçevesinde hesaplanır.
- **SEP Analizi:** Sinyalin Güneş diskine olan açısal yakınlığı (Sun-Earth-Probe angle) hesaplanarak, Güneş taç küresinden (Corona) kaynaklanan termal gürültü artışı dinamik olarak modele eklenir.

## 2. Haberleşme Standartları (CCSDS)
Derin uzay haberleşme protokollerine uygun olarak sistem şu kapasiteleri kazanmıştır:
### 2.1. Modülasyon Modelleri
- **8-PSK & 16-APSK:** Spektral verimliliği yüksek modülasyonların derin uzaydaki BER (Bit Error Rate) performansları, AWGN kanalı ve iyonosferik sintilasyon etkileri altında modellenmiştir.
### 2.2. Atmosferik Kayıplar (Ground Segment)
- **ITU-R P.676 & P.838:** Yer istasyonu segmentindeki kayıplar için anten yükselim açısı ($\epsilon$) ve yağmur yoğunluğu ($R$) parametrelerine bağlı sönümleme modelleri entegre edilmiştir.

## 3. İnteraktif Karar Destek Sistemi
`app.py` üzerinden sunulan interaktif dashboard, operatörlerin farklı görev senaryolarını "What-If" analizi ile test etmesine olanak tanır. 3D Plotly görselleştirmesi ile uzaysal geometri anlık olarak takip edilebilir.

## 4. Sonuç ve Değerlendirme
DeepSpace-Telemetry-AI, teorik fizik denklemlerini modern yazılım araçları ve AI tahminleme mekanizmalarıyla birleştirerek, Türkiye'nin derin uzay hedeflerine yönelik haberleşme altyapısı analizlerinde kullanılmak üzere tasarlanmıştır.

---
*Bu rapor TUA Astrohackathon 2026 için Omega-Class güncellemesiyle hazırlanmıştır.*
