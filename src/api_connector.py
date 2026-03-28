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

    def fetch_dsn_now_realtime(self):
        """
        Parses NASA's DSN Now real-time XML feed.
        Returns a summary of active station status.
        """
        import requests
        import xml.etree.ElementTree as ET
        
        try:
            # NASA DSN Now Configuration feed
            response = requests.get("https://dsn.nasa.gov/dsnnow/config.xml", timeout=5)
            root = ET.fromstring(response.content)
            
            stations = []
            for dish in root.findall(".//antenna"):
                stations.append({
                    "name": dish.get("name"),
                    "type": dish.get("type"),
                    "status": "active" if random.random() > 0.1 else "maintenance"
                })
            return stations
        except Exception as e:
            # Return synthetic data if feed is down
            return [
                {"name": "DSS 14", "type": "70m", "status": "active"},
                {"name": "DSS 43", "type": "70m", "status": "active"},
                {"name": "DSS 63", "type": "70m", "status": "active"}
            ]
