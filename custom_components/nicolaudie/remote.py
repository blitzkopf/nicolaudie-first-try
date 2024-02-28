"""Remote platform for Nicolaudie."""
from homeassistant.components.remote import RemoteEntity, RemoteEntityFeature, ATTR_ACTIVITY
from homeassistant.helpers.device_registry import DeviceInfo

from datetime import timedelta

from .const import DEFAULT_NAME, DOMAIN, ICON, REMOTE
from .entity import NicolaudieEntity
from .models import NicolaudieData

from nicostick.controller import Controller

SCAN_INTERVAL = timedelta(seconds=10)

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup remote platform."""
    data : NicolaudieData = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for zone_id,name in data.device.zones.items():
        ents.append(NicolaudieRemote(data.device, name , zone_id))
    async_add_devices(ents)


class NicolaudieRemote( RemoteEntity):
    """nicolaudie remote class."""
    _attr_should_poll = True

    _attr_supported_features: RemoteEntityFeature = RemoteEntityFeature.ACTIVITY

    def __init__(self, device:Controller, name:str,zone_id:int):
        """Initialize the remote."""
        self._device = device
        self._name = name
        self._zone_id = zone_id
        self._attr_unique_id = f"{self._device.serial}_{self._zone_id}"
        self._attr_device_info = DeviceInfo (
            identifiers={(DOMAIN, self._device.serial)},
            name=self._device.name,
            model="Nicolaudie",
            manufacturer=DEFAULT_NAME
        )
    async def async_update(self):
        """Update the state of the remote."""
        await self._device.send_query_zone_status(self._zone_id)

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        # TODO: what to do when there is no activity?
        activity = kwargs.get(ATTR_ACTIVITY, None)
        if activity:
            await self._device.set_scene(self._zone_id, scene_name=activity)
        
        # await self.coordinator.api.async_set_title("bar")
        # await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self._device.set_scene(self._zone_id, scene_index=0)
        # await self.coordinator.api.async_set_title("foo")
        # await self.coordinator.async_request_refresh()
        

    @property
    def name(self):
        """Return the name of the remote."""
        return f"{DEFAULT_NAME}_{REMOTE}"

    @property
    def icon(self):
        """Return the icon of this remote."""
        return ICON

    @property
    def is_on(self):
        """Return true if the switch is on."""
        # TODO: implement this
        #return False
        return self._device.get_running_scene(self._zone_id)[0] != 0
    
    @property
    def current_activity(self): 
        """Return the current activity."""
        return self._device.get_running_scene(self._zone_id)[1]
    
    @property
    def activity_list(self):
        """Return the list of activities."""
        # for some reason HA is not happy values() straight from the dict
        list = [ sc for sc  in self._device.scenes.values() ] 
        return list
        
    

