export const meta = {
  name: 'serie-de-videos',
  description: 'Produz N peças de uma série em paralelo (cenas por grupo), grava e monta em fila (trava global), revisa cada peça com um revisor independente e corrige até 2 voltas',
  whenToUse: 'Depois dos portões P1 (roteiro), P2 (direção de arte) e P3 (piloto) aprovados, com base/, vozes e ESTILOS.md congelados',
  phases: [
    { title: 'Produção', detail: 'um agente por grupo de 2-3 peças: cenas, folha de conferência, gravação em fila' },
    { title: 'Montagem', detail: 'gerar_reel.py + revisar.py, uma peça por vez (mesma trava)' },
    { title: 'Revisão', detail: 'revisor independente por peça, só leitura, veredito com evidência' },
    { title: 'Correção', detail: 'volta ao produtor com as falhas; no máximo 2 voltas' },
  ],
}

// ---------------------------------------------------------------------------
// MODELO do orquestrador-video. Baseado no script real dos 15 reels do cliente A
// (cliente-a-reels-cenas), com o que faltou nele: trava GLOBAL de gravação (lá cada
// agente gravava "um por vez", mas 5 agentes = 5 gravações juntas), scratchpad
// por prefixo, nomes exatos, montagem e revisão independente dentro do fluxo.
//
// Chame com args (objeto JSON de verdade, não string):
// {
//   "projeto": "~/motion-studio/projetos/<projeto>",
//   "nome": "cliente A CRM · 15 reels",
//   "scratch": "<scratchpad da sessão>",
//   "piloto": "r01a-ferramentas",                       // em base/, padrão de código e qualidade
//   "marcaJs": "~/motion-studio/marcas/<marca>/marca.js",
//   "regras": "nunca citar GoHighLevel; só dados inventados; nenhum número de resultado inventado",
//   "formato": { "w": 1080, "h": 1920, "fps": 30, "bitrate": "20M", "lufs": -14,   // padrão do dono: 1080p30 CBR alto
//                "zona": "y 230-1300 e x < 900 (coluna de botões à direita)" },
//   "pastaFinais": "reels",                             // onde gerar_reel.py escreve reel-NN.mp4
//   "grupos": [["02","03","04"],["05","06","07"],["08","09","10"],["11","12","13"],["14","15"]],
//   "pecas": { "02": { "missao": "o líd das 23h: quem responde primeiro leva", "vizinhas": "01, 03" }, ... },
//   "montar": true                                      // false = só cenas (monta você depois)
// }
// Retomar depois de queda/edição: Workflow({scriptPath, resumeFromRunId}) — o
// que já terminou volta do cache; por isso cada agente também confere o que já
// existe no disco antes de refazer (idempotente).
// ---------------------------------------------------------------------------

const A = args || {}
if (!A.projeto || !A.grupos || !A.pecas || !A.scratch) throw new Error('args precisa de projeto, scratch, grupos e pecas')
const P = A.projeto
// padrão do dono (15/10/2026): 1080p, 30 qps, bitrate alto em CBR; 4K ou 60 qps só se ele pedir para a peça
const F = A.formato || { w: 1080, h: 1920, fps: 30, bitrate: '20M', lufs: -14, zona: 'y 230-1300 e x < 900' }
// caminhos num lugar só (o Workflow roda sem variáveis de ambiente; ideia da cópia de um colaborador)
const HOME = process.env.HOME || '~'
const ESTUDIO = HOME + '/motion-studio'
const SKILLS = HOME + '/.claude/skills'
const K = SKILLS + '/motion-design'
const HFD = HOME + '/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/.claude/skills'
const PY = ESTUDIO + '/.ferramentas/.venv/bin/python'
const FINAIS = A.pastaFinais || 'reels'
const MAX_VOLTAS = 2
const todas = A.grupos.flat()

// Trava global: mkdir é atômico; vale para TODOS os agentes do computador.
const TRAVA = `L=${P}/.fila-render; until mkdir "$L" 2>/dev/null; do sleep 5; done; trap "rmdir $L" EXIT`
const regraFila = `GRAVAÇÃO/MONTAGEM EM FILA (uma por vez no computador inteiro). Todo comando pesado (hf.mjs, gravar.mjs, gerar_reel.py, revisar.py) roda assim, num bash só:
  bash -c '${TRAVA}; <comando>'
Nunca apague ${P}/.fila-render na mão; se parecer presa por mais de 20 min sem hyperframes/chrome/remotion rodando (pgrep -fl 'hyperframes|remotion|chrome'), relate em vez de apagar.`

