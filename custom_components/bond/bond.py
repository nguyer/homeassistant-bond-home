import requests

BOND_DEVICE_TYPE_CEILING_FAN = "CF"
BOND_DEVICE_TYPE_FIREPLACE = "FP"
BOND_DEVICE_TYPE_MOTORIZED_SHADES = "MS"
BOND_DEVICE_TYPE_GENERIC_DEVICE = "GX"

class Bond:
    def __init__(self, bondIp, bondToken):
        self.bondIp = bondIp
        self.bondToken = bondToken

    def setFanSpeed(self, deviceId, speed):
        return self.doAction(deviceId, 'SetSpeed', {'argument': speed})

    def turnFanOn(self, deviceId):
        return self.doAction(deviceId, 'TurnOn')

    def turnFanOff(self, deviceId):
        return self.doAction(deviceId, 'TurnOff')

    def toggleLight(self, deviceId):
        return self.doAction(deviceId, 'ToggleLight')

    def turnLightOn(self, deviceId):
        return self.doAction(deviceId, 'TurnLightOn')

    def turnLightOff(self, deviceId):
        return self.doAction(deviceId, 'TurnLightOff')

    def doAction(self, deviceId, action, payload={}):
        print(f'http://{self.bondIp}/v2/devices/{deviceId}/actions/{action}')
        print(payload)
        r = requests.put(
            f'http://{self.bondIp}/v2/devices/{deviceId}/actions/{action}', headers={'BOND-Token': self.bondToken}, json=payload)
        return r.content

    def getDeviceIds(self):
        r = requests.get(f'http://{self.bondIp}/v2/devices',
                         headers={'BOND-Token': self.bondToken})
        devices = []
        for key in r.json():
            if (key != '_'):
                devices.append(key)
        return devices

    def getDeviceType(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}',
                         headers={'BOND-Token': self.bondToken})
        return r.json()['type']

    def getDevice(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}',
                         headers={'BOND-Token': self.bondToken})
        return r.json()

    def getDeviceState(self, deviceId):
        r = requests.get(f'http://{self.bondIp}/v2/devices/{deviceId}/state',
                         headers={'BOND-Token': self.bondToken})
        return r.json()
