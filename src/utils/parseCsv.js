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

  const lower = filename.toLowerCase();

  if (lower && !lower.endsWith('.csv') && !lower.endsWith('.json')) {
    throw new Error('Unsupported file type');
  }

  // JSON input support
  if (lower.endsWith('.json') || trimmed.startsWith('{') || trimmed.startsWith('[')) {
    let arr;
    try {
      arr = JSON.parse(trimmed);
    } catch (e) {
      throw new Error('Invalid JSON file');
    }
    return arr.map(r => ({
      series: r.series,
      timestamp: new Date(r.timestamp),
      value: parseFloat(r.value),
      label: r.label || ''
    }));
  }

  let rows;
  try {
    rows = d3.csvParse(trimmed);
  } catch (e) {
    throw new Error('Invalid CSV format');
  }
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
    const rawTs = r[tsField];
    const ts = new Date(rawTs.replace(' ', 'T'));
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
