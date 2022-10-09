import sys
from solarInverterToHass.pv import PVConnector

def main():
  conn = PVConnector()
  
  if conn.connect("/dev/ttyUSB1"):
    print("Connected!")
  else:
    print("failed!!!")

  conn.reset()
  serial = conn.getSerialNumber()[0]
  conn.setDeviceAddress(serial, 1)
  print(conn.getSerialNumber())

  conn.close()

if __name__ == "__main__":
  main()