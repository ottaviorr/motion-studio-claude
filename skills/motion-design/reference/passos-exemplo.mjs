// Modelo de passos para scripts/fotos-telas.mjs. Recebe { go, ev, shot, wait, cdp }.
//   go(url)  → abre e espera 1,8 s   · ev(js) → roda JS na página e devolve o valor
//   shot(nome, clip?) → salva nome.png · wait(ms) · cdp(método, params) → Chrome DevTools direto
// Coordenadas que saem daqui (px CSS em 1600x900) são as mesmas usadas por TELA/cam/spot/cursor nas cenas.
const R = `(e)=>{if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]}`;
// preencher campo de app React/Vue (só trocar .value não avisa o componente)
const preenche = (sel, v) => `(()=>{const i=document.querySelector('${sel}');const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;set.call(i,'${v}');i.dispatchEvent(new Event('input',{bubbles:true}));return 'ok'})()`;
// clicar pelo texto visível
const clica = (txt) => `(()=>{const e=[...document.querySelectorAll('button,a,label,[role=button],div,span')].filter(x=>x.offsetParent&&x.children.length<4&&x.textContent.trim()==='${txt}').pop();if(!e)return 'não achei';e.click();return 'ok'})()`;
export default async ({ go, ev, shot, wait, cdp }) => {
  await go("http://localhost:3000/login"); await wait(4000);          // apps com script pesado: esperar antes de interagir
  await ev(preenche('input[type=email]', 'demo@exemplo.com')); await ev(preenche('input[type=password]', 'senha-de-teste'));
  await shot("01-login-preenchido");
  console.log(await ev(clica('Entrar'))); await wait(3000);
  await shot("02-painel");
  console.log("POSICOES", await ev(`(()=>{const R=${R};return JSON.stringify({botao:R(document.querySelector('button'))})})()`));
  // enviar arquivo num <input type=file>: const d=await cdp("DOM.getDocument",{}); const q=await cdp("DOM.querySelector",{nodeId:d.result.root.nodeId,selector:"input[type=file]"}); await cdp("DOM.setFileInputFiles",{nodeId:q.result.nodeId,files:["/caminho/arquivo.png"]});
  // celular: await cdp("Emulation.setDeviceMetricsOverride",{width:430,height:932,deviceScaleFactor:3,mobile:true});
};
