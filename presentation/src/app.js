(() => {
'use strict';
const NOTES = JSON.parse(document.getElementById('notes-data').textContent);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const NS = 'http://www.w3.org/2000/svg';
const isPresenter = /[?&]presenter/.test(location.search);
const stage = $('#stage'), scenes = $$('.scene'), N = scenes.length;
const stepsOf = scenes.map(s => +s.dataset.steps || 0);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let cur = -1, step = 0, lock = 0, calm = false, retTo = null, introT = 0, introAt = 0;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

/* ---------- mise à l'échelle 1920×1080 ---------- */
function fit() {
  const s = Math.min(innerWidth / 1920, innerHeight / 1080);
  stage.style.transform = `translate(-50%,-50%) scale(${s})`;
}
addEventListener('resize', fit); fit();

/* ---------- calme (animations suspendues) ---------- */
function setCalm(on) {
  calm = on; document.body.classList.toggle('calm', on);
  if (reduce) document.body.classList.toggle('motion', !on);
  const b = $('#b-calm'); if (b) b.setAttribute('aria-pressed', on);
  if (on) { tokenPlace(); } flashToast(on ? 'Animations non essentielles suspendues' : 'Animations rétablies');
}
let toastT; function flashToast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('on'), 1800); }

/* ---------- affichage des étapes ---------- */
function applySteps() {
  const sc = scenes[cur];
  $$('[data-s]', sc).forEach(el => {
    const a = +el.dataset.s, b = el.dataset.smax ? +el.dataset.smax : 99;
    el.classList.toggle('on', step >= a && step <= b);
  });
  (hooks[cur + 1] || {}).step?.(step);
  updateHud(); sendState();
}
function setStep(k) { step = clamp(k, 0, stepsOf[cur]); applySteps(); }

/* ---------- navigation ---------- */
function go(i, st = 0, dir) {
  i = clamp(i, 0, N - 1);
  if (i === cur) { setStep(st); return; }
  const d = dir ?? (i >= cur ? 1 : -1);
  const out = scenes[cur], inn = scenes[i];
  stage.style.setProperty('--dir', d);
  stage.dataset.tr = (d >= 0 ? inn : (out || inn)).dataset.tr || 'rise';
  const bands = stage.dataset.tr === 'bands' && cur >= 0 && !calm;
  const swap = () => {
    if (out) { out.classList.remove('active', 'entering'); out.classList.add('leaving'); out.inert = true; out.setAttribute('aria-hidden', 'true');
      (hooks[cur + 1] || {}).leave?.(); const o = out; setTimeout(() => { o.classList.remove('leaving'); $$('.st', o).forEach(e => e.classList.remove('on')); }, calm ? 20 : 900); }
    const prevCur = cur; cur = i; step = 0;
    if (i === 0) { if (d >= 0 && prevCur !== 1 && !calm && !reduce) playIntro(true); else playIntro(false); }
    inn.classList.add('active', 'entering'); inn.inert = false; inn.removeAttribute('aria-hidden');
    setTimeout(() => inn.classList.remove('entering'), 1100);
    (hooks[i + 1] || {}).enter?.(d);
    requestAnimationFrame(() => requestAnimationFrame(() => { applySteps(); setStep(st); }));
    $('#live').textContent = `Scène ${i + 1} sur ${N} : ${NOTES.scenes[i].title}`;
    history.replaceState(null, '', '#' + (i + 1));
    checkReturn();
  };
  if (bands) {
    const b = $('#bands'); b.classList.remove('go', 'back'); void b.offsetWidth; b.classList.add('go'); if (d < 0) b.classList.add('back');
    lock = performance.now() + 700; setTimeout(swap, 480); setTimeout(() => b.classList.remove('go', 'back'), 1250);
  } else { lock = performance.now() + (calm ? 0 : 450); swap(); }
}
function next() {
  if (performance.now() < lock) return;
  if (cur === 0 && scenes[0].classList.contains('intro')) { skipIntro(); return; }
  if (step < stepsOf[cur]) setStep(step + 1); else if (cur < N - 1) go(cur + 1, 0, 1);
}
function prev() {
  if (performance.now() < lock) return;
  if (cur === 0 && scenes[0].classList.contains('intro')) { skipIntro(); return; }
  if (step > 0) setStep(step - 1); else if (cur > 0) go(cur - 1, stepsOf[cur - 1], -1);
}
function jump(sceneNo, st) { go(sceneNo - 1, st ?? 0); }
function playIntro(on) {
  const s = scenes[0]; clearTimeout(introT); s.classList.remove('intro'); stage.classList.remove('introing');
  if (on) { void s.offsetWidth; s.classList.add('intro'); stage.classList.add('introing'); introAt = performance.now(); introT = setTimeout(() => { s.classList.remove('intro'); stage.classList.remove('introing'); }, 4700); }
}
function skipIntro() { clearTimeout(introT); scenes[0].classList.remove('intro'); stage.classList.remove('introing'); }

/* ---------- retour (depuis un détail de chantier ou la décision) ---------- */
function setReturn(sceneNo, st, label) { retTo = { sceneNo, st, label }; }
function checkReturn() {
  const b = $('#ret'); if (!retTo) { b.classList.remove('on'); return; }
  if (cur + 1 === retTo.sceneNo) { retTo = null; b.classList.remove('on'); return; }
  b.textContent = '← ' + retTo.label; b.classList.add('on');
}
$('#ret').addEventListener('click', e => { if (retTo) { const r = retTo; retTo = null; jump(r.sceneNo, r.st); } if (e.detail > 0) e.currentTarget.blur(); });

