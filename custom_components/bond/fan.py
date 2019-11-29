"""Bond Home Fan Integration"""
from homeassistant.components.fan import (FanEntity)
import logging
DOMAIN = 'bond'

from .bond import (
    BOND_DEVICE_TYPE_CEILING_FAN,
)

# Import the device class from the component that you want to support

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        if bond.getDeviceType(deviceId) == BOND_DEVICE_TYPE_CEILING_FAN:
            add_entities( [ BondFan(bond, deviceId) ] )


class BondFan(FanEntity):
    """Representation of an Bond Fan"""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Fan"""
        self._bond = bond
        self._deviceId = deviceId

        bondProperties = self._bond.getDevice(self._deviceId)

        self._name = bondProperties['name']
        self._state = None

    @property
    def name(self):
        """Return the display name of this fan"""
        return self._name

    @property
    def is_on(self):
        """Return true if fan is on"""
        return self._state

    def turn_on(self, speed=None, **kwargs):
        """Instruct the fan to turn on"""
        self._bond.turnFanOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the fan to turn off"""
        self._bond.turnFanOff(self._deviceId)

    def update(self):
        """Fetch new state data for this fan
        This is the only method that should fetch new data for Home Assistant
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        self._state = True if bondState['power'] == 1 else False