// ---------- schemas ----------
const PRODUCAO = {
  type: 'object',
  properties: {
    pecas: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          arquivos: { type: 'array', items: { type: 'string' } },
          duracoes: { type: 'string', description: 'duração de cada cena gravada' },
          folha: { type: 'string', description: 'caminho da folha de conferência que você OLHOU' },
          corrigido: { type: 'string', description: 'o que corrigiu depois de olhar a folha' },
          problemas: { type: 'string' },
          pedidos_ao_diretor: { type: 'string' },
          licao: { type: 'string' },
        },
        required: ['id', 'arquivos', 'folha'],
      },
    },
  },
  required: ['pecas'],
}
const MONTAGEM = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    final: { type: 'string' },
    revisao: { type: 'string', description: 'caminho do revisao.txt' },
    duracao_s: { type: 'number' },
    lufs: { type: 'number' },
    pico_dbfs: { type: 'number' },
    bitrate_mbps: { type: 'number' },
    ok: { type: 'boolean' },
    erro: { type: 'string' },
  },
  required: ['id', 'ok'],
}
const VEREDITO = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    aprovado: { type: 'boolean' },
    medidas: { type: 'string', description: 'LUFS, pico, voz-música, bitrate, resolução/fps, duração' },
    falhas: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          item: { type: 'string' },
          evidencia: { type: 'string', description: 'número, tempo ou foto' },
          correcao: { type: 'string' },
          arquivo: { type: 'string' },
        },
        required: ['item', 'evidencia', 'correcao'],
      },
    },
  },
  required: ['id', 'aprovado', 'falhas'],
}

// ---------- prompts ----------
const nomes = (n) => `Em ${P}/base/: r${n}-estilo.css, r${n}a-<nome-curto>.html (principal; se dividir: r${n}a1-, r${n}a2-…), r${n}b-fecho.html. Em ${P}/cenas/: os .mp4 com o MESMO nome das cenas. Em ${P}/reels/: ${n}.json (escreva num temporário em ${A.scratch}/r${n}/ e mova com mv — o gerador lê todos os JSON).`

const promptProducao = (g) => `Você vai produzir as CENAS das peças ${g.join(', ')} de ${A.nome} (${F.w}×${F.h}, ${F.fps} fps). Projeto: ${P}. Outros agentes fazem outras peças AO MESMO TEMPO na mesma pasta.

1. MISSÃO
${g.map(n => `- ${n}: ${(A.pecas[n] || {}).missao || 'ver ROTEIROS.md'}`).join('\n')}

2. LEIA ANTES: ${K}/SKILL.md, ${K}/reference/nivel.md, ${K}/reference/armadilhas.md, ${K}/reference/inspiracao.md; ${HFD}/motion-doctrine/SKILL.md e ${HFD}/cut-the-curve/SKILL.md; ${P}/BRIEFING.md (se existir); ${P}/ESTILOS.md SÓ as seções ${g.join(', ')} + regras gerais + ajustes do dono; ${P}/VOZES.md; ${P}/base/vozes-palavras.js; ${P}/base/LEIA-ME-KIT.md (se existir); o piloto aprovado ${P}/base/${A.piloto}.html; regras da marca ${A.marcaJs} (${A.regras}). Confira as suas folhas também com a skill hierarquia-visual, se estiver instalada.

3. ARQUIVOS QUE VOCÊ CRIA (nomes EXATOS, nada além):
${g.map(nomes).join('\n')}

4. NÃO TOQUE: kit e marca (comum.*, marca.*, *-ui.*, fontes/), ESTILOS.md, VOZES.md, BRIEFING.md, vozes-palavras.js, arquivos de outras peças, remotion/, git. Precisa mudar algo comum? Descreva em pedidos_ao_diretor. NÃO rode gerar_reel.py nem o Remotion.

5. RASCUNHO só em ${A.scratch}/r<NN>/ (uma pasta por peça sua). Nunca na raiz do scratchpad.

6. ${regraFila}
Gravar uma cena: bash -c '${TRAVA}; cd ${P}/base && node ${K}/kit/hf.mjs ../cenas/<cena>.mp4 --html <cena>.html --crf 12'

7. PADRÃO DO PILOTO: fontes LOCAIS (base/fontes/ + @font-face + elemento escondido com cada peso antes do quadro 0 — Google Fonts falhou em foto); zona segura ${F.zona}; gancho visível no quadro 0; DUR da principal = voz + 0,3 s; toda troca numa palavra com W('palavra', k): palavra curta ou repetida pede o índice k da ocorrência certa ou a palavra seguinte, mais rara. Sem legenda corrida. Uma direção de movimento por peça; nada de partícula/glitch/quique. NN.json com "bitrate":"${F.bitrate}", voz em 0, música da seção do ESTILOS.md (o gerador mede e põe ~21 dB abaixo da voz), sfx discretos.

8. IDEMPOTENTE: se um arquivo seu já existe e está certo (de uma rodada anterior), não refaça; confira e siga.

9. CONFERÊNCIA ANTES DE DEVOLVER: FOTOS_DIR=${A.scratch}/r<NN>/fotos GRAVAR=${K}/kit/gravar.mjs bash fotos.sh <cena>.html <≥12 tempos, incluindo cada palavra-chave> (de dentro de base/), folha em pé com a zona segura, e OLHE: ilegível, sobreposto, fora da zona, fonte genérica, texto que contradiz a voz, marca proibida → corrija e fotografe de novo. Depois de gravar: ffprobe (duração/resolução/fps) e um quadro a ~75 % de cada MP4.

10. PRONTO = existem no disco as cenas .mp4 e o reels/NN.json de cada peça sua. Responda pelo schema.`

