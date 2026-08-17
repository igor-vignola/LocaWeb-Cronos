# Cronos — Challenge FIAP 2026 com Locaweb

> **"Veja antes. Aja antes."**

Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão.
Mantém o contexto essencial para continuar o trabalho de onde parou.
Para detalhes específicos, consulte a pasta `context/`.

---

## O projeto

**Cronos** é um sistema de inteligência preditiva para incidentes operacionais da Locaweb. Transforma o histórico operacional (122.543 incidentes registrados; a base elegível ao KPI concentra-se em 2025) em previsões e alertas automáticos para antecipar violações de OLA e apoiar a tomada de decisão operacional.

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
| 2 | Arquitetura | 24/05/2026 | ✅ Entregue · **nota 5.00/5.00** |
| 3 | MVP Preliminar | 23/08/2026 | 🚧 **EM ANDAMENTO** (modelagem) |
| 4 | Solução Final | 08/09/2026 | ⏳ Futuro |

Detalhes em `context/sprints/` e `context/status.md`.

---

## Regras técnicas CRÍTICAS (nunca violar)

Estas decisões já estão tomadas. **Não revisitar sem motivo forte.**

1. **NÃO usar ARIMA/SARIMA.** Previsão de volume: **Prophet** (features de calendário `dia_semana` + `is_feriado`; treino em 2025, sazonalidade semanal ligada e anual desligada). Risco de OLA: **regressão logística** — medido em 03/08/2026: ROC AUC **0,869** contra 0,868 do XGBoost (empate) e PR-AUC **0,296** contra 0,253 (vantagem de 17% para a logística, e o PR-AUC é a métrica que vale para evento raro). Também é explicável por construção e mantém a calibração: prevê 48,1 quebras onde houve 50. XGBoost fica como baseline de comparação; com `scale_pos_weight` ele prevê 1.007 quebras onde houve 50 e inviabiliza a projeção do KPI.
2. **Clusterização DTW testada e DESCARTADA** — `TimeSeriesKMeans` com `metric='dtw'` deu silhueta ~0,13 (sem grupos reais). O requisito de "classificação ou clusterização" do desafio é atendido pelo **classificador de risco de OLA**. Não reabrir DTW nem K-Means sem novo motivo.
3. **NÃO usar Streamlit** — todo mundo usou ano passado. **Django** é mandatório.
4. **Filtro de elegibilidade ao KPI: usar o campo oficial `Entrou para KPI? == 'SIM'`.** Ele já codifica as três regras juntas: prioridade 1/2/3, `Incidente Pai` vazio e `Status ≠ "Sem Intervenção"`. Resultado: **25.600 elegíveis** (21% de 122.543). Atenção: filtrar apenas por `Incidente Pai` vazio devolve 107.416 registros (88% da base) e está errado. Confirmado pela Locaweb e implementado no `notebooks/02_base_kpi.ipynb`.
5. **Solução agnóstica de cloud provider.** A Locaweb É uma cloud — não amarrar a AWS/GCP/Azure. Usar apenas serviços portáveis.
6. **Entrega via Docker.** Facilita Locaweb pegar e rodar.
7. **Feriados não estão no dataset** — engineering via lib `holidays` BR ou `country_holidays='BR'` do Prophet.
8. **Claude API apenas nos bastidores** — para gerar texto dos alertas e morning brief. NÃO é interface de chat com usuário.
9. **Sem interface conversacional** — Cronos empurra insights proativamente, não espera perguntas.
10. **P2 e P3 SEMPRE juntos, com o mesmo peso.** Toda tela, bloco, gráfico, tabela ou número que
    fala de P3 tem de mostrar P2 do lado. As duas prioridades entram no KPI, cada uma tem meta
    própria, e o P2 é tão ou mais cobrado que o P3. Nunca entregar análise só de P3 — nem "por
    enquanto", nem "porque o dado do P2 dá mais trabalho". Se o dado do P2 não estiver publicado,
    publicar (o `03_previsao_diaria.parquet` já traz P2 com a mesma estrutura, e o `dados.py` já
    calcula `SEMANA2`). Igor já corrigiu isso várias vezes; é o erro que mais se repete.
11. **O SISTEMA NÃO ENXERGA O FUTURO. Os slides enxergam.** São dois artefatos com regras
    diferentes e não se misturam:
    - **Sistema (Django):** simula um relógio parado em **01/10/2025 às 15h**. Só pode mostrar o
      que existe nesse instante — histórico até 30/09, o dia de hoje até as 15h, e previsões para
      frente. **Proibido** exibir realizado de data posterior ao corte: cobertura do modelo
      medida em out–dez, "13 das 50 violações do trimestre", fila com incidente aberto em 08/11,
      máquina do tempo que roda 92 dias com o real. Um líder da Locaweb sentado na ferramenta não
      tem esses dados — e cartão com dado que não existe destrói a credibilidade da tela toda.
    - **Slides/notebooks:** é onde mora a avaliação dos modelos — cobertura, MAE, viés, ROC AUC,
      PR-AUC, backtest, ganho da fila contra o acaso. Ali o período de teste inteiro é legítimo,
      porque o assunto é "o modelo funciona?", não "o que faço no turno".
    Antes de publicar qualquer bloco novo, perguntar: **isso existiria na tela às 15h de
    01/10/2025?** Se a resposta for não, o lugar é o deck.

---

## Os diferenciais do produto

1. **Morning briefing** — resumo automático (Ontem / Hoje / Ações sugeridas) com botão "ver detalhes" para relatório completo. Aparece proativamente, não espera consulta.
2. **Score de saúde por produto** — nota 0-100 por produto com ranking, tendência e explicabilidade.

> **Descartado na Sprint 3:** o "detector de cascata" era o 2º diferencial (Sprint 1/2). Ao testar no dado, a **escalada** foi refutada — 87% das quebras de OLA são de incidentes isolados; taxa de escalada 21% contra ~60% do acaso. O padrão de **acúmulo** citado pela Locaweb na mentoria foi testado em 29/07/2026 e também não se sustentou (backlog diário × quebras: r = -0,139 em dias úteis). Fora do MVP. Ver `docs/sprint-3-mvp.md` → "Testado e descartado".

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
│   ├── locaweb/
│   └── Materal LocalWeb/LW-DATASET.xlsx  ← dataset oficial (o nome da pasta tem typo mesmo)
├── brand/                     ← identidade visual do Cronos
├── data/
│   └── interim/incidentes_kpi.parquet   ← base filtrada (gerada pelo 02_base_kpi)
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

### Conteúdo & escrita

- **`humanizer`** — remove sinais de IA-generated writing em qualquer texto (slides, README, docs). Detecta padrões como inflated symbolism, em-dash overuse, rule of three, vocab AI ("Elevate", "Seamless"), passive voice. Use ao revisar copy de slides/PPT, releases, docs públicas.

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

*Última atualização: 21/07/2026*
