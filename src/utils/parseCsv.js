const d3 = require('d3-dsv');

function detectFormat(columns) {
  const cols = columns.map(c => c.toLowerCase());
  if (cols.includes('series') && cols.some(c => c.startsWith('timestamp')) && cols.includes('value')) {
    return 2; // trainset style
  }
  return 1; // multi-column
}

module.exports = function parseCsv(text, filename = '') {
  const trimmed = text.trim();
  // JSON input support
  if (filename.toLowerCase().endsWith('.json') || trimmed.startsWith('{') || trimmed.startsWith('[')) {
    const arr = JSON.parse(trimmed);
    return arr.map(r => ({
      series: r.series,
      timestamp: new Date(r.timestamp),
      value: parseFloat(r.value),
      label: r.label || ''
    }));
  }

  const rows = d3.csvParse(trimmed);
  const cols = rows.columns || Object.keys(rows[0] || {});
  const format = detectFormat(cols);
  const result = [];

  if(format === 2){
    rows.forEach(r => {
      result.push({
        series: r.series,
        timestamp: new Date(r.timestamp),
        value: parseFloat(r.value),
        label: r.label || ''
      });
    });
    return result;
  }

  const tsField = cols[0];
  const labelCols = new Set(cols.filter(c => c.toLowerCase().includes('label')));

  rows.forEach(r => {
    const ts = new Date(r[tsField]);
    for(let i=1;i<cols.length;i++){
      const col = cols[i];
      if(labelCols.has(col)) continue;
      const labelCol = `${col}_label`;
      const label = r[labelCol] || r[`label${i}`] || '';
      result.push({
        series: col,
        timestamp: ts,
        value: parseFloat(r[col]),
        label
      });
    }
  });

  return result;
};
