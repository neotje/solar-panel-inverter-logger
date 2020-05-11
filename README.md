# solar-panel-inverter-logger
Log chint power inverter serial output to sql database and generate graphs

### Compatibility
- Windows :x:
- Linux :heavy_check_mark:
- Mac :heavy_minus_sign:

### install
```bash
npm install
```

### run
```
npm run start
```

# config

### MySQL settings
```
mysql: {
    host: "sql server address",
    user: "username",
    password: "user password",
    database: "database name"
}
```

### Devices
```
devices: [
    "/dev/ttyUSB0",
    "/dev/ttyUSB1"
],
```
**Note**: to see available serial ports on linux run: `dmesg | grep tty`

### Log
```
interval: 6000, // log to database every x ms.

// location is used to determine when your inverter turns off, because of no sunlight.
latitude: 51.9915,
longitude: 5.9868
```
