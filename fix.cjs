const fs = require('fs');
const files = fs.readdirSync('compositions/frames').filter(f => f.endsWith('.html'));
for (const file of files) {
  const path = 'compositions/frames/' + file;
  let content = fs.readFileSync(path, 'utf8');
  const id = file.replace('.html', '');
  content = content.replace(/<div\s+class="clip/g, '<div id="'+id+'-wrap" data-composition-id="'+id+'" data-width="1920" data-height="1080" class="clip');
  content = content.replace(/repeat:\s*-1/g, 'repeat: 10');
  fs.writeFileSync(path, content);
}
console.log('done');
