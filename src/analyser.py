import numpy as np

class MonteCarloAnalyser:
    """
    Haberleşme linki için Monte Carlo simülasyon motoru.
    Binlerce senaryo üzerinden 'Link Kullanılabilirliği' (Link Availability) hesaplar.
    """
    
    def __init__(self, engine):
        self.engine = engine

    def run_simulation(self, base_snr, iterations=1000):
        """
        Atmosferik ve güneş gürültüsü varyasyonları ile SNR dağılımını simüle eder.
        """
        results = []
        for _ in range(iterations):
            # Rastgele atmosferik sönümleme (0-3 dB varyasyon)
            atmos_jitter = np.random.exponential(0.5)
            # Rastgele terminal gürültüsü (Güneş aktiviteleri kaynaklı)
            solar_jitter = np.random.normal(0, 1.5)
            
            simulated_snr = base_snr - atmos_jitter + solar_jitter
            results.append(simulated_snr)
            
        results = np.array(results)
        
        # İstatistikler
        stats = {
            "mean": np.mean(results),
            "std": np.std(results),
            "p05": np.percentile(results, 5), # %95 güven aralığı alt sınırı
            "availability": (results > 5.0).sum() / iterations * 100 # SNR > 5 dB olanların oranı
        }
        
        return results, stats

class CoverageMapper:
    """
    3D Uzayda sinyal gücü haritalandırma modülü.
    """
    def __init__(self, engine):
        self.engine = engine

    def generate_heat_map_data(self, center_au, radius_au, points=10):
        """
        Belirli bir bölge için 3D sinyal gücü verisi üretir.
        """
        x = np.linspace(center_au - radius_au, center_au + radius_au, points)
        y = np.linspace(center_au - radius_au, center_au + radius_au, points)
        z = np.linspace(-0.1, 0.1, points)
        
        X, Y, Z = np.meshgrid(x, y, z)
        
        # Güç hesabı (Basitleştirilmiş 1/R^2)
        dist = np.sqrt(X**2 + Y**2 + Z**2)
        strength = -20 * np.log10(dist + 1e-6) # Bağıl dB
        
        return X, Y, Z, strength