const promptMontagem = (n) => `Monte e meça a peça ${n} de ${A.nome}. Projeto: ${P}. Você só monta e mede; não edite cenas nem JSON.
${regraFila}
1. Confira que ${P}/reels/${n}.json existe e que cada arquivo de "cenas" existe. Faltou algo → ok=false, erro com o que falta.
2. Num único bash com a trava: bash -c '${TRAVA}; cd ${ESTUDIO} && ${PY} ${K}/kit/gerar_reel.py ${P} --render ${n} && ${PY} ${SKILLS}/revisao-video/scripts/revisar.py ${P}/${FINAIS}/reel-${n}.mp4 --fotos 12'
   (se o nome do final for outro, use o que o gerar_reel.py imprimir).
3. Leia o revisao.txt e devolva pelo schema: final, revisao, duração, LUFS, pico, bitrate medido. ok=false se LUFS fora de ${F.lufs}±1, pico > -1 dBFS ou bitrate < ${parseInt(F.bitrate, 10) * 0.9} Mb/s.`

const promptRevisao = (n, m) => `Você é o REVISOR INDEPENDENTE da peça ${n} de ${A.nome}. Você não fez a peça e NÃO edita nada do projeto: leia, meça e dê o veredito com evidência.
Final: ${m && m.final ? m.final : `${P}/${FINAIS}/reel-${n}.mp4`}. Relatório técnico: ${m && m.revisao ? m.revisao : '(não veio: rode revisar.py com saída no seu rascunho)'}.
Rascunho só em ${A.scratch}/qa-${n}/. Comando pesado (revisar.py, ffmpeg em vídeo inteiro) só com a trava: bash -c '${TRAVA}; <comando>'.
Leia: ${SKILLS}/revisao-video/SKILL.md, a skill hierarquia-visual (se instalada), ${P}/BRIEFING.md, a seção ${n} de ESTILOS.md e de VOZES.md, ${A.marcaJs}.
Meça cada item, com número/tempo/foto:
1 Fala: transcrição × VOZES.md (voz inteira; diferença perto de emenda → recorte 6 s e transcreva antes de acusar).
2 Mixagem: LUFS ${F.lufs}±1, pico ≤ -1 dBFS, voz − música ~18–21 dB (meça um trecho com voz e o fecho só com música, ffmpeg ebur128 com -ss/-t).
3 Imagem: ${F.w}×${F.h}, ${F.fps} fps, bitrate medido ≥ ${F.bitrate}, quadro 0 não preto.
4 Sincronia: cada título/troca do roteiro × tempo da palavra em vozes-palavras.js (tolerância 0,3 s) — atenção a W() de palavra curta/repetida.
5 Fontes: as do cartão aparecem nas fotos (serif genérica = falha).
6 Hierarquia e legibilidade na folha de 12 fotos: uma leitura por tela, título ≥ 84 px, ≤ 3–4 palavras, contraste.
7 Zona segura (${F.zona}), gancho no quadro 0, fecho com a isca certa.
8 Marca: ${A.regras}.
9 Direção de arte bate com o cartão; não repete a vizinha (${(A.pecas[n] || {}).vizinhas || 'peças adjacentes'}).
aprovado=true só se nada falhar. Cada falha: item, evidência, correção sugerida, arquivo.`

