const fs = require('fs');

// 1. Fix 01-intro img crossorigin
let intro = fs.readFileSync('compositions/frames/01-intro.html', 'utf8');
intro = intro.replace('crossorigin="anonymous"', '');
fs.writeFileSync('compositions/frames/01-intro.html', intro);

// 2. Replace colors in all frames
const files = fs.readdirSync('compositions/frames').filter(f => f.endsWith('.html'));
for (const file of files) {
  const path = 'compositions/frames/' + file;
  let content = fs.readFileSync(path, 'utf8');
  content = content.replace(/#0B2046/g, '#27963C');
  // ensure we don't mess up anything else
  fs.writeFileSync(path, content);
}
console.log('done colors');
