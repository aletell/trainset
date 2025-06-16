const express = require('express');
const fs = require('fs');
const path = require('path');
const serveStatic = require('serve-static');
const history = require('connect-history-api-fallback');
const secure = require('ssl-express-www');

const app = express();

app.use(secure);
app.use(express.json());
app.use(history());
app.use(serveStatic(__dirname));

const ANNOTATIONS_FILE = path.join(__dirname, 'static', 'files', 'annotations.json');

app.get('/annotations', (req, res) => {
  fs.readFile(ANNOTATIONS_FILE, 'utf8', (err, data) => {
    if (err) return res.json([]);
    try {
      const json = JSON.parse(data);
      res.json(json);
    } catch (e) {
      res.json([]);
    }
  });
});

app.post('/annotations', (req, res) => {
  fs.writeFile(ANNOTATIONS_FILE, JSON.stringify(req.body), err => {
    if (err) {
      console.error(err);
      return res.status(500).end();
    }
    res.json({ status: 'ok' });
  });
});

// optional route for storing uploaded datasets when running locally
const UPLOAD_FILE = path.join(__dirname, 'static', 'files', 'uploaded.json');
app.post('/upload', (req, res) => {
  fs.writeFile(UPLOAD_FILE, JSON.stringify(req.body), err => {
    if (err) {
      console.error(err);
      return res.status(500).end();
    }
    res.json({ status: 'ok' });
  });
});

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

app.get('/data', (req, res) => {
  const rows = BASE_DATA.map(r => ({...r}));
  if(req.query.clip === '1'){ clipOutliers(rows); }
  res.json(rows);
});

app.get('/export', (req, res) => {
  const d3 = require('d3-dsv');
  fs.promises.readFile(ANNOTATIONS_FILE,'utf8').catch(()=> '[]').then(labelsText => {
    const labels = JSON.parse(labelsText);
    const rows = BASE_DATA.map((r,i)=>({
      series: r.series,
      timestamp: r.timestamp,
      value: r.value,
      label: labels[i] || r.label || ''
    }));
    res.type('text/csv').send(d3.csvFormat(rows));
  }).catch(err => {
    console.error(err);
    res.status(500).end();
  });
});

const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log('Listening on port ' + port);
});

process.on('SIGINT', () => process.exit(1));
