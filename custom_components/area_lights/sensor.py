import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback
from homeassistant.helpers import entity_registry, area_registry, device_registry
from .const import DOMAIN, ATTR_COUNT, ATTR_TOTAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    excluded = entry.data.get("excluded_entities", [])
    
    _LOGGER.debug("Starting Area Lights configuration")
    _LOGGER.debug(f"Excluded entities: {excluded}")
    
    area_reg = area_registry.async_get(hass)
    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)
    
    areas = area_reg.async_list_areas()
    _LOGGER.debug(f"Found areas: {[area.name for area in areas]}")
    
    sensors = []
    all_lights = set()
    
    for area in areas:
        area_lights = set()
        area_excluded = set()
        
        for entity in entity_reg.entities.values():
            if entity.entity_id.startswith("light.") and entity.area_id == area.id:
                if entity.entity_id not in excluded:
                    area_lights.add(entity.entity_id)
                    _LOGGER.debug(f"Light {entity.entity_id} found directly in {area.name}")
                else:
                    area_excluded.add(entity.entity_id)
        
        for device_id in device_reg.devices:
            device = device_reg.async_get(device_id)
            if device and device.area_id == area.id:
                for entity in entity_reg.entities.values():
                    if entity.device_id == device_id and entity.entity_id.startswith("light."):
                        if entity.entity_id not in excluded:
                            area_lights.add(entity.entity_id)
                            _LOGGER.debug(f"Light {entity.entity_id} found via device in {area.name}")
                        else:
                            area_excluded.add(entity.entity_id)
        
        if area_lights:
            _LOGGER.debug(f"Area {area.name}: {len(area_lights)} lights found: {area_lights}")
            sensors.append(RoomLightsSensor(area.name, list(area_lights), list(area_excluded)))
            all_lights.update(area_lights)

    if all_lights:
        _LOGGER.debug(f"Total lights found: {len(all_lights)}")
        sensors.append(AllLightsSensor(list(all_lights), excluded))
    
    _LOGGER.debug(f"Creating {len(sensors)} sensors")
    async_add_entities(sensors)

class RoomLightsSensor(SensorEntity):
    def __init__(self, room_name, lights, excluded_lights):
        self._room = room_name
        self._lights = lights
        self._excluded_lights = excluded_lights
        self._attr_name = f"Lights {room_name}"
        self._attr_unique_id = f"area_lights_{room_name.lower().replace(' ', '_')}"
        self._state = STATE_OFF
        self._count = 0
        self._total = len(lights)
        self._lights_on = []
        self._lights_off = []
        _LOGGER.debug(f"Initializing sensor {self._attr_name} with {self._total} lights: {self._lights}")

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:lightbulb-on" if self._state == STATE_ON else "mdi:lightbulb"

    @property
    def extra_state_attributes(self):
        return {
            "count": self._count,
            "of": self._total,
            "count_of": f"{self._count}/{self._total}",
            "lights_on": self._lights_on,
            "lights_off": self._lights_off,
            "excluded_lights": self._excluded_lights,
        }

    async def async_added_to_hass(self):
        @callback
        def async_state_changed(*_):
            self.async_schedule_update_ha_state(True)

        for light in self._lights:
            self.async_on_remove(
                self.hass.helpers.event.async_track_state_change(
                    light, async_state_changed
                )
            )
        
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        self._count = 0
        self._lights_on = []
        self._lights_off = []
        
        for light_id in self._lights:
            state = self.hass.states.get(light_id)
            if state:
                if state.state == STATE_ON:
                    self._count += 1
                    self._lights_on.append(light_id)
                else:
                    self._lights_off.append(light_id)
        
        self._state = STATE_ON if self._count > 0 else STATE_OFF
        _LOGGER.debug(f"Updating {self._attr_name}: {self._count}/{self._total} lights on")

class AllLightsSensor(RoomLightsSensor):
    def __init__(self, lights, excluded_lights):
        super().__init__("All", lights, excluded_lights)
        self._attr_name = "All Area Lights"
        self._attr_unique_id = "area_lights_all"
