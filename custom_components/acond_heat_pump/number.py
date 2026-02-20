"""Number platform for the Acond Heat Pump integration."""

from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
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
    """Set up the Acond number entities."""
    coordinator = entry.runtime_data
    entry_id = entry.entry_id
    async_add_entities(
        [
            AcondWaterBackTemperature(coordinator, entry_id),
            AcondPoolTemperature(coordinator, entry_id),
            AcondWaterCoolTemperature(coordinator, entry_id),
            AcondDhwTemperature(coordinator, entry_id),
        ]
    )


class AcondWaterBackTemperature(AcondEntity, NumberEntity):
    """Representation of the water back temperature setpoint."""

    _attr_icon = "mdi:thermometer-water"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 10.0
    _attr_native_max_value = 65.0
    _attr_native_step = 0.5
    _attr_mode = NumberMode.SLIDER
    _attr_translation_key = "water_back_temperature"

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_number_water_back_temp"

    @property
    def native_value(self) -> float | None:
        """Return the current water back temperature setpoint."""
        return self.coordinator.data.water_back_temp_set

    async def async_set_native_value(self, value: float) -> None:
        """Set new water back temperature setpoint."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_water_back_temperature, value
        )
        await self.coordinator.async_request_refresh()


class AcondPoolTemperature(AcondEntity, NumberEntity):
    """Representation of the pool temperature setpoint."""

    _attr_icon = "mdi:pool-thermometer"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 10.0
    _attr_native_max_value = 50.0
    _attr_native_step = 0.5
    _attr_mode = NumberMode.SLIDER
    _attr_translation_key = "pool_temperature_setpoint"

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_number_pool_temp"

    @property
    def native_value(self) -> float | None:
        """Return the current pool temperature setpoint."""
        return self.coordinator.data.pool_temp_set

    async def async_set_native_value(self, value: float) -> None:
        """Set new pool temperature setpoint."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_pool_temperature, value
        )
        await self.coordinator.async_request_refresh()


class AcondWaterCoolTemperature(AcondEntity, NumberEntity):
    """Representation of the water cooling outlet temperature setpoint."""

    _attr_icon = "mdi:snowflake-thermometer"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 15.0
    _attr_native_max_value = 30.0
    _attr_native_step = 0.5
    _attr_mode = NumberMode.SLIDER
    _attr_translation_key = "water_cool_temperature"

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_number_water_cool_temp"

    @property
    def native_value(self) -> float | None:
        """Return the current water cooling temperature setpoint."""
        return self.coordinator.data.water_outlet_temp_set

    async def async_set_native_value(self, value: float) -> None:
        """Set new water cooling temperature setpoint."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_water_cool_temperature, value
        )
        await self.coordinator.async_request_refresh()


class AcondDhwTemperature(AcondEntity, NumberEntity):
    """Representation of the DHW (boiler) temperature setpoint."""

    _attr_icon = "mdi:water-boiler"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 10.0
    _attr_native_max_value = 50.0
    _attr_native_step = 0.5
    _attr_mode = NumberMode.SLIDER
    _attr_translation_key = "dhw_temperature_setpoint"

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_number_dhw_temp"

    @property
    def native_value(self) -> float | None:
        """Return the current DHW temperature setpoint."""
        return self.coordinator.data.dhw_temp_set

    async def async_set_native_value(self, value: float) -> None:
        """Set new DHW temperature setpoint."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_dhw_temperature, value
        )
        await self.coordinator.async_request_refresh()
