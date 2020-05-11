const pv = require("./packages/pv");
const solarLogger = require("./packages/solarLogger");
const config = require("./config");

var intervals = [];


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

solarLogger.getDayReportFromDevice('1304DP0010', new Date(2020, 4, 6), res => {
    console.log(res);
})

