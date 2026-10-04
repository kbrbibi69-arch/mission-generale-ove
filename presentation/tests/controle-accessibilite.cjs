const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '..') + '/presentation_bureau_ove_sapin2.html';
(async () => {
  const br = await chromium.launch({ ...(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {}) });
  const ctx = await br.newContext({ viewport: { width: 1920, height: 1080 } });
  const p = await ctx.newPage(); await p.goto(URL); await p.waitForTimeout(500);
  await p.keyboard.press(' '); await p.waitForTimeout(1500);
  const small = [], low = [], noname = [], heads = [];
  for (let i = 1; i <= 18; i++) {
    const n = await p.evaluate(i => window.__ove.steps[i - 1], i);
    await p.evaluate(i => window.__ove.go(i, 0), i); await p.waitForTimeout(1300);
    await p.evaluate(([i, n]) => window.__ove.go(i, n), [i, n]); await p.waitForTimeout(1800);
    const r = await p.evaluate(i => {
      const sc = document.querySelectorAll('.scene')[i - 1], dark = sc.classList.contains('dark');
      const lum = c => { const a = c.match(/[\d.]+/g).map(Number); const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(a[0]) + .7152 * f(a[1]) + .0722 * f(a[2]); };
      const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
      const bgOf = el => { for (let e = el; e && e !== sc.parentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.backgroundImage !== 'none') return null; const m = cs.backgroundColor.match(/[\d.]+/g); if (m && (m.length < 4 || +m[3] >= .95)) return cs.backgroundColor; } return getComputedStyle(sc.querySelector('.bg')).backgroundColor; };
      const out = { small: [], low: [], noname: [], heads: [...sc.querySelectorAll('h1,h2,h3')].map(h => h.tagName) };
      const w = document.createTreeWalker(sc, NodeFilter.SHOW_TEXT);
      const seen = new Set();
      while (w.nextNode()) {
        const t = w.currentNode, txt = t.textContent.trim(); if (!txt) continue; const el = t.parentElement; if (seen.has(el) || el.closest('.sr-only,svg,script,style,#hud,.ov,#notes-panel')) continue; seen.add(el);
        const cs = getComputedStyle(el), rc = el.getBoundingClientRect(); if (!rc.width || !rc.height || cs.visibility === 'hidden') continue;
        let op = 1; for (let e = el; e && e !== sc; e = e.parentElement) op *= +getComputedStyle(e).opacity; if (op < .5) continue;
        const fs = parseFloat(cs.fontSize); if (fs < 22) out.small.push(fs + 'px « ' + txt.slice(0, 40) + ' »');
        const bg = bgOf(el); if (!bg) continue; const ratio = cr(cs.color, bg); const large = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
        if (ratio < (large ? 3 : 4.5)) out.low.push(ratio.toFixed(2) + ' ' + fs + 'px « ' + txt.slice(0, 40) + ' »');
      }
      sc.querySelectorAll('button,[role=button]').forEach(b => { if (!(b.textContent.trim() || b.getAttribute('aria-label'))) out.noname.push(b.className); });
      return out;
    }, i);
    r.small.forEach(x => small.push('S' + i + ' ' + x)); r.low.forEach(x => low.push('S' + i + ' ' + x)); r.noname.forEach(x => noname.push('S' + i + ' ' + x)); heads.push('S' + i + ':' + r.heads.join('/'));
  }
  console.log('TEXTES < 22 px :', small.length); console.log(small.join('\n'));
  console.log('\nCONTRASTES sous AA :', low.length); console.log(low.join('\n'));
  console.log('\nBOUTONS SANS NOM :', noname.length, noname.join(','));
  console.log('\nTITRES', heads.join('  '));
  // tabulation
  await p.evaluate(() => window.__ove.go(3, 4)); await p.waitForTimeout(1800);
  await p.evaluate(() => document.activeElement.blur());
  const seq = []; for (let k = 0; k < 14; k++) { await p.keyboard.press('Tab'); seq.push(await p.evaluate(() => { const a = document.activeElement; return (a.getAttribute('aria-label') || a.id || a.className || a.tagName).slice(0, 34) + ' | ombre:' + (getComputedStyle(a).boxShadow !== 'none' ? 'oui' : 'non'); })); }
  console.log('\nTABULATION S3 :\n' + seq.join('\n'));
  const inert = await p.evaluate(() => [...document.querySelectorAll('.scene')].filter(s => !s.classList.contains('active') && !s.classList.contains('leaving')).every(s => s.inert)); console.log('Scènes inactives non focalisables (inert) :', inert);
  // fluidité indicative
  await p.evaluate(() => window.__ove.go(3, 4)); await p.waitForTimeout(1500);
  const perf = await p.evaluate(async () => { const d = []; let t0 = performance.now(); await new Promise(res => { function f(t) { d.push(t - t0); t0 = t; if (d.length < 180) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); }); d.shift(); d.sort((a, b) => a - b); return { moy: (d.reduce((a, b) => a + b) / d.length).toFixed(1), p95: d[Math.floor(d.length * .95)].toFixed(1), max: d[d.length - 1].toFixed(1) }; });
  console.log('\nFLUIDITÉ (S3, rendu logiciel sans GPU, indicatif) ms/image :', JSON.stringify(perf));
  // mouvement réduit
  const c2 = await br.newContext({ viewport: { width: 1920, height: 1080 }, reducedMotion: 'reduce' }); const q = await c2.newPage(); await q.goto(URL); await q.waitForTimeout(600);
  console.log('Mouvement réduit : calm =', await q.evaluate(() => document.body.classList.contains('calm')), '| raccord rejoué =', await q.evaluate(() => document.getElementById('s1').classList.contains('intro')));
  await q.keyboard.press('ArrowRight'); await q.waitForTimeout(300); console.log('Mouvement réduit : navigation OK, étape =', JSON.stringify(await q.evaluate(() => window.__ove.state())));
  // 1280x720 et 1366x768 : mise à l'échelle
  for (const [w, h] of [[1280, 720], [1366, 768], [1024, 768]]) { const c3 = await br.newContext({ viewport: { width: w, height: h } }); const z = await c3.newPage(); await z.goto(URL + '#7'); await z.waitForTimeout(1800); const r = await z.evaluate(() => { const b = document.getElementById('stage').getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height), Math.round(b.left), Math.round(b.top)].join('x'); }); console.log('Viewport', w + 'x' + h, '→ scène', r, '(largeur×hauteur×gauche×haut)'); await z.screenshot({ path: require('os').tmpdir() + '/vp-' + w + '.png' }); }
  await br.close();
})();
