import numpy as np

class MissionRelay:
    """
    Simulates a Multi-Hop Deep Space Relay (e.g. Lander -> MRO -> Earth).
    Calculates cumulative noise and end-to-end latency.
    """
    
    def __init__(self, engine):
        self.engine = engine
        
    def simulate_hop(self, p_tx, dist_au, freq_band="X"):
        """Simulates a single communication hop."""
        freq = self.engine.frequencies.get(freq_band, 8.4e9)
        fspl = self.engine.calculate_fspl(dist_au, freq)
        # Assuming fixed relay antenna gains
        snr = self.engine.calculate_snr(p_tx, 30, 30, fspl, 1e-15)
        latency = (dist_au * 1.496e11) / 299792458
        return snr, latency

    def calculate_end_to_end(self, hops_data):
        """
        hops_data: List of (p_tx, dist_au, freq_band)
        """
        total_latency = 0
        min_snr = 999
        
        for hop in hops_data:
            snr, lat = self.simulate_hop(*hop)
            total_latency += lat
            min_snr = min(min_snr, snr)
            
        return min_snr, total_latency
