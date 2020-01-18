"""Bond Home Light Integration"""
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS
    Light
)

import logging
DOMAIN = 'bond'

from bond import (
    BOND_DEVICE_TYPE_CEILING_FAN,
    BOND_DEVICE_TYPE_FIREPLACE,
    BOND_DEVICE_ACTION_TURN_LIGHT_ON,
    BOND_DEVICE_ACTION_TURN_LIGHT_OFF,
    BOND_DEVICE_ACTION_TURN_ON,
    BOND_DEVICE_ACTION_TURN_OFF,
    BOND_DEVICE_ACTION_TOGGLE_LIGHT,
    BOND_DEVICE_ACTION_TOGGLE_POWER,
    BOND_DEVICE_ACTION_SET_FLAME,
    BOND_DEVICE_ACTION_INCREASE_FLAME,
    BOND_DEVICE_ACTION_DECREASE_FLAME
)

# Import the device class from the component that you want to support
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Light platform."""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        deviceProperties = self._bond.getDevice(deviceId)
        deviceType = deviceProperties['type'];
        deviceActions = deviceProperties['actions']

        if deviceType == BOND_DEVICE_TYPE_CEILING_FAN
            # If the device type is not Ceiling Fan, or it is Ceiling Fan but has no action for light control
            # then don't create a light instance
            actions = deviceProperties['actions']
            deviceSupportsLightActions = BOND_DEVICE_ACTION_TURN_LIGHT_ON in actions or \
                                         BOND_DEVICE_ACTION_TURN_LIGHT_OFF in actions or \
                                         BOND_DEVICE_ACTION_TOGGLE_LIGHT in actions
            if deviceSupportsLightActions
                newBondLight = BondLight(bond, deviceId, deviceProperties)
                add_entities([ newBondLight ])

        elif deviceType == BOND_DEVICE_TYPE_FIREPLACE
            actions = deviceProperties['actions']
            deviceSupportsFlameActions = BOND_DEVICE_ACTION_SET_FLAME in actions or \
                                         BOND_DEVICE_ACTION_INCREASE_FLAME in actions or \
                                         BOND_DEVICE_ACTION_DECREASE_FLAME in actions

            deviceSupportsGenericActions = BOND_DEVICE_ACTION_TURN_ON in actions or \
                BOND_DEVICE_ACTION_TURN_OFF in actions or \
                BOND_DEVICE_ACTION_TOGGLE_POWER in actions

            if deviceSupportsGenericActions
                newBondFireplace = BondFireplace(bond, deviceId, deviceProperties, deviceSupportsFlameActions)
                add_entities([ newBondFireplace ])

class BondLight(Light):
    """Representation of an Bond Light."""

    def __init__(self, bond, deviceId, properties):
        """Initialize a Bond Light."""
        self._bond = bond
        self._deviceId = deviceId
        self._properties = properties
        self._name = self._properties['location'] + " " + self._properties['name']
        self._state = None

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
        if 'light' in bondState:
            self._state = True if bondState['light'] == 1 else False
        # self._brightness = self._light.brightness

class BondFireplace(Light):
    """Representation of an Bond Fireplace."""

    def __init__(self, bond, deviceId, properties, supportsFlameFeature):
        """Initialize a Bond Fireplace."""
        self._bond = bond
        self._deviceId = deviceId
        self._properties = properties
        self._name = self._properties['location'] + " " + self._properties['name']
        self._supportsFlameFeature = supportsFlameFeature
        self._state = None
        self._flame = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def supported_features(self):
        """Flag supported features.
        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return SUPPORT_BRIGHTNESS if self._supportsFlameFeature else 0

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._flame

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the fireplace to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """

        if ATTR_BRIGHTNESS in kwargs:
            self._flame = int(kwargs[ATTR_BRIGHTNESS])
            self._bond.setFlame(self._deviceId, self._flame)
        else
            self._bond.turnOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the fireplace to turn off."""
        self._bond.turnOff(self._deviceId)

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'power' in bondState:
            self._state = True if bondState['power'] == 1 else False

        if 'flame' in bondState:
            self._flame = int(bondState['flame'])
