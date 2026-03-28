import numpy as np

class LivingTelemetry:
    """
    Kendi kendini optimize eden 'Yaşayan' telemetri protokolü.
    Ortam SNR değerine göre modülasyon ve veri hızını anlık (sub-ms) değiştirir.
    """
    def __init__(self):
        self.active_protocol = "Adaptive-v1"

    def adaptive_protocol_shift(self, current_snr):
        """
        SNR'a göre en verimli kodlama/modülasyon kombinasyonunu seçer.
        """
        if current_snr > 25:
            return "64-QAM (Ultra High Speed)", 5.0 # Gbps
        elif current_snr > 15:
            return "16-APSK (High Reliability)", 1.2
        elif current_snr > 5:
            return "QPSK (Safe Mode)", 0.5
        else:
            return "BPSK-Extended (Survival Mode)", 0.01

class StationDAO:
    """
    Merkezi olmayan yer istasyonu yönetim sistemi.
    İstasyonlar (Ankara, Erzurum, NASA DSN vb.) en düşük enerji/en yüksek SNR için 'ihale' usulü çalışır.
    """
    def __init__(self):
        self.stations = {
            "Ankara-1": {"power_cost": 0.5, "base_gain": 70},
            "Erzurum-HGT": {"power_cost": 0.2, "base_gain": 74}, # Yüksek rakım avantajı
            "Madrid-DSN": {"power_cost": 0.8, "base_gain": 72},
            "Canberra-DSN": {"power_cost": 0.9, "base_gain": 72}
        }

    def bid_for_link(self, target_elevation):
        """
        İstasyonlar arası otomatik seçim ihalesi.
        """
        best_station = None
        max_score = -1
        
        for name, data in self.stations.items():
            # Skor = Kazanç / (Güç Maliyeti * Atmosferik Etki Proxy)
            score = data["base_gain"] / (data["power_cost"] + 0.1)
            if score > max_score:
                max_score = score
                best_station = name
                
        return best_station, max_score
