// motion-design · ritmo: a cena é escrita em BATIDAS, não em segundos. Trocou a música (ou o BPM), a cena se reescala sozinha.
// Uso (antes do script da cena):
//   <script src="ritmo.js"></script>
//   <script>RITMO({bpm:121, batida0:0.244, batidaInicial:11, batidas:40});</script>
//   bpm, batida0 = saída do kit/batidas.py (BPM e 1ª batida da faixa, em s) · batidaInicial = batida da FAIXA onde o vídeo começa
//   (escolha um tempo forte: o "1" do compasso) · batidas = duração do vídeo em batidas · porCompasso = 4 (padrão).
// Depois, na cena:
//   bt(n)          segundo da batida n do vídeo (bt(0) = 0 s; aceita fração: bt(2.5) = meio da 3ª batida)
//   br(n)          segundo do compasso n (br(1) = bt(4) em 4/4)
//   BT, BR         duração de uma batida e de um compasso (s)
//   batida(t)      em que batida o tempo t está (número com fração) → pl = PLANOS.find(p => v >= p.a && v < p.b)
//   pulso(t, lista, d=.25)  1 na batida e cai até 0 em d batidas (bumbo, tremor, flash); lista = [0,4,8] ou n
//   window.DUR     já vem pronto (batidas × BT) · window.MUSICA.inicio = segundo da faixa em que o vídeo começa
//                  (cortar a música: ffmpeg -ss MUSICA.inicio …; o kit/som.py aceita os mesmos bpm/âncora)
// Regra que veio do Filme A: meça a grade fina no TRECHO usado (o BPM global da faixa escorregou ~130 ms até o drop).
// O corte acontece no meio do movimento (pico de velocidade na batida), não depois dele.
(function(){
  function RITMO(o){
    const bpm=o.bpm||120, pc=o.porCompasso||4, BT=60/bpm, BR=BT*pc;
    const b0=o.batida0||0, bi=o.batidaInicial||0;
    window.BPM=bpm; window.BT=BT; window.BR=BR;
    window.bt=n=>n*BT;
    window.br=n=>n*BR;
    window.batida=t=>t/BT;
    window.pulso=(t,lista,d=.25)=>{const v=t/BT;let m=0;for(const n of [].concat(lista)){const k=(v-n)/d;if(k>=0&&k<1)m=Math.max(m,1-k);}return m;};
    window.MUSICA=Object.assign({},window.MUSICA,{arquivo:o.arquivo,batida0:b0,batidaInicial:bi,inicio:b0+bi*BT});
    if(o.batidas)window.DUR=o.batidas*BT;
    return {BPM:bpm,BT,BR,inicio:b0+bi*BT,DUR:window.DUR};
  }
  window.RITMO=RITMO;
})();
