import random
import time

class SpaceWeatherAPI:
    """
    Mock API Connector for NASA/NOAA data streams.
    Simulates real-time ingestion of Solar Flux and TEC maps.
    """
    
    def __init__(self):
        self.base_url = "https://api.spaceweather.gov/v1/"
        
    def get_current_solar_flux(self):
        """Simulates fetching an F10.7 solar flux index."""
        # Random flux between 70 (quiet) and 250 (active)
        return random.uniform(70, 250)
    
    def get_tec_map(self):
        """Simulates fetching Total Electron Content (TEC) data."""
        return {
            "timestamp": time.time(),
            "global_avg_tec": random.uniform(5, 100),
            "region": "Global"
        }

    def fetch_latest_cme_events(self):
        """Simulates fetching Coronal Kütle Atımı events."""
        if random.random() > 0.8:
            return [{"id": "CME-2026-001", "intensity": "X-Class", "direction": "Earth-facing"}]
        return []
