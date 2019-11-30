"""Bond Home Fan Integration"""
from homeassistant.components.fan import (
    SUPPORT_SET_SPEED,
    SPEED_LOW,
    SPEED_MEDIUM,
    SPEED_HIGH,
    FanEntity
)
import logging
DOMAIN = 'bond'

from .bond import (
    BOND_DEVICE_TYPE_CEILING_FAN,
    BOND_DEVICE_ACTION_SETSPEED,
    BOND_DEVICE_ACTION_INCREASESPEED,
    BOND_DEVICE_ACTION_DECREASESPEED,
    BOND_DEVICE_ACTION_TURNON,
    BOND_DEVICE_ACTION_TURNOFF,
    BOND_DEVICE_ACTION_TOGGLEPOWER,

)

# Import the device class from the component that you want to support

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        newBondFan = BondFan(bond, deviceId)

        # If not Ceiling Fan type, do not instatiate object
        if newBondFan._device['type'] == BOND_DEVICE_TYPE_CEILING_FAN:
            add_entities( [ newBondFan ] )

class BondFan(FanEntity):
    """Representation of an Bond Fan"""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Fan"""
        self._bond = bond
        self._deviceId = deviceId
        self._device = self._bond.getDevice(self._deviceId)
        self._properties = self._bond.getProperties(self._deviceId)
        self._name = self._device['name']
        self._state = None
        self._speed_list = []

        if BOND_DEVICE_ACTION_SETSPEED in self._device['actions']:
            if 'max_speed' in self._properties:
                self._speed_high = int(self._properties['max_speed'])
                self._speed_low = int(1)
                self._speed_list.append(SPEED_LOW)
                if self._speed_high > 2:
                    self._speed_list.append(SPEED_MEDIUM)
                    self._speed_medium = (self._speed_high + 1) // 2
                    self._speed_list.append(SPEED_MEDIUM)
                self._speed_list.append(SPEED_HIGH)
            
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
        return self._speed_list

    @property
    def supported_features(self):
        """Flag supported features."""
        supported_features = 0

        if BOND_DEVICE_ACTION_SETSPEED in self._device['actions']:
            supported_features |= SUPPORT_SET_SPEED

        return supported_features

    def turn_on(self, speed=None, **kwargs):
        """Instruct the fan to turn on"""
        self._bond.turnFanOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the fan to turn off"""
        self._bond.turnFanOff(self._deviceId)

    def set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        if speed == SPEED_HIGH:
           self._bond.setFanSpeed(self._deviceId, self._speed_high)
        elif speed == SPEED_MEDIUM:
           self._bond.setFanSpeed(self._deviceId, self._speed_medium)
        elif speed == SPEED_LOW:
           self._bond.setFanSpeed(self._deviceId, self._speed_low)

    def update(self):
        """Fetch new state data for this fan
        This is the only method that should fetch new data for Home Assistant
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'power' in bondState:
            self._state = True if bondState['power'] == 1 else False
