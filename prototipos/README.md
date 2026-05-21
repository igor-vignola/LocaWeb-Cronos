# Protótipos — Cronos

## Estrutura

```
prototipos/
├── telas/          ← Protótipos do produto Cronos (entrega final)
├── slides/         ← HTMLs usados pra gerar slides do PPT da Sprint 2
│   └── png/        ← Exports PNG dos slides
├── variacoes/      ← Versões alternativas / experimentos não escolhidos
└── docs/           ← Documentos auxiliares (vocabulário, refs)
```

## Telas ativas (`telas/`)

| Arquivo | Função |
|---|---|
| `dashboard.html` | Tela principal — KPI mensal, cascatas, saúde por produto, heatmap, equipes |
| `morning-brief.html` | Briefing diário em formato editorial (jornal) — Cronos AI resume ontem/hoje + sugestões + decisões + horizonte 7d |

Ambos consomem `../../brand/design-system/assets/tokens.css` como única fonte de tokens (cores, espaçamento, motion).

## Slides Sprint 2 (`slides/`)

HTMLs usados para gerar os PNGs que entram no PPT. PNG exportado fica em `slides/png/` com mesmo nome base.

- `capa-slide.html` → capa
- `arquitetura-slide.html` → diagrama de arquitetura V2 (etapas + numeração)
- `tecnologias-slide-v1.html` → stack de tecnologias

## Variações (`variacoes/`)

Versões alternativas que não foram escolhidas mas valem manter pra histórico/referência.

- `arquitetura.html` — versão anterior do slide de arquitetura

## Docs (`docs/`)

- `vocabulario-real.md` — produtos, equipes, alertas e ICs extraídos do `LWDATASET.xlsx`. **Sempre consultar antes de inventar mock data nos protótipos.**

## Identidade visual ativa

Design system canônico: `brand/design-system/` (foundations, motion, atoms, molecules, patterns).

**Tokens-chave:**
- Accent único: `#2563EB`
- Tipografia: `Outfit` Sans (com `font-variant-numeric: tabular-nums` para números)
- Aesthetic: light glass (Apple HIG · Liquid Glass) — `backdrop-filter: blur(40px) saturate(180%)`
- Cor semântica é informação, não decoração — números grandes e títulos sempre em preto/cinza

## Próximas telas

- [ ] `telas/saude-produto.html` — score 0-100 por produto, ranking, explicabilidade
- [ ] `telas/cascata.html` — detalhe de cascata em formação, SHAP-style
