# solar-panel-inverter-logger

Log chint power inverter serial output to sql database and generate graphs

# MQTT Topics

## discovery

```
<discovery_prefix>/<component>/PV_<serial_number>_<status_field>/config
```

## available

```
<discovery_prefix>/<component>/PV_<serial_number>_<status_field>/available
```

## state

```
<discovery_prefix>/<component>/PV_<serial_number>_<status_field>/state
```

# Thanks

[Henk vergenot](https://github.com/hvegh) for the script to read out CMS2000 devices [PV-LOGGER](https://github.com/hvegh/PV-Logger.git)
