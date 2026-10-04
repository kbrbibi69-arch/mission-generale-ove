(() => {
'use strict';
const NOTES = JSON.parse(document.getElementById('notes-data').textContent);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const NS = 'http://www.w3.org/2000/svg';
const isPresenter = /[?&]presenter/.test(location.search);
const stage = $('#stage'), panels = $$('.scene'), N = panels.length;
const stepsOf = panels.map(s => +s.dataset.steps || 0);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const R = NOTES.rubriques;
let cur = -1, step = 0, lock = 0, calm = false, retTo = null;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const icon = (n, s = 40) => `<svg class="ic" width="${s}" height="${s}" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const mk = (tag, cls, html, parent, ns) => { const e = ns ? document.createElementNS(NS, tag) : document.createElement(tag); if (cls) e.setAttribute('class', cls); if (html != null) e.innerHTML = html; parent?.appendChild(e); return e; };
/* un élément est visible si tous ses ancêtres « .st » sont révélés */
const shown = el => { for (let e = el; e && e !== stage; e = e.parentElement) if (e.classList.contains('st') && !e.classList.contains('on')) return false; return true; };

/* ---------- mise à l'échelle 1920×1080 ---------- */
function fit() { const s = Math.min(innerWidth / 1920, innerHeight / 1080); stage.style.transform = `translate(-50%,-50%) scale(${s})`; }
addEventListener('resize', fit); fit();

/* ---------- animations suspendues ---------- */
let toastT; function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('on'), 1800); }
function setCalm(on) { calm = on; document.body.classList.toggle('calm', on); if (reduce) document.body.classList.toggle('motion', !on); $('#b-calm')?.setAttribute('aria-pressed', on); if (on) tokenPlace(); toast(on ? 'Animations non essentielles suspendues' : 'Animations rétablies'); }

/* ---------- étapes (réversibles) ---------- */
function applySteps() {
  const sc = panels[cur];
  $$('[data-s]', sc).forEach(el => { const a = +el.dataset.s, b = el.dataset.smax ? +el.dataset.smax : 99; el.classList.toggle('on', step >= a && step <= b); });
  (hooks[cur + 1] || {}).step?.(step);
  updateHud(); sendState();
}
function setStep(k) { step = clamp(k, 0, stepsOf[cur]); applySteps(); }

/* ---------- navigation ---------- */
function go(i, st = 0, dir) {
  i = clamp(i, 0, N - 1);
  if (i === cur) { setStep(st); return; }
  const d = dir ?? (i >= cur ? 1 : -1), out = panels[cur], inn = panels[i];
  stage.style.setProperty('--dir', d);
  stage.dataset.tr = (d >= 0 ? inn : (out || inn)).dataset.tr || 'rise';
  const bands = stage.dataset.tr === 'bands' && cur >= 0 && !calm;
  const swap = () => {
    if (out) { out.classList.remove('active', 'entering'); out.classList.add('leaving'); out.inert = true; out.setAttribute('aria-hidden', 'true'); (hooks[cur + 1] || {}).leave?.();
      setTimeout(() => { out.classList.remove('leaving'); $$('.st', out).forEach(e => e.classList.remove('on')); }, calm ? 20 : 900); }
    cur = i; step = 0;
    inn.classList.add('active', 'entering'); inn.inert = false; inn.removeAttribute('aria-hidden');
    setTimeout(() => inn.classList.remove('entering'), 1100);
    (hooks[i + 1] || {}).enter?.(d);
    requestAnimationFrame(() => requestAnimationFrame(() => { applySteps(); setStep(st); }));
    $('#live').textContent = `Rubrique ${i + 1} sur ${N} : ${R[i].level}, ${R[i].title}`;
    history.replaceState(null, '', '#' + (i + 1)); checkReturn();
  };
  if (bands) { const b = $('#bands'); b.classList.remove('go', 'back'); void b.offsetWidth; b.classList.add('go'); if (d < 0) b.classList.add('back'); lock = performance.now() + 700; setTimeout(swap, 480); setTimeout(() => b.classList.remove('go', 'back'), 1250); }
  else { lock = performance.now() + (calm ? 0 : 450); swap(); }
}
function next() { if (performance.now() < lock) return; if (step < stepsOf[cur]) setStep(step + 1); else if (cur < N - 1) go(cur + 1, 0, 1); }
function prev() { if (performance.now() < lock) return; if (step > 0) setStep(step - 1); else if (cur > 0) go(cur - 1, stepsOf[cur - 1], -1); }
function jump(n, st) { go(n - 1, st ?? 0); }

/* ---------- retour après un détour ---------- */
function setReturn(n, st, label) { retTo = { n, st, label }; }
function checkReturn() { const b = $('#ret'); if (!retTo) { b.classList.remove('on'); return; } if (cur + 1 === retTo.n) { retTo = null; b.classList.remove('on'); return; } b.textContent = '← ' + retTo.label; b.classList.add('on'); }
$('#ret').addEventListener('click', e => { if (retTo) { const r = retTo; retTo = null; jump(r.n, r.st); } if (e.detail > 0) e.currentTarget.blur(); });

/* ---------- cartes développables ---------- */
function toggleAcc(card, force) {
  const grp = card.dataset.acc, multi = card.hasAttribute('data-multi'), open = force ?? !card.classList.contains('open');
  if (open && !multi) $$(`[data-acc="${grp}"].open`, panels[cur]).forEach(c => { if (c !== card) { c.classList.remove('open'); c.querySelector('button')?.setAttribute('aria-expanded', 'false'); } });
  card.classList.toggle('open', open); card.querySelector('button')?.setAttribute('aria-expanded', open);
}
stage.addEventListener('click', e => {
  const o = e.target.closest('[data-open]'); if (o) { openOv(o.dataset.open); if (e.detail > 0) o.blur(); return; }
  const g = e.target.closest('[data-goto]');
  if (g) { if (cur === 2) setReturn(3, 4, 'Retour à la deuxième partie'); else if (cur === 7) setReturn(8, 10, 'Retour à la conclusion'); jump(+g.dataset.goto, 0); if (e.detail > 0) g.blur(); return; }
  const card = e.target.closest('[data-acc]');
  if (card && e.target.closest('button') === card.querySelector(':scope > button')) { toggleAcc(card); if (e.detail > 0) e.target.closest('button').blur(); }
});

/* ---------- jetons animés ---------- */
const runners = [];
function addRunner(panel, path, el, speed, off, kind) { runners.push({ panel, path, el, speed, off, kind, L: path.getTotalLength() }); }
function place(r, f) { const p = r.path.getPointAtLength(r.L * f), q = r.path.getPointAtLength(Math.min(r.L, r.L * f + 2)); const a = Math.atan2(q.y - p.y, q.x - p.x) * 180 / Math.PI; r.el.setAttribute('transform', `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)}) rotate(${r.kind === 'sup' ? a : 0})`); }
function tokenPlace() { runners.forEach(r => place(r, r.off)); }
let tprev = 0;
function loop(t) { requestAnimationFrame(loop); if (calm || document.hidden) return; const dt = Math.min(0.05, (t - tprev) / 1000); tprev = t; runners.forEach(r => { if (!panels[r.panel].classList.contains('active')) return; r.off = (r.off + dt * r.speed) % 1; place(r, r.off); }); }

/* ---------- données ---------- */
const S3 = {
  1: ['Au centre', 'Fondation OVE', 'La Fondation fonctionne au centre d’un ensemble très intégré : fonds de dotation IMOVE, SCI, associations du réseau.'],
  2: ['Fonds de dotation', 'IMOVE', 'Concerné par les flux financiers internes (apports en compte courant, avances, prestations, mises à disposition). Mandat décrit dans la note : le Directeur général en est administrateur.'],
  3: ['Sociétés civiles immobilières', 'SCI', 'Concernées par les flux financiers internes. Opérations immobilières et décisions impliquant les SCI : zone de vigilance. Mandat décrit dans la note : le Directeur général est gérant de toutes les SCI.'],
  4: ['Associations du réseau', 'Associations du réseau', 'Concernées par les flux internes et par les interventions du siège. Le Directeur général préside leurs directoires. Certains membres du Bureau président des associations partenaires et des conseils de surveillance.'],
  5: ['Fonctions support', 'Services du siège', 'Juridique, immobilier, fonctions support : interventions au profit des associations qui n’ont pas ces expertises.'],
  6: ['Gouvernance', 'Organes de gouvernance', 'Directoires, conseils de surveillance, Bureau, conseils d’administration : instances citées dans la note. Certains membres du Bureau sont présidents d’associations partenaires et de conseils de surveillance.']
};
const C2 = [['search', 'Identifier', 'Repérer une situation où des intérêts peuvent se croiser.'], ['doc', 'Déclarer', 'Appliquer les règles de déclaration des intérêts.'], ['gauge', 'Analyser', 'Apprécier la situation à la lumière du Code commun.'], ['pause', 'S’abstenir si nécessaire', 'La personne directement intéressée s’abstient, avec mention explicite de l’abstention.'], ['gov', 'Décision d’un organe non intéressé', 'Permettre la décision d’un organe non intéressé.'], ['pen', 'Documenter la décision', 'Consigner la décision et les abstentions.'], ['archive', 'Assurer la traçabilité', 'Garder la trace de la décision : traçabilité des décisions.']];
const C2LINK = [['a'], ['a'], ['a'], ['a'], ['b'], ['a'], ['a']];
const C3 = [['Flux identifié', ''], ['Flux recensé', 'recensement'], ['Flux qualifié', ''], ['Flux documenté', ''], ['Convention écrite', ''], ['Validation adaptée', ''], ['Abstention documentée', 'si nécessaire'], ['Décision traçable', '']];
const C3LINK = ['a', 'a', 'a', 'b', 'b', 'c', 'c', 'c'];
const C4SAT = [
  ['Direction générale', 'person', 'Le référent est rattaché à la Direction générale.'],
  ['Bureau', 'gov', 'Le Bureau reçoit un reporting régulier du référent et conserve ses décisions.'],
  ['Entités du réseau', 'network', 'Le référent pilote la cartographie dans l’ensemble des entités.'],
  ['Cartographie', 'map', 'Pilotage de la cartographie des risques.'],
  ['Conventions', 'doc', 'Préparation des modèles de conventions.'],
  ['Code commun', 'shield', 'Contribution au Code commun « probité et conflits d’intérêts ».'],
  ['Dispositif d’alerte', 'bell', 'Animation du dispositif d’alerte.'],
  ['Registre des mandats', 'table', 'Registre des mandats et fonctions (Fondation, IMOVE, SCI, associations) pour objectiver les cumuls.'],
  ['Reporting', 'gauge', 'Reporting régulier au Bureau.']
];
const C4MIS = [['Piloter la cartographie', [3, 2]], ['Préparer les modèles de conventions', [4]], ['Contribuer au Code commun', [5]], ['Animer le dispositif d’alerte', [6]], ['Assurer un reporting régulier au Bureau', [8, 1]]];

/* ---------- initialisations par rubrique ---------- */
const hooks = {};

/* 1. Titre : parallaxe légère */
(function () {
  const sc = $('#r1'); let raf = 0;
  stage.addEventListener('pointermove', e => { if (cur !== 0 || calm || raf) return; raf = requestAnimationFrame(() => { raf = 0; const b = stage.getBoundingClientRect(); sc.style.setProperty('--px', ((e.clientX - b.left) / b.width - .5) * 2); sc.style.setProperty('--py', ((e.clientY - b.top) / b.height - .5) * 2); }); });
})();

/* 2. Première partie : schéma de l'écosystème */
(function () {
  const sc = $('#r2'), nodes = $$('.s3n', sc), flt = { apport: true, avance: true, presta: true, mad: true, sup: true, man: true, gov: true }, idx = 1;
  const tokG = $('#s3-tokens'), edges = $$('.edge', sc);
  const types = [['apport', 'd'], ['avance', 'c'], ['presta', 's'], ['mad', 't']];
  edges.forEach((p, ei) => types.forEach(([ty, shape], ti) => {
    const g = mk('g', 'tok st st-fade', '', tokG, 1); g.dataset.t = ty; g.dataset.s = 2; g.style.pointerEvents = 'none'; let sh;
    if (shape === 'c') { sh = mk('circle', '', '', g, 1); sh.setAttribute('r', 9); sh.setAttribute('fill', '#B4C908'); sh.setAttribute('stroke', '#5C6600'); sh.setAttribute('stroke-width', 2); }
    else if (shape === 's') { sh = mk('rect', '', '', g, 1); ['x', -8, 'y', -8, 'width', 16, 'height', 16].forEach((v, j, a) => { if (j % 2 == 0) sh.setAttribute(v, a[j + 1]); }); sh.setAttribute('fill', '#55595D'); }
    else if (shape === 'd') { sh = mk('polygon', '', '', g, 1); sh.setAttribute('points', '0,-11 11,0 0,11 -11,0'); sh.setAttribute('fill', '#B4C908'); sh.setAttribute('stroke', '#5C6600'); sh.setAttribute('stroke-width', 2); }
    else { sh = mk('polygon', '', '', g, 1); sh.setAttribute('points', '0,-11 10,8 -10,8'); sh.setAttribute('fill', '#5C6600'); }
    addRunner(idx, p, g, 0.06 + 0.008 * ti, (ei * 0.17 + ti * 0.25) % 1, 'k');
  }));
  const sup = $('#m-sup');
  for (let k = 0; k < 3; k++) { const g = mk('g', 'tok st st-fade', '', tokG, 1); g.dataset.t = 'sup'; g.dataset.s = 3; g.style.pointerEvents = 'none'; const pl = mk('polyline', '', '', g, 1); pl.setAttribute('points', '-8,-9 6,0 -8,9'); pl.setAttribute('fill', 'none'); pl.setAttribute('stroke', '#25282B'); pl.setAttribute('stroke-width', 5); pl.setAttribute('stroke-linecap', 'round'); pl.setAttribute('stroke-linejoin', 'round'); addRunner(idx, sup, g, 0.16, k / 3, 'sup'); }
  function applyFilters() {
    $$('.tok', sc).forEach(t => t.style.opacity = flt[t.dataset.t] ? '' : '0');
    $('.s3-man', sc).style.opacity = flt.man ? '' : '0.08'; $('#m-sup').style.opacity = flt.sup ? '' : '0.1'; $('.s3-gov', sc).style.opacity = flt.gov ? '' : '0.08';
  }
  $$('.flt', sc).forEach(b => b.addEventListener('click', e => { const t = b.dataset.t; flt[t] = !flt[t]; b.setAttribute('aria-pressed', flt[t]); applyFilters(); if (e.detail > 0) b.blur(); }));
  function select(k) {
    const el = nodes.find(n => +n.dataset.k === k); if (!el || !shown(el) || sc.classList.contains('q-on')) return;
    nodes.forEach(n => n.classList.toggle('sel', n === el));
    const [kick, title, body] = S3[k]; $('#s3-pk').textContent = kick; $('#s3-pt').textContent = title; $('#s3-pb').textContent = body;
  }
  nodes.forEach(n => n.addEventListener('click', e => { select(+n.dataset.k); if (e.detail > 0) n.blur(); }));
  $$('.sci-grid').forEach(g => { if (!g.children.length) for (let j = 0; j < 21; j++) { const i = document.createElement('i'); i.style.cssText = `display:block;width:14px;height:14px;border-radius:3px;background:${j % 3 ? '#878787' : '#B4C908'}`; g.appendChild(i); } });
  hooks[2] = { select, enter() { nodes.forEach(n => n.classList.remove('sel')); }, step(k) { applyFilters(); const q = k >= 5; sc.classList.toggle('q-on', q); $('#r2-main').inert = q; } };
})();

/* 3. Deuxième partie */
hooks[3] = { step(k) { $('#r3-group').classList.toggle('dim', k >= 4); $$('.r3-ch', $('#r3')).forEach(b => b.tabIndex = k >= 4 ? 0 : -1); } };

/* 4. Chantier 1 : cartographie */
hooks[4] = { step(k) { $$('.tile', $('#r4')).forEach((t, i) => toggleAcc(t, i < k)); } };

/* 5. Chantier 2 : parcours du Code commun */
(function () {
  const sc = $('#r5'), host = $('#c2-stations'), path = $('#c2-prog'), tok = $('#c2-token'), det = $('#c2-detail'), cards = $$('.gc', $('#c2-cards'));
  const pos = [[790, 440], [1040, 440], [1290, 440], [1540, 440], [1540, 600], [1290, 600], [1040, 600]];
  const dist = [0, 250, 500, 750, 1002, 1252, 1502];
  C2.forEach(([ic, t, tx], i) => {
    const [x, y] = pos[i];
    const st = mk('div', 's9-st st st-fade' + (i < 4 ? ' up' : ''), '', host); st.dataset.s = i + 1; st.style.cssText = `left:${x}px;top:${y - 46}px`;
    const b = mk('button', 'nd', `${icon(ic, 40)}<span class="nn">${i + 1}</span>`, st); b.setAttribute('aria-label', `Étape ${i + 1} : ${t}`);
    mk('div', 'lb', esc(t), st); b.addEventListener('click', e => { showDetail(i); if (e.detail > 0) b.blur(); });
  });
  const showDetail = i => { det.textContent = `${i + 1}. ${C2[i][1]} — ${C2[i][2]}`; };
  hooks[5] = { enter() { det.textContent = ''; }, step(k) {
    const n = clamp(k, 0, 7); path.style.strokeDashoffset = 1 - (n > 0 ? dist[n - 1] / 1502 : 0); path.style.transition = calm ? 'none' : 'stroke-dashoffset 1s var(--ease)';
    const i = clamp(n - 1, 0, 6); tok.style.translate = `${pos[i][0]}px ${pos[i][1]}px`; tok.style.opacity = n > 0 ? 1 : 0;
    $$('.s9-st', sc).forEach((s, j) => s.classList.toggle('now', j === n - 1));
    cards.forEach(c => c.classList.toggle('hot', n > 0 && C2LINK[n - 1].includes(c.dataset.g) || (n > 0 && c.dataset.g === 'c')));
    if (n > 0) showDetail(n - 1); else det.textContent = '';
  } };
})();

/* 6. Chantier 3 : flux entre entités */
(function () {
  const sc = $('#r6'), ol = $('#c3-steps'), tok = $('#c3-token'), cards = $$('.gc', $('#c3-cards'));
  C3.forEach(([t, sub], i) => { const li = mk('li', '', `<b>${i + 1}</b>${esc(t)}${sub ? `<small>${esc(sub)}</small>` : ''}`, ol); li.style.top = (i * 76) + 'px'; li.style.left = (i * 8) + 'px'; li.style.width = '470px'; });
  $$('.cf', sc).forEach(b => b.addEventListener('click', e => { const o = b.getAttribute('aria-expanded') === 'true'; $$('.cf', sc).forEach(c => c.setAttribute('aria-expanded', 'false')); b.setAttribute('aria-expanded', !o); if (e.detail > 0) b.blur(); }));
  hooks[6] = { enter() { $$('.cf', sc).forEach(c => c.setAttribute('aria-expanded', 'false')); }, step(k) {
    $$('li', ol).forEach((li, i) => { li.classList.toggle('on', i < k); li.classList.toggle('now', i === k - 1); });
    const i = clamp(k - 1, 0, 7); tok.style.translate = `${664 + i * 8}px ${332 + i * 76}px`; tok.style.opacity = k > 0 ? 1 : 0;
    tok.dataset.sh = k <= 3 ? 1 : k <= 4 ? 2 : k === 5 ? 2 : k <= 7 ? 3 : 4;
    cards.forEach(c => c.classList.toggle('hot', k > 0 && C3LINK[k - 1] === c.dataset.g));
  } };
})();

/* 7. Chantier 4 : référent, registre, chartes et conventions */
(function () {
  const sc = $('#r7'), tabs = $$('.c4-tabs button', sc), tabStep = { a: 1, b: 7, c: 10 };
  /* A : référent */
  const host = $('#c4-sats'), lines = $('#c4-lines'), ml = $('#c4-missions'), det = $('#c4-detail');
  const C = [1150, 640], rx = 420, ry = 270;
  const sats = C4SAT.map(([t, ic], i) => {
    const a = (-90 + i * 40) * Math.PI / 180, x = C[0] + rx * Math.cos(a), y = C[1] + ry * Math.sin(a);
    const b = mk('button', 'sat st st-fade', `${icon(ic, 32)}${esc(t)}`, host); b.dataset.s = 1; b.style.cssText = `left:${x}px;top:${y}px;width:210px`; b.setAttribute('aria-label', `${t} : afficher le rôle`);
    const p = mk('path', '', '', lines, 1); p.setAttribute('d', `M${C[0]} ${C[1]} L${x} ${y}`); return { b, p };
  });
  C4MIS.forEach(([t], i) => { const li = mk('li', 'st st-left', `<b>${i + 1}</b><span>${esc(t)}</span>`, ml); li.dataset.s = i + 2; });
  const showSat = i => { det.textContent = C4SAT[i][2]; det.classList.add('on'); sats.forEach((s, j) => s.b.classList.toggle('sel', j === i)); };
  sats.forEach((s, i) => s.b.addEventListener('click', e => { showSat(i); if (e.detail > 0) s.b.blur(); }));
  /* B : registre */
  const reg = $('#c4-reg'), btn = $('#c4-ex'), lg = $('#c4-lg'), nt = $('#c4-nt'), link = $('#c4-link path');
  const cell = (r, c) => $(`.rr[data-r="${r}"] [data-c="${c}"]`, reg);
  const A = [[3, 0], [1, 2], [2, 1]], B = [[0, 2], [3, 1]], cx = c => 250 + 250 * (c + .5), cy = r => 80 + 76 * (r + .5);
  function example(on) {
    $$('[data-c]', reg).forEach(c => { c.classList.remove('m'); c.innerHTML = ''; });
    if (on) { A.forEach(([r, c]) => { const e = cell(r, c); e.classList.add('m'); e.innerHTML = '<span class="mk">●</span>'; }); B.forEach(([r, c]) => { const e = cell(r, c); e.classList.add('m'); e.innerHTML = '<span class="mk b">◆</span>'; });
      link.setAttribute('d', `M${cx(0)} ${cy(3)} L${cx(2)} ${cy(1)} L${cx(1)} ${cy(2)}`); nt.textContent = 'Lecture schématique : une même personne apparaît dans plusieurs structures → vigilance, abstention organisée, décision tracée.'; }
    else { link.setAttribute('d', ''); nt.textContent = 'Schéma illustratif : aucune donnée réelle, aucune personne nommée.'; }
    btn.setAttribute('aria-pressed', on); lg.classList.toggle('on', on);
  }
  btn.addEventListener('click', e => { example(btn.getAttribute('aria-pressed') !== 'true'); if (e.detail > 0) btn.blur(); });
  /* C : chartes et conventions */
  const tg = $('#c4-tokens');
  ['p13a', 'p13b', 'p13c', 'p13d', 'p13e'].forEach((id, pi) => { const p = document.getElementById(id); for (let k = 0; k < 3; k++) {
    const t = mk('g', '', '', tg, 1); const r = mk('rect', '', '', t, 1); ['x', -14, 'y', -10, 'width', 28, 'height', 20].forEach((v, j, a) => { if (j % 2 == 0) r.setAttribute(v, a[j + 1]); }); r.setAttribute('rx', 4); r.setAttribute('fill', '#fff'); r.setAttribute('stroke', '#5C6600'); r.setAttribute('stroke-width', 3);
    const l = mk('path', '', '', t, 1); l.setAttribute('d', 'M-7 -3H7M-7 3H3'); l.setAttribute('stroke', '#B4C908'); l.setAttribute('stroke-width', 3); l.setAttribute('stroke-linecap', 'round'); addRunner(6, p, t, 0.09 + pi * 0.008, (k / 3 + pi * 0.11) % 1, 'k'); } });
  const tabOf = k => k <= 6 ? 'a' : k <= 9 ? 'b' : 'c';
  tabs.forEach(b => b.addEventListener('click', e => { setStep(tabStep[b.dataset.tab]); if (e.detail > 0) b.blur(); }));
  hooks[7] = { tabKey(n) { setStep([1, 7, 10][n - 1]); }, enter() { det.classList.remove('on'); sats.forEach(s => s.b.classList.remove('sel')); example(false); }, step(k) {
    const t = tabOf(k); tabs.forEach(b => b.setAttribute('aria-selected', b.dataset.tab === t));
    const hot = new Set(); if (k >= 1) hot.add(0); C4MIS.forEach(([_, ids], mi) => { if (k >= mi + 2) ids.forEach(i => hot.add(i)); }); if (k >= 6) hot.add(7);
    sats.forEach((s, j) => { s.b.classList.toggle('hot', hot.has(j)); s.p.classList.toggle('hot', hot.has(j)); });
    if (k >= 2 && k <= 6) showSat(C4MIS[k - 2][1][0]); else if (k === 1) showSat(0); else if (k === 0) det.classList.remove('on');
  } };
})();

/* 8. Conclusion */
hooks[8] = { enter() { $$('[data-acc="cD"]', $('#r8')).forEach(c => toggleAcc(c, false)); }, step(k) { $('#r8').classList.toggle('dark', k >= 9 && k <= 10); } };

/* ---------- barre de navigation, sommaire, notes ---------- */
const hud = $('#hud'), prog = $('#prog');
R.forEach((r, i) => { const s = mk('i', '', '<b></b>', prog); s.title = `${r.level} · ${r.title}`; });
prog.style.display = 'flex'; prog.style.gridTemplateColumns = 'none';
function updateHud() {
  $('#cnt').textContent = `${String(cur + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')}`; $('#acts').textContent = R[cur].level;
  hud.classList.toggle('dk', panels[cur].classList.contains('dark'));
  $$('#prog i b').forEach((b, k) => { const f = cur > k ? 1 : cur < k ? 0 : (stepsOf[cur] ? step / stepsOf[cur] : 1); b.style.transform = `scaleX(${f})`; });
  $$('#toc .it').forEach(b => b.classList.toggle('cur', +b.dataset.n === cur + 1));
  $('#b-prev').disabled = cur === 0 && step === 0; $('#b-next').disabled = cur === N - 1 && step === stepsOf[N - 1];
  renderNotesPanel();
}
const ovs = { toc: $('#toc'), help: $('#help') };
function closeOv() { Object.values(ovs).forEach(o => o.classList.remove('on')); $('#notes-panel').classList.remove('on'); }
function openOv(k) { const was = ovs[k].classList.contains('on'); closeOv(); if (!was) { ovs[k].classList.add('on'); (ovs[k].querySelector('.it.cur,button,summary'))?.focus(); } }
(function () {
  const host = $('#toc .list');
  R.forEach((r, i) => { const b = mk('button', 'it lvl' + (r.level.startsWith('Chantier') ? 1 : 0), `<b>${esc(r.level)}</b><span>${esc(r.title)}</span>`, host); b.dataset.n = i + 1; b.addEventListener('click', () => { closeOv(); jump(i + 1, 0); }); });
})();
function notesHTML(i, st) {
  const n = R[i], ob = n.objection != null ? NOTES.objections[n.objection] : null;
  return `<div class="nt"><h3>${esc(n.level)} · ${esc(n.title)}</h3><div>Étape ${st} / ${stepsOf[i]} · rubrique ${i + 1} sur ${N}</div>
  <dl><dt>Objectif de conviction</dt><dd>${esc(n.obj)}</dd><dt>Message central</dt><dd>${esc(n.msg)}</dd><dt>Commentaire oral recommandé</dt><dd>${esc(n.oral)}</dd>
  <dt>Déclenchement des animations</dt><dd><ul>${n.decl.map(d => `<li>${esc(d)}</li>`).join('')}</ul></dd><dt>Transition avec la partie suivante</dt><dd>${esc(n.trans)}</dd>
  ${ob ? `<dt>Objection possible</dt><dd><b>${esc(ob.q)}</b><br>${esc(ob.r)}</dd>` : ''}<dt>Précautions juridiques</dt><dd>${esc(n.prud)}</dd>
  ${n.subs.length ? `<dt>Sous-parties</dt><dd>${n.subs.map(s => `<div class="sb"><b>${esc(s.t)}</b><br>${esc(s.msg)}<br><i>Oral : ${esc(s.oral)}</i><br>Déclenchement : ${esc(s.decl)}<br>Précaution : ${esc(s.prud)}</div>`).join('')}</dd>` : ''}</dl></div>`;
}
function renderNotesPanel() { const p = $('#notes-panel'); if (!p.classList.contains('on')) return; p.innerHTML = `<div class="warn">Notes du présentateur : à masquer avant projection (touche N), ou ouvrir la fenêtre présentateur (touche P).</div>` + notesHTML(cur, step); }

/* ---------- fenêtre présentateur synchronisée ---------- */
let chan = null; try { chan = 'BroadcastChannel' in window ? new BroadcastChannel('ove-sapin2') : null; } catch (e) {}
const seen = new Set();
function post(m) { m = { ...m, id: Date.now() + '-' + Math.random() }; try { chan?.postMessage(m); } catch (e) {} try { localStorage.setItem('ove-msg', JSON.stringify(m)); } catch (e) {} }
function sendState() { if (!isPresenter && cur >= 0) post({ type: 'state', rub: cur, step }); }
function onMsg(m) {
  if (!m || (m.id && seen.has(m.id))) return; if (m.id) { seen.add(m.id); if (seen.size > 200) seen.clear(); }
  if (isPresenter && m.type === 'state') renderPresenter(m.rub, m.step);
  if (!isPresenter && m.type === 'cmd') ({ next, prev, decision: () => jump(8, 10), conclusion: () => jump(8, 0) })[m.cmd]?.();
  if (!isPresenter && m.type === 'hello') sendState();
}
chan && (chan.onmessage = e => onMsg(e.data));
addEventListener('storage', e => { if (e.key === 'ove-msg' && e.newValue) { try { onMsg(JSON.parse(e.newValue)); } catch (_) {} } });
function renderPresenter(i, st) { const nx = R[i + 1]; $('#pv-t').textContent = `${R[i].level} · ${R[i].title}`; $('#pv-n').innerHTML = notesHTML(i, st); $('#pv-next').textContent = nx ? `Suivant : ${nx.level} · ${nx.title}` : 'Dernière rubrique'; }
if (isPresenter) {
  document.body.classList.add('presenter'); document.title = 'Présentateur — ' + document.title;
  $('#presenter').innerHTML = `<div class="bar"><strong id="pv-t">…</strong><button data-c="prev">◀ Précédent</button><button data-c="next">Suivant ▶</button><button data-c="conclusion">Conclusion (C)</button><button data-c="decision">Décision (D)</button><span class="tm" id="pv-tm">00:00</span></div><div id="pv-next" style="margin:10px 0;font-weight:700"></div><div id="pv-n"></div><p style="color:#55595D;font-size:18px">Cette fenêtre se synchronise avec la fenêtre de projection. Si elle reste vide, cliquez sur la fenêtre de projection puis avancez d’une étape.</p>`;
  $('#presenter .bar').addEventListener('click', e => { const c = e.target.dataset?.c; if (c) post({ type: 'cmd', cmd: c }); });
  const t0 = Date.now(); setInterval(() => { const s = Math.floor((Date.now() - t0) / 1000); $('#pv-tm').textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); }, 1000);
  addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === ' ') { post({ type: 'cmd', cmd: 'next' }); e.preventDefault(); } if (e.key === 'ArrowLeft') post({ type: 'cmd', cmd: 'prev' }); });
  post({ type: 'hello' }); renderPresenter(0, 0);
}

