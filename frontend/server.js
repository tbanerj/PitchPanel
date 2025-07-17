const { createServer } = require('https');
const { parse } = require('url');
const fs = require('fs');
const next = require('next');

const port = 443;
const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

// Load your .key and .cer files
const httpsOptions = {
  key: fs.readFileSync('./ssl/key.key'),   // your .key file
  cert: fs.readFileSync('./ssl/cert.cer')  // your .cer file
};

app.prepare().then(() => {
  createServer(httpsOptions, (req, res) => {
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  }).listen(port, () => {
    console.log(`> HTTPS server running at https://localhost:${port}`);
  });
});


require('http').createServer((req, res) => {
  res.writeHead(301, {
    Location: 'https://' + req.headers.host + req.url
  });
  res.end();
}).listen(80);
