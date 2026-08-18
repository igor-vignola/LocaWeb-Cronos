# Quadro do projeto no Trello · cards para montar

Como usar: crie o quadro **Cronos · Challenge FIAP 2026** com as cinco colunas abaixo e
cole um card por item. Todo card aqui descreve trabalho que de fato aconteceu, e a data
entre parênteses é a real, tirada de `context/status.md` e do histórico do repositório.

**Você preenche os responsáveis.** Eu não sei quem fez o quê, e inventar isso no card é
exatamente o que a banca vai perguntar. Onde escrevi `[responsável]`, troque pelo nome.

Etiquetas sugeridas: `Sprint 1`, `Sprint 2`, `Sprint 3`, `Sprint 4`, `Análise`, `Modelagem`,
`Aplicação`, `Entregável`.

---

## Coluna 1 · Backlog

**Publicar a aplicação num provedor**
Subir o contêiner e deixar a URL acessível para a banca.
Etiquetas: `Sprint 4` `Aplicação`

**Gravar o vídeo pitch de 5 minutos**
Roteiro em seis blocos, hands-on mostrando as seis abas. Upload no YouTube público.
Etiquetas: `Sprint 4` `Entregável`

**Simular o custo de operação da Claude API**
Pedido do Douglas na mentoria: quantos briefings por dia, tamanho médio do prompt, custo
mês e ano.
Etiquetas: `Sprint 4`

**Definir a posição sobre versionar o dado em repositório público**
A Sprint 4 exige repositório público. A varredura não achou dado pessoal, mas falta
decidir e registrar a posição.
Etiquetas: `Sprint 4`

**Repetir a varredura de dado pessoal no campo Solução**
Texto livre, ainda não coberto pela varredura.
Etiquetas: `Sprint 4`

---

## Coluna 2 · A fazer

**Atualizar os anexos das Sprints 1 e 2**
Os dois PPT ainda declaram XGBoost para risco, clusterização por DTW e o detector de
cascata. Precisam sair alinhados ao que foi medido depois, senão o material se contradiz.
Etiquetas: `Sprint 3` `Entregável`

**Acrescentar as referências bibliográficas**
Artigo do Prophet, definição de MAE e o protocolo de rolling backtest.
Etiquetas: `Sprint 3` `Entregável`

**Subir o arquivo final no portal FIAP ON**
Conferir nome do arquivo e formato antes de enviar.
Etiquetas: `Sprint 3` `Entregável`

---

## Coluna 3 · Em andamento

**Montar o PPT da Sprint 3** ← *este é o card do print aberto, detalhado no fim*
Etiquetas: `Sprint 3` `Entregável`

**Destilar em notebook os números do descarte da cascata**
Os três números (87% de violações isoladas, escalada de 21% contra os 60% do acaso)
ficaram em notebook de laboratório e não têm código versionado que os reproduza.
Etiquetas: `Sprint 3` `Análise`

---

## Coluna 4 · Em revisão

**Revisar o deck contra o checklist da sprint**
Percorrer item por item do template antes de fechar o arquivo.
Etiquetas: `Sprint 3` `Entregável`

---

## Coluna 5 · Concluído

**Ideação do projeto** (27/04)
Nome, problema, público, proposta e comparativo de mercado. Entregue com nota 5,00.
Etiquetas: `Sprint 1` `Entregável`

**Caracterização inicial do dataset** (maio)
122.543 incidentes, 19 colunas, janeiro de 2023 a dezembro de 2025.
Etiquetas: `Sprint 1` `Análise`

**Mentoria com Douglas Gouveia, da Locaweb** (maio)
Saíram duas hipóteses para testar: cascata de prioridade e acúmulo de backlog. As duas
entraram no backlog.
Etiquetas: `Sprint 2`

**Definir a arquitetura e as tecnologias** (maio)
Desenho do pipeline e escolha da stack, com justificativa por elemento.
Etiquetas: `Sprint 2`

**Protótipos das telas do dashboard** (maio)
Cinco telas em HTML para validar a ideia antes de escrever aplicação.
Etiquetas: `Sprint 2` `Aplicação`

**Entrega da Arquitetura da Solução** (24/05)
Entregue com nota 5,00. O professor pediu um slide explícito de gestão ágil.
Etiquetas: `Sprint 2` `Entregável`

