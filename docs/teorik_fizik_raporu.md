# 📑 DeepSpace-Telemetry-AI: Teorik Fizik ve Analiz Raporu

## 1. Giriş
Derin uzay haberleşmesi, Dünya atmosferi ve Güneş sistemi içindeki çeşitli bozucu etkiler nedeniyle yüksek derecede gürültüye maruz kalır. Bu rapor, projenin temelini oluşturan fiziksel modelleri ve simülasyon sonuçlarını detaylandırır.

## 2. Fiziksel Modeller
### 2.1. Serbest Uzay Yol Kaybı (FSPL)
Sinyal gücü, katedilen mesafenin karesiyle ters orantılı olarak azalır:
$$L_{fspl} = \left(\frac{4\pi d f}{c}\right)^2$$
Bu modelde mesafe ($d$) Astronomik Birim (AU) cinsinden hesaplanarak X-Band (8.4 GHz) frekansına uygulanmıştır.

### 2.2. Güneş Kavuşumu (Solar Conjunction)
Uzay aracı, Dünya ve Güneş ile aynı doğrultuya yaklaştığında, Güneş'in radyo gürültüsü antenin sistem sıcaklığını ($T_{sys}$) dramatik şekilde artırır. Modelimiz, SEP (Sun-Earth-Probe) açısına bağlı olarak gürültü sıcaklığını şu şekilde simüle eder:
$$T_{sun} \approx 1000 \cdot \left(\frac{1}{\theta_{sep}^2}\right)$$

### 2.3. İyonosferik Sintilasyon
İyonosferdeki plazma düzensizlikleri sinyalde hızlı faz ve genlik dalgalanmalarına (sintilasyon) yol açar. Bu durum Nakagami-m dağılımı ile modellenerek sinyal marjı hesaplanmıştır.

## 3. Yapay Zeka ile SNR Tahmini
Geliştirilen **TelemetryPredictor** modülü, anlık Güneş akısı (Solar Flux) verilerini kullanarak 24 saat sonraki SNR değerini tahmin eder. Bu, yer istasyonlarının veri hızlarını (data rate) proaktif olarak ayarlamasına olanak tanır.

## 4. Simülasyon Sonuçları
30 günlük bir Earth-Mars transiti simülasyonunda:
- **Solar Conjunction** döneminde (15. gün dolayları) SNR değerinin 5 dB altına düştüğü ve iletişimin riskli bölgeye girdiği gözlemlenmiştir.
- Mesafe artışına bağlı sönümlenmenin lineer bir düşüş yarattığı, ancak güneş aktivitelerinin bu düşüşe ani "spike" gürültüler eklediği doğrulanmıştır.

---
*Bu rapor TUA Astrohackathon 2026 için hazırlanmıştır.*
