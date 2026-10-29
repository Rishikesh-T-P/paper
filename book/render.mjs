import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const OUT = process.argv[2] || 'Network-Engineer-Placements-2027';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
const p = await b.newPage();
await p.goto('file://' + process.cwd() + '/dist/' + OUT + '.html');
await p.waitForFunction(() => document.querySelector('.pagedjs_pages') && !document.querySelector('.pagedjs_pages:empty'), null, { timeout: 600000 });
// wait until page count stops growing
let n = -1, m = 0;
while (n !== m) { n = m; await p.waitForTimeout(2500); m = await p.evaluate(() => document.querySelectorAll('.pagedjs_page').length); }
await p.pdf({ path: 'dist/' + OUT + '.pdf', preferCSSPageSize: true, outline: true, tagged: true, printBackground: true, timeout: 0 });
console.log('pages', m);
await b.close();
