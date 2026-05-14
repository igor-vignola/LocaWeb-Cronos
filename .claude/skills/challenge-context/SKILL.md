---
name: challenge-context
description: "Contexto completo do Challenge FIAP 2026 com Locaweb. SEMPRE consulte esta skill antes de produzir qualquer entregável do projeto (PPT, código, análise, documento). Use quando Igor mencionar: challenge, Locaweb, sprint, entrega, projeto, AIOps, incidentes, KPI, OLA, dataset, apresentação, pitch, MVP, arquitetura, ideação, ou qualquer referência ao trabalho da faculdade. Também use quando for gerar slides, analisar dados do LWDATASET, ou preparar qualquer material de entrega. Na dúvida, consulte — é melhor consultar demais do que esquecer um requisito."
---

# Challenge FIAP 2026 — Locaweb — Contexto Completo

## Regra de ouro
- Linguagem simples, sem jargões não explicados
- Explicar conceitos antes de usar termos técnicos
- Não avançar para execução sem que Igor confirme que entendeu
- Dividir respostas longas em partes
- Usar visualizações sempre que possível

---

## Identificação do aluno

- **Nome:** Igor Vignola
- **RM:** 561428
- **Email:** igor.vignola@gmail.com
- **Turma:** 2TSCOA — Tecnólogo Data Science
- **Grupo:** [A DEFINIR — perguntar ao Igor quando necessário]

---

## Sobre o Challenge

O Challenge é uma atividade extensionista da FIAP em parceria com a Locaweb. O objetivo é desenvolver um projeto simulando experiência profissional, aplicando técnicas de ciência de dados em um cenário real.

### Empresa parceira: Locaweb
- Uma das maiores empresas brasileiras de hospedagem, cloud e serviços de internet
- Líder na América Latina
- Focada em PMEs (pequenos e médios empreendedores)
- Operação 24x7 com disponibilidade crítica
- Mentor do projeto: Douglas Gouveia (Gerente Executivo de Operações)

### Tema do desafio
**AIOps — Previsão de Incidentes e Tendências Operacionais**

Aplicação de ciência de dados e machine learning em dados operacionais de TI, com foco em:
- Antecipação de incidentes
- Identificação de padrões
- Redução de riscos operacionais
- Apoio estratégico à tomada de decisão

---

## Objetivos obrigatórios do desafio

Os grupos DEVEM propor solução que:

### 1. Antecipe incidentes
- Previsão de volume para o próximo dia (D+1)
- Previsão de volume para a próxima semana (D+7)
- Identificar possíveis picos operacionais antes que ocorram

### 2. Identifique tendências
- Padrões de crescimento/redução de incidentes
- POR PRIORIDADE: P2 (Alta) e P3 (Média) são OBRIGATÓRIAS
- Agrupados por categoria, produto ou item de configuração

### 3. Projete impacto nos KPIs
- Tendência diária de volume de incidentes
- Risco de perda de OLA
- Pressão operacional futura

### 4. Apoie decisão operacional
- Onde agir preventivamente?
- Quais produtos ou categorias exigem atenção?
- Quais equipes podem ser sobrecarregadas?

---

## Desafios analíticos obrigatórios

### 1. Exploração e engenharia de features
- Identificar sazonalidade (dia da semana, horário, mês)
- Criar agrupamentos críticos (produto + categoria + prioridade)
- Detectar incidentes recorrentes
- Criar variáveis que ajudem modelos a capturar padrões ocultos

### 2. Modelagem preditiva
- Prever volume de incidentes (D+1 e D+7)
- Prever risco de perda de OLA
- Identificar possíveis picos operacionais

### 3. Classificação ou clusterização
- Identificar padrões de incidentes críticos
- Segmentar comportamentos semelhantes
- Agrupar causas recorrentes

### 4. Explicabilidade
- A solução DEVE explicar o que está acontecendo na organização por meio dos dados
- Não basta prever — precisa explicar POR QUE

