// Confere clipes construídos antes de gravar: erros de JS e palavras que M.w() não achou na narração.
// usage: NODE_PATH=motion/node_modules node checar.cjs motion/dist/*.html
const {chromium}=(()=>{try{return require('playwright')}catch(e){return require('playwright-core')}})();
const path=require('path'),fs=require('fs');const CHROME=process.env.CHROME||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{const b=await chromium.launch(fs.existsSync(CHROME)?{executablePath:CHROME}:{});let ruim=0;
 for(const f of process.argv.slice(2)){const p=await b.newPage();const L=[];p.on('console',m=>{if(/não encontrada/.test(m.text()))L.push(m.text())});p.on('pageerror',e=>L.push('ERRO '+e.message));
  await p.goto('file://'+path.resolve(f)+'?render');const T=await p.evaluate(()=>window.DURATION);
  for(let t=0;t<=T;t+=0.5) await p.evaluate(t=>seek(t),t).catch(e=>L.push('ERRO seek '+e.message));
  console.log((L.length?'✗ ':'✓ ')+path.basename(f)+(L.length?' → '+[...new Set(L)].join(' | '):''));ruim+=L.length;await p.close();}
 await b.close();process.exit(ruim?1:0);})();
