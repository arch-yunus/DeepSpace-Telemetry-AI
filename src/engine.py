import numpy as np

class TelemetryEngine:
    """
    Core physics engine for Deep Space Telemetry degradation analysis.
    Implements Friis transmission, Ionospheric delay, and Thermal noise models.
    """
    
    # Constants
    C = 299792458  # Speed of light (m/s)
    KB = 1.380649e-23  # Boltzmann constant (J/K)
    
    def __init__(self):
        self.frequencies = {
            "X": 8.4e9,   # X-Band (8.4 GHz)
            "Ka": 32.0e9  # Ka-Band (32.0 GHz)
        }

    def calculate_fspl(self, distance_au, frequency_hz):
        """Free Space Path Loss (FSPL) calculator."""
        distance_m = distance_au * 1.496e11
        wavelength = self.C / frequency_hz
        fspl = (4 * np.pi * distance_m / wavelength) ** 2
        return 10 * np.log10(fspl)

    def calculate_ionospheric_delay(self, tec, frequency_hz):
        """
        Calculates group delay due to ionosphere.
        tec: Total Electron Content (10^16 electrons/m^2)
        """
        delay = (40.3 * tec * 1e16) / (self.C * (frequency_hz ** 2))
        return delay

    def calculate_thermal_noise(self, system_temp, bandwidth):
        """Thermal noise power in Watts."""
        noise_power = self.KB * system_temp * bandwidth
        return noise_power

    def calculate_snr(self, p_transmit_dbm, g_transmit_db, g_receive_db, fspl_db, noise_power_w, other_losses_db=0):
        """Calculates Signal-to-Noise Ratio (SNR) in dB."""
        # P_receive = P_transmit + G_transmit + G_receive - FSPL - Other
        p_receive_dbm = p_transmit_dbm + g_transmit_db + g_receive_db - fspl_db - other_losses_db
        
        # Convert noise power to dBm
        noise_dbm = 10 * np.log10(noise_power_w * 1000)
        
        snr_db = p_receive_dbm - noise_dbm
        return snr_db

if __name__ == "__main__":
    # Quick Test
    engine = TelemetryEngine()
    print("Engine initialized successfully.")
    dist = 1.52 # Mars distance in AU
    freq = engine.frequencies["X"]
    fspl = engine.calculate_fspl(dist, freq)
    print(f"FSPL at {dist} AU for X-band: {fspl:.2f} dB")