**Fechar a base compartilhada com o campo oficial de KPI** (julho)
Filtro por `Entrou para KPI?`, 122.543 para 25.600 linhas, com asserts travando as duas
contagens. Todos os outros notebooks leem esse parquet.
Etiquetas: `Sprint 3` `Análise`

**Investigar a anomalia de setembro de 2025** (julho)
Volume salta de 4 mil para 21,6 mil no mês. Causa: expansão do monitoramento automático,
não piora da operação. A série que vale para o KPI atravessa intacta.
Etiquetas: `Sprint 3` `Análise`

**Definir alvo e escopo da modelagem** (20 e 21/07)
Foco em P2 e P3 separados, treino restrito a 2025, sazonalidade anual desligada por falta
de dado.
Etiquetas: `Sprint 3` `Modelagem`

**Treinar e validar a previsão de volume** (julho)
Prophet contra dois baselines, com rolling backtest. Erro de 11,8 por dia no P3 e 4,2 no P2.
Etiquetas: `Sprint 3` `Modelagem`

**Testar a hipótese de cascata do mentor** (julho)
Não se confirmou: 87% das violações são de incidentes isolados. Sai do MVP.
Etiquetas: `Sprint 3` `Modelagem`

**Testar a hipótese de acúmulo de backlog** (29/07)
Correlação de −0,139 entre backlog diário e violações. O sinal aponta para o lado contrário.
Etiquetas: `Sprint 3` `Modelagem`

**Rodar as verificações de robustez** (29/07)
Cobertura da banda, censura à direita e a relação entre volume e violação.
Etiquetas: `Sprint 3` `Modelagem`

**Escolher a regressão logística no lugar do XGBoost** (03/08)
PR-AUC 17% maior e calibração honesta: 48,1 violações previstas onde houve 50.
Etiquetas: `Sprint 3` `Modelagem`

**Escrever os notebooks de risco, causas e projeção do KPI** (04/08)
Notebooks 04, 05 e 06.
Etiquetas: `Sprint 3` `Modelagem`

**Construir o score de saúde por produto** (05/08)
Cinco componentes com peso igual, nota de 0 a 100, com teste de sensibilidade.
Etiquetas: `Sprint 3` `Modelagem`

**Subir a aplicação Django com as seis abas** (agosto)
Uma URL por aba, gráficos em SVG no servidor, contêiner que só lê parquet.
Etiquetas: `Sprint 3` `Aplicação`

**Auditar os números da tela contra os notebooks** (11 a 14/08)
Achou a escada do KPI invertida e três notebooks medindo fora da janela da aplicação.
Corrigidos e reexecutados.
Etiquetas: `Sprint 3` `Aplicação`

**Auditoria visual das seis abas** (17/08)
41 capturas em quatro larguras. 32 achados corrigidos, incluindo um gráfico cuja barra
contradizia o número impresso.
Etiquetas: `Sprint 3` `Aplicação`

**Capturar os prints da aplicação para a entrega** (17/08)
Seis abas e quatro modais, por script, para o enquadramento ser igual em todos.
Etiquetas: `Sprint 3` `Entregável`

---

## O card do print aberto

Abra **Montar o PPT da Sprint 3** e tire a captura com a descrição e o checklist à vista.

**Descrição:**

> Montar o PPT da Sprint 3 na ordem do template da FIAP, reunindo num arquivo só o bloco de
> análise e modelagem e os prints da aplicação. Formato .pptx, 16:9.
>
> Entregáveis do card: arquivo .pptx nomeado no padrão da FIAP, prints da aplicação e os
> anexos atualizados das sprints anteriores.

**Data de entrega:** 23/08/2026
**Etiquetas:** `Sprint 3` `Entregável`
**Membros:** [responsável]

**Checklist · Conferência do template** (marque os cinco primeiros, deixe os dois últimos
abertos, que é a situação real)

- [x] Identificação da equipe com RM em ordem alfabética
- [x] Contextualização, problema e proposta atualizados
- [x] Arquitetura e descrição das tecnologias
- [x] Prints da aplicação com explicação de cada tela
- [x] Amostra dos dados utilizados
- [ ] Imagem do quadro de planejamento
- [ ] Anexos atualizados das Sprints 1 e 2

**Comentário** (um só, seu, se quiser dar textura):

> Deck fechado em 63 slides. Falta o print do quadro e os anexos.
