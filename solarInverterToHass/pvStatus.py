import struct


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


TEMP_STATUS = StatusField("Internal temperature",
                          "TEMP", "C", 0.1, [0x0], "!H")
ETODAY_STATUS = StatusField(
    "Generated energy today", "ETODAY", "kWh", 0.01, [0x0d], "!H")
IAC_STATUS = StatusField("Grid current", "IAC", "A", 0.1, [0x41], "!H")
VAC_STATUS = StatusField("Grid voltage", "VAC", "V", 0.1, [0x42], "!H")
FAC_STATUS = StatusField("Grid frequency", "FAC", "Hz", 0.01, [0x43], "!H")
PAC_STATUS = StatusField("Output power", "PAC", "W", 1, [0x44], "!H")
ZAC_STATUS = StatusField("Grid impedance", "ZAC", "Ohm", 0.001, [0x45], "!H")
ETOTAL_STATUS = StatusField("Total amount of generated energy",
                            "ETOTAL", "kWh", 0.1, [0x47, 0x48], "!I")
HTOTAL_STATUS = StatusField(
    "Total on time", "HTOTAL", "H", 1, [0x49, 0x4a], "!I")
MODE_STATUS = StatusField("Internal temperature",
                          "MODE", "", 0.1, [0x4c], "!H")


class PVStatus:
    def __init__(self, statusFields: list, format: bytes = b'') -> None:
        self.statusFields = statusFields
        self.format = format

    def fromBytes(self, status: bytes) -> dict:
        statusObject = {}

        for i, dataKey in enumerate(self.format):
            statusObject[dataKey] = status[i*2:2 + i*2]

        statusReport = {}

        for statusField in self.statusFields:
            statusReport[statusField.key] = statusField.getValue(statusObject)

        return statusReport