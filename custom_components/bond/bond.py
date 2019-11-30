import requests

BOND_DEVICE_TYPE_CEILING_FAN = "CF"
BOND_DEVICE_TYPE_FIREPLACE = "FP"
BOND_DEVICE_TYPE_MOTORIZED_SHADES = "MS"
BOND_DEVICE_TYPE_GENERIC_DEVICE = "GX"

# Note that Bond Action "Stop" instructs the Bond Bridge to stop sending.  There are other
# actions such as "Hold" that send a message to stop the controlled-device's current action
BOND_DEVICE_ACTION_STOP = "Stop"

# Relating to Generic Device (GX)
BOND_DEVICE_ACTION_TURNON = "TurnOn"
BOND_DEVICE_ACTION_TURNOFF = "TurnOff"
BOND_DEVICE_ACTION_TOGGLEPOWER = "TogglePower"

# Relating to Motorized Shades (MS)
BOND_DEVICE_ACTION_OPEN = "Open"
BOND_DEVICE_ACTION_CLOSE = "Close"
BOND_DEVICE_ACTION_HOLD = "Hold"
BOND_DEVICE_ACTION_PAIR = "Pair"
BOND_DEVICE_ACTION_PRESET = "Preset"
BOND_DEVICE_ACTION_TOGGLEOPEN = "ToggleOpen"

# Relating to Ceiling Fan (CF)
BOND_DEVICE_ACTION_SETSPEED = "SetSpeed"
BOND_DEVICE_ACTION_INCREASESPEED = "IncreaseSpeed"
BOND_DEVICE_ACTION_DECREASESPEED = "DecreaseSpeed"
BOND_DEVICE_ACTION_TURNLIGHTON = "TurnLightOn"
BOND_DEVICE_ACTION_TURNLIGHTOFF = "TurnLightOff"
BOND_DEVICE_ACTION_TOGGLELIGHT = "ToggleLight"

class Bond:
    def __init__(self, bondIp, bondToken):
        self.bondIp = bondIp
        self.bondToken = bondToken

    def turnOn(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TURNON)

    def turnOff(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TURNOFF)

    def togglePower(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TOGGLEPOWER)

    def setFanSpeed(self, deviceId, speed):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_SETSPEED, {"argument":speed} )

    def toggleLight(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TOGGLELIGHT)

    def turnLightOn(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TURNLIGHTON)

    def turnLightOff(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_TURNLIGHTOFF)

    def openShade(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_OPEN)

    def closeShade(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_CLOSE)

    def holdShade(self, deviceId):
        return self.doAction(deviceId, BOND_DEVICE_ACTION_HOLD)

    def doAction(self, deviceId, action, payload={}):
        r = requests.put(
            f'http://{self.bondIp}/v2/devices/{deviceId}/actions/{action}', headers={'BOND-Token': self.bondToken}, json=payload)
        if r.status_code < 200 or r.status_code > 299:
            raise Exception(r.content)
        return r.content

    def getDeviceIds(self):
        r = requests.get(f'http://{self.bondIp}/v2/devices',
                         headers={'BOND-Token': self.bondToken})
        devices = []
        for key in r.json():
            if (key != '_'):
                devices.append(key)
        return devices

    def getDevice(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}',
                         headers={'BOND-Token': self.bondToken})
        return r.json()

    def getProperties(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}/properties/',
                         headers={'BOND-Token': self.bondToken})
        return r.json()

    def getDeviceState(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}/state',
                         headers={'BOND-Token': self.bondToken})
        return r.json()
