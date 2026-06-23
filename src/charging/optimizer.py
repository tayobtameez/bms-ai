"""
Charging Optimizer: Recommends optimal CC-CV charging profiles
based on battery state to minimize degradation and maximize throughput.
"""
from dataclasses import dataclass
from loguru import logger


@dataclass
class ChargingProfile:
    """A recommended charging profile."""
    constant_current_amps: float    # CC phase current (A)
    cutoff_voltage: float           # CV phase cutoff voltage (V)
    max_temperature_c: float        # Thermal limit during charging
    estimated_time_min: float       # Estimated charge time
    health_impact_score: float      # Lower = gentler on battery (0–1)


class ChargingOptimizer:
    """
    Recommends a CC-CV charging profile given battery state.
    Balances charging speed vs. long-term health.
    """

    # (soh_tier, urgency) → (cc_amps, cv_voltage, max_temp, est_time_min, health_impact)
    PROFILES = {
        ("high", "fast"):   (1.0, 4.2,  35, 60,  0.4),
        ("high", "normal"): (0.7, 4.15, 35, 80,  0.2),
        ("low",  "fast"):   (0.5, 4.1,  30, 100, 0.6),
        ("low",  "normal"): (0.3, 4.05, 30, 120, 0.1),
    }

    def recommend(
        self,
        soh: float,
        temperature_c: float,
        urgency: str = "normal",
    ) -> ChargingProfile:
        """
        Recommend a charging profile.

        Args:
            soh: State of Health (0–100 %)
            temperature_c: Current cell temperature (°C)
            urgency: "fast" or "normal"
        """
        soh_tier = "high" if soh >= 80 else "low"
        cc, cv, max_temp, est_time, health_impact = self.PROFILES[(soh_tier, urgency)]

        # Derate current if battery is running hot
        if temperature_c > 30:
            derate = 1 - 0.05 * (temperature_c - 30)
            cc = max(0.1, cc * derate)
            logger.warning(f"High temp ({temperature_c}°C): derated current to {cc:.2f}A")

        profile = ChargingProfile(
            constant_current_amps=cc,
            cutoff_voltage=cv,
            max_temperature_c=max_temp,
            estimated_time_min=est_time,
            health_impact_score=health_impact,
        )
        logger.info(f"Profile recommended: {cc}A CC → {cv}V CV | Est. {est_time} min")
        return profile
