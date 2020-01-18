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
    CoverDevice
)

from bond import (
    BOND_DEVICE_TYPE_MOTORIZED_SHADES
)

import logging
DOMAIN = 'bond'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    bond = hass.data[DOMAIN]['bond_hub']

    for deviceId in bond.getDeviceIds():
        device = bond.getDevice(deviceId)
        if device['type'] != BOND_DEVICE_TYPE_MOTORIZED_SHADES:
            continue

        deviceProperties = bond.getProperties(deviceId)
        cover = BondCover(bond, deviceId, device, deviceProperties)
        add_entities([cover])


class BondCover(CoverDevice):
    """Representation of an Bond Cover"""

    def __init__(self, bond, deviceId, device, properties):
        """Initialize a Bond Cover"""
        self._bond = bond
        self._deviceId = deviceId
        self._device = device
        self._properties = properties
        name = "Cover" if "name" not in properties else properties['name']
        if "location" in properties:
            self._name = f"{properties['location']} {name}"
        else:
            self._name = name
        self._state = None

    @property
    def name(self):
        """Return the display name of this cover"""
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
        self._bond.open(self._deviceId)

    def close_cover(self, **kwargs):
        """Instruct the cover to close."""
        self._bond.close(self._deviceId)

    def stop_cover(self, **kwargs):
        """Instruct the cover to stop."""
        self._bond.hold(self._deviceId)

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
