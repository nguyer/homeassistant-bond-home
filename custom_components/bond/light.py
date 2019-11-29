"""Bond Home Light Integration"""
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light)
import logging
DOMAIN = 'bond'

from .bond import (
    BOND_DEVICE_TYPE_CEILING_FAN,
)


# Import the device class from the component that you want to support

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Light platform."""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Verify that passed in configuration works
    # if not hub.is_valid_login():
    #     _LOGGER.error("Could not connect to AwesomeLight hub")
    #     return

    # Add devices
    for deviceId in bond.getDeviceIds():
        if bond.getDeviceType(deviceId) == BOND_DEVICE_TYPE_CEILING_FAN:
            add_entities( [ BondLight(bond, deviceId) ] )

class BondLight(Light):
    """Representation of an Bond Light."""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Light."""
        self._bond = bond
        self._deviceId = deviceId

        bondProperties = self._bond.getDevice(self._deviceId)

        self._name = bondProperties['name'] + ' Light'
        self._state = None
        # self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    # @property
    # def brightness(self):
    #     """Return the brightness of the light.

    #     This method is optional. Removing it indicates to Home Assistant
    #     that brightness is not supported for this light.
    #     """
    #     return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        #self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._bond.turnLightOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._bond.turnLightOff(self._deviceId)

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        self._state = True if bondState['light'] == 1 else False
        # self._brightness = self._light.brightness
