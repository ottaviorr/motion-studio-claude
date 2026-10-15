# Telas reais nas cenas

A cena fica muito melhor com a interface de verdade do produto do que com um desenho. Receita:

1. **Rodar o app** localmente (servidor de desenvolvimento) ou abrir o site/login público. Use uma conta de teste e dados de demonstração — nunca a conta de um cliente.
2. **Preparar os dados de demonstração** no banco local: nomes de clientes inventados, situações "ok/no ar", números bonitos mas plausíveis. Nada em produção.
3. **Fotografar com `scripts/fotos-telas.mjs`** (Chrome sem janela, 1600×900 em escala 2). Escreva um arquivo de passos a partir de `reference/passos-exemplo.mjs`: entrar, navegar, preencher (`preenche` para React/Vue), clicar (`clica`), enviar arquivo (`DOM.setFileInputFiles`), trocar para celular (`setDeviceMetricsOverride` 430×932 escala 3).
   - Apps pesados: espere ~4–5 s depois de abrir antes de interagir (senão o formulário envia antes do script do app carregar).
   - Muitos logins seguidos podem acionar a trava de tentativas do app: limpe a trava no banco local.
4. **Medir posições no mesmo passo** (`getBoundingClientRect` → `[x,y,w,h]` em px CSS 1600×900). São as coordenadas de `spot`, `cam` e do cursor na cena.
5. **Na cena:** `TELA('t',['foto1','foto2'],'endereco.com')` dentro de `#cam`; `seq` troca as fotos no tempo da fala; `cam` aproxima; `spot` destaca; `cursor` clica com onda; `wipe` faz a transição (ex.: o painel abrindo num círculo que sai do botão "Entrar").
6. **Sem acesso à tela de verdade** (ex.: dentro de um sistema de terceiros): faça a réplica em HTML com `frame(t)`, fotografe com `scripts/fotografar-cena.mjs` (dá para trocar o tema por variáveis CSS) e diga no guia que é ilustração.

Truque útil: se o app decide o que mostrar pelo **domínio** (multi-tenant, white label), rode uma segunda instância do servidor local "atendendo como" o domínio do cliente (ex.: opção de host do servidor de desenvolvimento) para fotografar a experiência do cliente final. Desligue a instância extra no fim.
