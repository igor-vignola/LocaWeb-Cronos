# Cronos — Challenge FIAP 2026 com Locaweb

> **"Veja antes. Aja antes."**

Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão.
Mantém o contexto essencial para continuar o trabalho de onde parou.
Para detalhes específicos, consulte a pasta `context/`.

---

## O projeto

**Cronos** é um sistema de inteligência preditiva para incidentes operacionais da Locaweb. Transforma 3 anos de dados (122.543 incidentes) em previsões e alertas automáticos para antecipar violações de OLA e apoiar a tomada de decisão operacional.

Domínio: **AIOps** — previsão de incidentes e tendências operacionais usando ML.

---

## Equipe — Super Data Bros · Turma 2TSCOA

- **Ana Beatriz Costa de Oliveira** — RM561310
- **Hygor Abrantes** — RM565063
- **Igor Vignola** — RM561428

**Mentor Locaweb:** Douglas Gouveia (Gerente Executivo de Operações)

---

## Status atual

| Sprint | Tema | Entrega | Status |
|--------|------|---------|--------|
| 1 | Ideação | 27/04/2026 | ✅ Entregue · **nota 5.00/5.00** |
| 2 | Arquitetura | 24/05/2026 | 🚧 **EM ANDAMENTO** |
| 3 | MVP Preliminar | 23/08/2026 | ⏳ Futuro |
| 4 | Solução Final | 08/09/2026 | ⏳ Futuro |

Detalhes em `context/sprints/` e `context/status.md`.

---

## Regras técnicas CRÍTICAS (nunca violar)

Estas decisões já estão tomadas. **Não revisitar sem motivo forte.**

1. **NÃO usar ARIMA/SARIMA** — é problema de série temporal. Stack aprovada: **Prophet + XGBoost** com features temporais (lag 1/7/30d, rolling 7d, dia_semana, is_feriado).
2. **NÃO usar K-Means puro** para clusterização — padrões podem estar deslocados no tempo. Usar **`TimeSeriesKMeans` com `metric='dtw'`** (tslearn).
3. **NÃO usar Streamlit** — todo mundo usou ano passado. **Django** é mandatório.
4. **Apenas incidente PAI conta para KPI.** Filtrar (`Incidente Pai` vazio) antes de modelar OLA — confirmado pela Locaweb.
5. **Solução agnóstica de cloud provider.** A Locaweb É uma cloud — não amarrar a AWS/GCP/Azure. Usar apenas serviços portáveis.
6. **Entrega via Docker.** Facilita Locaweb pegar e rodar.
7. **Feriados não estão no dataset** — engineering via lib `holidays` BR ou `country_holidays='BR'` do Prophet.
8. **Claude API apenas nos bastidores** — para gerar texto dos alertas e morning brief. NÃO é interface de chat com usuário.
9. **Sem interface conversacional** — Cronos empurra insights proativamente, não espera perguntas.

---

## Os 3 diferenciais do produto

1. **Morning briefing** — resumo automático (Ontem / Hoje / Ações sugeridas) com botão "ver detalhes" para relatório completo. Aparece proativamente, não espera consulta.
2. **Detector de cascata** — monitora acúmulo de alertas pequenos (P4/P5) que historicamente precedem falhas graves (P3/P2). **Padrão validado pela Locaweb na mentoria.**
3. **Score de saúde por produto** — nota 0-100 por produto com ranking, tendência e explicabilidade.

---

## Como trabalhar com Igor

Estilo de comunicação preferido (anotado pelo próprio Igor):

- **Linguagem simples**, sem jargões não explicados.
- **Dividir respostas longas em partes**, não despejar tudo de uma vez.
- **Não avançar para execução sem confirmação** de entendimento.
- Usar **visualizações** quando ajudar (tabelas, diagramas, mockups).
- **Pushback bem-vindo** — se a ideia tem furo, apontar. Não bajular.
- **Apresentar prós E contras** em decisões importantes, nunca só prós.
- **Não validar premissa falsa** só porque foi afirmada.
- **Direto e conciso**. Pode ser informal em PT-BR.
- Quando a resposta correta for "não sei" ou "depende de X", dizer isso em vez de inventar confiança.
- Para decisões com impacto irreversível, considerar invocar a skill **`council`** sem precisar de pedido explícito.

