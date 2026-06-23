import sys
sys.path.insert(0, "..")
from src.charging.optimizer import ChargingOptimizer


def test_normal_charge_healthy_battery():
    opt = ChargingOptimizer()
    profile = opt.recommend(soh=90, temperature_c=25, urgency="normal")
    assert profile.constant_current_amps == 0.7
    assert profile.cutoff_voltage == 4.15


def test_fast_charge_degraded_battery():
    opt = ChargingOptimizer()
    profile = opt.recommend(soh=60, temperature_c=25, urgency="fast")
    assert profile.constant_current_amps == 0.5


def test_high_temp_derate():
    opt = ChargingOptimizer()
    profile = opt.recommend(soh=90, temperature_c=40, urgency="fast")
    assert profile.constant_current_amps < 1.0  # should be derated
