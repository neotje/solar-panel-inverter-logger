const { exec } = require("child_process");
const suntime = require('sunrise-sunset-js');
const config = require('../../config');

/**
 * @module pv
 */


/**
 * get pv report from serial port.
 * @param {String} device path to device.
 * @param {pvReportCallback} callback 
 */
function getReport(device, callback) {
    exec(
        `perl ./pv.pl get ${device}`,
        { cwd: __dirname },
        (error, stdout, stderr) => {
            if (error) {
                console.error(error.message);
                
                callback(undefined, error);
                return;
            }
            if (stderr) {
                callback(undefined, new Error(stderr));
                return;
            }

            //console.log(stdout);
            callback(parseCSV(stdout)[0]);
        });
}

/**
 * Get pv report every x miliseconds. only reports when sun is up.
 * @param {String} device serial port path.
 * @param {Int} interval time between intervals in ms.
 * @param {pvReportCallback} listener 
 */
function reportInterval(device, interval, listener){
    return setInterval(()=>{
        var currentTime = new Date().getTime();
        var sunrise = suntime.getSunrise(config.latitude, config.longitude).getTime();
        var sunset = suntime.getSunset(config.latitude, config.longitude).getTime();

        if(currentTime > sunrise && currentTime < sunset) {
            getReport(device, listener);
        } else {
            console.log("sun gone");
        }
    }, interval);
}

/**
 * 
 * @param {String} csv 
 */
function parseCSV(csv) {
    var rows = csv.split("\n");
    var columns = rows[0].split("|");

    var arr = []

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i].split("|");

        if (row.length > 1) {
            var item = {};

            for (let ci = 0; ci < columns.length; ci++) {
                const column = columns[ci];

                item[column] = row[ci];
            }

            arr.push(item);
        }
    }

    return arr;
}

exports.getReport = getReport;
exports.reportInterval = reportInterval;

/**
 * @callback pvReportCallback
 * @param {pvReport} report pv report.
 * @param {Error} err defined if an error occured.
 */

 /**
  * @typedef {Object} pvReport
  * @property {String} serial
  * @property {String} time
  * @property {String} TEMP
  * @property {String} ETODAY
  * @property {String} IAC
  * @property {String} VAC
  * @property {String} FAC
  * @property {String} PAC
  * @property {String} ZAC
  * @property {String} ETOTAL
  * @property {String} HTOTAL
  * @property {String} MODE
  */