/* ---------- accordéons (cartes cliquables) ---------- */
function toggleAcc(card, force) {
  const grp = card.dataset.acc, multi = card.hasAttribute('data-multi');
  const open = force ?? !card.classList.contains('open');
  if (open && !multi) $$(`[data-acc="${grp}"].open`, scenes[cur]).forEach(c => { if (c !== card) { c.classList.remove('open'); c.querySelector('button')?.setAttribute('aria-expanded', 'false'); } });
  card.classList.toggle('open', open);
  card.querySelector('button')?.setAttribute('aria-expanded', open);
  if (grp === 's2') $$('.zone', scenes[1]).forEach(z => z.style.opacity = '');
}
stage.addEventListener('click', e => {
  const g = e.target.closest('[data-goto]');
  if (g) { e.stopPropagation(); if (cur === 6) setReturn(7, 2, 'Retour aux quatre chantiers'); else if (cur === 16) setReturn(17, 3, 'Retour à la décision'); jump(+g.dataset.goto, 0); if (e.detail > 0) g.blur(); return; }
  const card = e.target.closest('[data-acc]');
  if (card && e.target.closest('button') === card.querySelector(':scope > button')) { toggleAcc(card); if (e.detail > 0) e.target.closest('button').blur(); }
});

/* ---------- jetons animés (flux, diffusion) ---------- */
const runners = [];
function addRunner(scene, path, el, speed, off, kind) { runners.push({ scene, path, el, speed, off, kind, L: path.getTotalLength() }); }
function place(r, f) {
  const p = r.path.getPointAtLength(r.L * f), q = r.path.getPointAtLength(Math.min(r.L, r.L * f + 2));
  const a = Math.atan2(q.y - p.y, q.x - p.x) * 180 / Math.PI;
  r.el.setAttribute('transform', `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)}) rotate(${r.kind === 'sup' ? a : 0})`);
}
function tokenPlace() { runners.forEach(r => place(r, r.off)); }
let tprev = 0;
function loop(t) {
  requestAnimationFrame(loop);
  if (calm || document.hidden) return;
  const dt = Math.min(0.05, (t - tprev) / 1000); tprev = t;
  runners.forEach(r => { if (!scenes[r.scene].classList.contains('active')) return; r.off = (r.off + dt * r.speed) % 1; place(r, r.off); });
}

