"""Bond Home Generic Device Integration"""
from homeassistant.components.switch import (
    STATE_ON,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
    SERVICE_TOGGLE,
    SwitchDevice
)

from bond import (
    BOND_DEVICE_TYPE_GENERIC_DEVICE
)

import logging
DOMAIN = 'bond'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Generic Device platform."""
    bond = hass.data[DOMAIN]['bond_hub']

    for deviceId in bond.getDeviceIds():
        device = bond.getDevice(deviceId)
        if device['type'] != BOND_DEVICE_TYPE_GENERIC_DEVICE:
            continue

        deviceProperties = bond.getProperties(deviceId)
        switch = BondSwitch(bond, deviceId, device, deviceProperties)
        add_entities([switch])


class BondSwitch(SwitchDevice):
    """Representation of a Bond Generic Device."""

    def __init__(self, bond, deviceId, device, properties):
        """Initialize a Bond Generic Device."""
        self._bond = bond
        self._deviceId = deviceId
        self._device = device
        self._properties = properties
        name = "Switch" if "name" not in properties else properties['name']
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
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the Generic Device to turn on."""
        self._bond.turnOn(self._deviceId)

    def turn_off(self, **kwargs):
        """Instruct the Generic Device to turn off."""
        self._bond.turnOff(self._deviceId)

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'power' in bondState:
            self._state = True if bondState['power'] == 1 else False

    @property
    def unique_id(self):
        """Get the unique identifier of the device."""
        return self._deviceId

    @property
    def device_id(self):
        """Return the ID of this switch."""
        return self.unique_id

    @property
    def device_state_attributes(self):
        """Get the state attributes for the device."""
        return self._properties
