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

    def get_planetary_positions(self, date_str=None):
        """
        Uses Skyfield to get Earth and Mars positions.
        Returns distance in AU and SEP angle in degrees.
        """
        try:
            from skyfield.api import load
            planets = load('de421.bsp')
            earth, mars, sun = planets['earth'], planets['mars'], planets['sun']
            ts = load.timescale()
            t = ts.now() if not date_str else ts.utc(*map(int, date_str.split('-')))
            
            e_pos = earth.at(t).position.au
            m_pos = mars.at(t).position.au
            s_pos = sun.at(t).position.au
            
            # Distance Earth-Mars
            dist = np.linalg.norm(m_pos - e_pos)
            
            # SEP Angle (Sun-Earth-Probe)
            v_earth_sun = s_pos - e_pos
            v_earth_mars = m_pos - e_pos
            
            # dot product / (norm1 * norm2) = cos(theta)
            unit_v1 = v_earth_sun / np.linalg.norm(v_earth_sun)
            unit_v2 = v_earth_mars / np.linalg.norm(v_earth_mars)
            sep_angle = np.degrees(np.arccos(np.clip(np.dot(unit_v1, unit_v2), -1.0, 1.0)))
            
            return dist, sep_angle, {"earth": e_pos, "mars": m_pos, "sun": s_pos}
        except Exception:
            # Fallback to defaults if skyfield not installed or fails
            return 1.52, 5.0, None

    def calculate_atmospheric_loss(self, elevation_deg, rain_rate_mm_h=0):
        """
        Calculates attenuation due to Earth's atmosphere (Gas + Rain).
        Simplified ITU-R models.
        """
        # Gas attenuation (O2/H2O) base ~0.5 dB at zenith (90 deg)
        gas_loss = 0.5 / np.sin(np.radians(max(5, elevation_deg)))
        
        # Rain attenuation placeholder
        rain_loss = (rain_rate_mm_h * 0.1) / np.sin(np.radians(max(5, elevation_deg)))
        
        return gas_loss + rain_loss

    def calculate_ber(self, snr_db, modulation="BPSK"):
        """
        Calculates Bit Error Rate (BER) for various CCSDS modulations.
        """
        snr_linear = 10 ** (snr_db / 10.0)
        from scipy.special import erfc
        
        if modulation == "BPSK" or modulation == "QPSK":
            ber = 0.5 * erfc(np.sqrt(snr_linear))
        elif modulation == "8-PSK":
            # Approximation for M-PSK
            ber = (2 / 3) * 0.5 * erfc(np.sqrt(3 * snr_linear) * np.sin(np.pi / 8))
        elif modulation == "16-APSK":
            # High-order proxy
            ber = 0.5 * erfc(np.sqrt(0.5 * snr_linear))
        else:
            ber = 0.5 * erfc(np.sqrt(snr_linear))
            
        return max(ber, 1e-15)

    def calculate_snr(self, p_transmit_dbm, g_transmit_db, g_receive_db, fspl_db, noise_power_w, t_solar=0, fec_gain_db=0, atmos_loss_db=0, other_losses_db=0):
        """Calculates total SNR including all Phase 4 factors."""
        t_sys_assumed = 25.0
        scale_factor = (t_sys_assumed + t_solar) / t_sys_assumed
        total_noise_w = noise_power_w * scale_factor
        
        p_receive_dbm = p_transmit_dbm + g_transmit_db + g_receive_db - fspl_db - atmos_loss_db - other_losses_db
        noise_dbm = 10 * np.log10(total_noise_w * 1000)
        
        snr_db = p_receive_dbm - noise_dbm + fec_gain_db
        return snr_db

if __name__ == "__main__":
    # Quick Test
    engine = TelemetryEngine()
    print("Engine initialized successfully.")
    dist = 1.52 # Mars distance in AU
    freq = engine.frequencies["X"]
    fspl = engine.calculate_fspl(dist, freq)
    print(f"FSPL at {dist} AU for X-band: {fspl:.2f} dB")
