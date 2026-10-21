# 05 — Som de micro-interação e kit de overlays por cima da gravação

Estudo de 16/10/2026. Base lida antes de escrever: `edicao-video/remotion/` (package.json 4.0.534, `src/componentes.tsx`), `scripts/gerar_remotion.py`, `references/montagem-remotion.md`, `references/som.md`, `motion-design/kit/som.py`, `aprendizado/ferramentas.md` e `pesquisa/<estudo>/02-anotacoes-na-tela.md` (que já propôs `"anotacoes"` no `edicao.json` e o `vista.json`; este estudo aproveita as duas ideias). Nada foi instalado nem editado fora desta pasta. As funções novas do `som.py` (seção 4) rodaram num rascunho fora do repositório, e os níveis da seção 2 foram medidos nesse teste.

---

## 1. Resumo em 5 linhas

1. **Som de overlay é tempero.** Fica 12–18 dB abaixo da voz, dura 30–300 ms (a notificação pode chegar a ~500 ms de corpo), toca **só na entrada** e no **instante do contato** (não no começo do movimento). Na aula, no máximo ~4 por minuto, e **nenhum durante explicação técnica** (Moreno & Mayer 2000: som extra piorou a transferência).
2. **Sintetizar é o caminho principal.** O `som.py` ganha 6 tipos (`pop`, `tick_ui`, `notificacao`, `swoosh`, `marca`, `recolhe`), cada um com variação de afinação por semente (o mesmo pop 20 vezes não soa igual 20 vezes), e um modo `--um` que exporta um arquivo por som para o Remotion. Para comparar, já existem no disco 21 SFX da Pixabay que vêm com o HyperFrames, e há bibliotecas CC0 boas (Kenney UI Audio, freesound filtrado em CC0, Sonniss GDC).
3. **Cuidado com o `@remotion/sfx`.** O pacote é MIT, mas cada arquivo tem a licença dele. `whoosh`, `mouse-click`, `ui-switch`, `page-turn`, `whip` e `shutter-modern` são CC0. **`ding`, `snapchat-notification` e os "memes" não têm licença livre e nunca entram.**
4. **Componentes prontos e abertos:** o registro do HyperFrames está inteiro no disco (400 itens, Apache-2.0; uns 45 servem para overlay: notificação, lower third, círculo/seta/sublinhado à mão, holofote, cursor, chip de estado). Do lado do Remotion: Remotion Elements (oficial), Onda e RemotionUI (MIT, copiam o .tsx para o projeto) e reactvideoeditor/remotion-templates (MIT). Uso como **referência para portar**, não como dependência.
5. **Arquitetura:** a biblioteca mora em `edicao-video/remotion/src/overlays/`, com um `<Overlay>` base (envelope de entrada, repouso e saída; posição que foge da câmera; tema da marca), um `registro.json` (fonte única que o TSX e o Python leem: tempos, ponto de contato, som padrão) e um `"overlays"` no `edicao.json`. O `gerar_remotion.py` escreve um nó `<Sequence>` por overlay e um por som, e uma composição `Galeria` testa tudo (folha com 3 tempos por overlay e medição de nível e sincronia do som).

---

## 2. Regras de som de UI (com números e fontes)

### 2.1 Nível em relação à voz

