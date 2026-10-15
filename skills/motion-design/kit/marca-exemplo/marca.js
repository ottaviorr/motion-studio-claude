// Marca do projeto — copie para a pasta fonte do vídeo e troque. LOGO(h) usa estes dados.
window.MARCA={
  nome:'Sua Marca',
  // SVG em texto (cores próprias) ou caminho de imagem ('logo.svg'/'logo.png' na pasta fonte)
  logo:'<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#4f46e5"/><path d="M12 26l8-12 8 12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  moeda:'BRL', locale:'pt-BR',
  site:'suamarca.com.br',
  // regras de texto da marca (preços, palavras proibidas, nomes de clientes de exemplo) — leia antes de escrever cena
  regras:['Números e preços só os oficiais','Nomes de clientes nas telas são sempre inventados'],
};

// ---------- tempo pela voz real (tempos.js, gerado por kit/gerar-plano.py) ----------
// o número da cena vem do <title> ("05 marca"); lido na hora do uso, porque este arquivo carrega antes do <title>
const CENA_=()=>document.title.slice(0,2);
const dur=x=>{const p=(window.PLANO||{})[CENA_()];return p?+(p.out-p.in).toFixed(3):x;};
// W('domínio') = segundo (no clipe) em que a palavra é falada; k = qual ocorrência (0 = a primeira).
// Compara sem acento, sem pontuação e pelo começo da palavra. Sem voz, cai em 'reserva' (ou 0).
const norm_=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9$]/g,'');
// Procura primeiro a palavra exata; se não houver, a que começa com o texto.
const W=(s,k=0,reserva=0)=>{const L=(window.PALAVRAS||{})[CENA_()]||[];const q=norm_(s);
  for(const igual of [true,false]){let n=0;for(const [w,t] of L){const x=norm_(w);if(x&&(igual?x===q:x.startsWith(q))){if(n===k)return t;n++;}}}
  console.warn('palavra não achada',CENA_(),s);return reserva;};
// fim da fala da cena (última palavra)
const FALA_FIM=()=>{const L=(window.PALAVRAS||{})[CENA_()]||[];return L.length?L[L.length-1][1]+.5:0;};
