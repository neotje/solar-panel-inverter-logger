const config = {
    mysql: {
        host: "localhost",
        user: "root",
        password: "pass",
        database: "logs"
    },
    devices: [
        "/dev/ttyUSB0"//,
        //"/dev/ttyUSB1"
    ],
    interval: 6000, // ms
    latitude: 51.9915,
    longitude: 5.9868
}

module.exports = config;