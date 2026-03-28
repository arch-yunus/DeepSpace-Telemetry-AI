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

    def calculate_solar_conjunction_noise(self, sep_angle_deg):
        """
        Models noise temperature increase due to Solar Conjunction.
        SEP (Sun-Earth-Probe) angle in degrees.
        """
        # Empirical model for noise temperature increase (T_sun)
        # Based on typical DSN performance near solar conjunction
        if sep_angle_deg < 0.1:
            return 50000  # Extreme interference
        elif sep_angle_deg < 2.0:
            return 1000 * (1.0 / sep_angle_deg**2)
        else:
            return 0

    def calculate_scintillation_loss(self, m_parameter, frequency_hz):
        """
        Models signal fading due to ionospheric scintillation using Nakagami-m.
        Returns a statistical 'worst-case' loss in dB.
        """
        # Simplification: Higher m means less fading (m=1 is Rayleigh)
        # We return a margin needed to combat fading
        fading_margin = 10 * np.log10(m_parameter) # Placeholder heuristic
        return float(max(0.0, 5.0 / m_parameter)) 

    def calculate_snr(self, p_transmit_dbm, g_transmit_db, g_receive_db, fspl_db, noise_power_w, t_solar=0, other_losses_db=0):
        """Calculates Signal-to-Noise Ratio (SNR) in dB."""
        # Update noise power with solar contribution
        # P_noise = k * (T_sys + T_solar) * B
        # Since noise_power_w already includes T_sys, we add solar part
        # noise_power_w = k * T_sys * B 
        # T_sys = noise_power_w / (k * B)
        # Total T = T_sys + T_solar
        
        # For simplicity, we assume noise_power_w passed is the base thermal noise
        # and we scale it up by (T_sys + T_solar) / T_sys
        t_sys_assumed = 25.0
        scale_factor = (t_sys_assumed + t_solar) / t_sys_assumed
        total_noise_w = noise_power_w * scale_factor
        
        p_receive_dbm = p_transmit_dbm + g_transmit_db + g_receive_db - fspl_db - other_losses_db
        noise_dbm = 10 * np.log10(total_noise_w * 1000)
        
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
