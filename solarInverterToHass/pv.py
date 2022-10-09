from serial import Serial, PARITY_NONE, EIGHTBITS, STOPBITS_ONE
import struct

DEFAULT_HOST_ADDR = 0x0100

START_CODE = 0xAAAA

RESET_COMMAND = 0x04
GET_SERIAL_NUMBER_COMMAND = 0x0000
SET_DEVICE_ADDR_COMMAND = 0x01
GET_STATUS_COMMAND = 0x0102
GET_VERSION_COMMAND = 0x0103

SERIAL_NUMBER_PAYLOAD_CODE = 0x80
SUCCESS_PAYLOAD_CODE = 0x81
STATUS_PAYLOAD_CODE = 0x0182
VERSION_PAYLOAD_CODE = 0x0183


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
        packet = struct.pack("!HHHH", START_CODE, self.hostAddr, self.deviceAddr, self.command)
        
        # body
        size = len(self.payload) + 1
        packet = packet + struct.pack(str(size) + "p", self.payload)

        checksum = sum(packet)
        packet = packet + struct.pack("!H", checksum)

        return packet


class PVConnector:
    def __init__(self, hostAddr: int = DEFAULT_HOST_ADDR) -> None:
        self._port = Serial()
        self._isConnected = False
        self._hostAddr = hostAddr
        self._deviceAddr = 0

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

    def reset(self):
        packet = PVPacket(self._hostAddr, self._deviceAddr, RESET_COMMAND, b'').toBytes()

        self._port.write(packet)

    def getSerialNumber(self):
        packet = PVPacket(self._hostAddr, self._deviceAddr, GET_SERIAL_NUMBER_COMMAND, b'').toBytes()

        self._port.write(packet)
        packet = self._readPacket()

        print(packet)

        packet = PVPacket.fromBytes(packet)


        serial = packet.payload[1:-1]
        deviceAddr = packet.payload[-1]

        return (serial, deviceAddr)

    def setDeviceAddress(self, serial: bytes, addr: int):
        payload = struct.pack("{}sB".format(len(serial)), serial, addr)
        
        packet = PVPacket(self._hostAddr, 0, SET_DEVICE_ADDR_COMMAND, payload).toBytes()
        self._port.write(packet)

        packet = self._readPacket()
        packet = PVPacket.fromBytes(packet)


    def getStatus(self):
        packet = PVPacket(self._hostAddr, self._deviceAddr, GET_VERSION_COMMAND, b'').toBytes()
        print(packet)

        self._port.write(packet)
        packet = self._readPacket()

        print(packet)


    def close(self) -> None:
        self._port.close()


class ChecksumVerifyException(Exception):
  pass