| Elemento | Regra | De onde vem |
|---|---|---|
| Voz | -14 LUFS integrado, pico ≤ -1 dBTP | padrão de entrega do estúdio |
| Trilha sob a voz | 25 dB abaixo (faixa 22–28) | `edicao-video/references/som.md` (o dono aprovou 25 dB e reprovou 18 dB) |
| Whoosh de transição | 15–20 dB abaixo | `som.md` atual |
| **SFX de overlay (pop, swoosh, notificação)** | **12–18 dB abaixo da voz**, medido no **M máx (janela de 400 ms)** só do efeito. Com a voz em -14 LUFS, o alvo é **M máx entre -26 e -32 LUFS** | guias de mixagem de fala: vinhetas e efeitos 10–15 dB abaixo da fala ([busca](https://www.sageaudio.com/articles/mastering-dialogue-for-podcasts)); o HyperFrames usa SFX a volume 0,35 e trilha a 0,12 (≈ -18 dB) "por baixo da narração" (`media-use/audio/references/sfx.md` e `bgm.md`). Proposta nossa: mais baixo que o 0,35 deles, porque aula não é anúncio |
| Tiques em sequência (lista, contador) | 18–24 dB abaixo, cada tique seguinte ×0,85 | proposta nossa (repetição cansa: ver 2.3) |

**Calibração medida** (rascunho do estudo: cada efeito sozinho, `ebur128`, M máx):

| Tipo | M máx com g = 0,30 | **g sugerido** | M máx resultante (≈ dB abaixo da voz a -14) |
|---|---|---|---|
| `pop` | -26,9 LUFS | **0,25** | -28,5 (≈ 14,5 dB) |
| `tick_ui` | -32,6 | **0,30** (sozinho) / 0,18 (em fila) | -32,6 / -37 |
| `notificacao` | -19,8 | **0,12** | -27,8 (≈ 14 dB) |
| `swoosh` | -23,8 | **0,18** | -28,2 (≈ 14 dB) |
| `marca` (caneta) | -20,1 | **0,12** | -28,1 (≈ 14 dB) |
| `clique` (já existe) | -30,4 | 0,30 | -30,4 |
| `whoosh` (já existe) | -21,7 | 0,16 | -27,1 |

O M de 400 ms subestima um som de 35 ms (o ouvido "integra" menos). Por isso o `tick_ui` pode ficar mais baixo no medidor e ainda assim ser ouvido. Depois de montar, a revisão confere de ouvido em dois trechos.

### 2.2 Duração, ataque e sincronia

- **Clique e tap: 10–80 ms. Toggle: 80–200 ms. Sucesso: 200–500 ms. A maioria dos sons de UI fica abaixo de 300 ms** ([ui-sound-design skill](https://skillselion.com/skills/dannyjpwilliams/ui-sound-design-skill/ui-sound-design); [Violet Recording](https://violetrecording.com/how-to-design-ui-sounds/)). Notificação com corpo de até ~500 ms e cauda curta.
- **Nossa tabela:** pop 90 ms · tick_ui 35 ms · swoosh 200 ms · marca 350 ms (3 riscos) · notificação 2 notas em 85 ms, corpo de ~500 ms e cauda de sala de 0,6 s.
- **Sincronia = instante do contato.** O registro do HyperFrames faz assim: o `native-notification-pop` dispara o evento `hf:sfx` "no primeiro contato com o repouso" (+0,31 s depois do início da queda), e não quando o banner começa a cair. Regra nossa:
  - pop e notificação: ataque no **primeiro quadro em que a escala ou a posição chega a 1** (o "pouso");
  - swoosh: **pico na velocidade máxima** do deslize (como o whoosh atual: pico no corte);
  - marca: começa junto com o traço e dura o traço;
  - tolerância ±1 quadro (33 ms), medida na Galeria (seção 6.6).
- **Saída é muda** por padrão. O olho já está indo embora, e som na saída dobra a contagem de sons.

### 2.3 Frequência (não cansar)

- **Restrição é a regra:** "os melhores cliques são quase imperceptíveis"; som decorativo frequente cansa ([Violet Recording](https://violetrecording.com/how-to-design-ui-sounds/); [IRPR — UI sounds annoying](https://sounddesign.irpr.agency/solutions/ui-sounds-annoying/)).
- **Varie o mesmo som:** som tocado muitas vezes deve variar para evitar a fadiga de repetição ([userinterface wiki](https://tessl.io/registry/skills/github/gsd-build/gsd-2/userinterface-wiki)). No `som.py`, isso vira afinação ±3–4 % por semente, com 4 variações por tipo (`pop-1…pop-4.wav`) usadas em rodízio.
- **Espectro:** nada de grave abaixo de ~250 Hz nos sons de UI (o "sub" é do impacto e do fechamento) e nenhum pico áspero entre 2 e 5 kHz, a faixa que cansa e briga com a inteligibilidade da voz (1–4 kHz). O `pop` tem o corpo em 500–1100 Hz e o `tick_ui` em 1,9 kHz, mas só por 35 ms.
- **Orçamento por peça (proposta nossa, para o gerador avisar):**
  - **aula/tutorial:** ≤ 4 sons de overlay por minuto e nunca 2 em menos de 1,2 s, exceto os tiques de uma mesma lista;
  - **YouTube de canal:** ≤ 6/min;
  - **anúncio/VSL:** livre, desde que a voz continue ganhando.
- **Contexto:** a "edição de retenção" (som em tudo) está cansando o público, e para quem tem 25 anos ou mais o excesso de edição **diminui** a retenção ([YPulse 2024](https://www.ypulse.com/newsfeed/2024/04/02/young-people-are-getting-tired-of-retention-editing-on-youtube/); [Finchley](https://www.finchley.co.uk/finchley-learning/youtube-growth-strategy-retaining-viewers-with-sound-effects-for-video-editing)). O pop "pequeno, redondo, quase sem cauda" a cada callout deixa a edição "intencional, não ocupada", mas só em callout que importa.

### 2.4 Quando NÃO usar

1. **Durante explicação técnica** (passo a passo de configuração, campo a campo). No experimento de Moreno & Mayer (2000), sons adicionados a uma explicação narrada pioraram retenção e transferência (no Exp. 2, freio hidráulico), porque sobrecarregam a memória de trabalho auditiva ([PDF](https://tecfa.unige.ch/tecfa/teaching/methodo/Moreno_Mayer00.pdf)). No `edicao.json`, esses trechos vão como `"sem_sfx": [[ini, fim]]` e o gerador corta os sons que caírem ali (o overlay continua, sem som).
2. **Ênfase de texto na palavra que a voz está dizendo.** A voz já marca o tempo, então essa ênfase fica muda.
3. **Clique que já tem som na gravação** e clique comum de tela (regra atual do `som.md`).
4. **Em cima de outro som:** menos de 1,2 s depois de um whoosh de transição, de um impacto ou do pico da trilha.
5. **Na saída** de qualquer overlay.
6. **Imitação de som de marca** (o "ding" do iPhone, o Slack, a notificação do Snapchat): além da licença, confunde o espectador ("chegou mensagem no MEU celular?"). A nossa notificação usa duas notas de marimba numa quarta justa, sem copiar sistema nenhum.

---

## 3. Bibliotecas de SFX gratuitas

| Biblioteca | Link | Licença | Atribuição | O que pegar | Observação |
|---|---|---|---|---|---|
| **Sintetizado (`som.py`)** | `~/.claude/skills/motion-design/kit/som.py` | nosso | — | **tudo o que der**: pop, tick, notificação, swoosh, marca, clique | determinístico, sem risco de Content ID, varia por semente |
| **HyperFrames media-use (já no disco)** | `.ferramentas/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/` | Pixabay Content License (CREDITS.md) | não | `pop`, `click-soft`, `ping`, `notification`, `chime`, `whoosh-short`, `key-press`, `typing`, `sparkle` (21 arquivos, `manifest.json` com duração e uso) | bom para comparar A/B com o sintetizado sem baixar nada |
| **Kenney UI Audio** | [kenney.nl/assets/ui-audio](https://kenney.nl/assets/ui-audio) | **CC0** | não | 50 cliques, switches e toggles curtos | o `ui-switch` do Remotion é um destes ("Switch 35"). A Kenney tem outros pacotes de interface também CC0 (conferir cada página) |
| **freesound (filtro CC0)** | [freesound.org](https://freesound.org/help/faq/) | CC0 / CC BY / CC BY-NC (por arquivo) | CC BY: sim; **BY-NC: não pode** (cliente é comercial) | foley real: caneta no papel, marcador, clique de teclado | filtrar **só CC0**; o `whoosh`, o `mouse-click` e o `whip` do Remotion vêm daqui |
| **Mixkit SFX** | [mixkit.co/free-sound-effects](https://mixkit.co/free-sound-effects/) | Mixkit Sound Effects Free License | não (apreciada) | "pop", "interface", "notification", "swoosh" | YouTube, anúncio e cliente ok; não pode revender o arquivo sozinho. Já usamos Mixkit na trilha da aula SLA |
| **Pixabay SFX** | [pixabay.com/sound-effects](https://pixabay.com/sound-effects/) | Pixabay Content License | não | idem | proíbe distribuir o arquivo sozinho e usar com marca de terceiro. Guarde o link da página de cada arquivo (prova em caso de reivindicação) |
| **Sonniss GDC Game Audio Bundle** | [sonniss.com/gameaudiogdc](https://sonniss.com/gameaudiogdc) | royalty-free, uso comercial ilimitado | não | pacotes de "UI", "foley de papel", "whoosh" profissionais (2026: 7,47 GB; arquivo de 10 anos com mais de 200 GB) | **proíbe treinar IA** com os arquivos (não fazemos isso). Baixar só a pasta de UI/foley |
| **Zapsplat (grátis)** | [zapsplat.com](https://www.zapsplat.com/) | Standard License | **sim, obrigatória** ("Sound effects from zapsplat.com") | — | **evitar**: obriga crédito na descrição, e o Gold (pago) é que tira |
| **@remotion/sfx** | [remotion.dev/docs/sfx](https://www.remotion.dev/docs/sfx) | pacote MIT; **licença por arquivo** | depende | **só os CC0:** `whoosh` (0,154 s), `mouse-click`, `ui-switch` (Kenney), `page-turn` (Kenney), `whip`, `shutter-modern` | **`ding`, `snapchat-notification`, `vine-boom`, `bruh` e os outros memes vêm do myinstants e "não têm licença livre"** (palavras da própria doc): nunca. O gerador atual baixa só o `whoosh.wav` (CC0), então está certo |

**Regra de arquivo:** tudo que não for sintetizado entra em `~/.claude/skills/edicao-video/sfx/` com uma linha em `sfx/LICENCAS.md` (arquivo, origem, link da página, licença, data), igual ao `musica/LICENCAS.md` da trilha.

---

## 4. O que acrescentar ao `som.py`

O `som.py` já tem `tick` (moeda, 3,2 kHz), `tique` (relógio), `clique`, `tap`, `bip`, `acento`, `whoosh` e `sopro`. Faltam os sons "de interface por cima da tela": **pop** de entrada, **tique de UI** mais grave e curto, **notificação** própria, **swoosh curto** de card, **marca** de caneta e **recolhe** (opcional). Também faltam a **variação por semente** e um modo que exporta **um arquivo por som** para o Remotion.

Testado no rascunho (importando o `som.py` como está): tudo roda com numpy, e as durações saíram assim: pop 90 ms, tick_ui 35 ms, swoosh 200 ms (pico em 110 ms), marca 350 ms, notificação ~1,2 s com cauda.

```python
# ---------- micro-interação (overlays por cima da tela) ----------
def _varia(r, var):
    """fator de afinação aleatório ±var (semente do evento): o mesmo som 20× não soa igual 20×"""
    return 1 + var * (2 * r.random() - 1)

def pop(r, f=520, dur=.09, queda=2.2, var=.04):
    """pop de bolha (pop-up/card que POUSA): seno que despenca de f×queda para f em ~25 ms + 'boca' de ruído curtinho"""
    k = _varia(r, var); n = int(dur * SR); t = np.arange(n) / SR
    fr = f * k * (1 + (queda - 1) * np.exp(-t / .006))
    corpo = seno_var(fr) * env(n, .0015, .022)
    boca = lp(hp(r.standard_normal(n), 900), 4000) * env(n, .0003, .004) * .25
    return norm(corpo + boca), 0

def tick_ui(r, f=1900, var=.03, dur=.035):
    """tique de interface (item de lista, número que troca): mais grave e mais curto que o `tick` (moeda), cansa menos"""
    k = _varia(r, var); n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * k * t) * np.exp(-t / .0035) + .3 * np.sin(2 * np.pi * f * k * 2.02 * t) * np.exp(-t / .0018)
    x += hp(r.standard_normal(n), 2500) * np.exp(-t / .0008) * .15
    return norm(x * np.minimum(1, (dur - t) / .004)), 0

def notificacao(r, f=880, intervalo=1.335, gap=.085, var=0):
    """notificação própria (não imita iPhone/Slack): duas notas de marimba, f e f × intervalo (quarta justa)"""
    k = _varia(r, var); n = int((gap + .5) * SR); x = np.zeros(n)
    def nota(fr, t0, g):
        j = int(t0 * SR); u = np.arange(n - j) / SR
        y = (np.sin(2 * np.pi * fr * u) * np.exp(-u / .16) + .35 * np.sin(2 * np.pi * fr * 3.9 * u) * np.exp(-u / .025)   # marimba: 1 e ~4×
             + .2 * np.sin(2 * np.pi * fr * .5 * u) * np.exp(-u / .06))
        x[j:] += g * y * np.minimum(1, u / .002)
    nota(f * k, 0, .8); nota(f * k * intervalo, gap, 1.0)
    return norm(reverb(x, .6, .15, 5000, r)), 0

def swoosh(r, dur=.2, f0=1200, f1=6500, pico=.55):
    """swoosh curto de card que desliza (lateral, lower third): whoosh fino e rápido, sem grave; o PICO cai no tempo do evento"""
    y, d = whoosh(r, dur=dur, f0=f0, f1=f1, pico=pico); return norm(hp(y, 400)), d

def marca(r, dur=.35, golpes=3):
    """caneta/marcador riscando (sublinhado, círculo à mão): ruído de papel em `golpes` arrastos; dura o traço"""
    n = int(dur * SR); t = np.arange(n) / SR; x = lp(hp(r.standard_normal(n), 1500), 7000); e = np.zeros(n)
    for i in range(golpes):
        a, b = i / golpes, (i + .8) / golpes; u = np.clip((t / dur - a) / (b - a), 0, 1); e += np.sin(np.pi * u) ** 1.5 * (u > 0) * (u < 1)
    return norm(x * e), 0

def recolhe(r, f=520, dur=.07):
    """saída do pop-up (quase nunca usar): pop invertido, mais baixo e mais curto"""
    y, _ = pop(r, f=f * .8, dur=dur, queda=.6, var=0); return y * .6, 0

TIPOS.update(pop=pop, tick_ui=tick_ui, notificacao=notificacao, swoosh=swoosh, marca=marca, recolhe=recolhe)
```

**Modo `--um` (para o Remotion):** exporta um efeito sozinho, com o **ponto de alinhamento sempre em 0,5 s do arquivo**. Assim, o gerador põe o som em `from = t_contato − 0,5 s` sem precisar saber o deslocamento de cada tipo.

```python
PRE = .5   # ponto de alinhamento fixo dentro do arquivo exportado
def um(tipo, saida, semente=1, **extra):
    """uso: som.py --um pop public/sfx/ui/pop-2.wav --semente 2   (mono→estéreo, pico -3 dBFS como o @remotion/sfx)"""
    y, des = TIPOS[tipo](np.random.default_rng([semente, 0]), **extra)
    n0 = int(round((PRE + des) * SR)); x = np.zeros(n0 + len(y)); x[n0:] = y     # des ≤ 0: whoosh/swoosh começam antes do pico
    x *= 10 ** (-3 / 20) / (np.abs(x).max() + 1e-9)
    escreve(saida, np.stack([x, x], 1))
# em main(): if a and a[0] == '--um': um(a[1], a[2], int(op('--semente') or 1)); return
```

Também é preciso atualizar a docstring com a tabela de g sugeridos da seção 2.1 (pop 0,25 · tick_ui 0,30/0,18 · notificação 0,12 · swoosh 0,18 · marca 0,12) e a regra "saída muda".

---

## 5. Componentes prontos (o que já existe e aberto)

### 5.1 HyperFrames: registro inteiro no disco

O registro do HyperFrames está em `~/.claude/plugins/marketplaces/hyperframes/registry/` (`registry.json` com 400 itens: blocos, componentes e exemplos; licença do repositório **Apache-2.0**). O CLI fixo 0.8.140 tem `hyperframes catalog <palavras>` e `hyperframes add <nome>`, que instala o item no projeto da cena. São HTML + GSAP, cada um com o comentário de cabeçalho que diz variáveis, envelope e "Sound cue".

**Padrão que vale copiar:** 23 itens disparam o evento `hf:sfx` com um id no instante exato do som (ex.: `native-notification-pop` "no primeiro contato com o repouso") e **nunca tocam áudio sozinhos**. Quem decide o som é a mixagem. A nossa arquitetura faz igual (seção 6.3).

| Nome (tipo) | O que faz | Serventia para nós |
|---|---|---|
| `native-notification-pop` (comp.) | banner iOS/macOS que cai com mola fiel ao sistema, blur de fundo, app, título e uma linha; `exit` none/fade/up; som no contato | **notificação** por cima da tela (com marca nossa, não da Apple) |
| `notification-stack` / `notification-pileup` (comp.) / `notification-cascade` (bloco) | 1–5 cards que empilham; o mais novo em foco | "chegaram 3 leads" e afins |
| `macos-notification`, `liquid-glass-notification` (blocos) | banner macOS; cards de vidro fosco | estilo "vidro" |
| `badge-pop`, `spring-pop` (comp.) | selo que estoura com elástico e contagem; pop com um único overshoot | **pop-up curto** e selo de número |
| `success-check` (comp.) | anel que estoura + check desenhando | "funcionou" |
| `state-chip-rail` (comp.) | trilho de chips de estado (feito, ativo, pendente) | etapas ao vivo; primo do nosso `SeloStatus` |
| `count-up`, `number-pop-in` (comp.) | contador que acelera e pousa com pulso | número que importa |
| `hw-callout-circle` (comp.) | elipse à mão que se desenha em volta do alvo, conector curvo, rótulo manuscrito com "squash" no pouso | **círculo de anotação** (estilo "papel") |
| `hw-arrow`, `hw-underline`, `hw-box-label` (comp.) | seta à mão (3 curvas, 4 texturas), sublinhado/rabisco/colchete, caixa com rótulo; "boil" (traço vivo) | **seta, sublinhado, caixa** |
| `yt-circle-pointer` (comp.) | elipse desenhada + chip de contagem que pulsa | "olha aqui" com tempo |
| `vox-annotate` (comp.) | marcador na palavra + conector até um rótulo mono, num único gesto | **anotação editorial** (Vox) |
| `marker-highlight`, `inline-highlight` (comp.), `mk-callout-highlight` (bloco) | marca-texto/círculo/sublinhado na palavra; ênfase palavra a palavra puxada por um escalar | **ênfase de texto** |
| `caption-editorial-emphasis`, `mk-emphasis-type` (comp.) | duas fontes com grande contraste de tamanho; palavra gigante de fundo | **texto de ênfase** (Archivo × Instrument Serif) |
| `yt-feather-highlight` (comp.) | escurece tudo menos uma elipse com borda suave, que desliza entre alvos | **holofote** |
| `ui-focus-zoom` (comp.) | zoom e pan até uma região com halo | zoom na ação (já temos no `render.py`) |
| `oversized-cursor`, `press-ripple`, `gesture-tap` (comp.) | cursor macOS 3,5× que clica; anéis de clique; toque de dedo | **clique visível** |
| `lt-accent-underline`, `lt-dark-card`, `lower-third-bild`, `yt-lower-third` (blocos) | lower third sem card com fio de destaque; card escuro; estilo jornal; inscrição | **lower third** e nome de convidado |
| `yt-comment-card`, `chat-message` (bloco/comp.) | comentário digitando; balão de chat com rabicho real | prova social, réplica de conversa (dados inventados) |
| `spotlight-card`, `tilt-card`, `split-tilt-cards`, `testimonial-card` (comp.) | card com luz que segue o cursor; inclinação 3D; depoimento | **card** de informação |
| `hw-frame` (bloco) | moldura à mão com legenda | print destacado |

**Como usar:** (a) para **cenas de tela cheia** do HyperFrames, instalar direto com `hyperframes add` na pasta da cena; (b) para **overlays por cima da gravação no Remotion**, **portar a ideia e a curva** para o nosso TSX (a Apache-2.0 permite; manter o crédito no cabeçalho do arquivo portado). Itens muito ricos (o `hw-callout-circle` com "boil", o vidro líquido) podem sair do HyperFrames como camada com transparência e entrar como `<Video>` (é o caminho que a legenda já usa com ProRes alfa), mas perdem a edição no Studio.

### 5.2 Remotion

| Item | Licença | Serventia |
|---|---|---|
| **Remotion Elements** (oficial) — [remotion.dev/elements](https://www.remotion.dev/elements) | licença do Remotion (grátis para uma pessoa ou empresa de até 3) | blocos para pôr dentro de `<Sequence>`: lower thirds (nome, local), safe zones de Reels/TikTok, callouts, marcador, risco, mensagem na tela, polaroid, destaque de comentário do YouTube, lembrete de inscrição. Instala pelo **Studio** (Studio Protocol). Bom para ver o padrão oficial |
| **@remotion/transitions** | Remotion | já avaliado no estudo 1 (wipe, slide, iris) |
| **@remotion/sfx** (4.0.534 existe no npm) | MIT, licença por arquivo | ver seção 3: só os CC0 |
| **@remotion/lottie** (4.0.534 existe) | Remotion; lottie-web é MIT | `<Lottie animationData loop playbackRate direction renderer>`; herda `from`/`durationInFrames` de `Sequence`; quadro determinístico pelo tempo do Remotion. Carregar o JSON com `staticFile` + `delayRender` |
| **@remotion/rive** (4.0.534 existe) | Remotion; runtime Rive MIT | arquivos .riv; os da Comunidade Rive são **CC BY** (crédito obrigatório): evitar ou creditar |
| **reactvideoeditor/remotion-templates** — [github](https://github.com/reactvideoeditor/remotion-templates) | **MIT** (README) | 81 templates em .tsx com `useCurrentFrame`/`spring`: `notification-pop` (toasts empilhando), `lower-third`, `text-highlight` (palavra a palavra), `subscribe-reminder`, `end-card` |
| **Onda** — [onda.video](https://onda.video/) · [github](https://github.com/degueba/onda) | **MIT** | 70 componentes + 18 transições; `npx ondajs add <nome>` copia .tsx + schema Zod + README. Tem `callout`, `highlight`, `underline`, `bounding-box`, `lower-thirds`, `stat-cards`, `quote-cards`, `captions` |
| **RemotionUI** — [remotionui.com](https://remotionui.com) · [github](https://github.com/riaz37/remotion-ui) | **MIT** | 206 componentes copiáveis (`npx remotion-ui@latest add`, ou via shadcn); buscar com `search -q overlay` |
| **Remotion Bits** — [remotion-bits.dev](https://remotion-bits.dev/) | MIT no npm (0.2.1), **sem arquivo LICENSE no repositório** (conferir) | texto que revela, gráficos, transições |
| Remocn, snapcn (listados em [remotion.dev/docs/resources](https://www.remotion.dev/docs/resources)) | não confirmada | snapcn = "componentes que parecem software" (vale olhar como referência) |

**Postura:** nenhum desses entra como dependência de runtime. Copiar o .tsx (o Onda e o RemotionUI já trabalham assim), **reescrever no nosso tema e no nosso envelope**, e registrar a origem no cabeçalho. O nível do portfólio (Archivo/Serif/Mono, um destaque, cascata) não sai de template.

### 5.3 Lottie e motion packs

- **LottieFiles grátis:** em geral sob a **Lottie Simple License** (uso comercial, modificar e publicar; atribuição opcional; não pode montar serviço concorrente nem impor restrições; derivados com a mesma licença) — [lottiefiles.com/page/license](https://lottiefiles.com/page/license). Conferir **arquivo a arquivo** (há premium e outras licenças). Serve para ícone animado pequeno dentro de um card (check, loading, sino). **Recolorir para a paleta da marca** (o Lottie cru tem "cara de banco de ícones").
- **Packs de AE/Premiere grátis** (Mixkit templates etc.): só como **referência** de timing. Não entram no nosso pipeline (são .aep/.mogrt).

---

## 6. Arquitetura da biblioteca de overlays

### 6.1 Onde mora

```
~/.claude/skills/edicao-video/remotion/src/
  componentes.tsx            (já existe: Tela, Cena, MolduraMovel, Capitulo, SeloStatus…)
  overlays/
    registro.json            FONTE ÚNICA: tempos de entrada/saída, ponto de contato, som padrão, g, caixa, famílias, exemplo
    tema.ts                  fontes (Archivo · Instrument Serif · JetBrains Mono) + cores da marca (tema-marca.json gerado)
    estilos.ts               superfícies por família: vidro · papel · brutal · editorial · neutro
    base.tsx                 <Overlay> (envelope, posição que foge da câmera, contexto) + useOverlay()
    popup.tsx  card.tsx  enfase.tsx  notificacao.tsx  rotulo.tsx  lowerthird.tsx
    anotacao.tsx             sublinhado · círculo · seta · caixa (traço SVG que desenha)
    lista.tsx  contador.tsx  holofote.tsx (do estudo 02)
    index.tsx                REGISTRO: nome → componente; <RenderOverlay o={...}/>
    Galeria.tsx              composição de teste: cada tipo sobre uma tela de exemplo
  public/sfx/ui/             pop-1..4.wav, tick_ui-1..4.wav… (som.py --um, gerados uma vez por projeto)
  public/exemplo-tela.jpg    print FICTÍCIO (nunca de cliente) para a Galeria
```

O `gerar_remotion.py` hoje copia só `componentes.tsx`. Passa a copiar também a pasta `overlays/` (`copytree`) e a escrever `overlays/tema-marca.json` a partir de `marcas/<marca>/marca.css`, lendo as variáveis que todas as marcas já têm: `--m-fundo`, `--m-texto`, `--m-suave`, `--m-cor`, `--m-destaque`, `--m-ok`, `--m-alerta`.

### 6.2 API comum (props) — no `edicao.json`, tempo do vídeo editado

```jsonc
"overlays_estilo": "editorial",            // família do vídeo (varia de vídeo para vídeo; vai para o evolucao.md)
"sem_sfx": [[136.0, 171.5]],               // explicação técnica: overlays mudos aqui
"overlays": [
  { "tipo": "popup",       "ini": 55.4, "dur": 3.2, "lado": "alvo", "alvo": [0.188, 0.437, 0.276, 0.071],
    "texto": "Meta: vence em 5 min", "destaque": "5 min" },
  { "tipo": "enfase",      "ini": 61.0, "dur": 2.0, "texto": "o SLA *rompe* sozinho", "lado": "esq" },   // *palavra* = Instrument Serif itálico
  { "tipo": "notificacao", "ini": 221.3, "dur": 4.0, "titulo": "Lead novo", "texto": "Maria (fictícia) — chamou no WhatsApp", "lado": "dir" },
  { "tipo": "sublinhado",  "ini": 140.2, "dur": 2.5, "alvo": [0.64, 0.52, 0.33, 0.045], "estilo": "papel", "som": false },
  { "tipo": "lista",       "ini": 273.6, "dur": 8.0, "lado": "esq", "itens": [[0, "Filtrar fluxo"], [1.8, "Contar só mensagens"], [3.9, "Salvar"]] }
]
```

| Prop | Tipo | Padrão | O que é |
|---|---|---|---|
| `tipo` | nome do registro | — | qual overlay |
| `ini`, `dur` | s do vídeo editado | — | igual a `motions`, `capitulos` e `selos` |
| `lado` | `esq` `dir` `cima` `baixo` `centro` `alvo` `auto` | `auto` | onde fica; `auto` = do lado oposto à câmera; `alvo` = encostado no `alvo` |
| `alvo` | `[x, y, w, h]` do **bruto** 0–1 | — | convertido para px pela `vista.json` (estudo 02, 4.2) |
| `pos` | `[x, y]` px 1920×1080 | — | posição manual (vence `lado`) |
| `texto`, `titulo`, `destaque`, `itens` | texto | — | `*palavra*` ou `destaque` = serif itálico na cor de destaque |
| `estilo` | família | `overlays_estilo` | superfície |
| `cor` | `cor` `destaque` `ok` `alerta` | `destaque` | papel da cor na marca (nunca hex solto) |
| `som` | `false` · `"pop"` · `{tipo, g, desloc}` | do registro | `false` = mudo |
| `saida` | `some` `sobe` `lado` `nenhuma` | do registro | — |

### 6.3 Registro (fonte única para TSX e Python)

```jsonc
// overlays/registro.json — tempos em s; "contato" = instante do som, contado do ini (a Galeria confere com o quadro real)
{
  "popup":       { "ent": 0.45, "sai": 0.28, "curva": "back1.6", "contato": 0.27, "som": "pop",         "g": 0.25, "caixa": [520, 132],
                   "familias": ["vidro", "brutal", "editorial", "neutro"], "exemplo": { "texto": "Meta: vence em 5 min", "destaque": "5 min" } },
  "card":        { "ent": 0.50, "sai": 0.35, "curva": "expo",    "contato": 0.12, "som": "swoosh",      "g": 0.18, "caixa": [560, 300] },
  "notificacao": { "ent": 0.90, "sai": 0.45, "curva": "mola",    "contato": 0.31, "som": "notificacao", "g": 0.12, "caixa": [620, 120] },
  "enfase":      { "ent": 0.50, "sai": 0.30, "curva": "p4out",   "contato": 0,    "som": null },
  "sublinhado":  { "ent": 0.35, "sai": 0.25, "curva": "p4out",   "contato": 0,    "som": "marca",       "g": 0.12 },
  "circulo":     { "ent": 0.55, "sai": 0.25, "curva": "p4out",   "contato": 0,    "som": "marca",       "g": 0.12 },
  "lista":       { "ent": 0.40, "sai": 0.30, "curva": "p4out",   "contato": 0.2,  "som": "tick_ui",     "g": 0.18, "por_item": true },
  "contador":    { "ent": 0.40, "sai": 0.30, "curva": "expo",    "contato": "fim_contagem", "som": "tick_ui", "g": 0.30 },
  "lowerthird":  { "ent": 0.60, "sai": 0.40, "curva": "p4out",   "contato": 0.1,  "som": null }
}
```

```tsx
// overlays/tema.ts
import { loadFont as loadArchivo } from "@remotion/google-fonts/Archivo";
import { loadFont as loadSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import marca from "./tema-marca.json";                       // gerado do marcas/<marca>/marca.css
const GRITO = loadArchivo("normal", { weights: ["700", "800", "900"], subsets: ["latin", "latin-ext"] }).fontFamily;
const SERIF = loadSerif("italic", { weights: ["400"], subsets: ["latin", "latin-ext"] }).fontFamily;
const MONO = loadMono("normal", { weights: ["500", "700"], subsets: ["latin"] }).fontFamily;
export type Cores = { fundo: string; texto: string; suave: string; cor: string; destaque: string; ok: string; alerta: string };
export const TEMA = { f: { grito: GRITO, serif: SERIF, mono: MONO }, c: marca as Cores };
export const ESTILOS = {
  vidro:     { bg: "rgba(18,17,26,.62)", borda: "1px solid rgba(255,255,255,.14)", blur: 18, raio: 22, sombra: "0 18px 48px rgba(0,0,0,.40)" },
  papel:     { bg: "#f3efe4", borda: "none", blur: 0, raio: 4, sombra: "0 2px 0 rgba(0,0,0,.25), 0 14px 30px rgba(0,0,0,.30)" },
  brutal:    { bg: "var(--fundo)", borda: "2px solid var(--texto)", blur: 0, raio: 0, sombra: "6px 6px 0 var(--texto)" },
  editorial: { bg: "transparent", borda: "none", blur: 0, raio: 0, sombra: "none" },   // tipo solto com sombra de texto
  neutro:    { bg: "rgba(13,12,20,.86)", borda: "1px solid rgba(255,255,255,.10)", blur: 0, raio: 18, sombra: "0 14px 36px rgba(0,0,0,.35)" },
} as const;
export type Estilo = keyof typeof ESTILOS;
```

```tsx
// overlays/base.tsx — todo overlay passa por aqui: mesmo envelope, mesma posição, mesmo tema
import React, { createContext, useContext } from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import REG from "./registro.json";
import { TEMA, ESTILOS, type Estilo, type Cores } from "./tema";

export type Rect = [number, number, number, number];
export type Lado = "esq" | "dir" | "cima" | "baixo" | "centro" | "alvo" | "auto";
export type OverlayProps = {
  tipo: keyof typeof REG; ini: number; dur: number; escala: number;
  lado?: Lado; pos?: [number, number]; alvoPx?: Rect;           // alvo já em px da saída (o gerador converte pela vista.json)
  camera?: Rect; texto?: string; titulo?: string; destaque?: string; itens?: [number, string][];
  estilo?: Estilo; cor?: keyof Cores; saida?: "some" | "sobe" | "lado" | "nenhuma";
};
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CURVA = { back16: Easing.out(Easing.back(1.6)), expo: Easing.out(Easing.exp), p4out: Easing.out(Easing.poly(4)), mola: Easing.out(Easing.back(1.2)) };
const curva = (n: string) => (CURVA as any)[n.replace(".", "")] ?? CURVA.p4out;

type Env = { t: number; k: number; s: number; E: number; p: OverlayProps; st: (typeof ESTILOS)[Estilo]; tema: typeof TEMA; cor: string };
const Ctx = createContext<Env | null>(null);
export const useOverlay = () => useContext(Ctx)!;

// posição: âncora no lado pedido, dentro da margem segura (64 px), e NUNCA em cima da câmera (troca de lado se colidir)
const MARGEM = 64, W = 1920, H = 1080;
function posicao(p: OverlayProps, caixa: [number, number]): [number, number] {
  if (p.pos) return p.pos;
  const [cw, ch] = caixa; const cam = p.camera;
  const camDir = cam ? cam[0] + cam[2] / 2 > W / 2 : true;
  let lado = p.lado ?? "auto"; if (lado === "auto") lado = camDir ? "esq" : "dir";
  if (lado === "alvo" && p.alvoPx) {                              // encosta acima do alvo; se não couber, abaixo
    const [x, y, w, h] = p.alvoPx; const cima = y - ch - 18 > MARGEM;
    return [Math.min(Math.max(x + w / 2 - cw / 2, MARGEM), W - MARGEM - cw), cima ? y - ch - 18 : y + h + 18];
  }
  const xy: Record<string, [number, number]> = {
    esq: [MARGEM, H - MARGEM - ch - 120], dir: [W - MARGEM - cw, H - MARGEM - ch - 120],
    cima: [W / 2 - cw / 2, MARGEM + 40], baixo: [W / 2 - cw / 2, H - MARGEM - ch], centro: [W / 2 - cw / 2, H / 2 - ch / 2],
  };
  let [x, y] = xy[lado] ?? xy.esq;
  if (cam && x < cam[0] + cam[2] && x + cw > cam[0] && y < cam[1] + cam[3] && y + ch > cam[1]) [x, y] = xy[camDir ? "esq" : "dir"];
  return [x, y];
}

export const Overlay: React.FC<{ p: OverlayProps; children: React.ReactNode }> = ({ p, children }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const m = (REG as any)[p.tipo];
  const k = interpolate(t, [0, m.ent], [0, 1], { ...clamp, easing: curva(m.curva) });          // entrada 0→1 (pode passar de 1: overshoot)
  const s = p.saida === "nenhuma" ? 0 : interpolate(t, [p.dur - m.sai, p.dur], [0, 1], { ...clamp, easing: Easing.in(Easing.poly(4)) });
  const [x, y] = posicao(p, m.caixa ?? [480, 120]); const E = p.escala;
  const st = ESTILOS[p.estilo ?? "neutro"]; const cor = TEMA.c[p.cor ?? "destaque"];
  return (
    <Ctx.Provider value={{ t, k, s, E, p, st, tema: TEMA, cor }}>
      <div style={{ position: "absolute", left: x * E, top: y * E, opacity: Math.min(1, k * 1.6) * (1 - s),
        ["--fundo" as any]: TEMA.c.fundo, ["--texto" as any]: TEMA.c.texto }}>
        {children}
      </div>
    </Ctx.Provider>
  );
};
```

```tsx
// overlays/popup.tsx — exemplo de overlay concreto (o resto segue o mesmo molde)
import React from "react";
import { Overlay, useOverlay, type OverlayProps } from "./base";
const Caixa: React.FC = () => {
  const { k, s, E, p, st, tema, cor } = useOverlay();
  const esc = 0.82 + 0.18 * k;                                       // back easing: passa de 1 e volta (o "pouso" = contato do pop)
  const [antes, depois] = p.destaque && p.texto ? p.texto.split(p.destaque) : [p.texto ?? "", ""];
  return (
    <div style={{ transform: `translateY(${(1 - k) * 14 * E - s * 18 * E}px) scale(${esc})`, transformOrigin: "50% 100%",
      background: st.bg, border: st.borda, borderRadius: st.raio * E, boxShadow: st.sombra, backdropFilter: st.blur ? `blur(${st.blur * E}px)` : undefined,
      padding: `${18 * E}px ${28 * E}px`, display: "flex", alignItems: "baseline", gap: 10 * E, whiteSpace: "nowrap" }}>
      <span style={{ font: `800 ${40 * E}px ${tema.f.grito}`, letterSpacing: "-.03em", color: tema.c.texto }}>{antes}</span>
      {p.destaque && <span style={{ font: `400 ${48 * E}px ${tema.f.serif}`, color: cor }}>{p.destaque}</span>}
      <span style={{ font: `800 ${40 * E}px ${tema.f.grito}`, letterSpacing: "-.03em", color: tema.c.texto }}>{depois}</span>
    </div>
  );
};
export const Popup: React.FC<OverlayProps> = (p) => <Overlay p={p}><Caixa /></Overlay>;
```

```tsx
// overlays/index.tsx — o registro de componentes
import React from "react";
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";
import { Popup } from "./popup"; import { Card } from "./card"; import { Enfase } from "./enfase"; import { Notificacao } from "./notificacao";
import { Sublinhado, Circulo, Seta } from "./anotacao"; import { Lista } from "./lista"; import { Contador } from "./contador"; import { LowerThird } from "./lowerthird";
import type { OverlayProps } from "./base";
export const OVERLAYS = { popup: Popup, card: Card, enfase: Enfase, notificacao: Notificacao, sublinhado: Sublinhado,
  circulo: Circulo, seta: Seta, lista: Lista, contador: Contador, lowerthird: LowerThird } as const;
export type TipoOverlay = keyof typeof OVERLAYS;
export const RenderOverlay: React.FC<OverlayProps> = (p) => { const C = OVERLAYS[p.tipo as TipoOverlay]; return C ? <C {...p} /> : null; };
// som do overlay: arquivo do som.py --um (ponto de alinhamento em 0,5 s); o gerador põe a Sequence em t_contato − 0,5 s
export const SomOverlay: React.FC<{ arquivo: string; volume: number }> = ({ arquivo, volume }) =>
  <Audio src={staticFile(`sfx/ui/${arquivo}`)} volume={volume} />;
```

**Por que o som é uma `<Sequence>` irmã, e não filha do overlay:** a `Sequence` filha não toca antes do pai, e o swoosh e o whoosh começam **antes** do ponto de contato. Como irmã, cada som aparece **como uma faixa própria na linha do tempo do Studio**: dá para arrastar, aparar ou apagar sem mexer no overlay. Na `Galeria`, o overlay toca o próprio som, usando o mesmo `contato` do registro.

### 6.4 Como o `gerar_remotion.py` lê `"overlays"`

Entra depois do bloco de capítulos e selos (ordem das camadas do estudo 02, 4.6: overlays que escurecem → overlays que flutuam → câmera → selos/capítulos → cenas). O holofote fica abaixo da câmera, e o popup e a notificação ficam por cima dela só se o `lado` não colidir com ela (o `posicao()` já evita).

```python
# ---------- overlays por cima da tela (pop-up, card, ênfase, notificação, anotação) ----------
OVD = os.path.join(MODELO, 'src', 'overlays')
shutil.copytree(OVD, os.path.join(R, 'src', 'overlays'), dirs_exist_ok=True)
REG = json.load(open(os.path.join(OVD, 'registro.json')))
json.dump(tema_da_marca(J(C['marca_css'])) if C.get('marca_css') else {}, open(os.path.join(R, 'src', 'overlays', 'tema-marca.json'), 'w'))
SOM_PY = os.path.expanduser('~/.claude/skills/motion-design/kit/som.py'); PRE = .5; VAR = 4
os.makedirs(os.path.join(pub, 'sfx', 'ui'), exist_ok=True)
def arq_som(tipo, i):                                   # rodízio de 4 variações (afinação ±3–4 % por semente)
    nome = f'{tipo}-{i % VAR + 1}.wav'; dst = os.path.join(pub, 'sfx', 'ui', nome)
    if not os.path.exists(dst): subprocess.run([sys.executable, SOM_PY, '--um', tipo, dst, '--semente', str(i % VAR + 1)], check=True)
    return nome
def alvo_px(alvo, t):                                   # bruto 0–1 → px da saída no instante t (vista.json do render.py --camada-tela)
    x0, y0, w = VISTA[min(int(round(t * FPS)), len(VISTA) - 1)]; u, v, uw, vh = alvo
    return [round((u - x0) / w * OW / E, 1), round((v - y0) / w * OH / E, 1), round(uw / w * OW / E, 1), round(vh / w * OH / E, 1)]
VISTA = json.load(open(J(C.get('vista', 'vista.json')))) if any('alvo' in o for o in C.get('overlays', [])) else None
mudo = C.get('sem_sfx', []); sons, avisos, ultimo, n_som = [], [], -9.0, 0
estilo_video = C.get('overlays_estilo', 'neutro'); LIMITE = {'aula': 4, 'youtube': 6}.get(C.get('peca', 'aula'), 99)
L.append('      {/* overlays por cima da tela (registro: src/overlays/registro.json) */}')
for i, o in enumerate(sorted(C.get('overlays', []), key=lambda o: o['ini'])):
    if o['tipo'] not in REG: sys.exit(f"overlay desconhecido: {o['tipo']} (ver src/overlays/registro.json)")
    m = REG[o['tipo']]; q_a, q_b = int(round(o['ini'] * FPS)), int(round((o['ini'] + o['dur']) * FPS))
    if o['dur'] < m['ent'] + m['sai'] + 1.0: avisos.append(f"overlay {i+1} ({o['tipo']}) curto demais para ler: {o['dur']}s")
    p = {k: v for k, v in o.items() if k not in ('som', 'alvo')}; p.setdefault('estilo', estilo_video)
    if 'alvo' in o: p['alvoPx'] = alvo_px(o['alvo'], o['ini'] + m['ent'])
    p['camera'] = bloco_em(o['ini'])['saida']                       # o posicao() foge dela
    rot = (o.get('texto') or o.get('titulo') or '')[:28]
    L.append(f'      <Sequence name="overlay {i+1:02d} · {o["tipo"]} · {rot}" from={{{q_a}}} durationInFrames={{{q_b - q_a}}} premountFor={{fps}}>'
             f'<RenderOverlay {{...{json.dumps(p, ensure_ascii=False)}}} escala={{E}} /></Sequence>')
    # som: um ponto por overlay (ou por item da lista), no CONTATO; nunca na saída
    s = o.get('som', m.get('som'))
    if not s: continue
    s = {'tipo': s} if isinstance(s, str) else s
    pontos = [o['ini'] + t_ + m['contato'] for t_, _ in o.get('itens', [])] if m.get('por_item') else [o['ini'] + (m['contato'] if isinstance(m['contato'], (int, float)) else o['dur'] - m['sai'] - .2)]
    for j, t in enumerate(pontos):
        t += s.get('desloc', 0)
        if any(a <= t <= b for a, b in mudo): avisos.append(f"som {s['tipo']} em {t:.1f}s: trecho sem_sfx, tirado"); continue
        if j == 0 and t - ultimo < 1.2: avisos.append(f"som {s['tipo']} em {t:.1f}s colado no anterior ({t - ultimo:.2f}s): tirado"); continue
        g = s.get('g', m['g']) * (.85 ** j); arq = arq_som(s['tipo'], n_som); n_som += 1; ultimo = t
        sons.append(t)
        L.append(f'      <Sequence name="som · {s["tipo"]} · {t:.2f}s" from={{{int(round((t - PRE) * FPS))}}} durationInFrames={{{FPS * 2}}}>'
                 f'<SomOverlay arquivo="{arq}" volume={{{g:.3f}}} /></Sequence>')
for a_ in sons:                                          # orçamento por minuto
    if sum(1 for b_ in sons if a_ <= b_ < a_ + 60) > LIMITE: avisos.append(f'mais de {LIMITE} sons de overlay no minuto que começa em {a_:.0f}s'); break
for w_ in avisos: print('AVISO overlays:', w_)
```

Também muda: o `import` no topo do `Aula.tsx` ganha `import { RenderOverlay, SomOverlay } from "./overlays";`; a câmera (`bloco_em`) passa a ser calculada antes dos overlays; e o `render.py --camada-tela` grava `vista.json` (proposta do estudo 02). O `tema_da_marca()` é um parser de 10 linhas que lê `--m-*` do `marca.css`.

### 6.5 Editável no Remotion Studio

- **Um nó por overlay e um por som** no `Aula.tsx` (o mesmo princípio de hoje: "um nó JSX por clipe"). Na linha do tempo aparecem `overlay 03 · popup · Meta: vence em 5 min` e `som · pop · 55.67s`, e cada um pode ser movido, aparado ou apagado à mão.
- **Texto e estilo:** as props ficam escritas no próprio nó (JSON legível). Trocar `"estilo": "papel"` e salvar recarrega o Studio na hora (`npm run dev`).
- **Desenhar um overlay novo:** a composição `Galeria` recebe as props por um **schema Zod** (`<Composition schema={...} defaultProps={...}>`), e o painel de props do Studio vira um formulário (texto, estilo, lado, cor, som liga/desliga). O Studio consegue gravar os `defaultProps` de volta no arquivo (edição visual de props; conferir a versão exata em remotion.dev/docs/visual-editing e a versão do `zod` que a 4.0.534 pede antes de instalar). O que for aprovado na Galeria vira o `exemplo` do `registro.json`.
- Variar de vídeo para vídeo: cada vídeo escolhe **uma família** (`overlays_estilo`) e 3–5 tipos. A linha no `evolucao.md` da marca registra "overlays: editorial · popup, sublinhado, lista". O gerador pode ler a última linha e avisar se repetir a mesma família duas vezes seguidas (o dono já reclamou de vídeos parecidos).

### 6.6 Como testar (antes de usar num vídeo)

1. **Galeria** (`Galeria.tsx`): monta cada tipo do registro, 3 s cada, com o `exemplo` do registro, sobre `public/exemplo-tela.jpg` (print fictício), em cada família, com a moldura da câmera desenhada no canto (testa a fuga da câmera).
2. **Folha em 3 tempos por overlay:**
   - **meio da entrada** (`ini + ent/2`): a curva está viva, sem "pulo";
   - **repouso** (`ini + ent + 0,4`): leitura, contraste, margem;
   - **meio da saída** (`ini + dur − sai/2`).
   Mais rápido que 36 `remotion still` (cada um sobe um navegador): **um** `npx remotion render Galeria out/galeria.mp4 --crf=16` e depois `ffmpeg -vf "select='eq(n,15)+eq(n,52)+…',scale=640:-1,tile=3x12" -frames:v 1 out/folha-overlays.jpg`. A crítica da `direcao-de-arte` lê essa folha.
3. **Números (hierarquia-visual):** no still de repouso, medir a altura da caixa de texto (≥ o mínimo de apoio da `hierarquia-visual` para 16:9), o contraste texto × superfície (amostra de pixel, APCA/WCAG) e a margem de 64 px. No estilo `vidro`, medir sobre a parte mais clara do print de exemplo (o pior caso).
4. **Som:** renderizar a Galeria com áudio (`--codec=wav`) e, para cada som, conferir:
   - **sincronia:** o primeiro pico acima de -40 dBFS em relação ao quadro de contato (quadro em que a escala ou posição chega a 1, registrado num `contatos.json` que a Galeria escreve via `console.log` no render) não pode passar de **±1 quadro**;
   - **nível:** o M máx tem que estar na faixa da seção 2.1.
   Se o `contato` do `registro.json` estiver errado, a correção é **no registro**, nunca na mão no vídeo.
5. **Determinismo:** o mesmo quadro renderizado duas vezes dá o mesmo md5 (sem `Math.random`, sem `Date`; variação só por semente).
6. **No vídeo de verdade:** a `revisao-video` roda como sempre e, além disso, fotografa cada overlay no repouso (folha de overlays do vídeo) e lista os avisos do gerador (som tirado, minuto acima do orçamento).

### 6.7 Ordem para implementar (sugestão)

1. Funções novas + `--um` no `som.py`; ouvir A/B com os 21 da Pixabay (custo pequeno).
2. `overlays/` com `base`, `tema`, `registro.json` e 4 tipos (`popup`, `enfase`, `notificacao`, `sublinhado`), mais a `Galeria` e a folha.
3. `"overlays"` no `gerar_remotion.py` + `vista.json` no `render.py`.
4. Piloto numa aula curta, com rubrica e comparação com a aula SLA v2.
5. Portar do registro do HyperFrames, um por vídeo, o que fizer falta (`vox-annotate`, `hw-callout-circle`, `state-chip-rail`), com crédito Apache-2.0 no cabeçalho.

---

## Fontes

- Níveis e mixagem: [Adorama — níveis de áudio](https://www.adorama.com/alc/mastering-audio-levels/) · [Sage Audio — diálogo](https://www.sageaudio.com/articles/mastering-dialogue-for-podcasts) · [IRPR — LUFS para YouTube](https://sounddesign.irpr.agency/guides/what-is-the-right-lufs-for-youtube-podcast-broadcast/) · [Pixflow — diálogo, música e efeitos](https://pixflow.net/blog/audio-mixing-premiere-pro/)
- Som de UI: [Violet Recording — UI sounds](https://violetrecording.com/how-to-design-ui-sounds/) · [ui-sound-design (durações)](https://skillselion.com/skills/dannyjpwilliams/ui-sound-design-skill/ui-sound-design) · [userinterface wiki (fadiga de repetição)](https://tessl.io/registry/skills/github/gsd-build/gsd-2/userinterface-wiki) · [IRPR — sons de UI irritantes](https://sounddesign.irpr.agency/solutions/ui-sounds-annoying/) · [Material — sound](https://m2.material.io/design/sound/applying-sound-to-ui.html)
- Aprendizagem: [Moreno & Mayer 2000 (PDF)](https://tecfa.unige.ch/tecfa/teaching/methodo/Moreno_Mayer00.pdf) · [Cambridge — princípio da coerência](https://www.cambridge.org/core/books/abs/multimedia-learning/coherence-principle/4E80B70CB76E2166B76E5653EBDE7D3E)
- YouTube: [YPulse — cansaço da edição de retenção](https://www.ypulse.com/newsfeed/2024/04/02/young-people-are-getting-tired-of-retention-editing-on-youtube/) · [Finchley — SFX e retenção](https://www.finchley.co.uk/finchley-learning/youtube-growth-strategy-retaining-viewers-with-sound-effects-for-video-editing)
- Licenças de SFX: [Mixkit license](https://mixkit.co/license/) · [Pixabay license](https://pixabay.com/service/license-summary/) · [Kenney UI Audio](https://kenney.nl/assets/ui-audio) · [freesound FAQ](https://freesound.org/help/faq/) · [Zapsplat — licenças](https://www.zapsplat.com/copyright-and-audio-licensing-for-beginners) · [Sonniss GDC 2026](https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/) · [@remotion/sfx](https://www.remotion.dev/docs/sfx) (atribuição por arquivo lida em `packages/docs/docs/sfx/*.mdx` do repositório do Remotion)
- Componentes: registro do HyperFrames local (`~/.claude/plugins/marketplaces/hyperframes/registry/`, Apache-2.0) · [Remotion Elements](https://www.remotion.dev/elements) · [Remotion resources](https://www.remotion.dev/docs/resources) · [remotion-templates (MIT)](https://github.com/reactvideoeditor/remotion-templates) · [Onda (MIT)](https://github.com/degueba/onda) · [RemotionUI (MIT)](https://github.com/riaz37/remotion-ui) · [Remotion Bits](https://github.com/av/remotion-bits) · [@remotion/lottie](https://www.remotion.dev/docs/lottie/lottie) · [Lottie Simple License](https://lottiefiles.com/page/license) · [Rive Community (CC BY)](https://help.rive.app/community/overview) · [Remotion — licença](https://www.remotion.dev/docs/license)
- Conferir antes de adotar: a página completa da licença do Mixkit (o fetch não trouxe o texto; o resumo veio de busca), a licença do Remotion Bits (sem LICENSE no repositório), o Remocn e o snapcn (não verificados) e o recurso de salvar props no Studio na 4.0.534.
