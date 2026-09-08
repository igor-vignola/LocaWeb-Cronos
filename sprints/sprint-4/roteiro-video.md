# Roteiro do vídeo pitch · Sprint 4 · Cronos

**Duração alvo:** 5 minutos (limite do enunciado). Total escrito: cerca de 700 palavras.
**Formato:** hands on. Uma voz (Igor).
**Como gravar:** sete takes curtos, gravados separadamente e emendados. Nenhum take passa de
50 segundos. Se errar, regrava só aquele take.

> Marcação: `[TELA]` diz o que aparece. `//` é pausa de respiração.
> Leia devagar. O texto foi medido em 140 palavras por minuto, que já é ritmo calmo.

---

## TAKE 1 · Abertura · 0:00 a 0:25

`[TELA]` Slide 1, capa do Cronos.

> Meu nome é Igor Vignola, do grupo Super Data Bros, turma 2TSCOA. //
> Este é o Cronos, um sistema de previsão de incidentes operacionais construído sobre o
> histórico da Locaweb. //
> Em cinco minutos eu mostro o problema que ele resolve, o que os dados nos disseram, e a
> aplicação funcionando.

---

## TAKE 2 · O problema · 0:25 a 1:10

`[TELA]` Slide 2, o gráfico de violações acumuladas contra as faixas da meta.

> A Locaweb mede a operação por OLA, o prazo de resolução de cada incidente. //
> A meta é anual e funciona em degraus: o número de OLAs quebrados no ano define a nota da
> operação. //
> Em 2025, na prioridade 2, a contagem saiu de trinta e cinco violações em outubro para
> quarenta e uma em novembro. //
> Seis violações em um único mês atravessaram duas faixas da meta de uma vez. //
> O problema não é o volume de incidentes. É que ninguém sabe, no dia, qual incidente aberto
> vai virar a próxima violação.

---

## TAKE 3 · O achado que definiu o produto · 1:10 a 1:45

`[TELA]` Slide 3, a dispersão de volume contra quebras.

> A primeira hipótese óbvia é que dias movimentados quebram mais OLA. //
> Testamos, e ela é fraca: o volume diário explica apenas dois e meio por cento da variação
> de quebras. //
> Dias cheios concentram mais violações em número absoluto, mas a taxa de quebra é
> praticamente constante. //
> Isso dividiu a solução em duas metades. Prever volume dimensiona a carga do dia. Para saber
> qual incidente vai estourar, é preciso um modelo por incidente.

---

## TAKE 4 · A solução · 1:45 a 2:15

`[TELA]` Slide 4, a arquitetura.

> São dois modelos. //
> O Prophet prevê o volume de incidentes elegíveis ao KPI para os próximos sete dias, com
> sazonalidade semanal e feriados nacionais. //
> Uma regressão logística estima a probabilidade de cada incidente aberto estourar o prazo. //
> Escolhemos regressão logística e não gradient boosting porque ela mantém a calibração, e a
> calibração é o que permite projetar a meta do ano. //
> A aplicação é Django em Docker, sem dependência de provedor de nuvem.

---

## TAKE 5 · Demonstração · 2:15 a 4:15

Este é o take mais longo. Grave em cinco pedaços, um por tela.

### 5a · Panorama · 25 segundos
`[TELA]` Aba Panorama, e abra o modal do briefing.

> Esta é a tela que a operação abre no início do dia. //
> O briefing é escrito automaticamente: o que aconteceu ontem, o que se espera hoje, e onde
> agir. //
> Prioridade 2 e prioridade 3 aparecem sempre lado a lado, porque as duas entram no KPI e
> cada uma tem meta própria.

### 5b · Previsão · 25 segundos
`[TELA]` Aba Previsão.

> Aqui está a previsão de volume para sete dias, com a banda de incerteza. //
> O erro médio é de quatro incidentes por dia na prioridade 2 e onze na prioridade 3. //
> Abaixo, o padrão semanal e a curva de chegada ao longo do dia, que difere entre as duas
> prioridades.

### 5c · Projeção do KPI · 25 segundos
`[TELA]` Aba Projeção, e abra a régua da meta.

> Esta tela projeta onde o ano fecha. //
> O volume previsto multiplicado pelo risco por incidente dá a projeção de violações, e ela é
> comparada com a escada da meta. //
> A leitura hoje: a prioridade 3 está dentro da faixa, e a prioridade 2 está acima dela.

### 5d · Fila de risco · 30 segundos
`[TELA]` Aba Fila, e abra o detalhe de um incidente.

> Esta é a fila. Cada incidente aberto recebe uma probabilidade de estouro, e a lista está
> ordenada por ela. //
> Abrindo um incidente, a tela mostra por que ele está ali: quando existe histórico do mesmo
> agrupamento, ela mostra a evidência histórica; quando é um caso inédito, mostra a
> contribuição de cada característica. //
> Isso responde a exigência de explicabilidade do desafio.

### 5e · Saúde por produto · 15 segundos
`[TELA]` Aba Saúde.

> E aqui, uma nota de zero a cem por produto, com a decomposição do que puxa a nota para
> baixo e quem atende cada um.

---

## TAKE 6 · Resultados · 4:15 a 4:40

`[TELA]` Slide 5, as métricas.

> Nos números: a previsão de volume erra quatro incidentes por dia na prioridade 2 e onze na
> prioridade 3, validada por backtest deslizante. //
> O modelo de risco tem área sob a curva de zero vírgula oitocentos e sessenta e nove, e
> mantém a calibração: prevê quarenta e oito vírgula um quebras onde houve cinquenta. //
> O gradient boosting que testamos como comparação empata na ordenação e perde na precisão do
> evento raro.

---

## TAKE 7 · Limitações e fecho · 4:40 a 5:00

`[TELA]` Slide 6.

> Três limitações que assumimos. //
> A cobertura da banda de previsão cai na prioridade 3 quando a base muda de patamar, e não
> há alarme automático para isso. //
> Três hipóteses que propusemos nas sprints anteriores foram testadas e descartadas com dado,
> incluindo o efeito cascata. //
> E o dataset não tem custo por violação, então o ganho que defendemos é ordenação da fila, não
> redução de volume. //
> O Cronos está no ar em Docker, e o código está no repositório público. Obrigado.

---

## Notas de produção

**Como capturar a tela.** O caminho mais rápido, sem instalar nada: abra uma reunião do Teams
só com você, compartilhe a tela, grave, e baixe o mp4. Alternativa nativa do Windows:
`Win + G`, a barra de jogo grava a janela ativa.

**Ordem de gravação sugerida.** Grave o TAKE 5 primeiro, com a aplicação aberta, enquanto ela
está rodando e fresca na cabeça. Os takes de slide são mais fáceis e podem vir depois.

**Onde publicar.** YouTube. Marque como público, não como não listado: o enunciado pede
permissão pública de acesso, e público não deixa dúvida.

**Se o tempo estourar.** Corte primeiro o 5e (saúde por produto) e depois a terceira frase do
TAKE 6. São os dois trechos cuja ausência menos compromete a nota.
