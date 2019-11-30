"""Bond Home Generic Device Integration"""
from homeassistant.components.switch import (
    STATE_ON,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
    SERVICE_TOGGLE,
    SwitchDevice,
)
import logging
DOMAIN = 'bond'

from .bond import (
    BOND_DEVICE_TYPE_GENERIC_DEVICE,
    BOND_DEVICE_ACTION_TURNON,
    BOND_DEVICE_ACTION_TURNOFF,
    BOND_DEVICE_ACTION_TOGGLEPOWER,
)

# Import the device class from the component that you want to support

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Generic Device platform."""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        newBondSwitch = BondSwitch(bond, deviceId)

        # If the device type is not a Generic Device, then don't create a switch instance
        if newBondSwitch._properties['type'] == BOND_DEVICE_TYPE_GENERIC_DEVICE:
            add_entities( [ newBondSwitch ] )

class BondSwitch(SwitchDevice):
    """Representation of an Bond Generic Device."""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Generic Device."""
        self._bond = bond
        self._deviceId = deviceId
        self._properties = self._bond.getDevice(self._deviceId)
        self._name = self._properties['name']
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
