# 📜 DeepSpace-Telemetry-AI: Akademik Teknik Rapor
**Sürüm:** Galactic-Class (Zirve) | **Yazar:** DeepSpace AI Ekibi | **Tarih:** Mart 2026

---

## 1. Giriş
Bu rapor, **TUA Astrohackathon** kapsamında geliştirilen Derin Uzay Haberleşme Simülasyon platformunun matematiksel ve fiziksel temellerini detaylandırmak amacıyla hazırlanmıştır. Sistem, radyo frekansı (RF) ve optik (lazer) haberleşme linklerini, gerçek astronomik veriler ve iyonosferik etkiler altında modellemektedir.

## 2. Matematiksel Modeller

### 2.1 Serbest Uzay Yol Kaybı (FSPL)
Sinyal yayılımındaki temel kayıp Friis iletim formülü ile hesaplanmaktadır:
$$FSPL (dB) = 20 \log_{10}(d) + 20 \log_{10}(f) + 20 \log_{10}(\frac{4\pi}{c})$$
Burada $d$ mesafe (metre), $f$ frekans (Hz) ve $c$ ışık hızıdır.

### 2.2 Atmosferik Sönümlenme
Dünya atmosferinden geçişte oluşan kayıp, **ITU-R P.676** ve **P.838** modellerinden türetilen basitleştirilmiş bir algoritma ile hesaplanır. Gaz sönümlemesi ($L_{gas}$) ve yağış sönümlemesi ($L_{rain}$), anten yükselim açısına ($\theta$) bağlı olarak:
$$L_{total} = \frac{L_{zenith}}{\sin(\theta)}$$
formülüyle normalize edilir.

### 2.3 Optik (Lazer) Haberleşme Linki
Optik haberleşmede SNR, foton sayma (Poisson istatistiği) üzerinden modellenir:
$$N_{photons} = \frac{P_{rx}}{h \cdot f}$$
Alınan güç ($P_{rx}$), Airy disk difraksiyon limitleri ve açıklık (aperture) kazançları dikkate alınarak hesaplanır.

## 3. Yapay Zeka ve Optimizasyon

### 3.1 Rota Optimizasyonu (Dijkstra)
Sistem, çok sıçramalı (multi-hop) haberleşme senaryolarında, mevcut röle düğümleri (Gateway, Mars Relay vb.) arasından en yüksek toplam SNR değerini sağlayan yolu bulmak için Dijkstra algoritmasını kullanır.

### 3.2 Monte Carlo Analiz Motoru
Haberleşme linkinin güvenilirliğini test etmek için 1000 iterasyonlu Monte Carlo simülasyonu uygulanır. Bu simülasyon, atmosferik türbülans ve güneş gürültüsünü olasılıksal (Stochastic) bir modelle ele alarak "Link Kullanılabilirliği" yüzdesini hesaplar.

---
*İstikbal Göklerdedir!*
