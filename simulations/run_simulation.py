import sys
import os
import argparse

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine import TelemetryEngine

def run_scenario(distance_au, band, tec_level):
    engine = TelemetryEngine()
    
    # Parameters
    freq = engine.frequencies.get(band, engine.frequencies["X"])
    p_tx = 43  # 20W Transmit Power (43 dBm)
    g_tx = 48  # High gain antenna on spacecraft
    g_rx = 70  # 70m DSN antenna gain
    bw = 1e6   # 1 MHz bandwidth
    t_sys = 25 # System temperature (K)
    
    tec_values = {"Low": 5, "Medium": 25, "High": 80}
    tec = tec_values.get(tec_level, 25)
    
    # Calculations
    fspl = engine.calculate_fspl(distance_au, freq)
    delay = engine.calculate_ionospheric_delay(tec, freq)
    p_noise = engine.calculate_thermal_noise(t_sys, bw)
    snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise)
    
    print("="*40)
    print(" DEEP SPACE TELEMETRY SIMULATION ")
    print("="*40)
    print(f"Distance:      {distance_au} AU")
    print(f"Band:          {band}")
    print(f"TEC level:     {tec_level} ({tec} units)")
    print("-" * 40)
    print(f"FSPL Loss:     {fspl:.2f} dB")
    print(f"Iono Delay:    {delay * 1e9:.2f} ns")
    print(f"Signal SNR:    {snr:.2f} dB")
    
    if snr > 10:
        print("Status:        LINK STABLE [OK]")
    elif snr > 3:
        print("Status:        LINK DEGRADED [WARN]")
    else:
        print("Status:        LINK LOST [FAIL]")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DeepSpace-Telemetry-AI Simulation Trigger')
    parser.add_argument('--distance_au', type=float, default=1.52, help='Distance in Astronomical Units')
    parser.add_argument('--band', type=str, default='X', choices=['X', 'Ka'], help='Frequency Band')
    parser.add_argument('--tec_level', type=str, default='Medium', choices=['Low', 'Medium', 'High'], help='Ionosphere Electron Content Level')
    
    args = parser.parse_args()
    run_scenario(args.distance_au, args.band, args.tec_level)
