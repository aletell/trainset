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

const DATA_FILE = path.join(__dirname, 'static', 'files', 'multi_timeline_data.csv');
const parseCsv = require('./src/utils/parseCsv');

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
  fs.readFile(DATA_FILE, 'utf8', (err, text) => {
    if(err) return res.status(500).end();
    const rows = parseCsv(text);
    if(req.query.clip === '1'){ clipOutliers(rows); }
    res.json(rows);
  });
});

app.get('/export', (req, res) => {
  const d3 = require('d3-dsv');
  Promise.all([
    fs.promises.readFile(DATA_FILE,'utf8'),
    fs.promises.readFile(ANNOTATIONS_FILE,'utf8').catch(()=> '[]')
  ]).then(([dataText, labelsText]) => {
    const rows = d3.csvParse(dataText);
    const labels = JSON.parse(labelsText);
    rows.forEach((r,i)=>{ r.label1 = labels[i] || ''; });
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
