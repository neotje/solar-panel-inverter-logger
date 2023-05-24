import sys
from time import sleep
from solarInverterToHass.pv import PVConnector
from solarInverterToHass.pvStatus import ETODAY_STATUS, PVStatusDecoder
from solarInverterToHass.sensor import Sensor, StateClass
import paho.mqtt.client as mqtt
from argparse import ArgumentParser


class ConnectPVException(Exception):
    pass


class ConnectMQTTException(Exception):
    pass


def connectPV(port: str, deviceAddr: int) -> PVConnector:
    conn = PVConnector()

    if not conn.connect(port):
        raise ConnectPVException("Failed to open the serial port")

    conn.reset()
    serial = conn.getSerialNumber()

    if serial is None:
        raise ConnectPVException("No serial number found")

    if not conn.setDeviceAddress(serial[0], deviceAddr):
        raise ConnectPVException("Could not set device address")

    return conn

def connectMQTT(host, port, user = None, password = None) -> mqtt.Client:
    client = mqtt.Client()

    if user is not None:
        client.username_pw_set(user, password)

    client.connect(host, port)

    return client


def createPVEnergySensor(connPV: PVConnector, mqtt: mqtt.Client) -> Sensor:
    serial = connPV.serial.decode("utf-8")
    name = "Omvormer {}".format(serial)
    id = "PV_{}_ETODAY".format(serial)
    sensor = Sensor(mqtt, name, id, "kWh",
                    StateClass.TOTAL_INCREASING, "energy")

    return sensor

def createStatusDecoder(connPV: PVConnector) -> PVStatusDecoder:
    decoder = PVStatusDecoder([
        ETODAY_STATUS
    ])
    decoder.format = connPV.getStatusFormat()

    return decoder


def main():

    argParser = ArgumentParser(prog='solarInverterToHass')

    """
    arguments: serial port, mqtt host/port, 
    """
    argParser.add_argument("-m", "--mqttHost", type=str,
                           help="Host address of MQTT broker", required=True)
    argParser.add_argument("-d", "--device", type=str,
                           help="Serial port for PV communication", required=True)
    argParser.add_argument("-p", "--mqttPort", type=int,
                           help="MQTT broker port", default=1883)
    argParser.add_argument("-i", "--interval", type=int,
                           help="Report interval in seconds", default=60)
    argParser.add_argument("-u", "--user", type=str,
                           help="MQTT username", default=None)
    argParser.add_argument("-P", "--password", type=str,
                            help="MQTT password", default=None)

    args = argParser.parse_args()

    while True:
        sensor = None
        pvConn = None
        mqttClient = None

        try:
            pvConn = connectPV(args.device, 1)
            mqttClient = connectMQTT(args.mqttHost, args.mqttPort, args.user, args.password)
            
            statusDecoder = createStatusDecoder(pvConn)

            sensor = createPVEnergySensor(pvConn, mqttClient)
            sensor.discovery()

            status = statusDecoder.fromBytes(pvConn.getStatus())

            if not ETODAY_STATUS.key in status or status.get(ETODAY_STATUS.key) is None:
                raise Exception("ETODAY is empty")

            sensor.setOnline(True)
            sensor.setState(status.get(ETODAY_STATUS.key))
            print(status)

        except KeyboardInterrupt:
            if sensor is not None:
                sensor.setOnline(False)

            if pvConn is not None:
                pvConn.close()

            if mqttClient is not None:
                mqttClient.loop_stop()

            break
        except Exception as e:
            print(e)

            if sensor is not None:
                sensor.setOnline(False)

        sleep(args.interval)

if __name__ == "__main__":
    main()
