"""Base entity for the Acond Heat Pump integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AcondCoordinator


class AcondEntity(CoordinatorEntity[AcondCoordinator]):
    """Base class for Acond Heat Pump entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            manufacturer="Acond",
            model="Heat Pump",
        )
