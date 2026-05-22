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

| Arquivo | Função | Briefing coberto |
|---|---|---|
| `dashboard.html` | Home da demo · resumo das 4 dores do gestor + KPI mensal | Tendência diária (#5, #6) |
| `previsao.html` | Forecast D+1/D+7 por prioridade + por dimensão | **D+1 (#1), D+7 (#2), por prioridade (#3), por dimensão (#4)** |
| `saude-produto.html` | Score por produto · XGBoost + SHAP · drill-down inline | Tendências/clusters (#8), explicabilidade (#9) |
| `cascata.html` | Detector de acúmulo · lista REAL de incidentes-filhos + sugestão IA | Indicar onde agir (#7) |
| `morning-brief.html` | Briefing editorial diário com resumo executivo | Indicar onde agir (#7), tendências (#8) |

Todas consomem `../../brand/design-system/assets/tokens.css` como única fonte de tokens.

## Demo navegável

O protótipo é disponibilizado via **GitHub Pages** como demo navegável, complementando os screenshots do PPT:

🔗 (link a ser configurado nas settings do repositório · Settings → Pages → branch `main` · folder `/` ou `/prototipos/telas`)

Permite à Locaweb experimentar a navegação real entre as telas, não só ver imagens estáticas.

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
