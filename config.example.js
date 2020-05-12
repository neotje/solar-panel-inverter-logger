const config = {
    mysql: {
        host: "sql server address",
        user: "username",
        password: "password",
        database: "database"
    },
    devices: [
        "/dev/ttyUSB0"//,
        //"/dev/ttyUSB1"
    ],
    interval: 6000, // ms
    latitude: 51.9915,
    longitude: 5.9868,
    import: false
}

module.exports = config;