---

## Dataset — LWDATASET.xlsx

### Estrutura
- **Total de registros:** 122.543 (122.542 + header)
- **Período:** Janeiro/2023 a Dezembro/2025 (3 anos)
- **Campos:** 19 colunas

### Campos do dataset
| Campo | Descrição | Tipo |
|-------|-----------|------|
| Número | ID único do incidente (INCXXXXXXX) | Texto |
| Prioridade | Nível de urgência (1-Crítica a 5-Muito Baixa) | Texto |
| Produto | Produto/serviço afetado | Texto |
| Categoria | Classificação primária do incidente | Texto |
| Subcategoria | Classificação secundária | Texto |
| Grupo designado | Equipe responsável (ex: Team14) | Texto |
| Item de configuração | Ativo de TI com problema | Texto |
| Aberto | Data/hora de abertura | Data/Hora |
| Resolvido | Data/hora de resolução | Data/Hora |
| Encerrado | Data/hora de encerramento | Data/Hora |
| Duração | Tempo em SEGUNDOS entre abertura e resolução | Numérico |
| Código de fechamento | Razão formal do encerramento | Texto |
| Descrição resumida | Título conciso do incidente | Texto |
| Solução | Definitiva, Contorno, ou em branco | Texto |
| Aberto por | Manual ou Monitoramento | Texto |
| Incidente Pai | Referência a incidente relacionado | Texto |
| Status | Ponto atual no ciclo de vida | Texto |
| Entrou para KPI? | SIM ou NAO | Booleano |
| KPI Violado? | SIM, NAO ou N/A | Booleano |

### Distribuição dos dados (números reais do dataset)
- **Por prioridade:** P4-Baixa: 64.828 | P3-Média: 41.731 | P2-Alta: 15.649 | P5-Muito Baixa: 333 | P1-Crítica: 1
- **Por status:** Sem Intervenção: 80.372 | Encerrado Automaticamente: 26.830 | Encerrado: 15.339 | Aguardando Problema: 1
- **Entrou para KPI:** NAO: 96.942 | SIM: 25.600
- **KPI Violado:** N/A: 96.942 | NAO: 25.352 | SIM: 248
- **Aberto por:** Monitoramento: 104.298 | Manual: 18.244

### Regras de KPI (IMPORTANTE — nunca errar isso)

**O que ENTRA para KPI:**
- Apenas incidentes P1, P2 e P3
- Campo "Entrou para KPI?" = SIM

**O que NÃO ENTRA para KPI:**
- Incidentes com "Incidente Pai" preenchido
- Incidentes com Status = "Sem Intervenção"
- Obs: mesmo não entrando no KPI, podem prejudicar outros incidentes

**Tempos de resolução (OLA) por prioridade:**
- P1 (Crítica): até 4 horas
- P2 (Alta): até 4 horas
- P3 (Média): até 12 horas
- P4 (Baixa): até 24 horas
- P5 (Muito Baixa): até 96 horas

**Metas anuais — OLA quebrados (P2-Alta):**
| Quantidade de OLAs quebrados | % de atingimento |
|------------------------------|------------------|
| < 31 | 150% |
| 31 a 35 | 125% |
| 36 a 39 | 100% |
| 40 a 45 | 75% |
| 46 a 53 | 50% |
| > 53 | 0% |

**Metas anuais — OLA quebrados (P3-Média):**
| Quantidade de OLAs quebrados | % de atingimento |
|------------------------------|------------------|
| < 201 | 150% |
| 201 a 230 | 125% |
| 231 a 263 | 100% |
| 264 a 290 | 75% |
| 291 a 320 | 50% |
| > 320 | 0% |

**Metas anuais — Volume total de incidentes (P2-Alta):**
| Volume total | % de atingimento |
|--------------|------------------|
| < 4.585 | 150% |
| 4.585 a 5.388 | 125% |
| 5.389 a 6.168 | 100% |
| 6.169 a 6.252 | 75% |
| 6.253 a 6.336 | 50% |
| > 6.336 | 0% |

