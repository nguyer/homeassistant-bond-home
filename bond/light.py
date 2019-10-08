"""Platform for light integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light)
from homeassistant.const import CONF_HOST, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_TOKEN): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Light platform."""
    from bond import Bond

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    token = config[CONF_TOKEN]

    # Setup connection with devices/cloud
    bond = Bond(bondIp=host, bondToken=token)

    # Verify that passed in configuration works
    # if not hub.is_valid_login():
    #     _LOGGER.error("Could not connect to AwesomeLight hub")
    #     return

    # Add devices
    add_entities(BondLight(bond, deviceId) for deviceId in bond.getDeviceIds())


class BondLight(Light):
    """Representation of an Bond Light."""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Light."""
        self._bond = bond
        self._deviceId = deviceId

        bondProperties = self._bond.getDevice(self._deviceId)

        self._name = bondProperties['name']
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
