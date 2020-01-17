"""Bond Home Motorized Shade Integration"""
from homeassistant.components.cover import (
    SERVICE_OPEN_COVER,
    SERVICE_CLOSE_COVER,
    SERVICE_STOP_COVER,
    SERVICE_TOGGLE,
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
    SUPPORT_STOP,
    STATE_CLOSED,
    STATE_OPEN,
    CoverDevice,
)

import logging
DOMAIN = 'bond'

from bond import (
    BOND_DEVICE_TYPE_MOTORIZED_SHADES,
    BOND_DEVICE_ACTION_OPEN,
    BOND_DEVICE_ACTION_CLOSE,
    BOND_DEVICE_ACTION_HOLD,
    BOND_DEVICE_ACTION_PAIR,
    BOND_DEVICE_ACTION_PRESET,
    BOND_DEVICE_ACTION_TOGGLEOPEN,
)

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for deviceId in bond.getDeviceIds():
        newBondCover = BondCover(bond, deviceId)

        # If not Motorized Shade device, do not instantiate object
        if newBondCover._device['type'] == BOND_DEVICE_TYPE_MOTORIZED_SHADES:
            add_entities( [ newBondCover ] )

class BondCover(CoverDevice):
    """Representation of an Bond Shade"""

    def __init__(self, bond, deviceId):
        """Initialize a Bond Fan"""
        self._bond = bond
        self._deviceId = deviceId
        self._device = self._bond.getDevice(self._deviceId)
        self._properties = self._bond.getProperties(self._deviceId)
        self._name = self._device['name']
        self._state = None

    @property
    def name(self):
        """Return the display name of this fan"""
        return self._name

    @property
    def supported_features(self):
        """Flag supported features."""
        supported_features = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP
        return supported_features

    @property
    def is_closed(self):
        bondState = self._bond.getDeviceState(self._deviceId)
        if 'open' in bondState:
            return bondState['open'] == 0

    @property
    def state(self):
        if self.is_closed:
            return STATE_CLOSED
        else:
            return STATE_OPEN

    def open_cover(self, **kwargs):
        """Instruct the cover to open."""
        self._bond.openShade(self._deviceId)

    def close_cover(self, **kwargs):
        """Instruct the cover to close."""
        self._bond.closeShade(self._deviceId)

    def stop_cover(self, **kwargs):
        """Instruct the cover to stop."""
        self._bond.holdShade(self._deviceId)


