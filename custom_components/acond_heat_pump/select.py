"""Select platform for the Acond Heat Pump integration."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AcondConfigEntry
from .const import (
    HEAT_PUMP_MODE_BY_NAME,
    HEAT_PUMP_MODE_NAMES,
    OPERATION_MODE_OPTIONS,
    REGULATION_MODE_BY_NAME,
    REGULATION_MODE_NAMES,
)
from .coordinator import AcondCoordinator
from .entity import AcondEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Acond select entities."""
    coordinator = entry.runtime_data
    entry_id = entry.entry_id
    async_add_entities(
        [
            AcondRegimeSelect(coordinator, entry_id),
            AcondRegulationSelect(coordinator, entry_id),
            AcondOperationSelect(coordinator, entry_id),
        ]
    )


class AcondRegimeSelect(AcondEntity, SelectEntity):
    """Select entity for heat pump regime (operating mode)."""

    _attr_icon = "mdi:heat-pump"
    _attr_translation_key = "regime"
    _attr_options = list(HEAT_PUMP_MODE_NAMES.values())

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the regime select."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_select_regime"

    @property
    def current_option(self) -> str | None:
        """Return the current regime."""
        mode = self.coordinator.data.heat_pump_mode
        return HEAT_PUMP_MODE_NAMES.get(mode)

    async def async_select_option(self, option: str) -> None:
        """Set the regime."""
        if (mode := HEAT_PUMP_MODE_BY_NAME.get(option)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.change_setting, mode
        )
        await self.coordinator.async_request_refresh()


class AcondRegulationSelect(AcondEntity, SelectEntity):
    """Select entity for regulation mode."""

    _attr_icon = "mdi:tune"
    _attr_translation_key = "regulation"
    _attr_options = list(REGULATION_MODE_NAMES.values())

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the regulation select."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_select_regulation"

    @property
    def current_option(self) -> str | None:
        """Return the current regulation mode."""
        mode = self.coordinator.data.regulation_mode
        return REGULATION_MODE_NAMES.get(mode)

    async def async_select_option(self, option: str) -> None:
        """Set the regulation mode."""
        if (mode := REGULATION_MODE_BY_NAME.get(option)) is None:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_regulation_mode, mode
        )
        await self.coordinator.async_request_refresh()


class AcondOperationSelect(AcondEntity, SelectEntity):
    """Select entity for operation mode (Winter/Summer)."""

    _attr_icon = "mdi:sun-snowflake-variant"
    _attr_translation_key = "operation"
    _attr_options = OPERATION_MODE_OPTIONS

    def __init__(self, coordinator: AcondCoordinator, entry_id: str) -> None:
        """Initialize the operation select."""
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_select_operation"

    @property
    def current_option(self) -> str | None:
        """Return the current operation mode."""
        if self.coordinator.data.status.summer_mode:
            return "Summer"
        return "Winter"

    async def async_select_option(self, option: str) -> None:
        """Set the operation mode."""
        summer = option == "Summer"
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_summer_mode, summer
        )
        await self.coordinator.async_request_refresh()
