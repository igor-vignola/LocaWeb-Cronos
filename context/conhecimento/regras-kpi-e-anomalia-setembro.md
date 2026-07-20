---
data: 2026-07-20
tipo: conhecimento
status: ativo
relacionados: [alvo-modelagem-serie-kpi]
---

# Regras oficiais de KPI e a causa da anomalia de setembro/2025

## Contexto

Duas coisas que precisamos ter firmes pra Sprint 3: o que exatamente entra no cálculo do
KPI (fonte: `assets/Materal LocalWeb/Dicionário de Dados - v2.docx`) e por que o volume de
incidentes explode em setembro/2025 (pedido explícito da Locaweb na mentoria).

## O que ficou definido

### Regras de elegibilidade ao KPI (texto do dicionário oficial)

- "Somente as prioridades 1, 2 e 3 entram para o KPI."
- "Incidente Pai com valor preenchido não entram no KPI."
- "Status = 'Sem Intervenção' não entram no KPI."
- "A maioria dos incidentes fechados como 'Sem Intervenção' estão associados com Aberto por: 'Monitoramento'."
- Obs oficial: os que não entram no KPI "não significam que não possam prejudicar" os que entram (base do detector de cascata).
- Dois KPIs medidos por ano, por prioridade (P2 e P3): **OLA quebrada** (duração acima do limite) e **volume total tratado**.
- Limites de OLA por prioridade: P1 4h, P2 4h, P3 12h, P4 24h, P5 96h.

**Cuidado (correção de intuição):** não é a origem "Monitoramento" que exclui do KPI.
9.529 incidentes de origem Monitoramento entram no KPI. O que exclui é a regra acima
(pai preenchido, ou Sem Intervenção, ou prioridade 4/5).

### Causa da anomalia de setembro/2025

Volume mensal salta de ~4 mil (ago) pra ~21,6 mil (set) e fica alto até dez. Investigação
(agosto vs setembro) apontou a causa com 4 evidências independentes:

- Todo o salto é origem **Monitoramento** (2.404 → 20.008). Manual fica parado (1.592 → 1.553).
- Status **"Sem Intervenção"** vai de 47 → 17.838 (abre e fecha sozinho, sem humano).
- Entram ~1.700 **ICs novos** no mês (458 → 1.693), ativos que nunca tinham aparecido.
- Alerta que passa a dominar: **"Check Application Monitoring"** (6.590 em set).

**Teoria:** em set/2025 a Locaweb ligou/expandiu o monitoramento automático sobre muitos
ativos novos. A operação não piorou 5×, ela passou a enxergar 5× mais.

**Consequência para os dados:** a série elegível ao KPI é plana em setembro
(2.330 → 2.324). A anomalia vive toda fora do KPI. Ver [[alvo-modelagem-serie-kpi]].

## Por quê

Erro aqui contamina tudo: inflaria KPIs, confundiria o Prophet com uma quebra de regime
falsa, e perderia o "destaque" que a Locaweb pediu (a causa da anomalia). Ter a regra e a
causa por escrito evita retrabalho e desalinhamento entre Ana, Hygor e Igor.

## Como aplicar

- Qualquer cálculo de OLA/KPI: filtrar pela regra oficial antes de contar.
- EDA e slides: a anomalia de setembro entra como achado de destaque (mostra domínio dos dados).
- Modelagem: alvo é a série elegível ao KPI (decisão em [[alvo-modelagem-serie-kpi]]).

## Conexões

- Decisão de modelagem derivada: [[alvo-modelagem-serie-kpi]]
- Mentoria (pedido da anomalia): `../mentoria-locaweb.md`
- Números da Sprint 2: `../../prototipos/docs/vocabulario-real.md` (§11 padrões temporais)

---

*Última atualização: 2026-07-20*
