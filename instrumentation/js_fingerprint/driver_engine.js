/**
* Fingerprinting libraries loaded on the webserver.
* This module is a part of cryptojacking library detection.
*/
'use strinct'; 
const crawler_unit = require('./driver');
//the driver here loads a browser instance, allows the scanner to monitor the traffic, content, etc.
const fs = require('fs');
//Parsing the input argument
const filename = `${Date.now()}`;
const arguments1 = process.argv.slice(2);
const input = arguments1.shift() || '';

if (!input){
   process.stderr.write('Please provide the required page\n');
   process.exit(1);
}

var logged = `${input}\n`;
fs.appendFileSync('./checked_websites.txt', logged);
var input_options = {};
var agrument; 

while ( argument = arguments1.shift() ) {
  //console.log(argument);
   var matches = /--([^=]+)=(.+)/.exec(argument);
   //console.log('we are here');
   if (matches){
       var key = matches[1].replace(/-\w/g, matches => matches[1].toUpperCase());
       var value = matches[2];
       input_options[key] = value;
       console.log(key);
   }
}

const static_checker = new crawler_unit(input, input_options);

static_checker.analyze()
.then(json =>{     
    saveRecord(json);
})
.catch(error => {
    process.stderr.write(error + '\n');
    process.exit(1);
});

function saveRecord(data){
    fs.appendFile('output.json', JSON.stringify(data)+ ',\n', 'utf-8', function(err){
        if (err) throw err;
            process.exit(0);
    });
}