/* ---------- données des scènes ---------- */
const S3 = {
  1: ['Au centre', 'Fondation OVE', 'La Fondation fonctionne au centre d’un ensemble très intégré : fonds de dotation IMOVE, SCI, associations du réseau.'],
  2: ['Fonds de dotation', 'IMOVE', 'Concerné par les flux financiers internes : apports en compte courant, avances, prestations, mises à disposition. Mandat décrit dans la note : le Directeur général en est administrateur.'],
  3: ['Sociétés civiles immobilières', 'SCI', 'Concernées par les flux financiers internes. Opérations immobilières et décisions impliquant les SCI : zone de vigilance identifiée. Mandat décrit dans la note : le Directeur général est gérant de toutes les SCI.'],
  4: ['Associations du réseau', 'Associations du réseau', 'Concernées par les flux internes et par les interventions du siège. Le Directeur général préside leurs directoires. Certains membres du Bureau président des associations partenaires et des conseils de surveillance.'],
  5: ['Fonctions support', 'Services du siège', 'Juridique, immobilier, fonctions support : interventions au profit des associations qui n’ont pas ces expertises.'],
  6: ['Fonctions et mandats', 'Direction générale', 'Mandats décrits dans la note : le Directeur général est gérant de toutes les SCI, administrateur du fonds de dotation et président du directoire de toutes les associations du réseau.'],
  7: ['Gouvernance', 'Bureau', 'Certains membres du Bureau sont présidents d’associations partenaires et de conseils de surveillance.']
};
const S3NOTE = 'Source : la note. Une configuration décrite n’est ni une faute ni une irrégularité constatée.';
const S9 = [
  ['search', 'Identifier', 'Repérer une situation où des intérêts peuvent se croiser.'],
  ['doc', 'Déclarer', 'Appliquer les règles de déclaration des intérêts.'],
  ['gauge', 'Analyser', 'Apprécier la situation à la lumière du code commun.'],
  ['pause', 'S’abstenir si nécessaire', 'La personne directement intéressée s’abstient, avec mention explicite de l’abstention.'],
  ['gov', 'Faire décider un organe non intéressé', 'Validation par un organe non intéressé.'],
  ['pen', 'Documenter', 'Consigner la décision et les abstentions.'],
  ['archive', 'Conserver la trace', 'Garder la trace de l’arbitrage : traçabilité des décisions.']
];
const S10 = [['Flux identifié', ''], ['Flux recensé', 'recensement complet'], ['Flux qualifié', 'objet, nature'], ['Convention écrite', 'objet · conditions · responsabilités'], ['Validation adaptée', 'organe non intéressé'], ['Abstention documentée', 'le cas échéant'], ['Décision traçable', '']];
const S12SAT = [
  ['Bureau', 'gov', 'Reçoit un reporting régulier du référent. Le Bureau conserve ses décisions.'],
  ['Entités du réseau', 'network', 'Cartographie des risques dans l’ensemble des entités.'],
  ['Conventions', 'doc', 'Modèles de conventions pour les flux entre entités.'],
  ['Chartes', 'flag', 'Chartes et conventions : déclinaison du cadre commun dans toutes les entités du réseau.'],
  ['Dispositif d’alerte', 'bell', 'Animation du dispositif d’alerte.'],
  ['Registre des mandats', 'table', 'Registre des mandats et fonctions (Fondation, IMOVE, SCI, associations) pour objectiver les cumuls.']
];
const S12MIS = [['Piloter la cartographie des risques', 1], ['Proposer des modèles de conventions', 2], ['Contribuer au code commun et aux chartes', 3], ['Animer le dispositif d’alerte', 4], ['Assurer un reporting régulier au Bureau', 0], ['S’appuyer sur le registre des mandats et fonctions', 5]];
const S16 = [
  ['Décision d’orientation du Bureau', 'Aujourd’hui : le Bureau est invité à se prononcer sur le principe de la démarche.'],
  ['Recensement des flux et des mandats', 'Recenser l’ensemble des flux financiers et prestations, ainsi que les mandats et fonctions.'],
  ['Cartographie des risques', 'Cartographier les risques là où ils se situent vraiment.'],
  ['Code commun', 'Élaborer le code commun « probité et conflits d’intérêts ».'],
  ['Conventions et chartes types', 'Préparer les conventions et chartes types pour les entités du réseau.'],
  ['Fonction probité / compliance', 'Organiser la fonction probité / compliance, rattachée à la Direction générale.'],
  ['Calendrier', 'Définir le calendrier. Aucune date n’est arrêtée à ce stade.'],
  ['Priorités', 'Définir les priorités de mise en œuvre.'],
  ['Évaluation des moyens', 'Évaluer les moyens nécessaires. Aucun chiffre n’est avancé à ce stade.'],
  ['Présentation du plan', 'Le plan de mise en œuvre est présenté en fin d’année au Bureau.'],
  ['Validation par les instances', 'Le plan est soumis, pour validation, au Bureau et au Conseil d’administration.'],
  ['Déploiement progressif', 'Déploiement progressif, par chartes et conventions, dans l’ensemble des entités du réseau.'],
  ['Suivi et amélioration continue', 'La démarche se poursuit dans une logique d’amélioration continue.']
];
const icon = (n, s = 40) => `<svg class="ic" width="${s}" height="${s}" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const mk = (tag, cls, html, parent, ns) => { const e = ns ? document.createElementNS(NS, tag) : document.createElement(tag); if (cls) e.setAttribute('class', cls); if (html != null) e.innerHTML = html; parent?.appendChild(e); return e; };

/* ---------- initialisations par scène ---------- */
const hooks = {};
/* S1 : rien de plus (CSS) */
/* S2 : touches 1-3 gérées globalement */

/* S3 */
(function () {
  const sc = $('#s3'), nodes = $$('.s3n', sc), flt = { flux: true, presta: true, mad: true, sup: true, man: true };
  const tokG = $('#s3-tokens'); const idx = (scenes.indexOf(sc));
  const edges = $$('.edge', sc);
  const types = [['flux', 'c'], ['presta', 's'], ['mad', 't']];
  edges.forEach((p, ei) => types.forEach(([ty, shape], ti) => {
    const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'tok st st-fade'); g.dataset.t = ty; g.dataset.s = 2; g.style.pointerEvents = 'none';
    let sh;
    if (shape === 'c') { sh = mk('circle', '', '', g, 1); sh.setAttribute('r', 9); sh.setAttribute('fill', '#B4C908'); sh.setAttribute('stroke', '#5C6600'); sh.setAttribute('stroke-width', 2); }
    else if (shape === 's') { sh = mk('rect', '', '', g, 1); sh.setAttribute('x', -8); sh.setAttribute('y', -8); sh.setAttribute('width', 16); sh.setAttribute('height', 16); sh.setAttribute('fill', '#55595D'); }
    else { sh = mk('polygon', '', '', g, 1); sh.setAttribute('points', '0,-11 10,8 -10,8'); sh.setAttribute('fill', '#5C6600'); }
    tokG.appendChild(g);
    addRunner(idx, p, g, 0.07 + 0.01 * ti, (ei * 0.17 + ti * 0.33) % 1, 'k');
  }));
  const sup = $('#m-sup');
  for (let k = 0; k < 3; k++) {
    const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'tok st st-fade'); g.dataset.t = 'sup'; g.dataset.s = 3; g.style.pointerEvents = 'none';
    const pl = mk('polyline', '', '', g, 1); pl.setAttribute('points', '-8,-9 6,0 -8,9'); pl.setAttribute('fill', 'none'); pl.setAttribute('stroke', '#25282B'); pl.setAttribute('stroke-width', 5); pl.setAttribute('stroke-linecap', 'round'); pl.setAttribute('stroke-linejoin', 'round');
    tokG.appendChild(g); addRunner(idx, sup, g, 0.16, k / 3, 'sup');
  }
  function applyFilters() {
    $$('.tok', sc).forEach(t => t.style.opacity = flt[t.dataset.t] ? '' : '0');
    $('.s3-man', sc).style.opacity = flt.man ? '' : '0.08';
    $('#m-sup').style.opacity = flt.sup ? '' : '0.1';
  }
  $$('.flt', sc).forEach(b => b.addEventListener('click', e => {
    const t = b.dataset.t; flt[t] = !flt[t]; b.setAttribute('aria-pressed', flt[t]); applyFilters(); if (e.detail > 0) b.blur();
  }));
  function select(k) {
    const el = nodes.find(n => +n.dataset.k === k); if (!el || !el.classList.contains('on')) return;
    nodes.forEach(n => n.classList.toggle('sel', n === el));
    const [kick, title, body] = S3[k];
    $('#s3-pk').textContent = kick; $('#s3-pt').textContent = title;
    $('#s3-pb').textContent = body;
  }
  nodes.forEach(n => n.addEventListener('click', e => { select(+n.dataset.k); if (e.detail > 0) n.blur(); }));
  hooks[3] = { select, step() { applyFilters(); }, enter() { nodes.forEach(n => n.classList.remove('sel')); } };
  /* pastilles SCI */
  $$('.sci-grid').forEach(g => { if (!g.children.length) for (let j = 0; j < 21; j++) { const i = document.createElement('i'); i.style.cssText = `display:block;width:14px;height:14px;border-radius:3px;background:${j % 3 ? '#878787' : '#B4C908'}`; g.appendChild(i); } });
})();

/* S5 : comparateur */
(function () {
  const cmp = $('#s5-cmp'), handle = $('#s5-handle');
  let pos = 100, anim = 0;
  const apply = p => { pos = clamp(p, 0, 100); cmp.style.setProperty('--p', pos + '%'); };
  function to(p) { cancelAnimationFrame(anim); if (calm) { apply(p); return; } const a = pos, t0 = performance.now(); (function f(t) { const k = clamp((t - t0) / 900, 0, 1), e = 1 - Math.pow(1 - k, 3); apply(a + (p - a) * e); if (k < 1) anim = requestAnimationFrame(f); })(t0); }
  $$('.s5-btns .btn').forEach(b => b.addEventListener('click', e => { to(+b.dataset.pos); if (e.detail > 0) b.blur(); }));
  let drag = false;
  const pointer = e => { const r = cmp.getBoundingClientRect(); apply(((e.clientX - r.left) / r.width) * 100); };
  handle.addEventListener('pointerdown', e => { drag = true; handle.setPointerCapture(e.pointerId); cancelAnimationFrame(anim); });
  handle.addEventListener('pointermove', e => { if (drag) pointer(e); });
  handle.addEventListener('pointerup', () => drag = false);
  cmp.addEventListener('click', e => { if (e.target === handle || handle.contains(e.target)) return; });
  hooks[5] = { enter() { apply(100); }, step(k) { to([100, 100, 50, 0][k]); } };
})();

/* S6 : rien (CSS) — */

/* S8 : ouverture progressive */
hooks[8] = { step(k) { $$('.tile', $('#s8')).forEach((t, i) => { if (i < 4) toggleAcc(t, i < k); }); } };

/* S9 : parcours */
(function () {
  const sc = $('#s9'), host = $('#s9-stations'), path = $('#s9-prog'), tok = $('#s9-token'), det = $('#s9-detail');
  const X = i => 200 + i * (1520 / 6), Y = 520;
  let d = `M${X(0)} ${Y}`;
  for (let i = 0; i < 6; i++) { const s = i % 2 ? 1 : -1; d += ` C${X(i) + 95} ${Y + s * 105} ${X(i + 1) - 95} ${Y - s * 105} ${X(i + 1)} ${Y}`; }
  $$('path', $('.s9-path', sc)).forEach(p => p.setAttribute('d', d));
  S9.forEach(([ic, t, tx], i) => {
    const st = mk('div', 's9-st st st-fade' + (i % 2 ? '' : ' up'), '', host); st.dataset.s = i + 1; st.style.cssText = `left:${X(i)}px;top:${Y - 46}px`;
    const b = mk('button', 'nd', `${icon(ic, 40)}<span class="nn">${i + 1}</span>`, st); b.setAttribute('aria-label', `Étape ${i + 1} : ${t}`);
    mk('div', 'lb', esc(t), st);
    b.addEventListener('click', e => { showDetail(i); if (e.detail > 0) b.blur(); });
  });
  const showDetail = i => { det.textContent = `${i + 1}. ${S9[i][1]} — ${S9[i][2]}`; };
  hooks[9] = { enter() { det.textContent = ''; }, step(k) {
    const n = clamp(k, 0, 7);
    path.style.strokeDashoffset = 1 - (n > 0 ? (n - 1) / 6 : 0);
    path.style.transition = calm ? 'none' : 'stroke-dashoffset 1s var(--ease)';
    const i = clamp(n - 1, 0, 6); tok.style.translate = `${X(i)}px ${Y}px`; tok.style.opacity = n > 0 ? 1 : 0;
    $$('.s9-st', sc).forEach((s, j) => s.classList.toggle('now', j === n - 1));
    if (n > 0 && n <= 7) showDetail(n - 1);
  } };
})();

/* S10 : flux */
(function () {
  const sc = $('#s10'), ol = $('#s10-steps'), tok = $('#s10-token');
  S10.forEach(([t, sub], i) => { const li = mk('li', '', `<b>${i + 1}</b>${esc(t)}${sub ? `<small>${esc(sub)}</small>` : ''}`, ol); li.style.top = (i * 86) + 'px'; li.style.left = (i * 20) + 'px'; li.style.width = '640px'; });
  $$('.cf', sc).forEach(b => b.addEventListener('click', e => { const o = b.getAttribute('aria-expanded') === 'true'; $$('.cf', sc).forEach(c => c.setAttribute('aria-expanded', 'false')); b.setAttribute('aria-expanded', !o); if (e.detail > 0) b.blur(); }));
  hooks[10] = { enter() { $$('.cf', sc).forEach(c => c.setAttribute('aria-expanded', 'false')); }, step(k) {
    $$('li', ol).forEach((li, i) => { li.classList.toggle('on', i < k); li.classList.toggle('now', i === k - 1); });
    const i = clamp(k - 1, 0, 6); tok.style.translate = `${140 + i * 20}px ${309 + i * 86}px`; tok.style.opacity = k > 0 ? 1 : 0;
    tok.dataset.sh = k <= 3 ? 1 : k === 4 ? 2 : k <= 6 ? 3 : 4;
  } };
})();

/* S11 : registre */
(function () {
  const sc = $('#s11'), reg = $('#s11-reg'), btn = $('#s11-ex'), lg = $('#s11-lg'), nt = $('#s11-nt'), link = $('#s11-link path');
  const cell = (r, c) => $(`.rr[data-r="${r}"] [data-c="${c}"]`, reg);
  const A = [[3, 0], [1, 2], [2, 3]], B = [[0, 2], [3, 1]];
  const cx = c => 250 + 187.5 * (c + .5), cy = r => 80 + 76 * (r + .5);
  function show(on) {
    $$('[data-c]', reg).forEach(c => { c.classList.remove('m'); c.innerHTML = ''; });
    if (on) { A.forEach(([r, c]) => { const e = cell(r, c); e.classList.add('m'); e.innerHTML = '<span class="mk">●</span>'; }); B.forEach(([r, c]) => { const e = cell(r, c); e.classList.add('m'); e.innerHTML = '<span class="mk b">◆</span>'; });
      link.setAttribute('d', `M${cx(0)} ${cy(3)} L${cx(2)} ${cy(1)} L${cx(3)} ${cy(2)}`); nt.textContent = 'Lecture schématique : une même personne apparaît dans plusieurs structures → abstention organisée, arbitrage documenté.'; }
    else { link.setAttribute('d', ''); nt.textContent = 'Schéma illustratif : aucune donnée réelle, aucune personne nommée.'; }
    btn.setAttribute('aria-pressed', on); lg.classList.toggle('on', on);
  }
  btn.addEventListener('click', e => { show(btn.getAttribute('aria-pressed') !== 'true'); if (e.detail > 0) btn.blur(); });
  hooks[11] = { enter() { show(false); } };
})();

/* S12 : référent */
(function () {
  const sc = $('#s12'), host = $('#s12-sats'), lines = $('#s12-lines'), ml = $('#s12-missions'), det = $('#s12-detail');
  const C = [1000, 590], R = 310;
  const angs = [-90, -30, 30, 90, 150, 210];
  const sats = S12SAT.map(([t, ic, tx], i) => {
    const a = angs[i] * Math.PI / 180, x = C[0] + R * Math.cos(a), y = C[1] + R * Math.sin(a);
    const b = mk('button', 'sat st st-fade', `${icon(ic, 34)}${esc(t)}`, host); b.dataset.s = 1; b.style.cssText = `left:${x}px;top:${y}px`; b.setAttribute('aria-label', `${t} : afficher le rôle`);
    const p = mk('path', '', '', lines, 1); p.setAttribute('d', `M${C[0]} ${C[1]} L${x} ${y}`); return { b, p };
  });
  S12MIS.forEach(([t, s], i) => { const li = mk('li', 'st st-left', `<b>${i + 1}</b><span>${esc(t)}</span>`, ml); li.dataset.s = i + 1; li.style.setProperty('--d', '0s'); });
  const show = i => { det.textContent = S12SAT[i][2]; det.classList.add('on'); sats.forEach((s, j) => s.b.classList.toggle('sel', j === i)); };
  sats.forEach((s, i) => s.b.addEventListener('click', e => { show(i); if (e.detail > 0) s.b.blur(); }));
  hooks[12] = { enter() { det.classList.remove('on'); sats.forEach(s => s.b.classList.remove('sel')); }, step(k) {
    sats.forEach((s, j) => { const hot = S12MIS.some(([_, sj], mi) => sj === j && mi < k); s.b.classList.toggle('hot', hot); s.p.classList.toggle('hot', hot); });
    if (k > 0) show(S12MIS[k - 1][1]); else { det.classList.remove('on'); }
  } };
})();

/* S13 : diffusion */
(function () {
  const idx = scenes.indexOf($('#s13')), g = $('#s13-tokens');
  ['p13a', 'p13b', 'p13c', 'p13d'].forEach((id, pi) => {
    const p = document.getElementById(id);
    for (let k = 0; k < 3; k++) {
      const t = document.createElementNS(NS, 'g'); t.setAttribute('class', 'st st-fade'); t.dataset.s = 1;
      const r = mk('rect', '', '', t, 1); ['x', -14, 'y', -10, 'width', 28, 'height', 20].forEach((v, j, a) => { if (j % 2 == 0) r.setAttribute(v, a[j + 1]); });
      r.setAttribute('rx', 4); r.setAttribute('fill', '#fff'); r.setAttribute('stroke', '#5C6600'); r.setAttribute('stroke-width', 3);
      const l = mk('path', '', '', t, 1); l.setAttribute('d', 'M-7 -3H7M-7 3H3'); l.setAttribute('stroke', '#B4C908'); l.setAttribute('stroke-width', 3); l.setAttribute('stroke-linecap', 'round');
      g.appendChild(t); addRunner(idx, p, t, 0.09 + pi * 0.01, (k / 3 + pi * 0.11) % 1, 'k');
    }
  });
})();

/* S14 */
hooks[14] = { enter() { $$('[data-acc="s14"]', $('#s14')).forEach(c => toggleAcc(c, false)); } };

/* S15 : balance */
(function () {
  const sc = $('#s15'), beam = $('#s15-beam'), pl = $('#s15-pl'), pr = $('#s15-pr'), pile = $('#s15-pile'), crit = $$('.cr', sc);
  const W = []; crit.forEach(() => { const w = mk('div', 'wgt', '', pile); W.push(w); });
  function layout() {
    const n = crit.filter(c => c.getAttribute('aria-pressed') === 'true').length, th = n * 10 / 7;
    beam.style.transformOrigin = '730px 537px'; beam.style.rotate = th + 'deg';
    pl.style.transformOrigin = '300px 537px'; pl.style.rotate = -th + 'deg'; pr.style.transformOrigin = '1160px 537px'; pr.style.rotate = -th + 'deg';
    const a = th * Math.PI / 180, bx = 730 + 430 * Math.cos(a) - 163 * Math.sin(a), by = 537 + 430 * Math.sin(a) + 163 * Math.cos(a);
    let k = 0; crit.forEach((c, i) => { const on = c.getAttribute('aria-pressed') === 'true', w = W[i];
      if (on) { w.style.opacity = 1; w.style.translate = `${bx + ((k % 3) - 1) * 52}px ${by - 4 - Math.floor(k / 3) * 48}px`; k++; } else { w.style.opacity = 0; w.style.translate = `${bx}px ${by - 200}px`; } });
  }
  crit.forEach(c => c.addEventListener('click', e => { c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') !== 'true'); layout(); if (e.detail > 0) c.blur(); }));
  hooks[15] = { enter() { crit.forEach(c => c.setAttribute('aria-pressed', 'false')); layout(); }, step(k) {
    crit.forEach(c => { const s = +c.dataset.s; c.classList.toggle('show', k >= s); c.setAttribute('aria-pressed', k >= s + 0 && k >= (s === 2 ? 2 : 3) ? 'true' : 'false'); });
    layout();
  } };
})();

/* S16 : feuille de route */
(function () {
  const sc = $('#s16'), host = $('#s16-nodes'), det = $('#s16-detail'), prog = $('#s16-prog');
  const row = i => i < 5 ? 0 : i < 10 ? 1 : 2;
  const pos = i => { const r = row(i); const k = r === 0 ? i : r === 1 ? i - 5 : i - 10; const x = r === 1 ? 1720 - k * 380 : 200 + k * 380; return [x, [360, 520, 680][r]]; };
  const dist = i => { if (i < 5) return i * 380; if (i < 10) return 1520 + 251 + (i - 5) * 380; return 1520 + 251 + 1520 + 251 + (i - 10) * 380; };
  const total = 4302; const nodes = [];
  S16.forEach(([t, tx], i) => {
    const [x, y] = pos(i); const n = mk('button', 'nd16' + (i === 0 ? ' today' : ''), `<div class="c">${i + 1}</div><div class="t">${esc(t)}</div>`, host);
    n.style.cssText = `left:${x}px;top:${y - 31}px`; n.setAttribute('aria-label', `Étape ${i + 1} : ${t}`);
    n.addEventListener('click', e => { show(i); if (e.detail > 0) n.blur(); }); nodes.push(n);
  });
  const show = i => { det.textContent = `${i + 1}. ${S16[i][0]} — ${S16[i][1]}`; nodes.forEach((n, j) => n.classList.toggle('sel', j === i)); };
  const limit = [0, 3, 6, 9, 11, 13];
  hooks[16] = { enter() { det.textContent = ''; nodes.forEach(n => n.classList.remove('sel')); }, step(k) {
    const m = limit[clamp(k, 0, 5)]; nodes.forEach((n, i) => n.classList.toggle('on', i < m));
    prog.style.strokeDashoffset = 1 - (m > 0 ? dist(m - 1) / total : 0); prog.style.transition = calm ? 'none' : 'stroke-dashoffset 1.1s var(--ease)';
    if (m > 0 && k > 0) show(m - 1);
  } };
})();

/* S17 */
hooks[17] = { step(k) { scenes[16].classList.toggle('prop', k >= 1); } };
$('#s17-show').addEventListener('click', e => { if (step < 1) setStep(1); if (e.detail > 0) e.currentTarget.blur(); });

/* S18 */
hooks[18] = { step(k) { scenes[17].classList.toggle('fin', k >= 5); } };

/* ---------- HUD, sommaire, notes, aides ---------- */
const hud = $('#hud'), prog = $('#prog');
NOTES.acts.forEach(a => { const i = mk('i', '', '<b></b>', prog); i.style.flexGrow = a.scenes.length; i.title = `Acte ${a.n} · ${a.t}`; });
prog.style.display = 'flex'; prog.style.gridTemplateColumns = 'none';
function updateHud() {
  $('#cnt').textContent = `${String(cur + 1).padStart(2, '0')} / ${N}`;
  const act = NOTES.acts.find(a => a.scenes.includes(cur + 1)); $('#acts').textContent = act ? `Acte ${act.n} · ${act.t}` : '';
  hud.classList.toggle('dk', scenes[cur].classList.contains('dark'));
  $$('#prog i b').forEach((b, k) => { const a = NOTES.acts[k], first = a.scenes[0], cnt = a.scenes.length; const f = cur + 1 < first ? 0 : cur + 1 > first + cnt - 1 ? 1 : ((cur + 1 - first) + (stepsOf[cur] ? step / (stepsOf[cur] + 1) : 0.5)) / cnt; b.style.transform = `scaleX(${f})`; });
  $$('#toc .sc button').forEach(b => b.classList.toggle('cur', +b.dataset.n === cur + 1));
  renderNotesPanel();
}
const ovs = { toc: $('#toc'), help: $('#help'), obj: $('#obj') };
function closeOv() { Object.values(ovs).forEach(o => o.classList.remove('on')); $('#notes-panel').classList.remove('on'); }
function openOv(k) { const was = ovs[k].classList.contains('on'); closeOv(); if (!was) { ovs[k].classList.add('on'); const f = ovs[k].querySelector('button.cur,button,summary'); f?.focus(); } }
/* sommaire */
(function () {
  const host = $('#toc .acts');
  NOTES.acts.forEach(a => { const row = mk('div', 'act', `<h3>Acte ${a.n} · ${esc(a.t)}</h3>`, host); const sc = mk('div', 'sc', '', row);
    a.scenes.forEach(n => { const b = mk('button', '', `<b>${n}</b>${esc(NOTES.scenes[n - 1].title)}`, sc); b.dataset.n = n; b.addEventListener('click', () => { closeOv(); jump(n, 0); }); }); });
})();
const obH = $('#obj .list'); NOTES.objections.forEach(o => mk('details', '', `<summary>${esc(o.q)}</summary><p>${esc(o.r)}</p>`, obH));
function notesHTML(i, st) {
  const n = NOTES.scenes[i], ob = n.objection != null ? NOTES.objections[n.objection] : null;
  return `<div class="nt"><h3>Scène ${i + 1} · ${esc(n.title)}</h3><div>Étape ${st} / ${stepsOf[i]} · Acte ${(NOTES.acts.find(a => a.scenes.includes(i + 1)) || {}).n}</div>
  <dl><dt>Objectif de conviction</dt><dd>${esc(n.obj)}</dd><dt>Message à faire retenir</dt><dd>${esc(n.msg)}</dd><dt>Commentaire oral suggéré</dt><dd>${esc(n.oral)}</dd>
  <dt>Déclenchements</dt><dd><ul>${n.decl.map(d => `<li>${esc(d)}</li>`).join('')}</ul></dd><dt>Transition vers la scène suivante</dt><dd>${esc(n.trans)}</dd>
  ${ob ? `<dt>Objection possible</dt><dd><b>${esc(ob.q)}</b><br>${esc(ob.r)}</dd>` : ''}<dt>Temps de discussion possible</dt><dd>${esc(n.disc)}</dd><dt>Niveau de prudence juridique</dt><dd>${esc(n.prud)}</dd></dl></div>`;
}
function renderNotesPanel() {
  const p = $('#notes-panel'); if (!p.classList.contains('on')) return;
  p.innerHTML = `<div class="warn">Notes du présentateur : à masquer avant projection (touche N), ou ouvrir la fenêtre présentateur (touche P).</div>` + notesHTML(cur, step);
}
/* synchronisation avec la fenêtre présentateur */
let chan = null; try { chan = 'BroadcastChannel' in window ? new BroadcastChannel('ove-bureau-sapin2') : null; } catch (e) {}
const seen = new Set();
function post(m) { m = { ...m, id: Date.now() + '-' + Math.random() }; try { chan?.postMessage(m); } catch (e) {} try { localStorage.setItem('ove-msg', JSON.stringify(m)); } catch (e) {} }
function sendState() { if (!isPresenter && cur >= 0) post({ type: 'state', scene: cur, step }); }
function onMsg(m) {
  if (!m || (m.id && seen.has(m.id))) return; if (m.id) { seen.add(m.id); if (seen.size > 200) seen.clear(); }
  if (isPresenter && m.type === 'state') renderPresenter(m.scene, m.step);
  if (!isPresenter && m.type === 'cmd') ({ next, prev, decision: () => jump(17, 3), question: () => jump(2, 2) })[m.cmd]?.();
  if (!isPresenter && m.type === 'hello') sendState();
}
chan && (chan.onmessage = e => onMsg(e.data));
addEventListener('storage', e => { if (e.key === 'ove-msg' && e.newValue) { try { onMsg(JSON.parse(e.newValue)); } catch (_) {} } });
function renderPresenter(i, st) {
  const p = $('#presenter'), nx = NOTES.scenes[i + 1];
  $('#pv-t').textContent = `Scène ${i + 1}/${N} · ${NOTES.scenes[i].title}`; $('#pv-n').innerHTML = notesHTML(i, st);
  $('#pv-next').textContent = nx ? `Suivant : scène ${i + 2} · ${nx.title}` : 'Dernière scène';
}
if (isPresenter) {
  document.body.classList.add('presenter'); document.title = 'Présentateur — ' + document.title;
  $('#presenter').innerHTML = `<div class="bar"><strong id="pv-t">…</strong><button data-c="prev">◀ Précédent</button><button data-c="next">Suivant ▶</button><button data-c="question">Question (Q)</button><button data-c="decision">Décision (D)</button><span class="tm" id="pv-tm">00:00</span></div><div id="pv-next" style="margin:10px 0;font-weight:700"></div><div id="pv-n"></div><p style="color:#55595D;font-size:18px">Cette fenêtre se synchronise avec la fenêtre de projection. Si elle reste vide, cliquez sur la fenêtre de projection puis avancez d’une étape.</p>`;
  $('#presenter .bar').addEventListener('click', e => { const c = e.target.dataset?.c; if (c) post({ type: 'cmd', cmd: c }); });
  const t0 = Date.now(); setInterval(() => { const s = Math.floor((Date.now() - t0) / 1000); $('#pv-tm').textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); }, 1000);
  addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === ' ') { post({ type: 'cmd', cmd: 'next' }); e.preventDefault(); } if (e.key === 'ArrowLeft') post({ type: 'cmd', cmd: 'prev' }); });
  post({ type: 'hello' }); renderPresenter(0, 0);
}

/* ---------- boutons HUD ---------- */
function fullscreen() { try { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); } catch (e) {} }
function openPresenter() { const w = window.open(location.pathname + '?presenter=1', 'ove-presenter', 'width=1100,height=820'); if (!w) flashToast('Fenêtre bloquée par le navigateur : autorisez les fenêtres surgissantes'); setTimeout(sendState, 800); }
const act = { 'b-toc': () => openOv('toc'), 'b-q': () => jump(2, 2), 'b-d': () => jump(17, 3), 'b-obj': () => openOv('obj'), 'b-notes': () => { const was = $('#notes-panel').classList.contains('on'); closeOv(); if (!was) { $('#notes-panel').classList.add('on'); renderNotesPanel(); } }, 'b-pres': openPresenter, 'b-full': fullscreen, 'b-help': () => openOv('help'), 'b-calm': () => setCalm(!calm) };
$$('.hb').forEach(b => b.addEventListener('click', e => { act[b.id]?.(); if (e.detail > 0) b.blur(); }));
$$('.ov .x').forEach(b => b.addEventListener('click', closeOv));

/* ---------- clavier ---------- */
addEventListener('keydown', e => {
  if (isPresenter || e.ctrlKey || e.metaKey || e.altKey) return;
  const t = e.target, onBtn = t.closest && t.closest('button,summary,input,[role=button]');
  const ovOpen = Object.values(ovs).some(o => o.classList.contains('on'));
  if (e.key === 'Escape') { if (ovOpen || $('#notes-panel').classList.contains('on')) { closeOv(); e.preventDefault(); } return; }
  if (ovOpen) { if (ovs.toc.classList.contains('on') && (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'ArrowDown' || e.key === 'ArrowUp')) { const bs = $$('#toc .sc button'), i = bs.indexOf(document.activeElement), d = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : -1; bs[(i + d + bs.length) % bs.length].focus(); e.preventDefault(); } return; }
  const k = e.key;
  if (k === 'ArrowRight' || k === 'PageDown') { next(); e.preventDefault(); }
  else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { prev(); e.preventDefault(); }
  else if (k === ' ' || k === 'Enter') { if (onBtn) return; next(); e.preventDefault(); }
  else if (k === 'Home') { go(0, 0, -1); e.preventDefault(); }
  else if (k === 'End') { go(N - 1, stepsOf[N - 1], 1); e.preventDefault(); }
  else if (/^[1-9]$/.test(k)) { const n = +k, sc = scenes[cur];
    if (cur === 2) hooks[3].select(n);
    else { const c = $(`[data-acc-key="${n}"]`, sc); if (c && (!c.classList.contains('st') || c.classList.contains('on'))) { toggleAcc(c); if (cur === 6 && c.classList.contains('open')) c.querySelector('.go')?.focus({ preventScroll: true }); } } }
  else { const l = k.toLowerCase();
    if (l === 'f') fullscreen(); else if (l === 's') openOv('toc'); else if (l === 'n') act['b-notes'](); else if (l === 'p') openPresenter();
    else if (l === 'o') openOv('obj'); else if (l === 'q') jump(2, 2); else if (l === 'd') jump(17, 3); else if (l === 'a') setCalm(!calm);
    else if (k === '?' || l === 'h') openOv('help'); else if (l === 'r' && cur === 0) { playIntro(true); } }
});
/* focus sur un pilier ouvert : Entrée -> aller à son détail */
stage.addEventListener('keydown', e => { if (e.key === 'Enter' && cur === 6) { const p = e.target.closest('.pillar.open'); if (p) { const g = p.querySelector('.go'); if (g && e.target !== g) { g.click(); e.preventDefault(); } } } });

/* ---------- démarrage ---------- */
scenes.forEach((s, i) => { if (i) { s.inert = true; s.setAttribute('aria-hidden', 'true'); } });
if (reduce) setCalm(true);
requestAnimationFrame(loop);
const start = Math.max(1, Math.min(N, parseInt((location.hash || '#1').slice(1), 10) || 1)) - 1;
if (!isPresenter) { fit(); document.fonts && document.fonts.ready.then(() => 0); go(start, 0, 1); if (start > 0) playIntro(false); }
window.__ove = { go: (i, s) => go(i - 1, s || 0), next, prev, state: () => ({ scene: cur + 1, step }), scenes: N, steps: stepsOf };
})();
