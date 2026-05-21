---
data: 2026-05-21
tipo: decisao
status: superado
relacionados: [aesthetic-dark-glass-hibrido, brand-design-system-vs-prototipo, claude-design-limites-quirks]
---

# Prototipagem da Sprint 2 via Claude Design (não Figma)

## Atualização 2026-05-21 (mesmo dia, à tarde)

**Decisão superada.** Após receber o output do Claude Design, Igor sentiu que o protótipo gerado:
- Ficou genérico ("parece dashboard de IA igual qualquer outro")
- Inventou termos e equipes que não existem na Locaweb
- Fugiu da identidade Cronos canônica do `brand/design-system.html`
- Estava confuso por excesso de informação/funcionalidade

Novo caminho adotado:
1. Voltar pra identidade canônica light/operacional do `brand/`
2. Explorar `LWDATASET.xlsx` ANTES de prototipar (extrair vocabulário real)
3. Calibrar personalidade refinada (tipo "iOS premium" mas mantendo brand Cronos) via showcase visual em `prototipos/personalidade.html`
4. Prototipar do zero em HTML manual, uma tela por vez

Os arquivos da iteração Claude Design foram removidos (ver commit subsequente). Permanecem em git history (commit `ceb729f`).

Esta decisão fica marcada como **superado** mas preservada pra registro do aprendizado: ferramentas de geração de UI por IA precisam de spec ancorado em dados reais e identidade firme, senão regridem ao slop genérico.

## Contexto

Em 20/05/2026 tentamos prototipar no Figma mas batemos no limite do plano Starter do Figma MCP (arquivo de teste em `https://www.figma.com/design/OEBIG7Bh1P6z6TFi8FufSd`). Em 21/05 surgiu a opção do **Claude Design** (ferramenta nova da Anthropic em `claude.ai/design`) que aceita spec em markdown e gera protótipos React+Tailwind navegáveis.

## O que ficou definido

A rota oficial de prototipagem da Sprint 2 é o **Claude Design**. Figma foi abandonado pra esta sprint. Os 5 protótipos do Cronos (Dashboard, Morning Brief, Cascata, Saúde Produto, Probabilidade KPI) serão gerados a partir de specs `.md` em `prototipos/`.

## Por quê

- Sem teto do plano Starter (Figma cobra por componente complexo)
- Spec em markdown é versionável no Git e revisável em PR
- Output em React+Tailwind serve de esqueleto inicial pros templates Django da Sprint 3 (não joga fora trabalho)
- Iteração rápida — peça mudança em texto, recebe protótipo refeito

## Como aplicar

**Fluxo padrão de geração:**

1. Escrever spec completo em `prototipos/claude-design-prompt-*.md` (princípios, tokens, motion, copy)
2. Acessar `claude.ai/design` → New Design
3. Anexar o `.md` em "DROP FILES HERE"
4. Anexar 2 screenshots como referência visual (V1 e V5 dos protótipos exploratórios em `prototipos/dashboard-v{1,5}-*.html`)
5. Tags: "Hi-fi design" + "Interactive prototype". NÃO marcar "Design System" (ele extrai de sistema existente, não é nosso caso).
6. NÃO anexar `brand/design-system.html` — ele é a identidade light/operacional canônica, briga com o dark glass do protótipo. Reservar pra Sprint 3 (Django).
7. Prompt textbox curto (PT-BR): instrução pra seguir o spec literalmente, gerar tela por tela, rodar pre-flight ao final.

**Spec atual ativo:**
- `prototipos/claude-design-prompt.md` — V1 do spec (estética + estrutura)
- `prototipos/claude-design-prompt-v2-actionable.md` — iteração V2 (camadas de acionabilidade)

**Validação de estilo antes de aprovar:**
- `prototipos/preview-style.html` — sniff test visual local, abre no browser pra Igor bater olho

## Conexões

- [[aesthetic-dark-glass-hibrido]] — a estética escolhida
- [[brand-design-system-vs-prototipo]] — por que não anexar o brand atual
- [[claude-design-limites-quirks]] — quirks operacionais
- [[prototipo-reflete-arquitetura]] — princípio que rege o conteúdo do spec

---

*Última atualização: 2026-05-21*
