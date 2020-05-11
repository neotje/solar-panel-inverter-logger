'use strict';

const config = require('../../config');
const mysql = require('mysql');

/**
 * @module solarLogger
 */

var con = mysql.createConnection(config.mysql);

/**
 * save pv report to mongodb.
 * @param {pvReport} report 
 * @param {errCallback} callback 
 */

function savePVreport(report, callback) {
    // create table
    var sql = `CREATE TABLE \`${report.serial}\` (
        time INT(255),
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
            if (err) return callback(err);
            callback();
        });
    });
}

function getSerialNumberList(callback) {
    con.query('show tables', (err, res) => {
        callback(res);
    });
}

function getDayFromDevice(serial, day, callback) {
    var start = day.getUTCSeconds();

    day.setDate(day.getDate() + 1)
    var end = day.getTime();

    console.log(start, end);
    

    var sql = `
    SELECT * FROM ${serial} 
    WHERE time BETWEEN ${start} AND ${end}`;

    con.query(sql, (err, res) => {
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