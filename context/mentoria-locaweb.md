# Mentoria com a Locaweb

Live de mentoria com a equipe da Locaweb (Douglas Gouveia e time) durante a Sprint 2. Insights compartilhados foram capturados pelo Igor e estão sintetizados aqui.

> **Importante:** estes pontos vieram diretamente do cliente. Têm peso forte na avaliação técnica final (50% da nota).

---

## Anomalia de setembro/2025 — INVESTIGAR OBRIGATORIAMENTE

> 🔄 **Correção registrada em 21/05/2026 após análise do dataset:** o registro original desta mentoria dizia "queda anômala". **Os dados mostram o oposto — é uma ALTA anômala.** Ver `prototipos/docs/vocabulario-real.md` seção 11.

A Locaweb mencionou uma **anomalia em setembro de 2025**. Os dados estão corretos (não é registro faltando) — é fenômeno real. Volume mensal observado:

| Período | Volume médio/mês |
|---|---|
| 2023 (ano inteiro) | ~10 incidentes/mês |
| 2024 (ano inteiro) | ~52 incidentes/mês |
| jan–ago/2025 | ~3,5 mil/mês |
| **set/2025** | **21,6 mil** (≈ 5x ago/25) |
| out–dez/2025 | 21,5 k → 23 k → 27,3 k |

**Pedido explícito da Locaweb:** investigar e apresentar a hipótese da causa como destaque na AED.

> *"Vai ser um destaque entregar isso, o motivo."*

**Hipóteses a testar (começar por aqui):**
- **Mudança/expansão de processo interno de monitoramento** (mais sensores capturando mais eventos) ← mais provável dado o salto absoluto
- Migração de plataforma / mudança técnica
- Inclusão de nova base de clientes ou de novos produtos sob monitoração
- Mudança na categorização (eventos que antes eram silenciados viraram incidentes)
- Mudança de operação (terceirização, automação)

**Objetivo:** demonstrar que fomos a fundo nos dados, não fizemos análise superficial.

---

## Sazonalidade — entender corretamente

Pedras de tropeço comuns que a Locaweb levantou:

❌ **NÃO existe sazonalidade por dia da semana isolado** — não é que "incidentes caem na segunda".

✅ **Existe sazonalidade real em:**
- **Feriados** — empresas param de trabalhar, volume despenca
- **Fins de semana** — mesma lógica (parte das empresas para sábado/domingo)

**Implicação técnica:** features de calendário precisam combinar `is_feriado` + `dia_da_semana` corretamente. Não tratar como variáveis independentes.

---

## Padrão de cascata — VALIDADO pela Locaweb

Confirmado tecnicamente: **incidentes P4/P5 frequentemente escalam para P3/P2**.

**Exemplo real dado pelo Douglas:**
> *"Disco em 90% de uso → 95% → estourou. Vira P2."*

**Implicação para o Cronos:**
- O "Detector de cascata" (nosso 2º diferencial) deixa de ser hipótese e passa a ser feature baseada em padrão validado pelo cliente.
- Implementação: monitorar volume de P4/P5 no mesmo produto+categoria, em janela temporal, e disparar alerta quando ultrapassar threshold com histórico de escalada.

---

## Regra do KPI — apenas incidente PAI

**Confirmado:** apenas o **incidente pai** entra no cálculo do KPI. Filhos não.

**Implicação técnica imediata:**
- Toda análise/modelagem de OLA precisa filtrar `Incidente Pai` vazio antes de qualquer cálculo.
- Se ignorar, todos os números ficam inflados.

---

## Times têm especialização

Certos produtos/categorias **já são roteados automaticamente para times específicos**.

**Exemplo:** "banco de dados sem espaço" → time X (responsável por DBs).

**Implicação:**
- Recomendações de alocação do Cronos precisam respeitar essa lógica.
- O campo "Grupo designado" no dataset reflete essa especialização — vale usar como feature.

**Time N1:** primeiro nível de suporte, atende problemas mais simples.

---

## Dashboard — diretrizes confirmadas

**Estilo:** **near real-time** em Django, padrão "dashboard de consumo" (referência: **TIM, Unifique**).

- Interativo, com **2-3 abas** — não exagerar em quantidade de telas
- Sistema "bacana", clean, focado
- Visão clara do estado atual no topo
- Drill-down quando o usuário precisa de detalhe

**Funcionalidades-chave (vindas da mentoria):**

### Probabilidade de atingir KPI — foco forte

> *"Se logo no início do mês temos 2 quebras de KPI, a probabilidade cai muito."*

Mostrar projeção condicional: "dado o que já aconteceu, qual a probabilidade de fechar o mês dentro da meta?". Esse é o tipo de informação que faz o gestor agir antes.

### Previsão do que vai falhar

- Quais itens podem falhar amanhã/depois?
- Se continuar nessa trajetória, atinge o KPI?

### Morning brief — estrutura final

- Resumo curto na tela (Ontem / Hoje / Ações sugeridas)
- Botão "ver detalhes" abre relatório completo
- Não precisa ter "amanhã" como seção fixa — se relevante, entra no resumo

---

## Entrega — diretrizes

### Agnóstico de cloud provider

> *"Não dependa de uma cloud só."*

**Motivo:** a Locaweb É uma cloud provider. Entregar uma solução amarrada à AWS, GCP ou Azure seria constrangedor — estaríamos dizendo que a Locaweb precisa pagar concorrente para usar a nossa solução.

**Implicação:**
- Não usar serviços específicos de cloud (Lambda, S3, DynamoDB, BigQuery, etc.)
- Apenas serviços portáveis: Postgres comum, arquivos locais, etc.

### Docker para entrega

> *"Entrega tudo num Docker, fica fácil para eles testarem o programa e aplicarem."*

Outra equipe levantou na mentoria, Locaweb gostou da ideia.

**Implicação:** containerizar tudo. `docker compose up` e roda. Locaweb pega e testa na infra deles.

---

## Custos da Claude API — apresentação final

**Pedido específico do Douglas:** simular custos dos tokens da Claude API.

**Motivo:** a Locaweb **está avaliando solução para adoção real**. Quer ver expectativa de custo antes de decidir.

**Implicação:** na Sprint 4, incluir slide(s) de simulação de custo:
- Quantos morning briefs por dia
- Tamanho médio do prompt
- Custo por mês/ano
- Comparar com economia esperada (OLAs evitados, etc.)

Esse é um diferencial que outras equipes não vão ter.

---

## Comunicação com a Locaweb

- **Contato principal:** Douglas Gouveia (Gerente Executivo de Operações)
- **Canal:** via Scrum Master do grupo, que aciona o Douglas
- Não contatar Douglas diretamente

---

*Última atualização: 14/05/2026*
