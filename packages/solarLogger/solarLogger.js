'use strict';

const config = require('../../config');
const mysql = require('mysql');

/**
 * @module solarLogger
 */


/**
 * save pv report to sql database.
 * @param {pvReport} report 
 * @param {errCallback} callback 
 */

function savePVreport(report, callback) {
    var con = mysql.createConnection(config.mysql);

    // create table
    var sql = `CREATE TABLE \`${report.serial}\` (
        time BIGINT(255) UNIQUE,
        TEMP FLOAT(24),
        ETODAY FLOAT(24),
        IAC FLOAT(24),
        VAC FLOAT(24),
        FAC FLOAT(24),
        PAC FLOAT(24),
        ZAC FLOAT(24),
        ETOTAL FLOAT(24),
        HTOTAL FLOAT(24),
        MODE FLOAT(24)
    )`;

    con.query(sql, (err, result) => {
        // insert data into the table
        var sql = `
        INSERT INTO \`${report.serial}\` (
            time,
            TEMP,
            ETODAY,
            IAC,
            VAC,
            FAC,
            PAC,
            ZAC,
            ETOTAL,
            HTOTAL,
            MODE
        ) VALUES (
            ${report.time},
            ${report.TEMP},
            ${report.ETODAY},
            ${report.IAC},
            ${report.VAC},
            ${report.FAC},
            ${report.PAC},
            ${report.ZAC},
            ${report.ETOTAL},
            ${report.HTOTAL},
            ${report.MODE}
        )`;

        con.query(sql, (err) => {
            con.end()
            if (err) return callback(err);
            callback();
        });
    });


}

/**
 * get array of serialnumbers in the database.
 * @param {Function} callback callback(arr).
 */
function getSerialNumberList(callback) {
    var con = mysql.createConnection(config.mysql);

    con.query('show tables', (err, res) => {
        var arr = []

        for (const row of res) {
            arr.push(row[Object.keys(row)[0]]);
        }
        con.end();
        callback(arr);
    });
}

/**
 * get day report from one device by serial number.
 * @param {String} serial serial number of inverter.
 * @param {Date} day the day to get the report of. day start at 00:00
 * @param {Function} callback array of data.
 */
function getDayFromDevice(serial, day, callback) {
    var con = mysql.createConnection(config.mysql);

    var start = day.getTime();

    day.setDate(day.getDate() + 1)
    var end = day.getTime();

    var sql = `
    SELECT * FROM ${serial} 
    WHERE time BETWEEN ${start} AND ${end}`;

    con.query(sql, (err, res) => {
        con.end();
        callback(res);
    });
}

exports.savePVreport = savePVreport;
exports.getDeviceList = getSerialNumberList;
exports.getDayReportFromDevice = getDayFromDevice;

/**
 * @callback errCallback
 * @param {Error} err
 */