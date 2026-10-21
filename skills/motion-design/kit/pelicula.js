// motion-design · película procedural (técnica da abertura MEIA-NOITE): grão, riscos, poeira e fios, flicker de projetor,
// vinheta e oscilação de quadro (gate weave). Tudo semeado pelo QUADRO DE FILME (24 q/s): o mesmo t desenha sempre o mesmo quadro
// (sem Math.random), e a película "anda" a 24 q/s mesmo com o vídeo a 30/60 — é isso que faz parecer filme.
// Uso:
//   <script src="pelicula.js"></script>
//   const P = PELICULA($('st'), {semente:7});        // elemento → cria um <canvas> por cima de tudo; ou passe um <canvas> seu
//   frame(t){ …; const o = P(t); $('cam').style.transform = `translate(${o.x}px,${o.y}px)`; }
//   P(t, forca)  forca 0..1 multiplica tudo (ex.: .35 num preto de corte: a película continua, mais fraca)
//   devolve {x, y, f}: a oscilação de quadro em px (aplique na "câmera" da cena, não no canvas) e o quadro de filme
//   ou deixe a película aplicar sozinha: PELICULA(el, {oscila: $('cam')}) (soma translate ao transform que a cena já pôs;
//   chame P(t) DEPOIS de a cena mexer no transform da câmera naquele quadro).
// Opções (0 desliga): grao .42 (opacidade do grão) · escalaGrao 1.5 (tamanho do grão) · riscos 3 (trilhas verticais)
//   poeira 4 (máx. de partículas por quadro) · flicker .07 · vinheta .8 (escuro na borda) · weave [2.2, 1.6] (px x, y)
//   claro '#E8E2D0' e escuro '#000' (cores do pó/risco; troque pela paleta da peça) · q 24 (quadros de filme por s) · semente 1
// Desempenho: só canvas 2D + alfa normal (nada de mix-blend-mode/drop-shadow: desliga a captura rápida do HyperFrames).
// O canvas tem o tamanho do palco em px CSS: em 4K (--escala 2) o grão fica 2× maior na imagem — suba escalaGrao para .75 se quiser fino.
(function(){
  // hash inteiro → 0..1 (igual em qualquer computador; Math.sin varia entre motores)
  function hs(n,s){let h=(Math.imul((n|0)^0x9E3779B9,0x85EBCA6B)^Math.imul((s|0)+0x632BE5AB,0xC2B2AE35))>>>0;
    h^=h>>>16;h=Math.imul(h,0x7FEB352D)>>>0;h^=h>>>15;h=Math.imul(h,0x846CA68B)>>>0;h^=h>>>16;return (h>>>0)/4294967296;}
  // ruído suave 0..1 (para a oscilação não pular)
  function vn(x,s){const i=Math.floor(x),f=x-i,u=f*f*(3-2*f);return hs(i,s)+(hs(i+1,s)-hs(i,s))*u;}
  function rnd(seed){let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
  const hex=c=>{c=c.replace('#','');if(c.length===3)c=[...c].map(x=>x+x).join('');return [0,2,4].map(i=>parseInt(c.slice(i,i+2),16));};

  function PELICULA(alvo,o={}){
    const op=Object.assign({grao:.42,escalaGrao:1.5,riscos:3,poeira:4,flicker:.07,vinheta:.8,weave:[2.2,1.6],claro:'#E8E2D0',escuro:'#000',q:24,semente:1,oscila:null},o);
    let cv=alvo;
    if(!alvo||alvo.tagName!=='CANVAS'){
      cv=document.createElement('canvas');cv.width=alvo.offsetWidth||1920;cv.height=alvo.offsetHeight||1080;
      cv.setAttribute('data-hv','ignorar');   // o conferir_hierarquia não mede a película
      Object.assign(cv.style,{position:'absolute',left:0,top:0,width:cv.width+'px',height:cv.height+'px',pointerEvents:'none',zIndex:9999});
      alvo.appendChild(cv);
    }
    const W=cv.width,H=cv.height,g=cv.getContext('2d'),S=op.semente*1000;
    // 6 telhas de grão 512×512 semeadas (claro e escuro, média de 3 sorteios ≈ gaussiano)
    const T=[],CL=hex(op.claro),TAM=512;
    if(op.grao>0)for(let k=0;k<6;k++){const c=document.createElement('canvas');c.width=c.height=TAM;const x=c.getContext('2d'),im=x.createImageData(TAM,TAM),R=rnd(S+1234+k*99);
      for(let i=0;i<TAM*TAM;i++){const v=(R()+R()+R()-1.5)/1.5,a=Math.min(255,Math.abs(v)*150),cl=v>0;
        im.data[i*4]=cl?CL[0]:0;im.data[i*4+1]=cl?CL[1]:0;im.data[i*4+2]=cl?CL[2]:0;im.data[i*4+3]=a;}
      x.putImageData(im,0,0);T.push(g.createPattern(c,'repeat'));}
    const raio=Math.hypot(W,H)/2;
    const vin=op.vinheta>0?(()=>{const r=g.createRadialGradient(W/2,H*.52,raio*.45,W/2,H*.52,raio);r.addColorStop(0,'rgba(0,0,0,0)');r.addColorStop(1,`rgba(0,0,0,${op.vinheta})`);return r;})():null;

    return function(t,forca=1){
      const f=Math.floor(t*op.q+1e-6);
      g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,W,H);
      // grão: troca a cada quadro de filme, com deslocamento sorteado
      if(T.length){const e=op.escalaGrao,ox=Math.floor(hs(f,S+3)*TAM),oy=Math.floor(hs(f,S+4)*TAM);
        g.globalAlpha=op.grao*forca;g.fillStyle=T[((f%6)+6)%6];g.setTransform(e,0,0,e,-ox*e,-oy*e);g.fillRect(0,0,W/e+TAM*2,H/e+TAM*2);g.setTransform(1,0,0,1,0,0);}
      // riscos verticais: trilhas que vivem por trechos de ~0,6 s e escorregam devagar
      for(let k=0;k<op.riscos;k++){const seg=Math.floor(t/.6+k*.37);if(hs(seg,S+10+k)>=.55)continue;
        const x=hs(seg,S+20+k)*(W-120)+60+Math.sin(t*1.3+k)*6,w=hs(seg,S+40+k)<.7?1:2;
        g.globalAlpha=(.05+.1*hs(f,S+30+k))*forca;g.fillStyle=hs(seg,S+50+k)<.75?op.claro:op.escuro;g.fillRect(x,0,w,H);}
      // poeira e fios: cada um dura um quadro de filme
      const n=Math.floor(hs(f,S+60)*(op.poeira+1));
      for(let k=0;k<n;k++){const x=hs(f,S+70+k)*W,y=hs(f,S+80+k)*H,r=1+hs(f,S+90+k)*3.2;
        g.globalAlpha=(.25+.35*hs(f,S+95+k))*forca;g.fillStyle=g.strokeStyle=hs(f,S+99+k)<.6?op.escuro:op.claro;
        if(hs(f,S+110+k)<.22){g.lineWidth=1.2;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+20*hs(f,S+120+k)-10,y+18,x+30*hs(f,S+130+k)-15,y+34*hs(f,S+140+k)+8);g.stroke();}
        else{g.beginPath();g.ellipse(x,y,r,r*(.6+.5*hs(f,S+150+k)),hs(f,S+160+k)*3,0,7);g.fill();}}
      // flicker do projetor: escurece o quadro inteiro um pouco, a 24 q/s
      if(op.flicker>0){g.globalAlpha=Math.min(1,(.025+op.flicker*Math.pow(hs(f,S+7),3))*forca);g.fillStyle='#000';g.fillRect(0,0,W,H);}
      if(vin){g.globalAlpha=Math.min(1,forca*1.2);g.fillStyle=vin;g.fillRect(0,0,W,H);}
      g.globalAlpha=1;
      // oscilação de quadro (gate weave), também em quadros de filme
      const [ax,ay]=op.weave,x=(vn(f*.35,S+11)-.5)*2*ax*forca,y=(vn(f*.35,S+12)-.5)*2*ay*forca;
      if(op.oscila){const el=op.oscila,cur=el.style.transform;if(cur!==el.__pelEscrito)el.__pelBase=cur;   // a cena mudou o transform: vira a nova base
        el.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px) ${el.__pelBase||''}`;el.__pelEscrito=el.style.transform;}
      return {x,y,f};
    };
  }
  window.PELICULA=PELICULA;
})();