/* ---------- boutons ---------- */
function fullscreen() { try { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); } catch (e) {} }
function openPresenter() { const w = window.open(location.pathname + '?presenter=1', 'ove-presenter', 'width=1100,height=820'); if (!w) toast('Fenêtre bloquée par le navigateur : autorisez les fenêtres surgissantes'); setTimeout(sendState, 800); }
const act = { 'b-prev': prev, 'b-next': next, 'b-toc': () => openOv('toc'), 'b-c': () => jump(8, 0), 'b-d': () => jump(8, 10),
  'b-notes': () => { const was = $('#notes-panel').classList.contains('on'); closeOv(); if (!was) { $('#notes-panel').classList.add('on'); renderNotesPanel(); } },
  'b-pres': openPresenter, 'b-full': fullscreen, 'b-help': () => openOv('help'), 'b-calm': () => setCalm(!calm) };
$$('.hb').forEach(b => b.addEventListener('click', e => { act[b.id]?.(); if (e.detail > 0) b.blur(); }));
$$('.ov .x').forEach(b => b.addEventListener('click', closeOv));

/* ---------- clavier ---------- */
addEventListener('keydown', e => {
  if (isPresenter || e.ctrlKey || e.metaKey || e.altKey) return;
  const t = e.target, onBtn = t.closest && t.closest('button,summary,input,[role=button],[role=tab]');
  const ovOpen = Object.values(ovs).some(o => o.classList.contains('on'));
  if (e.key === 'Escape') { if (ovOpen || $('#notes-panel').classList.contains('on')) { closeOv(); e.preventDefault(); } return; }
  if (ovOpen) { if (ovs.toc.classList.contains('on') && ['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'].includes(e.key)) { const bs = $$('#toc .it'), i = bs.indexOf(document.activeElement), d = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : -1; bs[(i + d + bs.length) % bs.length].focus(); e.preventDefault(); } return; }
  const k = e.key;
  if (k === 'ArrowRight' || k === 'PageDown') { next(); e.preventDefault(); }
  else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { prev(); e.preventDefault(); }
  else if (k === ' ' || k === 'Enter') { if (onBtn) return; next(); e.preventDefault(); }
  else if (k === 'Home') { go(0, 0, -1); e.preventDefault(); }
  else if (k === 'End') { go(N - 1, stepsOf[N - 1], 1); e.preventDefault(); }
  else if (/^[1-9]$/.test(k)) { const n = +k, sc = panels[cur];
    if (cur === 1) hooks[2].select(n);
    else if (cur === 2) { if (step >= 4 && n <= 4) { setReturn(3, 4, 'Retour à la deuxième partie'); jump(3 + n, 0); } }
    else if (cur === 6) { if (n <= 3) hooks[7].tabKey(n); }
    else { const c = $(`[data-acc-key="${n}"]`, sc); if (c && shown(c)) toggleAcc(c); } }
  else { const l = k.toLowerCase();
    if (l === 'f') fullscreen(); else if (l === 's') openOv('toc'); else if (l === 'n') act['b-notes'](); else if (l === 'p') openPresenter();
    else if (l === 'c') jump(8, 0); else if (l === 'd') jump(8, 10); else if (l === 'q') jump(2, 5); else if (l === 'a') setCalm(!calm); else if (k === '?' || l === 'h') openOv('help'); }
});
/* Entrée sur un bouton de chantier, etc. : comportement natif des boutons */

/* ---------- démarrage ---------- */
panels.forEach((s, i) => { if (i) { s.inert = true; s.setAttribute('aria-hidden', 'true'); } });
if (reduce) setCalm(true);
requestAnimationFrame(loop);
const start = clamp((parseInt((location.hash || '#1').slice(1), 10) || 1) - 1, 0, N - 1);
if (!isPresenter) { fit(); go(start, 0, 1); }
window.__ove = { go: (i, s) => go(i - 1, s || 0), next, prev, state: () => ({ rub: cur + 1, step }), n: N, steps: stepsOf };
})();
