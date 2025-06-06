const { readFile } = require('fs').promises;
const d3 = require('d3-dsv');

function generateData(){
  const start = Date.parse('2019-01-01T00:00:00Z');
  const rows = [];
  for(let i=0;i<40;i++){
    const ts = new Date(start + i*300000).toISOString();
    const vals = [
      20 + Math.sin(i/2)*10,
      30 + Math.cos(i/3)*15,
      25 + Math.sin(i/4)*8
    ];
    vals.forEach((v,idx)=>{
      rows.push({
        series: `series${idx+1}`,
        timestamp: ts,
        value: parseFloat(v.toFixed(2)),
        label: i%12 < 6 ? 'occupied' : ''
      });
    });
  }
  return rows;
}
const BASE_DATA = generateData();
const ANNO_FILE = require('path').join(__dirname, '..', '..', 'static', 'files', 'annotations.json');

exports.handler = async function(){
  try{
    const labelsText = await readFile(ANNO_FILE,'utf8').catch(()=> '[]');
    const labels = JSON.parse(labelsText);
    const rows = BASE_DATA.map((r,i)=>({
      series: r.series,
      timestamp: r.timestamp,
      value: r.value,
      label: labels[i] || r.label || ''
    }));
    const csv = d3.csvFormat(rows);
    return { statusCode:200, headers:{'Content-Type':'text/csv'}, body: csv };
  }catch(err){
    console.error(err);
    return { statusCode:500, body:'error' };
  }
};
