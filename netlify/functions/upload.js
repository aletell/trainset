const { writeFile } = require('fs').promises;
const path = require('path');

const FILE = path.join(__dirname, '..', '..', 'static', 'files', 'uploaded.json');

exports.handler = async function(event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  try {
    await writeFile(FILE, event.body || '[]');
    return { statusCode: 200, body: JSON.stringify({ status: 'ok' }) };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: 'error' };
  }
};
