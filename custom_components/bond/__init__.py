"""Example Load Platform integration."""
from homeassistant.const import CONF_HOST, CONF_TOKEN
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import logging
DOMAIN = 'bond'

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Your controller/hub specific code."""

    from .bond import Bond

    # Assign configuration variables.
    # The configuration check takes care they are present.
    conf = config[DOMAIN]

    host = conf[CONF_HOST]
    token = conf[CONF_TOKEN]

    # Setup connection with devices/cloud
    bond = Bond(bondIp=host, bondToken=token)

    hass.data[DOMAIN] = {
        'bond_hub': bond
    }

    hass.helpers.discovery.load_platform('light', DOMAIN, {}, config)
    hass.helpers.discovery.load_platform('fan', DOMAIN, {}, config)

    return True
