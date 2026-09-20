// Uses the host's existing Playwright installation; no app dependency is added.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const frames = require('../manifest.json');
const only = process.argv.slice(2);
(async () => {
  fs.mkdirSync(path.join(root, 'screens'), { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const results = [];
  for (const frame of frames.filter(f => !only.length || only.includes(f.slug))) {
    const page = await browser.newPage({ viewport: { width: frame.width, height: frame.height }, deviceScaleFactor: 2 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.join(root, 'pages', frame.slug + '.html')).href);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all([...document.images].map(img => img.decode())));
    const geometry = await page.evaluate(() => {
      const bounds = document.querySelector('.app,.board,.phone,.mobile-board,.journey').getBoundingClientRect();
      const overflow = [...document.querySelectorAll('h1,h2,h3,p,button,.panel,.notice,.phone-content,.screen-foot,.consent-actions')].filter(el => {
        const b = el.getBoundingClientRect();
        return el.checkVisibility() && b.width && (b.right > bounds.right + 1 || b.bottom > bounds.bottom + 1 || b.left < bounds.left - 1);
      }).map(el => ({ element: el.tagName, class: el.className, bottom: Math.round(el.getBoundingClientRect().bottom), text: el.textContent.slice(0,80) }));
      const overlaps = [...document.querySelectorAll('.content,.phone-content')].flatMap(main => {
        const footer = main.closest('.phone')?.querySelector('.phone-nav') || document.querySelector('.screen-foot');
        const limit = footer.getBoundingClientRect().top - 8;
        return [...main.children].filter(el => el.getBoundingClientRect().bottom > limit).map(el => ({ text:el.textContent.slice(0,70), bottom:Math.round(el.getBoundingClientRect().bottom), limit:Math.round(limit) }));
      });
      const smallMobileTargets = [...document.querySelectorAll('.phone button,.phone .link,.phone-nav .nav,.phone .consent-check,.phone-header .avatar')].filter(el => {
        const b = el.getBoundingClientRect();
        return b.width < 44 || b.height < 44;
      }).map(el => ({ text:el.textContent, width:el.getBoundingClientRect().width, height:el.getBoundingClientRect().height }));
      return { width: bounds.width, height: bounds.height, overflow, overlaps, smallMobileTargets };
    });
    await page.screenshot({ path: path.join(root,'screens',frame.slug+'.png'), fullPage: false });
    results.push({ screen: frame.slug, ...geometry, errors });
    console.log(`${frame.slug}: ${geometry.width}x${geometry.height}, overflow=${geometry.overflow.length}, overlaps=${geometry.overlaps.length}, smallTargets=${geometry.smallMobileTargets.length}, errors=${errors.length}`);
    await page.close();
  }
  const gallery = await browser.newPage({ viewport: { width: 1600, height: 1800 }, deviceScaleFactor: 1 });
  await gallery.goto(pathToFileURL(path.join(root,'index.html')).href);
  await gallery.evaluate(() => Promise.all([...document.images].map(img => img.decode())));
  await gallery.screenshot({ path:path.join(root,'contact-sheet.png'), fullPage:true });
  await browser.close();
  const previous = only.length && fs.existsSync(path.join(root, 'verification.json')) ? JSON.parse(fs.readFileSync(path.join(root, 'verification.json'))) : [];
  const merged = [...previous.filter(x => !results.some(r => r.screen === x.screen)), ...results].sort((a,b) => a.screen.localeCompare(b.screen));
  fs.writeFileSync(path.join(root,'verification.json'), JSON.stringify(merged,null,2)+'\n');
  if (results.some(r => r.overflow.length || r.overlaps.length || r.smallMobileTargets.length || r.errors.length)) process.exitCode = 1;
})().catch(e => { console.error(e); process.exit(1); });
