const { readFile } = require('fs').promises;
const path = require('path');
const d3 = require('d3-dsv');

const DATA_FILE = path.join(__dirname, '..', '..', 'static', 'files', 'multi_timeline_data.csv');
const ANNO_FILE = path.join(__dirname, '..', '..', 'static', 'files', 'annotations.json');

exports.handler = async function(){
  try{
    const [dataText, labelsText] = await Promise.all([
      readFile(DATA_FILE,'utf8'),
      readFile(ANNO_FILE,'utf8').catch(()=> '[]')
    ]);
    const rows = d3.csvParse(dataText);
    const labels = JSON.parse(labelsText);
    rows.forEach((r,i)=>{ r.label1 = labels[i] || ''; });
    const csv = d3.csvFormat(rows);
    return { statusCode:200, headers:{'Content-Type':'text/csv'}, body: csv };
  }catch(err){
    console.error(err);
    return { statusCode:500, body:'error' };
  }
};
