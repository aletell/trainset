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
    const rows = BASE_DATA.map(r => ({...r}));
    if(event.queryStringParameters && event.queryStringParameters.clip === '1'){
      clipOutliers(rows);
    }
    return { statusCode: 200, body: JSON.stringify(rows) };
  }catch(err){
    console.error(err);
    return { statusCode: 500, body: 'error' };
  }
};
