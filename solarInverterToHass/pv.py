from serial import Serial, PARITY_NONE, EIGHTBITS, STOPBITS_ONE
import struct

DEFAULT_HOST_ADDR = 0x0100

START_CODE = 0xAAAA

RESET_COMMAND = 0x04
GET_SERIAL_NUMBER_COMMAND = 0x0000
SET_DEVICE_ADDR_COMMAND = 0x01
GET_STATUS_FORMAT_COMMAND = 0x0100
GET_STATUS_COMMAND = 0x0102
GET_VERSION_COMMAND = 0x0103


SERIAL_NUMBER_PAYLOAD_CODE = 0x80
SUCCESS_PAYLOAD_CODE = 0x81
STATUS_PAYLOAD_CODE = 0x0182
VERSION_PAYLOAD_CODE = 0x0183


class StatusField:
    def __init__(self, name: str, key: str, unit: str, mult: float, dataKeys: list, fmt: str) -> None:
        self.name = name
        self.key = key
        self.unit = unit
        self.mult = mult
        self.dataKeys = dataKeys
        self.fmt = fmt

    def getValue(self, statusData: dict):
        data = b''

        for k in self.dataKeys:
            fieldValue = statusData.get(k)

            if fieldValue is None:
                return

            data += fieldValue

        return struct.unpack(self.fmt, data)[0] * self.mult


STATUS_FIELDS = [
    StatusField("Internal temperature", "TEMP", "C", 0.1, [0x0], "!H"),
    StatusField("Generated energy today", "ETODAY", "kWh", 0.01, [0x0d], "!H"),
    StatusField("Grid current", "IAC", "A", 0.1, [0x41], "!H"),
    StatusField("Grid voltage", "VAC", "V", 0.1, [0x42], "!H"),
    StatusField("Grid frequency", "FAC", "Hz", 0.01, [0x43], "!H"),
    StatusField("Output power", "PAC", "W", 1, [0x44], "!H"),
    StatusField("Grid impedance", "ZAC", "Ohm", 0.001, [0x45], "!H"),
    StatusField("Total amount of generated energy",
                "ETOTAL", "kWh", 0.1, [0x47, 0x48], "!I"),
    StatusField("Total on time", "HTOTAL", "H", 1, [0x49, 0x4a], "!I"),
    StatusField("Internal temperature", "MODE", "", 0.1, [0x4c], "!H")
]


def verifyChecksum(packet: bytes) -> bool:
    packetChecksum = struct.unpack("!H", packet[-2:])[0]
    headAndBody = packet[:-2]
    checksum = sum(headAndBody)
    return packetChecksum == checksum


class PVPacket:
    def __init__(self, hostAddr: int, deviceAddr: int, command: int, payload: bytes) -> None:
        self.hostAddr = hostAddr
        self.deviceAddr = deviceAddr
        self.command = command
        self.payload = payload

    @classmethod
    def fromBytes(cls, packet: bytes):
        if not verifyChecksum(packet):
            raise ChecksumVerifyException()

        head = packet[0:8]
        payload = packet[8:-1]

        head = struct.unpack("!HHHH", head)

        hostAddr = head[1]
        deviceAddr = head[2]
        command = head[3]

        return cls(hostAddr, deviceAddr, command, payload)

    def toBytes(self) -> bytes:
        # head
        packet = struct.pack("!HHHH", START_CODE,
                             self.hostAddr, self.deviceAddr, self.command)

        # body
        size = len(self.payload) + 1
        packet = packet + struct.pack(str(size) + "p", self.payload)

        checksum = sum(packet)
        packet = packet + struct.pack("!H", checksum)

        return packet

    def __repr__(self) -> str:
        return "host: {}, device: {}, command: {}, payload: {}:{}".format(hex(self.hostAddr), hex(self.deviceAddr), hex(self.command), len(self.payload), '\\'.join([hex(b) for b in self.payload]))


class PVConnector:
    def __init__(self, hostAddr: int = DEFAULT_HOST_ADDR) -> None:
        self._port = Serial()
        self._isConnected = False
        self._hostAddr = hostAddr
        self._deviceAddr = 0
        self._serial = None

    @property
    def serial(self):
        return self._serial

    def connect(self, port: str) -> bool:
        if self._port.is_open:
            self._port.close()

        self._port = Serial()
        self._port.baudrate = 9600
        self._port.parity = PARITY_NONE
        self._port.bytesize = EIGHTBITS
        self._port.stopbits = STOPBITS_ONE
        self._port.dtr = False
        self._port.rts = True
        self._port.port = port
        self._port.write_timeout = 0
        self._port.timeout = 1000/480

        self._port.open()
        return self._port.is_open

    def _readPacket(self) -> bytes:
        return self._port.read(255)

    def _call(self, packet: PVPacket, rx: bool = True) -> PVPacket:
        self._port.write(packet.toBytes())

        if not rx:
            return

        rxPacket = self._readPacket()
        if len(rxPacket) == 0:
            raise NoResponseException()

        return PVPacket.fromBytes(rxPacket)

    def reset(self, deviceAddr: int = 0):
        self._call(PVPacket(self._hostAddr, deviceAddr,
                            RESET_COMMAND, b''), False)

    def getSerialNumber(self, deviceAddr: int = 0):
        # broadcast get serial number command
        response = self._call(PVPacket(self._hostAddr, deviceAddr,
                                       GET_SERIAL_NUMBER_COMMAND, b''))

        # decode payload
        serial = response.payload[1:-1]
        deviceAddr = response.payload[-1]
        return (serial, deviceAddr)

    def setDeviceAddress(self, serial: bytes, addr: int):
        payload = struct.pack("!{}sB".format(len(serial)), serial, addr)

        response = self._call(
            PVPacket(self._hostAddr, 0, SET_DEVICE_ADDR_COMMAND, payload))

        result = response.payload[0] == 0x01

        if result:
          self._deviceAddr = addr
          self._serial = serial
        
        return result

    def getStatusFormat(self):
        response = self._call(PVPacket(self._hostAddr, self._deviceAddr,
                                       GET_STATUS_FORMAT_COMMAND, b''))

        return response.payload[1:-1]

    def getStatus(self):
        response = self._call(
            PVPacket(self._hostAddr, self._deviceAddr, GET_STATUS_COMMAND, b''))

        return response.payload[1:-1]

    def close(self) -> None:
        self._port.close()


class ChecksumVerifyException(Exception):
    pass


class NoResponseException(Exception):
    pass
