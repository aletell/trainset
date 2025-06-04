const d3 = require('d3-dsv');

function detectFormat(columns){
  if(columns.length === 4 && columns[0].toLowerCase() === 'series' &&
     columns[1].toLowerCase().startsWith('timestamp')){
    return 2; // trainset format
  }
  return 1; // multi-column format
}

module.exports = function parseCsv(text){
  const rows = d3.csvParse(text.trim());
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
