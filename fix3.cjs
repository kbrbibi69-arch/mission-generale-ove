const fs = require('fs');
const files = fs.readdirSync('compositions/frames').filter(f => f.endsWith('.html'));
for (const file of files) {
  const path = 'compositions/frames/' + file;
  let content = fs.readFileSync(path, 'utf8');
  content = content.replace(/id="[^"]+" (data-composition-id="[^"]+" data-width="1920" data-height="1080") class="clip f[0-9]-wrapper"/g, 'id="root" $1 class="clip"');
  content = content.replace(/id="methode-wrap" (data-composition-id="[^"]+" data-width="1920" data-height="1080") data-duration="45"/g, 'id="root" $1 class="clip" data-duration="45"');
  content = content.replace(/id="conclusion-wrap" (data-composition-id="[^"]+" data-width="1920" data-height="1080") data-duration="40"/g, 'id="root" $1 class="clip" data-duration="40"');
  content = content.replace(/\.f[0-9]-wrapper\s*\{/g, '#root {');
  fs.writeFileSync(path, content);
}
console.log('done');
