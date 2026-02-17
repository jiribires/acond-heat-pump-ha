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
    Platform.WATER_HEATER,
]

# HeatPumpMode -> UI display name
HEAT_PUMP_MODE_NAMES: dict[HeatPumpMode, str] = {
    HeatPumpMode.AUTOMATIC: "Automatic",
    HeatPumpMode.HEAT_PUMP_ONLY: "Heat Pump",
    HeatPumpMode.BIVALENT_ONLY: "Bivalency Source",
    HeatPumpMode.COOLING: "Cooling",
    HeatPumpMode.OFF: "Off",
}

# UI display name -> HeatPumpMode (reverse lookup)
HEAT_PUMP_MODE_BY_NAME: dict[str, HeatPumpMode] = {
    v: k for k, v in HEAT_PUMP_MODE_NAMES.items()
}

# RegulationMode -> UI display name
REGULATION_MODE_NAMES: dict[RegulationMode, str] = {
    RegulationMode.ACOND_THERM: "SmartTherm",
    RegulationMode.EQUITHERMAL: "Ekviterm",
    RegulationMode.MANUAL: "Standard",
}

# UI display name -> RegulationMode (reverse lookup)
REGULATION_MODE_BY_NAME: dict[str, RegulationMode] = {
    v: k for k, v in REGULATION_MODE_NAMES.items()
}

OPERATION_MODE_OPTIONS: list[str] = ["Winter", "Summer"]
