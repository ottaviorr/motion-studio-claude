// Camada de legenda "palavra por palavra" para vídeo em pé (anúncio). Página transparente (#st class="v alfa"),
// gravada uma vez sobre o vídeo inteiro (ProRes 4444 com alfa) e sobreposta no fim. Lê window.LEG ([palavra, início, fim])
// e window.LEG_DUR (gerados por base/gerar-plano.py). Configuração opcional: window.LEG_CFG = {y, ouro:[...], cor:[...]}.
(function(){
  const CFG=Object.assign({y:1400,maxCar:15,maxPal:3,ouro:[],cor:[]},window.LEG_CFG||{});
  const limpa=s=>s.replace(/\.\.\.$/,'').replace(/[.,;:]+$/,'');
  const nrm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9$]/g,'');
  // agrupa: até maxPal palavras ou maxCar letras; quebra depois de pontuação forte
  const G=[];let cur=[];
  LEG.forEach(([w,a,b],i)=>{
    const txt=limpa(w);const len=cur.reduce((n,x)=>n+x.txt.length+1,0)+txt.length;
    if(cur.length&&(cur.length>=CFG.maxPal||len>CFG.maxCar)){G.push(cur);cur=[];}
    cur.push({txt,a,b,tom:CFG.ouro.some(o=>nrm(w).startsWith(nrm(o)))?'ouro':CFG.cor.some(o=>nrm(w).startsWith(nrm(o)))?'cor':''});
    if(/[.?!:]$|\.\.\.$/.test(w)){G.push(cur);cur=[];}
  });
  if(cur.length)G.push(cur);
  // cada grupo aparece na 1ª palavra e fica até o próximo começar (ou um respiro depois da última palavra)
  G.forEach((g,i)=>{g.ini=g[0].a-.06;const prox=G[i+1]?G[i+1][0].a-.06:1e9;g.fim=Math.min(prox,g[g.length-1].b+.55);});
  const st=$('st');
  st.innerHTML=G.map((g,i)=>`<div class="lg" id="lg${i}">${g.map((p,j)=>`<span class="pw ${p.tom}" id="lg${i}-${j}"><i></i><b>${p.txt}</b></span>`).join(' ')}</div>`).join('');
  st.querySelectorAll('.lg').forEach(e=>e.style.top=CFG.y+'px');
  cena(window.LEG_DUR||10,t=>{
    G.forEach((g,i)=>{
      const el=$('lg'+i);const on=t>=g.ini&&t<g.fim;
      if(!on){el.style.visibility='hidden';return;}
      el.style.visibility='visible';
      const k=back(p(t,g.ini,g.ini+.22),1.6);el.style.transform=`translateY(-50%) scale(${(.86+.14*k).toFixed(4)})`;el.style.opacity=Math.min(1,p(t,g.ini,g.ini+.08)).toFixed(3);
      g.forEach((pw,j)=>{
        const s=$('lg'+i+'-'+j),hl=s.querySelector('i');
        const ativa=t>=pw.a-.04&&(j===g.length-1?t<g.fim:t<g[j+1].a-.04);
        const k2=back(p(t,pw.a-.04,pw.a+.16),2.2);
        hl.style.opacity=ativa?1:0;hl.style.transform=`scale(${ativa?(.7+.3*k2).toFixed(3):.7})`;
        s.style.transform=`scale(${ativa?(1+.08*Math.sin(Math.PI*p(t,pw.a-.04,pw.a+.22))).toFixed(4):1})`;
        s.classList.toggle('dito',t>=pw.a-.04);
      });
    });
  });
})();
