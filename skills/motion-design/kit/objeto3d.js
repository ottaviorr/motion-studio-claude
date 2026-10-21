// motion-design · objeto 3D (three.js) numa cena, com câmera e objeto como FUNÇÃO PURA DO TEMPO (técnica do Filme A e do Filme B).
// O three NÃO vem no kit (≈ 600–750 KB): copie para a pasta da cena o vendor/three-r186.js (+ three-LICENSE.txt, MIT) de um projeto
// que já tenha, ou baixe o build UMD (window.THREE). Carregue antes deste arquivo:
//   <canvas id="gl" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>
//   <script src="three-r186.js"></script><script src="objeto3d.js"></script>
// Uso:
//   const O = OBJETO3D($('gl'), {w:1080, h:1920, fov:20, exposicao:1.1});   // renderer, cena, câmera, luz de estúdio
//   O.objeto.add(new O.THREE.Mesh(geometria, new O.THREE.MeshPhysicalMaterial({color:0xC4C8CF, metalness:1, roughness:.3})));
//   const anima = O.anima({
//     camera: [[0,{az:-40, el:12, dist:7}], [1.5,{az:15, el:20, dist:5},'eo'], [3,{az:30, el:20, dist:4.6},'eio']],
//     objeto: [[0,{ry:0}], [3,{ry:360},'eio']],    // x y z (unidades do three), rx ry rz (graus), s (escala)
//   });
//   frame(t){ anima(t); }       // posiciona tudo e desenha (O.render() se você mexer em mais coisas depois)
// Chaves: [tempo, {valores}, curva] — a curva vale para o trecho que CHEGA nessa chave: 'lin' 'ei' 'eo' 'eio' 'eo5' 'back' ou função.
//   Valor que falta numa chave repete o da anterior. Câmera em órbita: az/el em graus, dist, alvo [x,y,z], yc = altura na tela (px)
//   onde o alvo aparece (setViewOffset; padrão = meio). O.chaves(t, K) serve para animar qualquer outra coisa (cor, intensidade…).
// Opções: fundo null (transparente: o canvas fica por cima do fundo HTML) ou cor · exposicao 1.05 · tom 'aces' | 'agx' | 'neutro'
//   pixelRatio (padrão devicePixelRatio: em 4K sai nítido) · estudio true (faixas de luz refletindo no metal; false = sem ambiente)
//   corEstudio (cor do chão/rebatimento do estúdio = cor do fundo da cena) · luzChave .55
// Regras (vieram dos fontes do portfólio):
//   - Nada de THREE.Clock, AnimationMixer com relógio, requestAnimationFrame ou controles: o tempo só vem de t.
//   - preserveDrawingBuffer: true (senão a captura pega o canvas vazio) — já vem ligado aqui.
//   - three r149 (build antigo): ColorManagement.legacyMode = false e outputEncoding sRGB, senão as cores hex saem lavadas/cinza.
//     r152+: ColorManagement.enabled = true e outputColorSpace = SRGBColorSpace. O helper detecta a versão e liga o certo.
//   - Versão do three: fixe UMA por projeto. Mesmo objeto/ambiente, o metal sai mais claro no r149 que no r186 (medido no recorte do objeto:
//     luma média 110 × 103, ~7 % mais claro). A unidade das luzes mudou no r155 (antes ×π) — a luz-chave já é compensada aqui; o resto é do ambiente.
//   - Fundo transparente + material com transmission: o vidro clareia (a transmissão amostra um fundo que não existe).
//     Vidro escuro e fosco: transmission 0, clearcoat 1, clearcoatRoughness ~.05, roughness ~.45 com mapa de sulcos.
//   - Metal só fica bonito com AMBIENTE (reflexo): o estúdio daqui é uma sala com faixas de luz convertida em PMREM.
//     Troque o ambiente por cor de fundo (corEstudio) quando o fundo da cena muda: o metal rebate a cor do fundo.
//   - Texto/UI por cima do objeto: projete pontos com O.proj([x,y,z]) → px da tela (para ancorar etiquetas e recortes).
(function(){
  const CL=x=>Math.max(0,Math.min(1,x));
  const CURVAS={lin:x=>x,ei:x=>x*x*x,eo:x=>1-Math.pow(1-x,3),eo5:x=>1-Math.pow(1-x,5),
    eio:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back:x=>{const s=1.6,c=s+1;return 1+c*Math.pow(x-1,3)+s*Math.pow(x-1,2);}};
  // valor de um conjunto de chaves no tempo t (número ou objeto de números)
  function chaves(t,K){
    if(!K||!K.length)return {};
    const cheio=[];let ac={};
    for(const [tk,v,c] of K){ac=typeof v==='number'?v:Object.assign({},ac,v);cheio.push([tk,ac,c]);}
    if(t<=cheio[0][0])return cheio[0][1];
    for(let i=1;i<cheio.length;i++){const [b,vb,c]=cheio[i],[a,va]=cheio[i-1];if(t>b)continue;
      const f=typeof c==='function'?c:(CURVAS[c||'eio']||CURVAS.eio),k=f(CL((t-a)/(b-a||1)));
      if(typeof vb==='number')return va+(vb-va)*k;
      const r={};for(const n in vb){const A=va[n]??vb[n],B=vb[n];r[n]=Array.isArray(B)?B.map((x,j)=>(A[j]??x)+(x-(A[j]??x))*k):A+(B-A)*k;}return r;}
    return cheio[cheio.length-1][1];
  }

  function OBJETO3D(canvas,o={}){
    const T=window.THREE;if(!T)throw new Error('OBJETO3D: carregue o three.js (window.THREE) antes');
    const op=Object.assign({w:canvas.width,h:canvas.height,fov:20,exposicao:1.05,tom:'aces',fundo:null,pixelRatio:window.devicePixelRatio||1,estudio:true,corEstudio:0x8a8c90,luzChave:.55},o);
    const rev=parseInt(T.REVISION,10);
    if(T.ColorManagement){if(rev<152&&'legacyMode' in T.ColorManagement)T.ColorManagement.legacyMode=false;else T.ColorManagement.enabled=true;}
    const R=new T.WebGLRenderer({canvas,antialias:true,alpha:op.fundo==null,preserveDrawingBuffer:true,powerPreference:'high-performance'});
    R.setPixelRatio(op.pixelRatio);R.setSize(op.w,op.h,false);
    if('outputColorSpace' in R)R.outputColorSpace=T.SRGBColorSpace;else R.outputEncoding=T.sRGBEncoding;
    R.toneMapping=op.tom==='agx'&&T.AgXToneMapping?T.AgXToneMapping:op.tom==='neutro'&&T.NeutralToneMapping?T.NeutralToneMapping:T.ACESFilmicToneMapping;
    R.toneMappingExposure=op.exposicao;
    if(op.fundo==null)R.setClearColor(0x000000,0);else R.setClearColor(op.fundo,1);
    const cena=new T.Scene(),camera=new T.PerspectiveCamera(op.fov,op.w/op.h,.05,500);
    const giro=new T.Group(),objeto=new T.Group();giro.add(objeto);cena.add(giro);
    const chave=new T.DirectionalLight(0xffffff,rev<155?op.luzChave/Math.PI:op.luzChave);   // r155+ mudou a unidade das luzes (antes ×π)
    chave.position.set(-3,6,4);cena.add(chave);

    // estúdio: sala escura com faixas de luz (é o que desenha os riscos de brilho no metal e no verniz)
    const AMB={};
    function estudio(corChao){
      const k=String(corChao);if(AMB[k])return AMB[k];
      const s=new T.Scene();
      s.add(new T.Mesh(new T.BoxGeometry(40,40,40),new T.MeshBasicMaterial({color:new T.Color(.23,.235,.25),side:T.BackSide})));
      {const ch=new T.Mesh(new T.PlaneGeometry(40,40),new T.MeshBasicMaterial({color:new T.Color(corChao).multiplyScalar(.9)}));ch.rotation.x=-Math.PI/2;ch.position.y=-7;s.add(ch);}
      const faixa=(w,h,x,y,z,rx,ry,rz,i)=>{const m=new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({color:new T.Color(i,i,i),side:T.DoubleSide}));m.position.set(x,y,z);m.rotation.set(rx,ry,rz);s.add(m);};
      faixa(3,16,-3.5,7,1,Math.PI/2,0,.35,3.2);    // faixa longa no teto
      faixa(1,16,2.6,7,-1,Math.PI/2,0,.35,3.2);    // faixa fina paralela
      faixa(14,3.2,0,2.5,10,0,0,0,3.6);            // softbox frontal (borda do metal)
      faixa(1.4,10,9,1.5,-1,0,-Math.PI/2,0,5);     // recorte direito
      faixa(1.4,10,-9,1.5,2,0,Math.PI/2,0,2.2);    // recorte esquerdo, mais fraco
      faixa(18,1.4,0,9,-8,.7,0,0,3);               // contra-luz alta
      const pm=new T.PMREMGenerator(R),tx=pm.fromScene(s,.02).texture;pm.dispose();return AMB[k]=tx;
    }
    if(op.estudio)cena.environment=estudio(op.corEstudio);

    const V=new T.Vector3(),TAN=Math.tan(op.fov/2*Math.PI/180);
    const O={THREE:T,renderer:R,cena,camera,objeto,giro,luz:chave,chaves,curvas:CURVAS,
      estudio:c=>{cena.environment=estudio(c);},
      render(){R.render(cena,camera);},
      // distância em que um objeto de raio r aparece com diâmetro px na tela
      distPara:(r,px)=>r*op.h/(TAN*px),
      // ponto do objeto (coordenadas locais) → px da tela
      proj(p){objeto.updateMatrixWorld(true);V.set(p[0],p[1],p[2]).applyMatrix4(objeto.matrixWorld).project(camera);return [(V.x+1)*op.w/2,(1-V.y)*op.h/2];},
      // câmera em órbita em volta do alvo
      poeCamera({az=0,el=10,dist=6,alvo=[0,0,0],yc=null,rolo=0}={}){
        const e=el*Math.PI/180,a=az*Math.PI/180;
        camera.position.set(alvo[0]+dist*Math.cos(e)*Math.sin(a),alvo[1]+dist*Math.sin(e),alvo[2]+dist*Math.cos(e)*Math.cos(a));
        camera.up.set(Math.sin(rolo*Math.PI/180),Math.cos(rolo*Math.PI/180),0);camera.lookAt(alvo[0],alvo[1],alvo[2]);
        if(yc!=null)camera.setViewOffset(op.w,op.h,0,op.h/2-yc,op.w,op.h);else camera.clearViewOffset();
        camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
      },
      poeObjeto({x=0,y=0,z=0,rx=0,ry=0,rz=0,s=1}={}){const d=Math.PI/180;objeto.position.set(x,y,z);objeto.rotation.set(rx*d,ry*d,rz*d);objeto.scale.setScalar(s);objeto.updateMatrixWorld(true);},
      anima(K){return t=>{O.poeCamera(chaves(t,K.camera));O.poeObjeto(chaves(t,K.objeto));if(K.extra)K.extra(t,O);O.render();};},
    };
    O.poeCamera();
    return O;
  }
  window.OBJETO3D=OBJETO3D;
})();
