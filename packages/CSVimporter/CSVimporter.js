const p = require("path");
const fs = require("fs")
const mysql = require('mysql');

const logger = require("../solarLogger");

const config = require('../../config');

var con = mysql.createConnection(config.mysql);

exports.fromImportLogs = function fromImportLogs(callback) {
    var files = fs.readdirSync(p.join(__dirname, '/import-logs/'));

    console.log(p.join(__dirname, '/import-logs/'));
    

    var i = 0;
    let loop = () => {
        var file = files[i];

        if (file) {
            var path = p.join('./import-logs', file);

            exports.importOne(path, loop);
        } else {
            callback();
        }
        
        i++;
    }
}

exports.importOne = function importOne(path, callback) {
    var fileName = p.basename(path);
    var serialNumber = fileName.split("_")[1];

    var fileContent = fs.readFileSync(path).toString();

    var table = parseCSV(fileContent);

    var i = 0;

    let loop = (err) => {
        if (err) console.log(err);

        var row = table[i];

        if (row) {
            row.time = parseInt(row.time) * 1000;
            console.log(row.time);
            
            row.serial = serialNumber;
            logger.savePVreport(row, loop);
        } else {
            return callback();
        }

        i++;
    }

    loop(undefined);
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