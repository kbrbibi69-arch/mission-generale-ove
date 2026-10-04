const { chromium } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '..') + '/presentation_bureau_ove_sapin2.html';
let pass = 0, fail = 0; const out = [];
const ok = (c, m) => { (c ? pass++ : fail++); out.push((c ? 'PASS ' : 'FAIL ') + m); };
(async () => {
  const br = await chromium.launch({ ...(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {}) });
  const ctx = await br.newContext({ viewport: { width: 1920, height: 1080 } });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(URL); await p.waitForTimeout(600);
  const st = () => p.evaluate(() => window.__ove.state());
  const key = async (k, w = 120) => { await p.keyboard.press(k); await p.waitForTimeout(w); };
  // intro : Espace passe le raccord
  await key(' ', 300); ok((await st()).scene === 1 && !(await p.evaluate(() => document.getElementById('s1').classList.contains('intro'))), 'Espace saute le raccord de la scène 1');
  await p.waitForTimeout(1200);
  await key('ArrowRight'); ok((await st()).step === 1, 'Flèche droite : étape 1 de la scène 1');
  await key('ArrowRight'); await key('ArrowRight', 1500); let s = await st(); ok(s.scene === 2 && s.step === 0, 'Après les étapes, passage à la scène 2');
  await key('ArrowLeft', 1500); s = await st(); ok(s.scene === 1 && s.step === 2, 'Flèche gauche : retour à la scène 1, dernière étape');
  await key('ArrowRight', 1500);
  // S2 : cartes
  await key(' '); await key(' ');  // steps 1, 2
  await p.click('.zone[data-acc-key="2"] .zbtn'); await p.waitForTimeout(500);
  ok(await p.evaluate(() => document.querySelector('.zone[data-acc-key="2"]').classList.contains('open')), 'S2 : clic ouvre la carte « conflits d’intérêts »');
  await key('3'); ok(await p.evaluate(() => document.querySelector('.zone[data-acc-key="3"]').classList.contains('open') && !document.querySelector('.zone[data-acc-key="2"]').classList.contains('open')), 'S2 : touche 3 ouvre la carte 3 et ferme la 2');
  // Space après un clic souris : avance (focus relâché)
  const before = await st(); await key(' ', 1500); const after = await st(); ok(after.scene === 3 || after.step > before.step, 'Espace avance encore après un clic souris');
  // S3
  await p.evaluate(() => window.__ove.go(3, 4)); await p.waitForTimeout(1800);
  await p.click('.s3-i'); await p.waitForTimeout(300);
  ok((await p.textContent('#s3-pt')) === 'IMOVE', 'S3 : clic sur IMOVE affiche son détail');
  await key('6'); ok((await p.textContent('#s3-pt')) === 'Direction générale', 'S3 : touche 6 affiche la Direction générale');
  await p.click('.flt[data-t="flux"]'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => [...document.querySelectorAll('#s3 .tok[data-t="flux"]')].every(t => t.style.opacity === '0')) && await p.evaluate(() => [...document.querySelectorAll('#s3 .tok[data-t="presta"]')].every(t => t.style.opacity !== '0')), 'S3 : filtre « flux financiers » masque seulement ces jetons');
  // S5
  await p.evaluate(() => window.__ove.go(5, 0)); await p.waitForTimeout(1800);
  await p.click('.s5-btns .btn[data-pos="0"]'); await p.waitForTimeout(1300);
  ok(await p.evaluate(() => getComputedStyle(document.getElementById('s5-cmp')).getPropertyValue('--p').trim()) === '0%', 'S5 : bouton « Cadre commun » amène le curseur à 0 %');
  const h = await p.locator('#s5-handle').boundingBox(); await p.mouse.move(h.x + 3, h.y + 270); await p.mouse.down(); await p.mouse.move(h.x + 700, h.y + 270, { steps: 8 }); await p.mouse.up();
  const pv = await p.evaluate(() => parseFloat(getComputedStyle(document.getElementById('s5-cmp')).getPropertyValue('--p'))); ok(pv > 30 && pv < 70, 'S5 : glisser la poignée déplace le curseur (' + pv.toFixed(0) + ' %)');
  // S7 : pilier + retour
  await p.evaluate(() => window.__ove.go(7, 2)); await p.waitForTimeout(1800);
  await key('2'); ok(await p.evaluate(() => document.querySelector('.pillar[data-acc-key="2"]').classList.contains('open')), 'S7 : touche 2 ouvre le chantier 2');
  await p.click('.pillar[data-acc-key="2"] .go'); await p.waitForTimeout(1800); s = await st(); ok(s.scene === 9, 'S7 : « Voir le détail » mène à la scène 9 (code commun)');
  ok(await p.evaluate(() => document.getElementById('ret').classList.contains('on')), 'Bouton « Retour aux quatre chantiers » visible');
  await p.click('#ret'); await p.waitForTimeout(1800); s = await st(); ok(s.scene === 7 && s.step === 2, 'Retour ramène à la scène 7');
  // S9 stations
  await p.evaluate(() => window.__ove.go(9, 7)); await p.waitForTimeout(1800);
  await p.click('.s9-st:nth-child(4) .nd'); await p.waitForTimeout(200);
  ok((await p.textContent('#s9-detail')).includes('S’abstenir'), 'S9 : clic sur l’étape 4 affiche son explication');
  // S10 convention
  await p.evaluate(() => window.__ove.go(10, 7)); await p.waitForTimeout(1800);
  await p.click('.cf[data-k="1"]'); await p.waitForTimeout(300); ok(await p.evaluate(() => document.querySelector('.cf[data-k="1"]').getAttribute('aria-expanded')) === 'true', 'S10 : clic sur un champ de la convention le développe');
  // S11
  await p.evaluate(() => window.__ove.go(11, 3)); await p.waitForTimeout(1800);
  await p.click('#s11-ex'); await p.waitForTimeout(300); ok(await p.evaluate(() => document.querySelectorAll('#s11-reg .mk').length) === 5, 'S11 : « Exemple de lecture » place 5 repères schématiques');
  // S12
  await p.evaluate(() => window.__ove.go(12, 6)); await p.waitForTimeout(1800);
  await p.click('.sat:nth-child(4)'); await p.waitForTimeout(300); ok((await p.textContent('#s12-detail')).includes('Chartes'), 'S12 : clic sur « Chartes » affiche son rôle');
  // S14
  await p.evaluate(() => window.__ove.go(14, 3)); await p.waitForTimeout(1800);
  await key('2'); ok(await p.evaluate(() => document.querySelector('.ben[data-acc-key="2"]').classList.contains('open')), 'S14 : touche 2 ouvre « Prévenir »');
  // S15
  await p.evaluate(() => window.__ove.go(15, 4)); await p.waitForTimeout(2200);
  const ang1 = await p.evaluate(() => document.getElementById('s15-beam').style.rotate);
  await p.locator('#s15-crit li:nth-child(1) .cr').click(); await p.waitForTimeout(300);
  const ang2 = await p.evaluate(() => document.getElementById('s15-beam').style.rotate); ok(ang1 !== ang2, 'S15 : retirer un critère fait pencher la balance (' + ang1 + ' → ' + ang2 + ')');
  // S16
  await p.evaluate(() => window.__ove.go(16, 5)); await p.waitForTimeout(2200);
  await p.locator('.nd16').nth(9).click(); await p.waitForTimeout(200); ok((await p.textContent('#s16-detail')).includes('fin d’année'), 'S16 : étape 10 mentionne « fin d’année » (note)');
  // S17 + D / Q
  await key('d', 1800); s = await st(); ok(s.scene === 17 && s.step === 3, 'Touche D : décision complète depuis n’importe où');
  await key('q', 1800); s = await st(); ok(s.scene === 2 && s.step === 2, 'Touche Q : retour à la question centrale');
  await p.evaluate(() => window.__ove.go(17, 0)); await p.waitForTimeout(1800);
  ok(await p.evaluate(() => getComputedStyle(document.querySelector('.s17-prop')).opacity) === '0', 'S17 : la proposition n’est pas affichée avant la commande');
  await p.click('#s17-show'); await p.waitForTimeout(900); ok(await p.evaluate(() => getComputedStyle(document.querySelector('.s17-prop')).opacity) === '1', 'S17 : « Afficher la proposition de décision » la révèle');
  await p.click('.s17-cmd .btn.light'); await p.waitForTimeout(1800); s = await st(); ok(s.scene === 7, 'S17 : « Revoir les quatre chantiers » mène à la scène 7');
  ok((await p.textContent('#ret')).includes('décision'), 'Un bouton de retour vers la décision est proposé');
  // Sommaire, notes, objections, aide
  await key('s', 300); ok(await p.evaluate(() => document.getElementById('toc').classList.contains('on')), 'S : sommaire ouvert');
  await p.click('#toc .sc button[data-n="11"]'); await p.waitForTimeout(1800); s = await st(); ok(s.scene === 11, 'Sommaire : clic sur la scène 11');
  await key('n', 300); ok(await p.evaluate(() => document.getElementById('notes-panel').classList.contains('on') && document.getElementById('notes-panel').textContent.includes('Rendre les mandats lisibles')), 'N : panneau de notes avec la scène courante');
  await key('Escape', 200); ok(!(await p.evaluate(() => document.getElementById('notes-panel').classList.contains('on'))), 'Échap ferme le panneau de notes');
  await key('o', 300); ok((await p.locator('#obj details').count()) === 8, 'O : 8 objections avec réponses');
  await key('Escape', 200); await key('?', 300); ok(await p.evaluate(() => document.getElementById('help').classList.contains('on')), '? : aide des raccourcis'); await key('Escape', 200);
  // hash + fin
  await key('End', 1800); s = await st(); ok(s.scene === 18, 'Fin : dernière scène');
  const hash = await p.evaluate(() => location.hash); ok(hash === '#18', 'URL mémorise la scène (' + hash + ')');
  // calme
  await key('a', 200); ok(await p.evaluate(() => document.body.classList.contains('calm')), 'A : animations suspendues'); await key('a', 200);
  // présentateur
  const pr = await ctx.newPage(); await pr.goto(URL + '?presenter=1'); await pr.waitForTimeout(500);
  await p.bringToFront(); await p.evaluate(() => window.__ove.go(4, 2)); await p.waitForTimeout(800);
  const synced = await pr.evaluate(() => document.getElementById('pv-t').textContent); ok(synced.includes('Scène 4'), 'Fenêtre présentateur synchronisée : « ' + synced + ' »');
  await pr.click('button[data-c="next"]'); await p.waitForTimeout(800); s = await st(); ok(s.step === 3, 'Commande « Suivant » du présentateur pilote la projection');
  ok(errs.length === 0, 'Aucune erreur JavaScript (' + errs.length + ')');
  console.log(out.join('\n')); console.log(`\n${pass} réussis, ${fail} échoués`); if (errs.length) console.log(errs);
  await br.close();
})();
