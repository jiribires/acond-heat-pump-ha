"""DataUpdateCoordinator for the Acond Heat Pump integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from acond_heat_pump import AcondHeatPump, HeatPumpConnectionError, HeatPumpResponse

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)


class AcondCoordinator(DataUpdateCoordinator[HeatPumpResponse]):
    """Coordinator to manage fetching data from the Acond heat pump."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: AcondHeatPump,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Acond Heat Pump",
            update_interval=SCAN_INTERVAL,
            config_entry=config_entry,
        )
        self.client = client

    async def _async_update_data(self) -> HeatPumpResponse:
        """Fetch data from the heat pump."""
        try:
            return await self.hass.async_add_executor_job(self.client.read_data)
        except HeatPumpConnectionError as err:
            raise UpdateFailed(f"Error communicating with heat pump: {err}") from err
