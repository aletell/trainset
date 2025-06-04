const { readFile } = require('fs').promises;
const path = require('path');
const d3 = require('d3-dsv');

const FILE = path.join(__dirname, '..', '..', 'static', 'files', 'multi_timeline_data.csv');

function clipOutliers(rows){
  const numericKeys = Object.keys(rows[0]).filter(k => k !== 'timestamp' && !isNaN(rows[0][k]));
  const stats = {};
  numericKeys.forEach(k => {
    const values = rows.map(r => +r[k]);
    const mean = values.reduce((a,b)=>a+b,0)/values.length;
    const sd = Math.sqrt(values.reduce((a,b)=>a+(b-mean)**2,0)/values.length);
    stats[k] = {mean, sd};
  });
  rows.forEach(r => {
    numericKeys.forEach(k => {
      const v = +r[k];
      const {mean, sd} = stats[k];
      if(Math.abs(v-mean) > 5*sd){
        r[k] = mean + Math.sign(v-mean)*5*sd;
      }
    });
  });
}

exports.handler = async function(event){
  try{
    const text = await readFile(FILE, 'utf8');
    const rows = d3.csvParse(text);
    rows.forEach(r => { r.timestamp = new Date(r.timestamp); });
    if(event.queryStringParameters && event.queryStringParameters.clip === '1'){
      clipOutliers(rows);
    }
    return { statusCode: 200, body: JSON.stringify(rows) };
  }catch(err){
    console.error(err);
    return { statusCode: 500, body: 'error' };
  }
};
