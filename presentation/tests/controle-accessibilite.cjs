// Contrôles réels (Chromium) : taille de police ≥ 22 px, contraste AA, palette, focus visible, mouvement réduit, lang/titre.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const FILE = path.resolve(__dirname, '..', 'presentation_ove_sapin2.html');
const F = 'file://' + FILE;
const lum = c => { const a = c.map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * a[0] + .7152 * a[1] + .0722 * a[2]; };
const ratio = (a, b) => { const A = lum(a), B = lum(b); return (Math.max(A, B) + .05) / (Math.min(A, B) + .05); };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const ok = (c, m) => { console.log((c ? 'OK   ' : 'ÉCHEC') + ' ' + m); if (!c) process.exitCode = 1; };
  await p.goto(F); await p.waitForTimeout(1000);
  const n = await p.evaluate(() => window.__ove.n), steps = await p.evaluate(() => window.__ove.steps);
  const small = new Map(), low = new Map();
  for (let r = 1; r <= n; r++) for (let s = 0; s <= steps[r - 1]; s++) {
    await p.evaluate(([r, s]) => window.__ove.go(r, s), [r, s]); await p.waitForTimeout(r === 1 ? 300 : 1300);
    const res = await p.evaluate(() => {
      const out = [], pan = document.querySelector('.scene:not([aria-hidden="true"])');
      const walker = document.createTreeWalker(pan, NodeFilter.SHOW_TEXT);
      const bgOf = el => { let e = el; const st = [];  while (e) { if (e.classList.contains('scene') && e.classList.contains('dark')) return [31, 35, 38]; const c = getComputedStyle(e).backgroundColor; const m = c.match(/[\d.]+/g); if (m && (m.length < 4 || +m[3] > .6)) return m.slice(0, 3).map(Number); e = e.parentElement; } return [246, 246, 242]; };
      while (walker.nextNode()) {
        const t = walker.currentNode, txt = t.textContent.trim(); if (!txt) continue; const el = t.parentElement;
        const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        let hid = false, op = 1; for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e); op *= +c.opacity; if (e.classList?.contains('st') && !e.classList.contains('on')) hid = true; } if (hid || op < .9) continue;
        const rc = el.getBoundingClientRect(); if (rc.width < 2 || rc.height < 2 || rc.bottom < 0 || rc.top > 1080) continue;
        const scale = rc.width / el.offsetWidth || 1; const fs = parseFloat(cs.fontSize);
        const col = cs.color.match(/[\d.]+/g).slice(0, 3).map(Number);
        out.push({ txt: txt.slice(0, 40), fs, col, bg: bgOf(el), tag: el.className?.toString?.().slice(0, 20) });
      }
      return out;
    });
    for (const x of res) { if (x.fs < 22) small.set(x.txt, `${x.fs}px [${x.tag}] r${r}.s${s}`); const cr = ratio(x.col, x.bg); const lim = x.fs >= 24 ? 3 : 4.5; if (cr < lim) low.set(x.txt, `${cr.toFixed(2)} [${x.tag}] r${r}.s${s}`); }
  }
  ok(small.size === 0, `texte visible ≥ 22 px (${small.size} exception(s))`); [...small].slice(0, 25).forEach(([k, v]) => console.log('   <22px:', k, v));
  ok(low.size === 0, `contraste AA des textes visibles (${low.size} exception(s))`); [...low].slice(0, 25).forEach(([k, v]) => console.log('   contraste:', k, v));
  // palette
  const html = fs.readFileSync(FILE, 'utf8').replace(/data:font[^)"']+/g, '');
  const pal = new Set(['#B4C908', '#DCE58A', '#5C6600', '#878787', '#55595D', '#25282B', '#1F2326', '#F6F6F2', '#FFFFFF', '#FFF', '#fff']);
  const hex = new Set((html.replace(/<svg width="0"[\s\S]*?<\/defs><\/svg>/, '').replace(/<svg class="logo [^>]*>[\s\S]*?<\/svg>/g, '').match(/#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b/g) || []).map(h => h.toUpperCase()));
  const off = [...hex].filter(h => !pal.has(h) && !pal.has(h.toLowerCase()) && !/^#[0-9A-F]{3}$/.test(h) || false);
  console.log('   couleurs hors charte (hors logos) :', off.join(' ') || 'aucune');
  // focus visible
  await p.evaluate(() => window.__ove.go(1, 0)); await p.waitForTimeout(500);
  await p.keyboard.press('Tab'); await p.keyboard.press('Tab');
  const fo = await p.evaluate(() => { const e = document.activeElement; if (!e) return null; const s = getComputedStyle(e); return { tag: e.tagName, id: e.id, outline: s.outlineStyle + ' ' + s.outlineWidth, shadow: s.boxShadow }; });
  ok(fo && (fo.outline.startsWith('solid') || fo.shadow !== 'none'), 'focus clavier visible ' + JSON.stringify(fo));
  ok(await p.evaluate(() => document.documentElement.lang === 'fr' && !!document.title), 'lang=fr et <title>');
  // mouvement réduit
  const p2 = await (await b.newContext({ reducedMotion: 'reduce', viewport: { width: 1920, height: 1080 } })).newPage(); await p2.goto(F); await p2.waitForTimeout(800);
  ok(await p2.evaluate(() => document.body.classList.contains('calm')), 'prefers-reduced-motion → mode calme automatique');
  await b.close();
})();
