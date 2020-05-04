"""Bond Home Fan Integration"""
from homeassistant.components.fan import (
    SUPPORT_SET_SPEED,
    SPEED_LOW,
    SPEED_MEDIUM,
    SPEED_HIGH,
    FanEntity
)

from bond import (
    BOND_DEVICE_TYPE_CEILING_FAN,
    BOND_DEVICE_ACTION_SET_SPEED
)

import logging
DOMAIN = 'bond'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    bond = hass.data[DOMAIN]['bond_hub']

    for deviceId in bond.getDeviceIds():
        device = bond.getDevice(deviceId)
        if device['type'] != BOND_DEVICE_TYPE_CEILING_FAN:
            continue

        deviceProperties = bond.getProperties(deviceId)
        fan = BondFan(bond, deviceId, device, deviceProperties)
        add_entities([fan])


class BondFan(FanEntity):
    """Representation of an Bond Fan"""

    def __init__(self, bond, deviceId, device, properties):
        """Initialize a Bond Fan"""
        self._bond = bond
        self._deviceId = deviceId
        self._device = device
        self._properties = properties
        name = "Fan" if "name" not in properties else properties['name']
        if "location" in properties:
            self._name = f"{properties['location']} {name}"
        else:
            self._name = name
        self._state = None
        self._attributes = {}
        self._speed_map = {}

        if BOND_DEVICE_ACTION_SET_SPEED in self._device['actions']:
            if 'max_speed' in self._properties:
                self._speed_high = int(self._properties['max_speed'])
                self._speed_low = int(1)
                self._speed_map[SPEED_LOW] = self._speed_low
                if self._speed_high > 2:
                    self._speed_medium = (self._speed_high + 1) // 2
                    self._speed_map[SPEED_MEDIUM] = self._speed_medium
                self._speed_map[SPEED_HIGH] = self._speed_high

    @property
    def name(self):
        """Return the display name of this fan"""
        return self._name

    @property
    def is_on(self):
        """Return true if fan is on"""
        return self._state

    @property
    def speed_list(self) -> list:
        """Get the list of available speeds."""
        return self._speed_map.keys()

    @property
    def supported_features(self):
        """Flag supported features."""
        supported_features = 0

        if BOND_DEVICE_ACTION_SET_SPEED in self._device['actions']:
            supported_features |= SUPPORT_SET_SPEED

        return supported_features
    
    @property
    def device_state_attributes(self):
        """Return state attributes """
        return self._attributes
    
    def turn_on(self, speed=None, **kwargs):
        """Instruct the fan to turn on"""
        self._bond.turnOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the fan to turn off"""
        self._bond.turnOff(self._deviceId)

    def set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        self._bond.setSpeed(self._deviceId, self._speed_map[speed])

    def update(self):
        """Fetch new state data for this fan
        This is the only method that should fetch new data for Home Assistant
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'power' in bondState:
            self._state = True if bondState['power'] == 1 else False
            self._attributes['speed'] = [speed_name for speed_name, speed_value in self._speed_map if bondState['speed'] == speed_value][0]

    @property
    def unique_id(self):
        """Get the unique identifier of the device."""
        return self._deviceId

    @property
    def device_id(self):
        """Return the ID of this fan."""
        return self.unique_id
