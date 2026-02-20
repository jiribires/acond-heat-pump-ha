"""Constants for the Acond Heat Pump integration."""

from homeassistant.const import Platform

from acond_heat_pump import HeatPumpMode, RegulationMode

DOMAIN = "acond_heat_pump"
DEFAULT_PORT = 502

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
]

# HeatPumpMode -> translation key
HEAT_PUMP_MODE_KEYS: dict[HeatPumpMode, str] = {
    HeatPumpMode.AUTOMATIC: "automatic",
    HeatPumpMode.HEAT_PUMP_ONLY: "heat_pump",
    HeatPumpMode.BIVALENT_ONLY: "bivalency_source",
    HeatPumpMode.COOLING: "cooling",
    HeatPumpMode.OFF: "off",
}

# Translation key -> HeatPumpMode (reverse lookup)
HEAT_PUMP_MODE_BY_KEY: dict[str, HeatPumpMode] = {
    v: k for k, v in HEAT_PUMP_MODE_KEYS.items()
}

# RegulationMode -> translation key
REGULATION_MODE_KEYS: dict[RegulationMode, str] = {
    RegulationMode.ACOND_THERM: "smart_therm",
    RegulationMode.EQUITHERMAL: "ekviterm",
    RegulationMode.MANUAL: "standard",
}

# Translation key -> RegulationMode (reverse lookup)
REGULATION_MODE_BY_KEY: dict[str, RegulationMode] = {
    v: k for k, v in REGULATION_MODE_KEYS.items()
}

OPERATION_MODE_OPTIONS: list[str] = ["winter", "summer"]
