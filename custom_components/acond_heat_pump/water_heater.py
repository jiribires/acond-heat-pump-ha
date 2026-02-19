"""Water heater platform for the Acond Heat Pump integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AcondConfigEntry
from .coordinator import AcondCoordinator
from .entity import AcondEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Acond water heater entity."""
    async_add_entities([AcondWaterHeater(entry.runtime_data, entry.entry_id)])


class AcondWaterHeater(AcondEntity, WaterHeaterEntity):
    """Representation of the Acond heat pump boiler/DHW."""

    _attr_icon = "mdi:water-boiler"
    _attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_min_temp = 10.0
    _attr_max_temp = 50.0
    _attr_precision = 0.1
    _attr_translation_key = "dhw"

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the water heater entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_water_heater_dhw"

    @property
    def current_temperature(self) -> float | None:
        """Return the current DHW temperature."""
        return self.coordinator.data.dhw_temp_actual

    @property
    def target_temperature(self) -> float | None:
        """Return the target DHW temperature."""
        return self.coordinator.data.dhw_temp_set

    @property
    def current_operation(self) -> str:
        """Return current operation."""
        if self.coordinator.data.status.heating_dhw:
            return "Heating"
        return "Idle"

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get("temperature")) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_dhw_temperature, temperature
        )
        await self.coordinator.async_request_refresh()
