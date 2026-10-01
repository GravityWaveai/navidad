const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright-core');
const root = __dirname;
const types = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
const srv = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
});
(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const port = srv.address().port;
  const shots = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--disable-web-security'] });
  for (const s of shots) {
    const t0 = Date.now();
    const p = await b.newPage({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: 1 });
    p.on('console', m => console.log('[page]', m.text()));
    p.on('pageerror', e => console.log('[pageerror]', e.message));
    const qs = new URLSearchParams(s).toString();
    await p.goto(`http://127.0.0.1:${port}/scene.html?${qs}`);
    await p.waitForFunction(() => window.__done === true, null, { timeout: 600000 });
    const anchors = await p.evaluate(() => window.__anchors);
    await p.locator('canvas').screenshot({ path: s.out, omitBackground: true });
    fs.writeFileSync(s.out.replace(/\.png$/, '.json'), JSON.stringify({ anchors, ...s }));
    console.log(s.out, anchors, ((Date.now() - t0) / 1000).toFixed(1) + 's');
    await p.close();
  }
  await b.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