Igor revisa e aprova cada componente antes de avançar. Não pular etapas de validação.

---

## Estrutura do projeto

```
Challenge-LocaWeb/
├── CLAUDE.md                  ← este arquivo
├── README.md                  ← apresentação pública do projeto
├── .gitignore
├── .claude/
│   └── skills/                ← skills carregadas sob demanda
│       ├── sprint-checklist/
│       └── challenge-context/
├── context/                   ← contexto persistente (LER quando precisar)
│   ├── README.md              ← índice
│   ├── projeto.md
│   ├── decisoes-tecnicas.md
│   ├── mentoria-locaweb.md
│   ├── status.md
│   └── sprints/
│       ├── 01-ideacao.md
│       └── 02-arquitetura.md
├── assets/                    ← arquivos da FIAP/Locaweb (read-only)
│   ├── briefings/
│   └── locaweb/
├── brand/                     ← identidade visual do Cronos
├── data/
│   └── raw/LWDATASET.xlsx     ← versionado (anonimizado)
├── notebooks/                 ← AED, features, modelagem (Sprint 2+)
└── sprints/                   ← entregáveis .pptx
    ├── sprint-1/
    └── sprint-2/
```

---

## Skills disponíveis

Skills carregam sob demanda quando o contexto pede. **9 skills ativas no projeto**, agrupadas:

### Cronos-canonical (sempre relevantes)

- **`challenge-context`** — contexto completo do desafio: dataset (122k incidentes, 19 campos), regras de KPI/OLA, metas anuais, prioridades. Consultar antes de qualquer entregável.
- **`sprint-checklist`** — checklist obrigatório antes de qualquer entregável (PPT, código, slide).
- **`context-keeper`** — mantém `context/` sempre atualizado. Auto-invoca quando tomamos decisão técnica, Igor expressa preferência, aprendemos algo novo, ou ele pede pra "lembrar disso".
- **`commit-style`** — padrão de commits do projeto (conventional commits em PT-BR).

### Código & análise

- **`python-style`** — convenções de Python (.py + células em .ipynb, Django + pandas).
- **`notebook-style`** — estrutura obrigatória dos `.ipynb` (AED, modelagem).
- **`viz-style`** — padrão visual dos gráficos (AED, dashboard, slides).

### UI & design (Sprint 2+)

- **`design-taste-frontend`** — regras métricas de UI (protótipos, Claude Design, Django). Bloqueia AI slop (THE LILA BAN, Inter font, scale-zero entry, etc.).
- **`emil-design-eng`** — polish e micro-interações (durações, easing, transform-origin, scale-on-press). Pareada com `design-taste-frontend`.

---

## Onde buscar informação adicional

Quando precisar de algo além desta visão geral:

- `context/projeto.md` — identidade Cronos completa
- `context/decisoes-tecnicas.md` — stack detalhada, features, restrições, os 3 diferenciais expandidos
- `context/mentoria-locaweb.md` — insights da live com Douglas (IMPORTANTE: ler antes de decidir coisas técnicas)
- `context/status.md` — onde estamos AGORA, próximos passos
- `context/sprints/01-ideacao.md` — sprint entregue, nota, feedback do professor
- `context/sprints/02-arquitetura.md` — sprint ativa, 8 frentes de trabalho
- `assets/` — briefings oficiais da FIAP, dicionário de dados, apresentação Locaweb

---

## Princípios de manutenção deste contexto

1. **Toda decisão técnica importante** → documentar em `context/decisoes-tecnicas.md`.
2. **Toda conversa com a Locaweb ou mentoria** → atualizar `context/mentoria-locaweb.md`.
3. **Toda entrega ou marco de sprint** → atualizar `context/sprints/0X-NOME.md` e `context/status.md`.
4. **Commits** em português, padrão Conventional Commits:
   - `feat:` nova funcionalidade
   - `fix:` correção
   - `docs:` documentação (inclui atualização de `context/`)
   - `chore:` manutenção, configuração
   - `refactor:` refatoração sem mudança de comportamento
   - `test:` testes
   - `style:` formatação

---

*Última atualização: 14/05/2026*
