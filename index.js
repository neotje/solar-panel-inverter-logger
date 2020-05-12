const pv = require("./packages/pv");
const solarLogger = require("./packages/solarLogger");
const config = require("./config");
const importer = require("./packages/CSVimporter");
const path = require("path")

var intervals = [];

console.log(config);


for (const device of config.devices) {
    intervals.push(pv.reportInterval(device, config.interval, (report, err)=>{
        if (!err) {
            solarLogger.savePVreport(report, (err) => {
                if(err) console.error(err);
            });   
        }
    }));

    console.log(`started report interval for: ${device}`);
}

if (config.import == true) {
    importer.fromImportLogs(()=>{
        console.log('done!');
        
    });
}