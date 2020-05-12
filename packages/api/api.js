const express = require("express");
const solarLogs = require("../solarLogger");
const app = express();
const config = require("../../config");

app.get('/get/:device/report/:year/:month/:day', function (req, res) {
    var date = new Date(req.params.year, req.params.month - 1, req.params.day)
    var report = solarLogs.getDayReportFromDevice(req.params.device, date, (data) => {
        res.json(data);
    });
});

app.get('/get/list', function (req, res) {
    solarLogs.getDeviceList((list) => {
        res.json(list);
    });
});

exports.startApiServer = (callback = () => { }) => {
    app.listen(config.port, () => {
        console.log(`solar panel inverter logger API listening at http://localhost:${config.port}`);
        callback();
    });
}