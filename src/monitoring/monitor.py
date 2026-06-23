"""
Real-time Battery Monitor: tracks telemetry, raises alerts,
and logs events for dashboard consumption.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
from loguru import logger


@dataclass
class BatteryTelemetry:
    voltage: float        # V
    current: float        # A
    temperature: float    # °C
    soc: float            # State of Charge (0–100 %)
    soh: float            # State of Health (0–100 %)
    cycle_count: int
    timestamp: datetime = field(default_factory=datetime.utcnow)


ALERT_THRESHOLDS = {
    "overvoltage":  lambda t: t.voltage > 4.25,
    "undervoltage": lambda t: t.voltage < 2.8,
    "overtemp":     lambda t: t.temperature > 45,
    "low_soh":      lambda t: t.soh < 70,
    "low_soc":      lambda t: t.soc < 10,
}


class BatteryMonitor:
    """Processes telemetry and fires alert callbacks."""

    def __init__(self):
        self.history: list[BatteryTelemetry] = []
        self._alert_handlers: list[Callable] = []

    def add_alert_handler(self, handler: Callable):
        """Register a callback for alerts (e.g., push notification, log)."""
        self._alert_handlers.append(handler)

    def ingest(self, telemetry: BatteryTelemetry):
        """Process a new telemetry reading."""
        self.history.append(telemetry)
        self._check_alerts(telemetry)

    def _check_alerts(self, t: BatteryTelemetry):
        for name, condition in ALERT_THRESHOLDS.items():
            if condition(t):
                logger.warning(
                    f"⚠️  ALERT [{name.upper()}] | "
                    f"V={t.voltage}V  T={t.temperature}°C  SoH={t.soh}%"
                )
                for handler in self._alert_handlers:
                    handler(name, t)

    def latest(self) -> BatteryTelemetry | None:
        return self.history[-1] if self.history else None
