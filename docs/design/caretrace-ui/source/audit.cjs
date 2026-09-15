// Read-only checks of the rendered artwork, including inherited surface colors.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const results = [];
  for (const frame of require('../manifest.json')) {
    const page = await browser.newPage({ viewport: { width: frame.width, height: frame.height } });
    await page.goto(pathToFileURL(path.join(root, 'pages', frame.slug + '.html')).href);
    await page.evaluate(() => document.fonts.ready);
    const result = await page.evaluate(() => {
      const rgb = value => (value.match(/[\d.]+/g) || []).map(Number);
      const lum = color => color.slice(0, 3).map(v => v / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4).reduce((a, v, i) => a + v * [.2126, .7152, .0722][i], 0);
      const surface = el => {
        if (!el) return [255, 255, 255];
        const c = rgb(getComputedStyle(el).backgroundColor);
        const alpha = c[3] ?? 1;
        if (alpha === 1) return c;
        return surface(el.parentElement).map((v, i) => c[i] * alpha + v * (1 - alpha));
      };
      const contrast = [], clipped = [];
      for (const el of document.querySelectorAll('body *')) {
        if (!el.checkVisibility() || el.closest('svg')) continue;
        const text = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
        if (!text) continue;
        const style = getComputedStyle(el), fg = rgb(style.color), bg = surface(el);
        const a = lum(fg), b = lum(bg), ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
        const large = parseFloat(style.fontSize) >= 24 || (parseFloat(style.fontSize) >= 18.66 && parseFloat(style.fontWeight) >= 700);
        contrast.push({ text: text.slice(0, 65), foreground: style.color, background: bg, ratio: +ratio.toFixed(2), required: large ? 3 : 4.5 });
        if (el.clientWidth && el.scrollWidth > el.clientWidth + 2 && !['visible', 'auto'].includes(style.overflowX)) clipped.push(text.slice(0, 80));
      }
      return { fontLoaded: document.fonts.check('400 15px Manrope'), contrastFailures: contrast.filter(x => x.ratio < x.required), textSamples: contrast.length, minimumContrast: Math.min(...contrast.map(x => x.ratio)), clipped };
    });
    results.push({ screen: frame.slug, ...result });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(root, 'accessibility-review.json'), JSON.stringify(results, null, 2) + '\n');
  const failures = results.filter(x => !x.fontLoaded || x.contrastFailures.length || x.clipped.length);
  console.log(JSON.stringify(failures.length ? failures : { screens: results.length, status: 'passed', minimumContrast: Math.min(...results.map(x => x.minimumContrast)) }, null, 2));
  if (failures.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exit(1); });
