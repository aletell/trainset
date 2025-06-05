const { readFile, writeFile } = require('fs').promises;
const path = require('path');

const FILE = path.join(__dirname, '..', '..', 'static', 'files', 'annotations.json');

exports.handler = async function(event) {
  if (event.httpMethod === 'GET') {
    try {
      const data = await readFile(FILE, 'utf8');
      return { statusCode: 200, body: data };
    } catch (err) {
      return { statusCode: 200, body: '[]' };
    }
  }

  if (event.httpMethod === 'POST') {
    try {
      await writeFile(FILE, event.body || '[]');
      return { statusCode: 200, body: JSON.stringify({ status: 'ok' }) };
    } catch (err) {
      console.error(err);
      return { statusCode: 500, body: 'error' };
    }
  }

  return { statusCode: 405, body: 'Method Not Allowed' };
};
