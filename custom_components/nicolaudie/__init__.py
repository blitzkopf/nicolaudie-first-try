"""
Custom integration to integrate Nicolaudie with Home Assistant.

For more details about this integration, please refer to
https://github.com/blitzkopf/nicolaudie
"""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, Event,HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator,UpdateFailed
from homeassistant.const import CONF_ADDRESS, EVENT_HOMEASSISTANT_STOP, Platform

from nicostick.controller import Controller

from .const import CONF_HOST,DOMAIN, PLATFORMS, STARTUP_MESSAGE
from .models import NicolaudieData

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)
    _LOGGER.debug("async_setup_entry %s", entry.data)
    host = entry.data.get(CONF_HOST)
    _LOGGER.debug("Got HOst %s", host)

    device = Controller(host)
    await device.start()
    await device.initialize()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = NicolaudieData(
        entry.title, device #, coordinator
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    async def _async_stop(event: Event) -> None:
        """Close the connection."""
        await device.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_stop)
    )

    return True

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    data: NicolaudieData = hass.data[DOMAIN][entry.entry_id]
    if entry.title != data.title:
        await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data: NicolaudieData = hass.data[DOMAIN].pop(entry.entry_id)
        await data.device.stop()

    return unload_ok

