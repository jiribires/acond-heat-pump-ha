"""Binary sensor platform for the Acond Heat Pump integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from acond_heat_pump import HeatPumpStatus

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AcondConfigEntry
from .coordinator import AcondCoordinator
from .entity import AcondEntity


@dataclass(frozen=True, kw_only=True)
class AcondBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an Acond binary sensor entity."""

    value_fn: Callable[[HeatPumpStatus], bool]


BINARY_SENSOR_DESCRIPTIONS: tuple[AcondBinarySensorEntityDescription, ...] = (
    AcondBinarySensorEntityDescription(
        key="running",
        translation_key="running",
        icon="mdi:heat-pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda status: status.running,
    ),
    AcondBinarySensorEntityDescription(
        key="fault",
        translation_key="fault",
        icon="mdi:alert-octagon",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda status: status.fault,
    ),
    AcondBinarySensorEntityDescription(
        key="defrost",
        translation_key="defrost",
        icon="mdi:snowflake-melt",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.defrost,
    ),
    AcondBinarySensorEntityDescription(
        key="dhw_heating",
        translation_key="dhw_heating",
        icon="mdi:water-boiler",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda status: status.heating_dhw,
    ),
    AcondBinarySensorEntityDescription(
        key="pump_circuit1",
        translation_key="pump_circuit1",
        icon="mdi:pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.pump_circuit1,
    ),
    AcondBinarySensorEntityDescription(
        key="summer_mode",
        translation_key="summer_mode",
        icon="mdi:weather-sunny",
        value_fn=lambda status: status.summer_mode,
    ),
    AcondBinarySensorEntityDescription(
        key="power",
        translation_key="power",
        icon="mdi:power",
        device_class=BinarySensorDeviceClass.POWER,
        value_fn=lambda status: status.on,
    ),
    AcondBinarySensorEntityDescription(
        key="pump_circuit2",
        translation_key="pump_circuit2",
        icon="mdi:pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.pump_circuit2,
    ),
    AcondBinarySensorEntityDescription(
        key="solar_pump",
        translation_key="solar_pump",
        icon="mdi:solar-power",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.solar_pump,
    ),
    AcondBinarySensorEntityDescription(
        key="pool_pump",
        translation_key="pool_pump",
        icon="mdi:pool",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.pool_pump,
    ),
    AcondBinarySensorEntityDescription(
        key="bivalence_running",
        translation_key="bivalence_running",
        icon="mdi:fire",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.bivalence_running,
    ),
    AcondBinarySensorEntityDescription(
        key="brine_pump",
        translation_key="brine_pump",
        icon="mdi:pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.brine_pump,
    ),
    AcondBinarySensorEntityDescription(
        key="cooling_running",
        translation_key="cooling_running",
        icon="mdi:snowflake",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda status: status.cooling_running,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Acond binary sensor entities."""
    coordinator = entry.runtime_data
    async_add_entities(
        AcondBinarySensor(coordinator, entry.entry_id, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class AcondBinarySensor(AcondEntity, BinarySensorEntity):
    """Representation of an Acond binary sensor."""

    entity_description: AcondBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: AcondCoordinator,
        entry_id: str,
        description: AcondBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entry_id)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_binary_sensor_{description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.entity_description.value_fn(self.coordinator.data.status)
