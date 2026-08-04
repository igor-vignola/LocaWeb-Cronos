# Status · onde estamos AGORA

> Primeiro arquivo a consultar para retomar o trabalho. Atualizar a cada bloco concluído.
> O detalhamento técnico da sprint corrente fica em `docs/sprint-3-mvp.md`; a preparação para a banca, em `docs/dossie-banca.md`.

**Atualizado em:** 29/07/2026

---

## Sprint atual: Sprint 3 · MVP Preliminar (entrega 23/08/2026)

| Sprint | Tema | Entrega | Situação |
|---|---|---|---|
| 1 | Ideação | 27/04/2026 | Entregue · nota 5,00/5,00 |
| 2 | Arquitetura | 24/05/2026 | Entregue · nota 5,00/5,00 |
| 3 | MVP Preliminar | 23/08/2026 | **Em andamento** |
| 4 | Solução Final | 08/09/2026 | Futuro |

Único ajuste pedido pelo professor na Sprint 2: slide explícito de gestão ágil. O template da Sprint 3 já tem dois slides dedicados a Kanban e gestão, então isso se resolve na montagem do PPT.

---

## O que está pronto

### Base de dados e análise
- **`notebooks/02_base_kpi.ipynb`** · base compartilhada. Carrega o dataset oficial, tipa as colunas, aplica o filtro de elegibilidade pelo campo `Entrou para KPI?` e grava `data/interim/incidentes_kpi.parquet` (25.600 linhas × 24 colunas: as 19 originais mais 5 de calendário). Tem asserts de invariante (122.543 no total, 25.600 elegíveis) e verificação pós-tipagem.
- **`notebooks/01_eda.ipynb`** · análise exploratória completa, com a investigação da anomalia de setembro rastreável em célula (status "Sem Intervenção" 47 para 17.838, itens de configuração novos 458 para 1.693, descrição mais frequente "Problem: Check Application Monitoring") e o perfil do Team14.

### Modelo 1 · Previsão de volume
- **`notebooks/03_previsao_volume.ipynb`** · executado sem erro, 49 células, 8 figuras em `notebooks/figures/03_previsao_volume/`.
- Prophet com sazonalidade semanal, anual desligada, feriados nacionais, banda de 80%, previsões não negativas; treino restrito a 2025.
- Validado por corte out-of-time e por rolling backtest. Erro divulgado: **P2 com erro médio de 4/dia e P3 de 11/dia** (MAE médio D+1 a D+7).
- Seção 4.10 de robustez: cobertura empírica da banda (P2 entre 86% e 88%, P3 entre 59% e 61%), verificação de que a queda de novembro e dezembro é efeito real e não censura, e o teste da relação entre volume e quebra de OLA.

### Deck da sprint
- **`prototipos/slides/mvp/deck/viewer.html`** · 19 slides navegáveis (seta para baixo troca slide, seta lateral troca variação). Seções: Análise Exploratória e Previsão de Volume.
- Linguagem visual definida: divisória escura com painel de preview, conteúdo em fundo claro com gradiente azul, número sempre rotulado com cor semântica. Gráficos pesados são exportações reais do matplotlib dos notebooks. Ver `memory/deck-mvp-v2-linguagem.md`.

### Preparação para a banca
- **`docs/dossie-banca.md`** · dossiê v2 (100 KB). Produzido por revisão adversarial com quatro perfis de avaliador (machine learning, gestor Locaweb, metodologia acadêmica e cético), cinco auditorias de artefato e uma matriz de conformidade com as 51 exigências das três fontes oficiais. Dos 114 achados brutos, 73 foram verificados um a um contra o dado: 63 confirmados e 10 derrubados. Placar da conformidade: 17 atendidas, 21 parciais, 13 pendentes.
- Um crítico de completude revisou o próprio dossiê e apontou onde ele se contradizia; esses pontos foram corrigidos, incluindo uma resposta que estava invertida sobre a janela de antecedência do alerta.

---

## Achado que define o escopo do produto

Testado em 29/07/2026: o volume diário explica apenas **2,5%** da variação de quebras de OLA (r = 0,159; p = 0,011), medido em dias úteis. Dias de volume alto concentram cerca de 60% mais quebras em absoluto, mas a taxa de quebra é praticamente constante.

Consequência: **a previsão de volume dimensiona carga e projeta o atingimento da meta; o modelo de risco por incidente é o que responde qual incidente vai estourar.** O modelo de risco não é complemento, é a metade que fecha a proposta. Isso está declarado no slide 18 do deck e no dossiê.

---

## O que falta

Em ordem de impacto na nota:

- [ ] **Notebook oficial do risco de OLA** (`04_risco_ola.ipynb`). O modelo está fechado e medido no laboratório: ROC AUC 0,8693, PR-AUC 0,2958, 72% das quebras nos 20% de maior risco, 15 quebras nos 50 primeiros contra 6 da melhor regra simples. Falta destilar o laboratório no notebook limpo. O SHAP foi dispensado: para modelo linear a contribuição é `peso × desvio da média`, calculada de forma exata na seção 9 do laboratório (erro de reconstrução na ordem de 10⁻¹⁵).
- [ ] **Decisão a tomar sobre versionamento do dado (LGPD).** O dataset bruto está versionado e o diretório `data/` não está no `.gitignore`, então o parquet entra no próximo commit. A Sprint 4 exige repositório público. A varredura de 29/07/2026 não encontrou PII (zero e-mails, CPF, telefone ou IP; nenhuma coluna de pessoa; `Aberto por` só tem Manual e Monitoramento), então não há exposição, mas a posição formal precisa ser decidida e registrada. Ver `docs/dossie-banca.md`, seção 2.5.
- [ ] Repetir a varredura de PII no campo `Solução` (texto livre ainda não coberto).
- [ ] Projeção de atingimento das metas anuais a partir da previsão de volume.
- [ ] Score de saúde por produto (segundo diferencial).
- [ ] Telas alimentadas com a saída real dos modelos.
- [ ] Aplicação Django servindo as previsões (regra do projeto; ainda não existe, escopo da Sprint 4).
- [ ] Montagem do PPT da Sprint 3 no template oficial, incluindo os slides de gestão ágil e Kanban.
- [ ] Tratamento da cauda recente da série no desenho do pipeline: o rótulo de elegibilidade depende do fechamento do incidente, então em produção os últimos dias ficam incompletos.

