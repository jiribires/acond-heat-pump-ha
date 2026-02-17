"""The Acond Heat Pump integration."""

from __future__ import annotations

import logging

from acond_heat_pump import AcondHeatPump

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DEFAULT_PORT, DOMAIN, PLATFORMS
from .coordinator import AcondCoordinator

_LOGGER = logging.getLogger(__name__)

type AcondConfigEntry = ConfigEntry[AcondCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: AcondConfigEntry) -> bool:
    """Set up Acond Heat Pump from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    client = AcondHeatPump(host, port)

    try:
        connected = await hass.async_add_executor_job(client.connect)
    except Exception as err:
        raise ConfigEntryNotReady(
            f"Could not connect to heat pump at {host}:{port}"
        ) from err

    if not connected:
        raise ConfigEntryNotReady(
            f"Could not connect to heat pump at {host}:{port}"
        )

    coordinator = AcondCoordinator(hass, client, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: AcondConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        await hass.async_add_executor_job(entry.runtime_data.client.close)

    return unload_ok
