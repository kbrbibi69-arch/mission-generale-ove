const fs = require('fs');

const frames = [
  {
    id: '02-ecosystem',
    css: `.stat-box { position: relative; padding: 2cqw; border: 2px solid var(--brand-accent, #D4AF37); background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; }
    .f2-line { position: absolute; bottom: 0; left: 0; height: 4px; background: var(--brand-accent, #D4AF37); width: 100%; transform-origin: left; }`,
    logic: `const stats = root_02ecosystem.querySelectorAll('.stat');
    // Box elastic pop
    tl_02ecosystem.fromTo(stats, { scale: 0.5, opacity: 0, rotationX: 45 }, { scale: 1, opacity: 1, rotationX: 0, duration: 1, stagger: 0.2, ease: 'back.out(1.5)' }, 0.5);
    const nums = root_02ecosystem.querySelectorAll('.f2-num');
    nums.forEach((num, i) => {
      const val = parseInt(num.getAttribute('data-val'), 10);
      tl_02ecosystem.fromTo(num, { innerHTML: 0, scale: 0.5, color: '#FFFFFF' }, { innerHTML: val, scale: 1, color: '#D4AF37', duration: 2, snap: { innerHTML: 1 }, ease: 'power2.out' }, 1 + i * 0.2);
    });
    // Draw lines
    const lines = root_02ecosystem.querySelectorAll('.f2-line');
    tl_02ecosystem.fromTo(lines, { scaleX: 0 }, { scaleX: 1, duration: 1, stagger: 0.2, ease: 'power2.out' }, 1.5);
    // Continuous subtle floating
    tl_02ecosystem.to(stats, { y: -10, duration: 2, repeat: 10, yoyo: true, ease: 'sine.inOut', stagger: 0.1 }, 2);`
  },
  {
    id: '03-message',
    css: `.f3-quote { position: absolute; font-size: 40cqw; color: rgba(255,255,255,0.05); font-family: Georgia, serif; top: -10cqw; left: -5cqw; z-index: 0; }
    .f3-text { position: relative; z-index: 1; text-shadow: 0 5px 15px rgba(0,0,0,0.3); }`,
    logic: `const words = root_03message.querySelectorAll('.f3-word');
    // Giant quote slow rotation
    tl_03message.fromTo(root_03message.querySelector('.f3-quote'), { rotation: -10, scale: 0.8 }, { rotation: 5, scale: 1.1, duration: 20, ease: 'none' }, 0);
    // Kinetic typography entrance
    tl_03message.fromTo(words, { opacity: 0, z: 100, rotationX: -90, y: 50 }, { opacity: 1, z: 0, rotationX: 0, y: 0, duration: 0.8, stagger: 0.1, ease: 'back.out(1.5)' }, 0.5);
    // Highlight words glow
    const highlights = root_03message.querySelectorAll('.f3-highlight');
    tl_03message.to(highlights, { textShadow: '0 0 20px #D4AF37', scale: 1.1, duration: 0.5, stagger: 0.1, yoyo: true, repeat: 1 }, 3);`
  },
  {
    id: '04-risks',
    css: `.f4-svg { position: absolute; inset: 0; z-index: 0; width: 100%; height: 100%; }
    .f4-line { stroke: var(--brand-accent, #D4AF37); stroke-width: 4px; stroke-dasharray: 1000; stroke-dashoffset: 1000; fill: none; }
    .f4-ripple { position: absolute; border-radius: 50%; border: 2px solid var(--brand-accent, #D4AF37); opacity: 0; }
    .f4-shield { z-index: 2; box-shadow: 0 0 30px rgba(212,175,55,0.5); }
    .f4-node { z-index: 2; transform-origin: center; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }`,
    logic: `// Shield entrance
    tl_04risks.fromTo(root_04risks.querySelector('.f4-shield'), { scale: 0, rotationY: 180 }, { scale: 1, rotationY: 0, duration: 1.5, ease: 'elastic.out(1, 0.5)' }, 0.5);
    // Shield pulse
    tl_04risks.to(root_04risks.querySelector('.f4-shield'), { scale: 1.05, boxShadow: '0 0 50px rgba(212,175,55,0.8)', duration: 2, repeat: 10, yoyo: true, ease: 'sine.inOut' }, 2);
    // Draw SVG lines (simulated)
    const lines = root_04risks.querySelectorAll('.f4-line');
    tl_04risks.to(lines, { strokeDashoffset: 0, duration: 1.5, stagger: 0.2, ease: 'power2.inOut' }, 1.5);
    // Nodes pop
    const nodes = root_04risks.querySelectorAll('.f4-node');
    tl_04risks.fromTo(nodes, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8, stagger: 0.2, ease: 'back.out(1.5)' }, 2);
    tl_04risks.to(nodes, { y: -10, duration: 1.5, stagger: 0.1, repeat: 10, yoyo: true, ease: 'sine.inOut' }, 3);`
  },
  {
    id: '05-dispositif',
    css: `.f5-item { position: relative; overflow: hidden; background: rgba(0,0,0,0.2); backdrop-filter: blur(10px); margin-bottom: 2cqw; border-radius: 4px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .f5-wipe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--brand-accent, #D4AF37); z-index: 10; transform-origin: left; }
    .f5-text { position: relative; z-index: 1; }
    .f5-icon { display: inline-block; margin-right: 1cqw; color: var(--brand-accent, #D4AF37); font-weight: bold; }`,
    logic: `const items = root_05dispositif.querySelectorAll('.f5-item');
    const wipes = root_05dispositif.querySelectorAll('.f5-wipe');
    const texts = root_05dispositif.querySelectorAll('.f5-text');
    // Hide texts initially
    tl_05dispositif.set(texts, { opacity: 0, x: -20 });
    // Item slide in
    tl_05dispositif.fromTo(items, { x: -100, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, stagger: 0.4, ease: 'power2.out' }, 0.5);
    // Wipe effect reveal
    tl_05dispositif.fromTo(wipes, { scaleX: 0 }, { scaleX: 1, duration: 0.4, stagger: 0.4, ease: 'power2.inOut' }, 0.7);
    tl_05dispositif.to(texts, { opacity: 1, x: 0, duration: 0.1, stagger: 0.4 }, 0.9);
    tl_05dispositif.to(wipes, { scaleX: 0, transformOrigin: 'right', duration: 0.4, stagger: 0.4, ease: 'power2.inOut' }, 1.1);`
  }
];

