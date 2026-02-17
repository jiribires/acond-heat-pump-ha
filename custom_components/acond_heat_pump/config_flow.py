"""Config flow for the Acond Heat Pump integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from acond_heat_pump import AcondHeatPump, HeatPumpConnectionError

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
)

from .const import DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Acond Heat Pump"

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): TextSelector(),
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): NumberSelector(
            NumberSelectorConfig(
                min=1, max=65535, step=1, mode=NumberSelectorMode.BOX
            )
        ),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): TextSelector(),
    }
)


class AcondHeatPumpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Acond Heat Pump."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = int(user_input.get(CONF_PORT, DEFAULT_PORT))

            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            try:
                await self._test_connection(host, port)
            except HeatPumpConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data={CONF_HOST: host, CONF_PORT: port},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self, host: str, port: int) -> None:
        """Test if we can connect to the heat pump."""
        client = AcondHeatPump(host, port)
        try:
            connected = await self.hass.async_add_executor_job(client.connect)
            if not connected:
                raise HeatPumpConnectionError(f"Cannot connect to {host}:{port}")
            await self.hass.async_add_executor_job(client.read_data)
        finally:
            await self.hass.async_add_executor_job(client.close)