---

---

## Plano até o fim da Sprint 3 e a integração com Django

Traçado em 30/07/2026. Entrega da Sprint 3 em **23/08** (24 dias) e da Sprint 4 em **08/09**.

### Fase 1 · Fechar o modelo de risco (2 a 3 dias)

| # | Item | Situação |
|---|---|---|
| 1.1 | Treino, baselines e avaliação | ✅ feito no lab |
| 1.2 | Quatro gráficos de avaliação | ✅ em `notebooks/figures/04_risco_ola/` |
| 1.3 | Explicabilidade: contribuição por incidente, direto dos pesos | ⏳ próximo |
| 1.4 | Notebook oficial `04_risco_ola.ipynb`, executado e comitado | ⏳ |

### Fase 2 · Fechar as exigências analíticas que faltam (3 a 4 dias)

| # | Item | Por que |
|---|---|---|
| 2.1 | **Agrupar causas recorrentes** (categoria, código de fechamento, descrição) | Exigência 3 do desafio, nunca feita |
| 2.2 | **Projeção de atingimento do KPI**: volume previsto × risco por incidente, comparado à meta anual | Exigência oficial de visualização, hoje pendente |
| 2.3 | Formalizar a detecção de incidentes recorrentes em notebook | Exigência 1, hoje só medido fora de notebook |

### Fase 3 · Produto e entregáveis da Sprint 3 (5 a 7 dias)

| # | Item |
|---|---|
| 3.1 | Telas alimentadas com a saída real dos dois modelos |
| 3.2 | Tela de detalhe do incidente com o texto do motivo (evidência histórica quando houver grupo, contribuição das características quando for caso inédito) |
| 3.3 | Slides do risco, das causas recorrentes e da projeção, na linguagem visual já definida |
| 3.4 | Montagem do PPT no template oficial (14 blocos), incluindo gestão ágil e Kanban |
| 3.5 | Anexar os `.pptx` atualizados das Sprints 1 e 2, como o template exige |

### Fase 4 · Django integrado (a começar antes do fim da Sprint 3)

O template chama o bloco de "versão preliminar do MVP baseado na arquitetura", e a Sprint 4 vem 16 dias depois, com peso em código-fonte e repositório público. Deixar o Django inteiro para a Sprint 4 é risco de cronograma.

| # | Item |
|---|---|
| 4.1 | Esqueleto Django: projeto, app, settings, Docker |
| 4.2 | Camada de serviço que carrega os modelos treinados e serve previsão de volume e fila de risco |
| 4.3 | Views e templates reaproveitando o HTML dos protótipos |
| 4.4 | Rotina de re-treino semanal, com a janela consolidada resolvendo a cauda recente da série |
| 4.5 | Texto do morning briefing pela Claude API, a partir dos números dos modelos |

### Decisões pendentes de definição

- **Versionamento do dado e LGPD**: o dataset bruto está versionado e `data/` não está no `.gitignore`. A Sprint 4 exige repositório público. A varredura de 29/07 não encontrou dado pessoal, mas a posição precisa ser decidida.
- **Calibração da faixa de risco alto**: descartada por ora. O desvio está em 31 incidentes e ajustar sobre esse volume seria ajustar ruído. Limitação declarada.

## Decisões técnicas em vigor

Detalhamento em `context/decisoes-tecnicas.md` e nas regras críticas do `CLAUDE.md`.

- Previsão de volume com **Prophet**; risco de OLA com **regressão logística** (XGBoost apenas como baseline de comparação).
- Proibidos: ARIMA e SARIMA, Streamlit. Django é mandatório, entrega via Docker, solução agnóstica de provedor de nuvem.
- Alvo dos modelos: a **série elegível ao KPI**, não o volume bruto. Treino apenas em 2025 (98% dos casos elegíveis estão nesse ano).
- Diferenciais do produto: **morning briefing** e **score de saúde por produto**.
- Testados e descartados, com número: detector de cascata, padrão de acúmulo, clusterização por DTW, sugestão de realocação de equipe.

---

## Pontos de atenção

- Do feedback da Sprint 1: toda menção de impacto ou benefício precisa vir com número ou gráfico.
- Da mentoria com a Locaweb: dashboard próximo do estilo TIM e Unifique, dado quase em tempo real, duas a três abas no máximo.
- Resolvido em 29/07/2026: as cinco telas da Sprint 2 (`dashboard`, `morning-brief`, `previsao`, `saude-produto`, `cascata`) ainda apresentavam o detector de cascata como funcionalidade viva, inclusive com link de menu e menção a classificador XGBoost. Receberam uma tarja fixa de **referência histórica** explicando que a cascata foi descartada na Sprint 3 e que o protótipo atual é o `mvp-mockup.html`. O `mvp-mockup.html` também foi corrigido: dizia "Prophet + XGBoost" na previsão de volume, quando o XGBoost é apenas baseline de comparação do modelo de risco.

## Bloqueios

- Nenhum no momento.
