import numpy as np

class SwarmCoordinator:
    """
    Otonom uydu sürüsü koordinasyon ve kazanç hesaplama modülü.
    Yüzlerce ufak uydunun (CubeSat) birleşerek dev bir anten gibi çalışmasını simüle eder.
    """
    
    def __init__(self):
        self.swarm_size = 100 # Varsayılan sürü büyüklüğü

    def calculate_array_gain(self, n_satellites=None):
        """
        Sürüdeki uydu sayısına bağlı olarak link bütçesine eklenen kazanç (dB).
        Formül: 10 * log10(N)
        """
        n = n_satellites if n_satellites else self.swarm_size
        gain = 10 * np.log10(n)
        return gain

    def simulate_phased_array_alignment(self, jitter_level=0.1):
        """
        Sürü uydularının faz dizilimi hassasiyetini simüle eder.
        """
        alignment_efficiency = np.exp(-jitter_level)
        return alignment_efficiency
