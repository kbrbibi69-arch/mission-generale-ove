const fs = require('fs');

function fix(id) {
  const path = 'compositions/frames/' + id + '.html';
  let content = fs.readFileSync(path, 'utf8');
  content = content.replace(/<script type="module">[\s\S]*?<\/script>/, `<script>
  window.__timelines = window.__timelines || {};
  const tl_${id.replace('-','')} = window.gsap ? gsap.timeline({ paused: true }) : { fromTo: ()=>{}, to: ()=>{} };
  const root_${id.replace('-','')} = document.getElementById("root") || document.body;
  // logic
  window.__timelines["${id}"] = tl_${id.replace('-','')};
</script>`);
  fs.writeFileSync(path, content);
}

const frames = [
  {id: '01-intro', logic: `tl_01intro.fromTo(root_01intro.querySelector('.f1-logo'), { opacity: 0 }, { opacity: 1, duration: 1 }, 0);
  tl_01intro.fromTo(root_01intro.querySelector('.f1-sub'), { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1 }, 1);`},
  
  {id: '02-ecosystem', logic: `const stats = root_02ecosystem.querySelectorAll('.stat');
  tl_02ecosystem.fromTo(stats, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.5 }, 0.5);
  const nums = root_02ecosystem.querySelectorAll('.f2-num');
  nums.forEach((num, i) => {
    const val = parseInt(num.getAttribute('data-val'), 10);
    tl_02ecosystem.fromTo(num, { innerHTML: 0 }, { innerHTML: val, duration: 2, snap: { innerHTML: 1 }, ease: 'power1.out' }, 1 + i * 0.5);
  });`},
  
  {id: '03-message', logic: `const words = root_03message.querySelectorAll('.f3-word');
  tl_03message.to(words, { opacity: 1, y: 0, duration: 0.5, stagger: 0.2 }, 1);`},
  
  {id: '04-risks', logic: `tl_04risks.fromTo(root_04risks.querySelector('.f4-shield'), { scale: 0 }, { scale: 1, duration: 1, ease: 'back.out(1.7)' }, 0.5);
  tl_04risks.to(root_04risks.querySelector('.f4-shield'), { scale: 1.05, duration: 2, repeat: 10, yoyo: true, ease: 'sine.inOut' }, 1.5);
  const nodes = root_04risks.querySelectorAll('.f4-node');
  tl_04risks.fromTo(nodes, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, stagger: 0.3 }, 1);`},
  
  {id: '05-dispositif', logic: `const items = root_05dispositif.querySelectorAll('.f5-item');
  tl_05dispositif.fromTo(items, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.8, stagger: 0.5 }, 0.5);`}
];

for (const f of frames) {
  const path = 'compositions/frames/' + f.id + '.html';
  let content = fs.readFileSync(path, 'utf8');
  content = content.replace(/<script type="module">[\s\S]*?<\/script>/, `<script>
  window.__timelines = window.__timelines || {};
  const tl_${f.id.replace('-','')} = window.gsap ? gsap.timeline({ paused: true }) : { fromTo: ()=>{}, to: ()=>{} };
  const root_${f.id.replace('-','')} = document.getElementById("root") || document.body;
  ${f.logic}
  window.__timelines["${f.id}"] = tl_${f.id.replace('-','')};
</script>`);
  // also fix the encoding issue for 01-intro
  if (f.id === '01-intro') {
    content = content.replace('PR%VENTION & D%TECTION DES ATTEINTES ? LA PROBIT%', 'PRÉVENTION & DÉTECTION DES ATTEINTES À LA PROBITÉ');
  }
  fs.writeFileSync(path, content);
}
console.log('done scripts');
