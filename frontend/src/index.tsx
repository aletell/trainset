import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import Plot from 'react-plotly.js';
import axios from 'axios';

const App = () => {
  const [data, setData] = useState([]);
  const [filename, setFilename] = useState('');
  const [hoverData, setHoverData] = useState(null);
  const [selectedData, setSelectedData] = useState([]);
  const [labels, setLabels] = useState([]);
  const [selectedLabel, setSelectedLabel] = useState('');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const contents = e.target.result;
      const parsedData = parseCSV(contents);
      setData(parsedData);
      setFilename(file.name);
    };
    reader.readAsText(file);
  };

  const parseCSV = (contents) => {
    const rows = contents.split('\n');
    const header = rows[0].split(',');
    const parsedData = rows.slice(1).map((row) => {
      const values = row.split(',');
      const obj = {};
      header.forEach((key, index) => {
        obj[key] = values[index];
      });
      return obj;
    });
    return parsedData;
  };

  const handleHover = (event) => {
    setHoverData(event.points[0]);
  };

  const handleSelect = (event) => {
    setSelectedData(event.points);
  };

  const handleAddLabel = () => {
    const updatedData = data.map((point) => {
      if (selectedData.some((selected) => selected.x === point.timestamp && selected.y === point.value)) {
        return { ...point, label: selectedLabel };
      }
      return point;
    });
    setData(updatedData);
  };

  const handleDeleteLabel = () => {
    const updatedData = data.map((point) => {
      if (selectedData.some((selected) => selected.x === point.timestamp && selected.y === point.value)) {
        return { ...point, label: '' };
      }
      return point;
    });
    setData(updatedData);
  };

  const handleLabelChange = (event) => {
    setSelectedLabel(event.target.value);
  };

  const handleAddNewLabel = () => {
    const newLabel = prompt('Enter new label:');
    if (newLabel && !labels.includes(newLabel)) {
      setLabels([...labels, newLabel]);
      setSelectedLabel(newLabel);
    }
  };

  const handleDeleteSelectedLabel = () => {
    setLabels(labels.filter((label) => label !== selectedLabel));
    setSelectedLabel(labels[0] || '');
  };

  const handleExport = () => {
    const csvContent = [
      'series,timestamp,value,label',
      ...data.map((point) => `${point.series},${point.timestamp},${point.value},${point.label}`)
    ].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename.split('.csv')[0]}-labeled.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <h1>TRAINSET: Time Series Labeling Tool</h1>
      <input type="file" onChange={handleFileUpload} />
      <div>
        <label>
          Label:
          <select value={selectedLabel} onChange={handleLabelChange}>
            {labels.map((label) => (
              <option key={label} value={label}>
                {label}
              </option>
            ))}
          </select>
          <button onClick={handleAddNewLabel}>Add Label</button>
          <button onClick={handleDeleteSelectedLabel}>Delete Label</button>
        </label>
      </div>
      <Plot
        data={[
          {
            x: data.map((point) => point.timestamp),
            y: data.map((point) => point.value),
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: 'red' },
          },
        ]}
        layout={{ title: 'Time Series Plot' }}
        onHover={handleHover}
        onSelected={handleSelect}
      />
      {hoverData && (
        <div>
          <h3>Hover Data</h3>
          <p>Time: {hoverData.x}</p>
          <p>Value: {hoverData.y}</p>
          <p>Series: {hoverData.curveNumber}</p>
        </div>
      )}
      <button onClick={handleAddLabel}>Add Label</button>
      <button onClick={handleDeleteLabel}>Delete Label</button>
      <button onClick={handleExport}>Export</button>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
