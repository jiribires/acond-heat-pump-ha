"""Climate platform for the Acond Heat Pump integration."""

from __future__ import annotations

from typing import Any

from acond_heat_pump import HeatPumpMode, RegulationMode

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AcondConfigEntry
from .const import HEAT_PUMP_MODE_NAMES
from .coordinator import AcondCoordinator
from .entity import AcondEntity

# HeatPumpMode -> HVACMode (read mapping)
_MODE_TO_HVAC: dict[HeatPumpMode, HVACMode] = {
    HeatPumpMode.AUTOMATIC: HVACMode.AUTO,
    HeatPumpMode.HEAT_PUMP_ONLY: HVACMode.HEAT,
    HeatPumpMode.BIVALENT_ONLY: HVACMode.HEAT,
    HeatPumpMode.OFF: HVACMode.OFF,
    HeatPumpMode.COOLING: HVACMode.COOL,
}

# HVACMode -> HeatPumpMode (write mapping)
_HVAC_TO_MODE: dict[HVACMode, HeatPumpMode] = {
    HVACMode.AUTO: HeatPumpMode.AUTOMATIC,
    HVACMode.HEAT: HeatPumpMode.HEAT_PUMP_ONLY,
    HVACMode.COOL: HeatPumpMode.COOLING,
    HVACMode.OFF: HeatPumpMode.OFF,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Acond climate entities."""
    async_add_entities(
        [
            AcondClimate(entry.runtime_data, entry.entry_id),
            AcondClimateCircuit2(entry.runtime_data, entry.entry_id),
        ]
    )


class AcondClimate(AcondEntity, ClimateEntity):
    """Representation of the Acond heat pump Circuit I climate entity."""

    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.HEAT, HVACMode.COOL, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.1
    _attr_min_temp = 10.0
    _attr_max_temp = 30.0
    _attr_icon = "mdi:heat-pump-outline"
    _attr_translation_key = "circuit1"
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_climate_circuit1"

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return supported features, disabling temperature control in Standard mode."""
        if (
            self.coordinator.data
            and self.coordinator.data.regulation_mode == RegulationMode.MANUAL
        ):
            return ClimateEntityFeature(0)
        return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def current_temperature(self) -> float | None:
        """Return the current indoor temperature."""
        return self.coordinator.data.indoor1_temp_actual

    @property
    def target_temperature(self) -> float | None:
        """Return the target indoor temperature."""
        return self.coordinator.data.indoor1_temp_set

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        mode = self.coordinator.data.heat_pump_mode
        return _MODE_TO_HVAC.get(mode, HVACMode.AUTO)

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action."""
        status = self.coordinator.data.status
        if not status.on:
            return HVACAction.OFF
        if status.cooling_running:
            return HVACAction.COOLING
        if status.running:
            return HVACAction.HEATING
        if status.defrost:
            return HVACAction.DEFROSTING
        return HVACAction.IDLE

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_indoor_temperature, temperature, 1
        )
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new HVAC mode."""
        if (mode := _HVAC_TO_MODE.get(hvac_mode)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.change_setting, mode
        )
        await self.coordinator.async_request_refresh()


class AcondClimateCircuit2(AcondEntity, ClimateEntity):
    """Representation of the Acond heat pump Circuit II climate entity."""

    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.HEAT, HVACMode.COOL, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.1
    _attr_min_temp = 10.0
    _attr_max_temp = 30.0
    _attr_icon = "mdi:heat-pump-outline"
    _attr_translation_key = "circuit2"
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_climate_circuit2"

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return supported features, disabling temperature control in Standard mode."""
        if (
            self.coordinator.data
            and self.coordinator.data.regulation_mode == RegulationMode.MANUAL
        ):
            return ClimateEntityFeature(0)
        return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def current_temperature(self) -> float | None:
        """Return the current indoor temperature for circuit 2."""
        return self.coordinator.data.indoor2_temp_actual

    @property
    def target_temperature(self) -> float | None:
        """Return the target indoor temperature for circuit 2."""
        return self.coordinator.data.indoor2_temp_set

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        mode = self.coordinator.data.heat_pump_mode
        return _MODE_TO_HVAC.get(mode, HVACMode.AUTO)

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action."""
        status = self.coordinator.data.status
        if not status.on:
            return HVACAction.OFF
        if status.cooling_running:
            return HVACAction.COOLING
        if status.running:
            return HVACAction.HEATING
        if status.defrost:
            return HVACAction.DEFROSTING
        return HVACAction.IDLE

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature for circuit 2."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_indoor_temperature, temperature, 2
        )
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new HVAC mode."""
        if (mode := _HVAC_TO_MODE.get(hvac_mode)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.change_setting, mode
        )
        await self.coordinator.async_request_refresh()
