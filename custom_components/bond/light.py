"""Bond Home Light Integration"""
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    Light
)

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

import logging
DOMAIN = 'bond'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Light platform."""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        device = bond.getDevice(deviceId)
        deviceType = device['type']
        actions = device['actions']

        if deviceType == BOND_DEVICE_TYPE_CEILING_FAN:
            # If the device type is not Ceiling Fan, or it is
            # Ceiling Fan but has no action for light control
            # then don't create a light instance.
            supportsLightActions = \
                BOND_DEVICE_ACTION_TURN_LIGHT_ON in actions or \
                BOND_DEVICE_ACTION_TURN_LIGHT_OFF in actions or \
                BOND_DEVICE_ACTION_TOGGLE_LIGHT in actions
            if supportsLightActions:
                deviceProperties = bond.getProperties(deviceId)
                light = BondLight(bond, deviceId, device, deviceProperties)
                add_entities([light])

        elif deviceType == BOND_DEVICE_TYPE_FIREPLACE:
            supportsFlameActions = \
                BOND_DEVICE_ACTION_SET_FLAME in actions or \
                BOND_DEVICE_ACTION_INCREASE_FLAME in actions or \
                BOND_DEVICE_ACTION_DECREASE_FLAME in actions

            supportsGenericActions = \
                BOND_DEVICE_ACTION_TURN_ON in actions or \
                BOND_DEVICE_ACTION_TURN_OFF in actions or \
                BOND_DEVICE_ACTION_TOGGLE_POWER in actions

            if supportsGenericActions:
                deviceProperties = bond.getProperties(deviceId)
                fireplace = BondFireplace(bond,
                                          deviceId,
                                          device,
                                          deviceProperties,
                                          supportsFlameActions)
                add_entities([fireplace])


class BondLight(Light):
    """Representation of an Bond Light."""

    def __init__(self, bond, deviceId, device, properties):
        """Initialize a Bond Light."""
        self._bond = bond
        self._deviceId = deviceId
        self._device = device
        self._properties = properties
        name = "Light" if "name" not in properties else properties['name']
        if "location" in properties:
            self._name = f"{properties['location']} {name}"
        else:
            self._name = name
        self._state = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
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

    @property
    def unique_id(self):
        """Get the unique identifier of the device."""
        return self._deviceId

    @property
    def device_id(self):
        """Return the ID of this Hue light."""
        return self.unique_id

    @property
    def device_state_attributes(self):
        """Get the state attributes for the device."""
        return self._properties


class BondFireplace(Light):
    """Representation of an Bond Fireplace."""

    def __init__(self, bond, deviceId, device, properties, supportsFlame):
        """Initialize a Bond Fireplace."""
        self._bond = bond
        self._deviceId = deviceId
        self._device = device
        self._properties = properties
        name = "Fireplace" if "name" not in properties else properties['name']
        if "location" in properties:
            self._name = f"{properties['location']} {name}"
        else:
            self._name = name
        self._supportsFlameAction = supportsFlame
        self._last_flame = 255
        self._flame = None
        self._state = None

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
        return SUPPORT_BRIGHTNESS if self._supportsFlameAction else 0

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
        if self._supportsFlameAction:
            # Convert Home Assistant flame level (0-255) to bond level (0-100)
            brightness = kwargs.get(ATTR_BRIGHTNESS, self._last_flame)
            flame = int((brightness * 100) / 255)
            self._bond.setFlame(self._deviceId, flame)
            self._flame = flame
        else:
            self._bond.turnOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the fireplace to turn off."""
        self._bond.turnOff(self._deviceId)
        if self._flame:
            self._last_flame = self._flame

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'power' in bondState:
            self._state = True if bondState['power'] == 1 else False

        # Convert bond level (0-100) to Home Assistant flame level (0-255)
        if 'flame' in bondState:
            self._flame = int((bondState['flame'] * 255) / 100)

    @property
    def unique_id(self):
        """Get the unique identifier of the device."""
        return self._deviceId

    @property
    def device_id(self):
        """Return the ID of this Hue light."""
        return self.unique_id

    @property
    def device_state_attributes(self):
        """Get the state attributes for the device."""
        return self._properties
