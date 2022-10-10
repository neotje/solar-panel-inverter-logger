from enum import Enum
import paho.mqtt.client as mqtt
import json

DEFAULT_DISCOVERY_PREFIX = "homeassistant"

class StateClass(Enum):
    NONE = None
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class Sensor:
    def __init__(self, client: mqtt.Client, name: str, uniqueId: str, unitOfMeasurement: str, stateClass: StateClass, deviceClass: str, discoveryPrefix: str = DEFAULT_DISCOVERY_PREFIX):
        self._client = client
        self.name = name
        self.uniqueId = uniqueId
        self.unitOfMeasurement = unitOfMeasurement
        self.stateClass = stateClass
        self.deviceClass = deviceClass
        self.discoveryPrefix = discoveryPrefix

    @property
    def baseTopic(self):
        return "{}/sensor/{}".format(self.discoveryPrefix, self.uniqueId)

    @property
    def availabilityTopic(self):
        return "{}/available".format(self.baseTopic)

    @property
    def stateTopic(self):
        return "{}/state".format(self.baseTopic)
    
    @property
    def discoveryTopic(self):
        return "{}/config".format(self.baseTopic)

    def discovery(self):
        config = {
           "availability_topic": self.availabilityTopic,
           "device_class": self.deviceClass,
           "name": self.name,
           "state_class": self.stateClass.value,
           "state_topic": self.stateTopic,
           "unique_id": self.uniqueId,
           "unit_of_measurement": self.unitOfMeasurement
        }

        self._client.publish(self.discoveryTopic, json.dumps(config), retain=True).wait_for_publish()

    def setOnline(self, isOnline: bool):
        payload = "online" if isOnline else "offline"

        self._client.publish(self.availabilityTopic, payload).wait_for_publish()

    def setState(self, state):
        self._client.publish(self.stateTopic, str(state)).wait_for_publish()