const promptCorrecao = (n, falhas) => `A peça ${n} de ${A.nome} foi REPROVADA pelo revisor independente. Projeto: ${P}. Corrija SÓ isto:
${falhas.map((f, i) => `${i + 1}. [${f.item}] ${f.evidencia} → ${f.correcao}${f.arquivo ? ` (${f.arquivo})` : ''}`).join('\n')}
Limites: só os arquivos da peça ${n} (${nomes(n)}); rascunho em ${A.scratch}/r${n}/; nada compartilhado.
${regraFila}
Regrave só as cenas afetadas (bash -c '${TRAVA}; cd ${P}/base && node ${K}/kit/hf.mjs ../cenas/<cena>.mp4 --html <cena>.html --crf 12'), fotografe e OLHE de novo. Não monte (a montagem roda depois). Responda pelo schema com uma peça só (id ${n}) e diga em "corrigido" o que mudou e como conferiu cada falha.`

// ---------- fluxo ----------
async function montar(n) {
  if (A.montar === false) return null
  return agent(promptMontagem(n), { label: `montagem ${n}`, phase: 'Montagem', schema: MONTAGEM, effort: 'low' })
}

async function revisarECorrigir(n, m0) {
  let m = m0
  for (let volta = 0; volta <= MAX_VOLTAS; volta++) {
    const v = await agent(promptRevisao(n, m), { label: `revisão ${n}${volta ? ' (volta ' + volta + ')' : ''}`, phase: 'Revisão', schema: VEREDITO })
    if (!v) return { id: n, aprovado: false, voltas: volta, falhas: [{ item: 'revisor', evidencia: 'agente não respondeu', correcao: 'revisar à mão' }] }
    if (v.aprovado) return { ...v, voltas: volta }
    if (volta === MAX_VOLTAS) { log(`peça ${n}: reprovada depois de ${MAX_VOLTAS} voltas, vai para o diretor`); return { ...v, voltas: volta } }
    log(`peça ${n}: ${v.falhas.length} falha(s), volta ${volta + 1}`)
    await agent(promptCorrecao(n, v.falhas), { label: `correção ${n}`, phase: 'Correção', schema: PRODUCAO })
    m = await montar(n)
  }
}

// pipeline: um grupo pode estar em revisão enquanto outro ainda produz (sem barreira).
// A trava global serializa só o que pesa (gravar/montar/medir); o resto corre junto.
const resultado = await pipeline(
  A.grupos,
  (g) => agent(promptProducao(g), { label: 'cenas ' + g.join('+'), phase: 'Produção', schema: PRODUCAO }),
  async (prod, g) => {
    const feitas = new Set(((prod && prod.pecas) || []).map(p => p.id))
    const faltam = g.filter(n => !feitas.has(n))
    if (faltam.length) log(`grupo ${g.join('+')}: sem relatório para ${faltam.join(', ')} (o montador confere o disco)`)
    const out = []
    for (const n of g) out.push({ n, m: await montar(n) })          // em série dentro do grupo; a trava cuida dos outros grupos
    return { prod, out }
  },
  async (r) => Promise.all(r.out.map(({ n, m }) => revisarECorrigir(n, m).then(v => ({ id: n, montagem: m, veredito: v, producao: ((r.prod && r.prod.pecas) || []).find(p => p.id === n) || null })))),
)

const linhas = resultado.filter(Boolean).flat()
const reprovadas = linhas.filter(l => !l.veredito || !l.veredito.aprovado).map(l => l.id)
const semResultado = todas.filter(n => !linhas.find(l => l.id === n))
log(`aprovadas: ${linhas.length - reprovadas.length}/${todas.length}` + (reprovadas.length ? ` · reprovadas: ${reprovadas.join(', ')}` : '') + (semResultado.length ? ` · sem resultado: ${semResultado.join(', ')}` : ''))
return {
  aprovadas: linhas.filter(l => l.veredito && l.veredito.aprovado).map(l => l.id),
  reprovadas,
  semResultado,
  pedidosAoDiretor: linhas.map(l => l.producao && l.producao.pedidos_ao_diretor ? `${l.id}: ${l.producao.pedidos_ao_diretor}` : null).filter(Boolean),
  licoes: linhas.map(l => l.producao && l.producao.licao ? `${l.id}: ${l.producao.licao}` : null).filter(Boolean),
  pecas: linhas,
}
