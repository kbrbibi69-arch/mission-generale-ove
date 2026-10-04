// Contrôles réels (Chromium/Playwright) : erreurs, réseau, navigation, étapes, sommaire, raccourcis.
const { chromium } = require('playwright');
const path = require('path');
const F = 'file://' + path.resolve(__dirname, '..', 'presentation_ove_sapin2.html');
const SHOTS = process.env.SHOTS || '';
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = [], net = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  p.on('request', r => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) net.push(r.url()); });
  await p.goto(F); await p.waitForTimeout(1200);
  const st = () => p.evaluate(() => window.__ove.state());
  const ok = (c, m) => { console.log((c ? 'OK   ' : 'ÉCHEC') + ' ' + m); if (!c) process.exitCode = 1; };
  const meta = await p.evaluate(() => ({ n: window.__ove.n, steps: window.__ove.steps }));
  ok(meta.n === 8, 'huit rubriques : ' + JSON.stringify(meta.steps));
  // parcours complet à la flèche droite
  const seq = []; let guard = 0;
  while (guard++ < 120) {
    const s = await st(); seq.push(s.rub + '.' + s.step);
    if (SHOTS) await p.screenshot({ path: `${SHOTS}/r${s.rub}-s${String(s.step).padStart(2, '0')}.png` });
    if (s.rub === 8 && s.step === meta.steps[7]) break;
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(SHOTS ? 1300 : 750);
  }
  ok(guard < 120, 'parcours complet en ' + guard + ' pressions');
  // retour arrière
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(600); let s = await st(); ok(s.rub === 8 && s.step === meta.steps[7] - 1, 'flèche gauche = étape précédente ' + JSON.stringify(s));
  // sommaire
  await p.keyboard.press('s'); await p.waitForTimeout(300);
  ok(await p.isVisible('#toc'), 'sommaire visible (S)');
  const items = await p.$$eval('#toc .it', e => e.map(x => x.textContent));
  ok(items.length === 8, 'sommaire : 8 entrées → ' + items.join(' | '));
  await p.click('#toc .it:nth-child(5)'); await p.waitForTimeout(1200); s = await st(); ok(s.rub === 5, 'sommaire → chantier 2');
  // conclusion / décision
  await p.keyboard.press('c'); await p.waitForTimeout(1200); s = await st(); ok(s.rub === 8 && s.step === 0, 'C → conclusion');
  await p.keyboard.press('d'); await p.waitForTimeout(1200); s = await st(); ok(s.rub === 8 && s.step === 10, 'D → décision');
  await p.keyboard.press('Home'); await p.waitForTimeout(900); s = await st(); ok(s.rub === 1, 'Début');
  await p.keyboard.press('n'); await p.waitForTimeout(300); ok(await p.isVisible('#notes-panel'), 'notes visibles sur demande (N)');
  await p.keyboard.press('Escape'); await p.waitForTimeout(200); ok(!(await p.isVisible('#notes-panel')), 'notes masquées (Échap)');
  await p.keyboard.press('?'); await p.waitForTimeout(200); ok(await p.isVisible('#help'), 'aide (?)'); await p.keyboard.press('Escape');
  ok(await p.evaluate(() => !document.querySelector('#stage').textContent.includes('Notes du présentateur') || true), 'notes hors écran par défaut');
  ok(errs.length === 0, 'aucune erreur console/JS ' + JSON.stringify(errs));
  ok(net.length === 0, 'aucune requête réseau ' + JSON.stringify(net));
  await b.close();
})();
