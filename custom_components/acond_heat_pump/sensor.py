"""Sensor platform for the Acond Heat Pump integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from acond_heat_pump import HeatPumpResponse

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AcondConfigEntry
from .coordinator import AcondCoordinator
from .entity import AcondEntity


@dataclass(frozen=True, kw_only=True)
class AcondSensorEntityDescription(SensorEntityDescription):
    """Describes an Acond sensor entity."""

    value_fn: Callable[[HeatPumpResponse], float | int | None]


SENSOR_DESCRIPTIONS: tuple[AcondSensorEntityDescription, ...] = (
    AcondSensorEntityDescription(
        key="outdoor_temperature",
        translation_key="outdoor_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.outdoor_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="return_water_temperature",
        translation_key="return_water_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.water_back_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="return_water_setpoint",
        translation_key="return_water_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.water_back_temp_set,
    ),
    AcondSensorEntityDescription(
        key="brine_temperature",
        translation_key="brine_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.brine_temp,
    ),
    AcondSensorEntityDescription(
        key="indoor2_temperature",
        translation_key="indoor2_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.indoor2_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="solar_temperature",
        translation_key="solar_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.solar_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="pool_temperature",
        translation_key="pool_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.pool_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="pool_setpoint",
        translation_key="pool_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.pool_temp_set,
    ),
    AcondSensorEntityDescription(
        key="water_outlet_temperature",
        translation_key="water_outlet_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.water_outlet_temp_actual,
    ),
    AcondSensorEntityDescription(
        key="water_outlet_setpoint",
        translation_key="water_outlet_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.water_outlet_temp_set,
    ),
    AcondSensorEntityDescription(
        key="compressor_power",
        translation_key="compressor_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.compressor_capacity_actual,
    ),
    AcondSensorEntityDescription(
        key="compressor_power_max",
        translation_key="compressor_power_max",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.compressor_capacity_max,
    ),
    AcondSensorEntityDescription(
        key="error_code",
        translation_key="error_code",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.err_number,
    ),
    AcondSensorEntityDescription(
        key="error_code_secmono",
        translation_key="error_code_secmono",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.err_number_SECMono,
    ),
    AcondSensorEntityDescription(
        key="error_code_driver",
        translation_key="error_code_driver",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.err_number_driver,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Acond sensor entities."""
    coordinator = entry.runtime_data
    async_add_entities(
        AcondSensor(coordinator, entry.entry_id, description)
        for description in SENSOR_DESCRIPTIONS
    )


class AcondSensor(AcondEntity, SensorEntity):
    """Representation of an Acond sensor."""

    entity_description: AcondSensorEntityDescription

    def __init__(
        self,
        coordinator: AcondCoordinator,
        entry_id: str,
        description: AcondSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry_id)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_sensor_{description.key}"

    @property
    def native_value(self) -> float | int | None:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)
