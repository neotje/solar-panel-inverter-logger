const p = require("path");
const fs = require("fs")
const mysql = require('mysql');

const logger = require("../solarLogger");

const config = require('../../config');

var con = mysql.createConnection(config.mysql);

exports.fromImportLogs = function fromImportLogs(callback) {
    var files = fs.readdirSync(p.join(__dirname, '/import-logs/'));

    console.log(p.join(__dirname, '/import-logs/'), files);
    

    var i = 0;
    let loop = () => {
        var file = files[i];        

        if (file) {
            var path = p.join(__dirname, '/import-logs/', file);

            exports.importOne(path, loop);
        } else {
            callback();
        }
        
        i++;
    }

    loop();
}

exports.importOne = function importOne(path, callback) {
    var fileName = p.basename(path);
    var serialNumber = fileName.split("_")[1];

    var fileContent = fs.readFileSync(path).toString();

    var table = parseCSV(fileContent);

    var query ='';

    console.log(fileName);


    // create table
    var sql = `CREATE TABLE \`${serialNumber}\` (
        time BIGINT(255),
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
        
        for (const report of table) {
            report.time = parseInt(report.time) * 1000;
            report.serial = serialNumber;

            query += `
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
            );`;
        }
        

        con.query(query, (err) => {
            console.log(err);
            
            if (err) return callback(err);
            callback();
        });
    });
}

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