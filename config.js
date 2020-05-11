const config = {
    mysql: {
        host: "hopsrv01.hopjes.net:3306",
        user: "meting",
        password: "YENTemEr",
        database: "omvormers"
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