// Helper to inject CSS
function injectCSS(content, cssStr) {
  return content.replace('</style>', cssStr + '\n  </style>');
}

// Helper to replace logic
function replaceLogic(content, newLogic, id) {
  // Finds the body between root setup and window.__timelines registration
  const regex = new RegExp('(const root_'+id.replace('-','')+' = document.getElementById\\("root"\\) \\|\\| document.body;)[\\s\\S]*?(window.__timelines\\["'+id+'"\\] = tl_'+id.replace('-','')+';)');
  return content.replace(regex, '$1\n' + newLogic + '\n    $2');
}

for (const f of frames) {
  const path = 'compositions/frames/' + f.id + '.html';
  if (!fs.existsSync(path)) continue;
  let content = fs.readFileSync(path, 'utf8');
  
  if (f.id === '02-ecosystem') {
    content = content.replace(/class="stat"/g, 'class="stat stat-box"');
    content = content.replace(/<\/div><\/div>/g, '</div><div class="f2-line"></div></div>');
  }
  
  if (f.id === '03-message') {
    content = content.replace('<div class="f3-text">', '<div class="f3-quote">"</div>\n    <div class="f3-text">');
  }
  
  if (f.id === '04-risks') {
    // Add SVG background lines
    const svg = `<svg class="f4-svg">
      <path class="f4-line" d="M 960 300 Q 600 500 400 800" />
      <path class="f4-line" d="M 960 300 Q 960 500 960 800" />
      <path class="f4-line" d="M 960 300 Q 1320 500 1520 800" />
    </svg>`;
    content = content.replace('<div class="f4-shield">', svg + '\n    <div class="f4-shield">');
  }
  
  if (f.id === '05-dispositif') {
    // Modify item structure
    content = content.replace(/<div class="f5-item">1. Engagement de la Direction<\/div>/g, '<div class="f5-item"><div class="f5-wipe"></div><div class="f5-text"><span class="f5-icon">▶</span> Engagement de la Direction</div></div>');
    content = content.replace(`<div class="f5-item">2. Code de conduite intégré</div>`, `<div class="f5-item"><div class="f5-wipe"></div><div class="f5-text"><span class="f5-icon">▶</span> Code de conduite intégré</div></div>`);
    content = content.replace(`<div class="f5-item">3. Dispositif d'alerte interne</div>`, `<div class="f5-item"><div class="f5-wipe"></div><div class="f5-text"><span class="f5-icon">▶</span> Dispositif d'alerte interne</div></div>`);
    content = content.replace(`<div class="f5-item">4. Formations ciblées</div>`, `<div class="f5-item"><div class="f5-wipe"></div><div class="f5-text"><span class="f5-icon">▶</span> Formations ciblées</div></div>`);
  }
  
  content = injectCSS(content, f.css);
  content = replaceLogic(content, f.logic, f.id);
  fs.writeFileSync(path, content);
}
console.log('done upgrades');
