const { readFile } = require('fs').promises;
const path = require('path');
const d3 = require('d3-dsv');
const parseCsv = require('../../src/utils/parseCsv');

const FILE = path.join(__dirname, '..', '..', 'static', 'files', 'multi_timeline_data.csv');

function clipOutliers(rows){
  const stats = {};
  rows.forEach(r => {
    if(!stats[r.series]) stats[r.series] = [];
    stats[r.series].push(r.value);
  });
  Object.keys(stats).forEach(k => {
    const values = stats[k];
    const mean = values.reduce((a,b)=>a+b,0)/values.length;
    const sd = Math.sqrt(values.reduce((a,b)=>a+(b-mean)**2,0)/values.length);
    stats[k] = {mean, sd};
  });
  rows.forEach(r => {
    const {mean, sd} = stats[r.series];
    if(Math.abs(r.value-mean) > 5*sd){
      r.value = mean + Math.sign(r.value-mean)*5*sd;
    }
  });
}

exports.handler = async function(event){
  try{
    const text = await readFile(FILE, 'utf8');
    const rows = parseCsv(text);
    if(event.queryStringParameters && event.queryStringParameters.clip === '1'){
      clipOutliers(rows);
    }
    return { statusCode: 200, body: JSON.stringify(rows) };
  }catch(err){
    console.error(err);
    return { statusCode: 500, body: 'error' };
  }
};
