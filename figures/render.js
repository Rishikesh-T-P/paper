const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [svgPath, pngPath, pdfPath] = process.argv.slice(2);
  const svg = fs.readFileSync(svgPath, 'utf8');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 1240 }, deviceScaleFactor: 2 });
  await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await p.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: 1100, height: 1240 } });
  await p.pdf({ path: pdfPath, width: '1100px', height: '1240px', printBackground: true, pageRanges: '1' });
  await b.close();
})();
