# Sprint 3 — MVP Preliminar · documentação de trabalho

Documento vivo. Vai sendo preenchido conforme fechamos cada bloco da modelagem, e é a base do PPT da Sprint 3. Cada seção grande aqui vira um ou mais slides. Não resumir para caber: se está longo, é porque tem trabalho pra mostrar.

**Equipe:** Ana Beatriz Costa de Oliveira · Hygor Abrantes · Igor Vignola — Super Data Bros · 2TSCOA

---

## A anomalia de setembro/2025: o que aconteceu e por quê

### O dado que salta aos olhos

O dataset cobre três anos, de janeiro de 2023 a dezembro de 2025. Só que o volume não se espalha por esses três anos de um jeito nem parecido. Mês a mês:

| Período | Volume/mês |
|---|---|
| 2023 (ano inteiro) | ~10 |
| 2024 (ano inteiro) | ~52 |
| jan–ago/2025 | ~3,5 mil |
| **set/2025** | **21,6 mil** (quase 5× agosto) |
| out/2025 | 23,0 mil |
| nov/2025 | 21,5 mil |
| dez/2025 | 27,3 mil |

2023 e 2024 juntos não passam de ~750 incidentes. Em 2025 o volume já está na casa dos milhares por mês. E em setembro ele quintuplica de uma vez, ficando nesse novo patamar até o fim do ano.

A Locaweb já sabia dessa quebra e foi direta na mentoria: o que interessa é descobrir a causa. Nas palavras do Douglas, "vai ser um destaque entregar isso, o motivo". Então fomos atrás.

### O que testamos

Peguei agosto e setembro de 2025 e quebrei o volume por várias dimensões, procurando qual delas explicava o salto. A resposta apareceu limpa em quatro cortes que não dependem um do outro:

| Corte | Agosto | Setembro | Leitura |
|---|---|---|---|
| Origem: Monitoramento | 2.404 | 20.008 | a explosão está toda aqui |
| Origem: Manual | 1.592 | 1.553 | o humano não mudou nada |
| Status "Sem Intervenção" | 47 | 17.838 | alerta que abre e fecha sozinho |
| Ativos novos no mês (ICs) | 458 | 1.693 | onda de ativos que nunca tinham aparecido |
| Alerta nº 1 do mês | disco cheio | "Check Application Monitoring" (6.590) | health-check de monitoração |

### A conclusão

O salto é inteiro de origem Monitoramento. Os incidentes abertos por gente ficaram em torno de 1,5 mil por mês o ano todo, setembro incluído. Quem multiplicou por cinco foi o monitoramento automático.

Dá pra ir além e dizer que tipo de monitoramento. Os incidentes que apareceram são quase todos "Sem Intervenção", ou seja, abrem e fecham sozinhos sem ninguém encostar (foram de 47 em agosto para 17,8 mil em setembro). Entraram cerca de 1,7 mil ativos novos que nunca tinham dado as caras no dataset. E o alerta que passou a liderar é literalmente "Check Application Monitoring".

Juntando os quatro sinais: em setembro de 2025 a Locaweb ligou, ou expandiu bastante, o monitoramento automático sobre um monte de ativos que antes não eram observados. A operação não piorou cinco vezes. Ela passou a enxergar cinco vezes mais.

### Por que isso muda a modelagem

Aqui o achado deixa de ser bonito e passa a ser útil. Se a gente jogasse os três anos inteiros no Prophet, ele tentaria aprender uma "tendência de crescimento" que não existe. O que houve foi troca do instrumento de medição, não piora da operação.

A saída vem das próprias regras da Locaweb. Pelo dicionário de dados, incidente com status "Sem Intervenção" não entra no cálculo do KPI. Como quase todo o salto de setembro é exatamente isso (monitoramento que se resolve sozinho), a série que importa pro KPI nem sente a anomalia:

| Mês | Volume TOTAL | Volume que entra no KPI |
|---|---|---|
| ago/2025 | 3.996 | 2.330 |
| set/2025 | 21.561 | 2.324 |
| dez/2025 | 27.321 | 1.423 |

O volume elegível ao KPI fica plano em setembro (2.330 → 2.324). Por isso a decisão é modelar a série elegível ao KPI, e não o volume total. Resolve dois problemas ao mesmo tempo: atende ao que o desafio pede (prever os KPIs de P2 e P3) e tira a quebra de regime do caminho do treino.

O ruído de monitoramento não é lixo. O próprio dicionário avisa que os incidentes de fora do KPI "não significam que não possam prejudicar" os que estão dentro. É esse o papel dele na nossa solução: sinal do detector de cascata (P4/P5 se acumulando antes de escalar pra P3/P2), não alvo de previsão.

---

## Decisão de modelagem (alvo dos modelos)

Fechada em 20/07/2026, com base no dicionário oficial e na investigação acima.

- **Prophet** prevê o volume diário **elegível ao KPI** (D+1 e D+7), separado por P2 e P3.
- **XGBoost** estima o risco de estourar a OLA sobre essa mesma base.
- Filtro que define "elegível ao KPI": `Incidente Pai` vazio, prioridade 1/2/3, `Status ≠ Sem Intervenção`. Na prática é o campo `Entrou para KPI? = SIM`.
- O que fica de fora do KPI (P4/P5, monitoramento que fecha sozinho) alimenta o **detector de cascata**, em notebook próprio.

Detalhe que corrige uma intuição inicial: não é a origem "Monitoramento" que exclui do KPI. Tanto que 9.529 incidentes de origem Monitoramento entram no KPI. O que exclui é a regra acima.

---

## Seções a preencher (conforme a modelagem avança)

- [ ] Contextualização do problema (atualiza Sprints 1 e 2)
- [ ] Proposta de solução (atualiza Sprints 1 e 2)
- [ ] Gestão do projeto / Kanban (resolve o feedback da Sprint 2)
- [ ] Arquitetura da solução (atualiza Sprint 2, com fontes de dados)
- [ ] EDA: sazonalidade real (feriado + fim de semana)
- [ ] EDA: distribuição operacional e produtos/grupos críticos
- [ ] Modelo Prophet: setup, resultado, leitura
- [ ] Modelo XGBoost + SHAP: risco de OLA e explicabilidade
- [ ] Clusterização DTW
- [ ] Detector de cascata
- [ ] MVP nas telas (prints com saída real)
