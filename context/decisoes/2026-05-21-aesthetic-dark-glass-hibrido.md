---
data: 2026-05-21
tipo: decisao
status: superado
relacionados: [prototipagem-claude-design, brand-design-system-vs-prototipo]
---

# Aesthetic dos protótipos — dark glass híbrido V1+V5

## Atualização 2026-05-21 (mesmo dia, à tarde)

**Decisão superada.** Após ver o output do Claude Design baseado neste spec, Igor concluiu que:
- O dark glass criou distância da identidade canônica do brand Cronos (que é LIGHT)
- Tentar manter "dois sistemas conscientes" (light pra Django, dark pra protótipo) introduziu fricção desnecessária
- A apresentação na banca FIAP fica mais coesa com **uma identidade única continuada da Sprint 1**

Nova direção: **manter a identidade canônica light do `brand/design-system.html`** e refinar com personalidade premium (iOS-style soft elevations, frosted glass sutil sobre fundo claro). Sem mudar a paleta.

Ver decisão sucessora em [[2026-05-21-identidade-prototipo-light-refinada]] (a ser criada após calibração via `prototipos/personalidade.html`).

## Contexto

Em 13–20/05 geramos 4 protótipos exploratórios de dashboard em `prototipos/dashboard-v{1,2,3,5}-*.html`:
- **V1 Command Center** — Datadog/Honeycomb style, light theme primário, denso operacional, heatmap GitHub-style, sidebar com labels
- **V2 Analytical Workspace** — Linear/Notion, bento grid, tabs, chips coloridos
- **V3 Executive Cockpit** — Stripe/Mercury, hero gigante, Monte Carlo
- **V5 Glass Console** — Vercel v0 / Apple Vision Pro, dark default, mesh gradient animado, glassmorphism, glow

Igor gostou de V1 e V5 e pediu meio-termo.

## O que ficou definido

**Aesthetic locked:** dark glass com identidade Cronos canônica. Tokens fixos:

- **Base:** off-black `#0A0A0F` (NUNCA `#000000`)
- **Surfaces:** glass `rgba(255,255,255,0.04)` + `backdrop-blur(32px) saturate(160%)` + hairline 1px `rgba(255,255,255,0.08)`
- **Accent único:** `#2563EB` (Cronos blue canônico do brand) — NÃO o `#3B82F6` do V5
- **Semânticas:** danger `#DC2626`, warning `#D97706`, success `#059669` (canonical do brand)
- **Tipografia:** Outfit Sans + JetBrains Mono pra TODOS os números
- **Mesh BG:** 2 blobs ESTÁTICOS (azul top-left + danger bottom-right) + grain texture. NUNCA animar — performance.
- **Outer glow proibido**, com 2 exceções únicas: hero pulse dot + cascata predicted ring

## Por quê

**Estrutura V1, polish V5, identidade brand:**
- V1 traz a densidade operacional necessária pra dashboard real (manager olha 20+ vezes por dia)
- V5 traz a estética premium que impressiona banca FIAP
- Acent `#2563EB` mantém continuidade com Sprint 1 e o brand canônico em `brand/design-system.html`
- Outfit + JetBrains Mono evita conflitar com Geist (que a skill `design-taste-frontend` recomenda mas não é canônico do projeto)

**THE LILA BAN ativo** — a skill `design-taste-frontend` bane explicitamente gradiente roxo+azul ("AI Purple/Blue"). O V5 original usava `#3B82F6 → #A855F7` em todo lugar — corrigimos pra accent único + gradient roxo/rosa apenas em texto crítico (hero number, score crit).

**Mesh estático** — V5 original animava 3 blobs em loop infinito 22–28s. Mesmo com `blur(80px)` em pseudo-element, é repaint contínuo de GPU. Skill `design-taste-frontend` cobra performance. Trocamos por estático + grain — visualmente 95% igual, 0% custo contínuo.

## Como aplicar

Toda vez que gerar UI do Cronos pra protótipo da Sprint 2:

1. Usar os tokens acima literalmente — não improvisar
2. Sniff test visual disponível em `prototipos/preview-style.html` — abrir no browser pra calibrar olho
3. NÃO usar tokens do `brand/design-system.html` (que é light/operacional, conflita) — ver [[brand-design-system-vs-prototipo]]
4. Single accent rule: gradients só em (a) hero number text, (b) score crit text — NUNCA em botões, glows, accents de UI

**Quando virar Django na Sprint 3:** este aesthetic se transforma. O Django vai usar a paleta canônica light do `brand/design-system.html`. Não migrar 1:1 o dark glass.

## Conexões

- [[prototipagem-claude-design]] — a ferramenta que aplica esta aesthetic
- [[brand-design-system-vs-prototipo]] — por que não usar o brand atual no protótipo
- [[claude-design-limites-quirks]] — quirks operacionais da ferramenta

---

*Última atualização: 2026-05-21*
