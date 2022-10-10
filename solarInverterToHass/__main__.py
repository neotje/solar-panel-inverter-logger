import sys
from solarInverterToHass.pv import PVConnector
from solarInverterToHass.pvStatus import ETODAY_STATUS, PVStatus

def main():
  conn = PVConnector()
  status = PVStatus([ETODAY_STATUS])
  
  if conn.connect("/dev/ttyUSB0"):
    print("Connected!")
  else:
    print("failed!!!")

  conn.reset()
  serial = conn.getSerialNumber()
  
  if serial is not None:
    print(serial)
    
    if conn.setDeviceAddress(serial[0], 1):
      print("device addr changed!")
    else:
      print("could not set device addr!")

    status.format = conn.getStatusFormat(1)

    print(status.fromBytes(conn.getStatus(1)))

  conn.close()

if __name__ == "__main__":
  main()