**Metas anuais — Volume total de incidentes (P3-Média):**
| Volume total | % de atingimento |
|--------------|------------------|
| < 19.489 | 150% |
| 19.489 a 22.116 | 125% |
| 22.117 a 22.524 | 100% |
| 22.525 a 23.892 | 75% |
| 23.893 a 24.276 | 50% |
| > 24.276 | 0% |

---

## Normas e regras gerais

- Grupos de até 5 alunos
- Troca de componentes permitida até Sprint 3
- Entregas pelo portal FIAP ON (nunca por links)
- Entregas tardias com desconto de nota
- Preferência: arquivos funcionem no Windows
- Todos devem ter cópia dos arquivos como backup
- RMs e nomes sempre em ordem alfabética

---

## Cronograma de sprints

| Sprint | Tema | Data limite | Formato entrega |
|--------|------|-------------|-----------------|
| 1 | Ideação | 27/04/2026 (segunda) | .pptx |
| 2 | Arquitetura | 24/05/2026 (domingo) | .pptx |
| 3 | MVP Preliminar | 23/08/2026 (domingo) | .pptx |
| 4 | Solução Final | 08/09/2026 (terça) | .pptx + .zip + vídeo + planilha |

---

## Critérios de avaliação final (Sprint 4)

### Pesos
| Item | Peso |
|------|------|
| PPT com tópicos do pitch | 10% |
| Vídeo pitch no YouTube (≤5min) | 10% |
| Link da aplicação funcionando | 10% |
| Código-fonte / GitHub público | 20% |
| Avaliação técnica pela banca | 50% |

### Critérios da banca
1. **Alinhamento com o objetivo** — A solução resolve o desafio proposto?
2. **Inovação** — Houve melhorias vs. o que a empresa tem? O grupo foi além?
3. **Usabilidade** — Interface intuitiva e fácil de usar?
4. **MVP em funcionamento** — Funcionalidades esperadas funcionando?
5. **Condução da apresentação** — Slides, síntese, oratória, clareza?

### Etapas pós-entrega Sprint 4
1. Professor tutor + Scrum Master avaliam todos os trabalhos
2. Seleção dos 6 melhores (Top 6)
3. Apresentação ao vivo via Teams (16/09/2026, 19h30)
4. Banca escolhe os 3 melhores
5. Finalistas apresentam no evento NEXT 2026
6. Premiação: shape, camiseta, medalha, voucher em dinheiro + entrada gratuita no NEXT

---

## Entregáveis técnicos obrigatórios

A solução deve ser:
- **Agnóstica a cloud provider** (não depender de AWS/Azure/GCP específico)
- Conter **modelo preditivo documentado**
- Conter **visualizações claras** de tendência diária, projeção de KPIs, risco de OLA
- Conter **recomendações práticas** para a operação

### Liberdade técnica
Qualquer abordagem é permitida:
- Modelos estatísticos, séries temporais, regressão
- Random Forest, XGBoost, redes neurais
- Clusterização, técnicas híbridas

---

## Dicas de fontes externas
O enunciado diz: as fontes fornecidas pela Locaweb são apenas um exemplo. Sinta-se à vontade para incrementar com outras fontes, desde que sejam públicas e fidedignas.

---

## Templates disponibilizados pela FIAP
- Sprint 1: 01Template_IDEACAO_Challenge_2026_01_locaweb_v1
- Sprint 2: 02Template_Arquitetura_Challenge_2026_01_locaweb_v1
- Sprint 3: 03Template_MVP_Preliminar_Challenge_2026_01_locaweb
- Sprint 4: 04Template_SolucaoFinal_Challenge_2026_01_locaweb_v1

(Igor pode ter esses templates — perguntar se precisa deles)
