const fs = require('fs');
const files = fs.readdirSync('compositions/frames').filter(f => f.endsWith('.html'));
for (const file of files) {
  const path = 'compositions/frames/' + file;
  let content = fs.readFileSync(path, 'utf8');
  
  // replace id="...-wrap" class="clip f...-wrapper" with id="root" class="clip"
  content = content.replace(/<div id="[^"]+" class="clip f[0-9]-wrapper"/, '<div id="root" class="clip"');
  content = content.replace(/<div id="methode-wrap" class="clip f6-wrapper"/, '<div id="root" class="clip"');
  content = content.replace(/<div id="conclusion-wrap" class="clip f7-wrapper"/, '<div id="root" class="clip"');
  
  // replace css class
  content = content.replace(/\.f[0-9]-wrapper\s*\{/g, '#root {');
  
  fs.writeFileSync(path, content);
}
console.log('done');
