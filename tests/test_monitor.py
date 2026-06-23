import sys
sys.path.insert(0, "..")
from src.monitoring.monitor import BatteryMonitor, BatteryTelemetry


def test_alert_fires_on_overvoltage():
    monitor = BatteryMonitor()
    alerts = []
    monitor.add_alert_handler(lambda name, t: alerts.append(name))
    t = BatteryTelemetry(voltage=4.3, current=1.0, temperature=25, soc=90, soh=95, cycle_count=10)
    monitor.ingest(t)
    assert "overvoltage" in alerts


def test_no_alert_normal_conditions():
    monitor = BatteryMonitor()
    alerts = []
    monitor.add_alert_handler(lambda name, t: alerts.append(name))
    t = BatteryTelemetry(voltage=3.8, current=0.5, temperature=25, soc=80, soh=90, cycle_count=5)
    monitor.ingest(t)
    assert alerts == []
