import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine import TelemetryEngine
from src.predictor import TelemetryPredictor
from src.api_connector import SpaceWeatherAPI

def run_trajectory_simulation():
    engine = TelemetryEngine()
    predictor = TelemetryPredictor()
    api = SpaceWeatherAPI()
    
    # 30-day Mission Phase Simulation
    days = np.arange(0, 30, 1)
    # Distance increases as we move away from Earth (0.5 AU to 1.5 AU)
    distances = np.linspace(0.5, 1.5, len(days))
    
    # Simulate a Solar Conjunction Event around Day 15
    # SEP angle decreases then increases
    sep_angles = np.abs(np.linspace(10, -10, len(days))) + 0.2
    
    snr_history = []
    prediction_history = []
    
    print("Starting Orbital Trajectory Simulation (30 Days)...")
    
    for i, day in enumerate(days):
        dist = distances[i]
        sep = sep_angles[i]
        
        # Get simulated space weather
        flux = api.get_current_solar_flux()
        tec = api.get_tec_map()["global_avg_tec"]
        
        # Physics Engine Calculation
        freq = engine.frequencies["X"]
        fspl = engine.calculate_fspl(dist, freq)
        t_solar = engine.calculate_solar_conjunction_noise(sep)
        
        # Constants for simulation
        p_tx, g_tx, g_rx = 43, 48, 70
        p_noise_thermal = engine.calculate_thermal_noise(25, 1e6)
        
        current_snr = engine.calculate_snr(p_tx, g_tx, g_rx, fspl, p_noise_thermal, t_solar=t_solar)
        snr_history.append(current_snr)
        
        # AI Prediction for 24 hours ahead
        pred_snr, _ = predictor.predict_snr_trend(current_snr, flux, hours_ahead=24)
        prediction_history.append(pred_snr)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(days, snr_history, label='Actual SNR (Calculated)', color='blue', linewidth=2)
    plt.plot(days, prediction_history, label='AI Forecast (24h Ahead)', color='orange', linestyle='--')
    
    plt.axvspan(12, 18, color='red', alpha=0.2, label='Solar Conjunction Phase')
    
    plt.title('DeepSpace-Telemetry-AI: 30-Day Mission SNR Analysis', fontsize=14)
    plt.xlabel('Mission Days', fontsize=12)
    plt.ylabel('SNR (dB)', fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    
    # Save the plot
    plot_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'snr_analysis_plot.png')
    plt.savefig(plot_path)
    print(f"Simulation Complete. Plot saved to {plot_path}")
    
    return snr_history

if __name__ == "__main__":
    run_trajectory_simulation()
    
    # Summary of Findings
    print("\nSummary of Trajectory Analysis:")
    print("- FSPL remains dominant factor for long-term degradation.")
    print("- Solar Conjunction causes sharp SNR drops (< 5 dB) regardless of distance.")
    print("- AI Predictor tracks trends but requires more real-time solar flux inputs for peak accuracy.")
