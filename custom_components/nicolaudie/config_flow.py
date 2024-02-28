"""Adds config flow for Nicolaudie."""

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback,HomeAssistant
#from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_HOST
from .const import DOMAIN
from .const import PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    #hub = PlaceholderHub(data["host"])

    #if not await hub.authenticate(data["username"], data["password"]):
    #    raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Nicolaudie"}

class NicolaudieFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for nicolaudie."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                self._errors["base"] = "cannot_connect"
            except InvalidAuth:
                self._errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                self._errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)
            
        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return NicolaudieOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_HOST): str}
            ),
            errors=self._errors,
        )

    async def _validate_connection(self, host):
        """Return true if credentials is valid."""
        try:
            # TODO: test connection to the host and see if it is a Stick 3
            # session = async_create_clientsession(self.hass)
            # client = NicolaudieApiClient(username, password, session)
            # await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class NicolaudieOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for nicolaudie."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            # This is strange 
            title=self.config_entry.data.get(CONF_HOST), data=self.options
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""