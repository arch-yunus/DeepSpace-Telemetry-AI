import numpy as np

class DSNScheduler:
    """
    Deep Space Network (DSN) Station Scheduler.
    Selects the best ground station (Goldstone, Madrid, Canberra) 
    based on the spacecraft's current visibility and signal quality.
    """
    
    def __init__(self):
        self.stations = {
            "Goldstone": {"lat": 35.4, "lon": -116.8, "gain_adj": 0.0},
            "Madrid": {"lat": 40.4, "lon": -4.2, "gain_adj": -0.5},
            "Canberra": {"lat": -35.4, "lon": 148.9, "gain_adj": -0.2}
        }
        
    def get_best_station(self, sc_lon, current_snr):
        """
        Simplistic logic to pick a station based on longitude 'visibility'.
        In reality, this involves complex orbit geometry.
        """
        # Distribute stations roughly 120 degrees apart
        # Goldstone (-116), Madrid (-4), Canberra (+148)
        
        # Mock visibility check
        best_station = "Goldstone"
        max_score = -999
        
        for name, data in self.stations.items():
            # Distance from station longitude to SC longitude
            diff = abs(data["lon"] - sc_lon) % 360
            visibility_score = 100 - min(diff, 360-diff)
            
            # Combine visibility with station-specific gain adjustments
            total_score = visibility_score + data["gain_adj"]
            
            if total_score > max_score:
                max_score = total_score
                best_station = name
                
        return best_station, max_score
