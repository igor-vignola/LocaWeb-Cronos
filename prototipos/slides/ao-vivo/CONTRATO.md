# Contrato do deck da banca ao vivo

Fonte única de verdade para quem constrói um bloco de slide deste deck. Se este
documento e a sua intuição discordarem, este documento ganha.

**Contexto.** Banca final do Challenge FIAP 2026 com a Locaweb, em 15/09/2026,
19h30, ao vivo pelo Teams. Seis grupos, cerca de 15 minutos cada. A banca tem
professores e a Locaweb, representada pelo mentor **Douglas Gouveia, Gerente
Executivo de Operações**. Eles **não verão os decks das sprints anteriores**:
este é o único material que passa na frente deles. Três pessoas apresentam.

---

## 1. Registro do texto: o que mais importa

O deck anterior foi reprovado pelo dono do projeto por parecer escrito por
máquina. O defeito era de **forma**, não de conteúdo. Os títulos seguiam todos
o mesmo molde: fragmento de frase, pausa, segundo fragmento.

**Títulos reprovados, do deck anterior:**

- "Dois modelos. Uma pergunta para cada um."
- "Django numa imagem Docker, sem nuvem amarrada."
- "Erro baixo nas duas prioridades. E a projeção fecha."
- "O painel operacional, em seis telas."
- "O dia quase dobra de volume. A taxa de perda não sobe."

**A regra:** título é **uma oração declarativa completa**, no tom de quem
relata um fato a um colega mais graduado. Sujeito, verbo, e o número quando ele
existir. Sem fragmento, sem antítese de dois tempos, sem frase de efeito.

**Proibido em qualquer texto do slide:**

| Padrão | Exemplo do que não fazer |
|---|---|
| Fragmento como título | "Dois modelos. Uma pergunta para cada um." |
| Antítese de dois tempos | "Não é X. É Y." / "A nota não cai. Ela despenca." |
| Frase começando com "E" ou "Mas" | "E a projeção fecha." |
| Travessão em texto corrido | qualquer `—` |
| Regra de três | "rápido, confiável e escalável" |
| Vocabulário de IA | crucial, fundamental, robusto, revolucionar, transformar, potencializar, elevar, garantir (como enfeite), destacar, ressaltar |
| Gerúndio de análise rasa | "garantindo maior eficiência", "refletindo a maturidade" |
| Superlativo sem número | "erro baixíssimo", "altíssima precisão" |
| Emoji | qualquer um |
| Negrito decorativo | negrito só no dado ou no termo técnico, nunca em frase inteira |

**Exemplos de reescrita, para calibrar:**

| Reprovado | Aprovado |
|---|---|
| "Dois modelos. Uma pergunta para cada um." | "A solução separa a previsão de volume do risco por incidente." |
| "Django numa imagem Docker, sem nuvem amarrada." | "A aplicação roda em contêiner e não depende de provedor de nuvem." |
| "O dia quase dobra de volume. A taxa não sobe." | "Dias de volume alto e de volume baixo perdem prazo na mesma proporção." |
| "Erro baixo nas duas prioridades." | "O erro médio é de 4 incidentes por dia na prioridade 2 e 11 na prioridade 3." |

---

## 2. Regras do projeto que não se negociam

1. **Prioridade 2 e prioridade 3 sempre juntas, com o mesmo peso visual.**
   Nenhum bloco, número, gráfico ou tabela fala de uma sem a outra do lado.
   É o erro que o dono do projeto mais corrige.
2. **A palavra "turno" é proibida.** Use "no dia", "durante o dia", "a
   operação", "quem opera". O produto se chama **painel operacional**.
3. **Nenhum número que você não tenha recebido nesta lista.** Não calcule, não
   some, não estime, não arredonde para um número mais bonito.
4. **Nada de dado realizado posterior a 01/10/2025 15h** nas telas do produto.
   Métrica de avaliação de modelo (erro, ROC AUC, calibração, backtest) é
   permitida, porque ali o assunto é "o modelo funciona".
5. **Um slide, uma mensagem.** Se o slide precisa de parágrafo, ele está
   fazendo o trabalho de dois.
6. **Nunca três cartões iguais em fileira.** É o molde que a máquina produz
   sozinha. Prefira composição assimétrica, empilhamento com fio de 1px, ou um
   objeto dominante com apoio ao lado.

---

## 3. As duas variações

Cada slide tem **duas variações**, `data-var="a"` e `data-var="b"`. Elas são
**a mesma mensagem, o mesmo estilo e os mesmos números, em formas diferentes de
apresentar o dado.** Não são duas paletas nem dois títulos diferentes.

Exemplos de par legítimo:

- número gigante rotulado **contra** barra proporcional com o número na ponta
- dois blocos lado a lado **contra** um bloco empilhado com fio divisor
- objeto dominante à esquerda com apoio à direita **contra** objeto centralizado
  com apoio embaixo
- tabela de três linhas **contra** três linhas empilhadas sem grade

O dono do projeto vai alternar com a seta para baixo e escolher. Faça as duas
merecerem ser escolhidas: uma variação claramente pior é trabalho perdido.

---

## 4. Contrato técnico do bloco

Arquivo: `blocos/NN-nome.html`. Ele contém, nesta ordem e **nada mais**:

1. um `<style>` com o CSS só dos seus slides, **todo prefixado pela classe do
   slide** (ex.: `.pb .algo{...}`), para não vazar para os outros blocos
2. as `<section>`, duas por slide

```html
<section class="slide light pb" data-slide="2" data-var="a" data-quem="igor">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd">
    <div class="bi"><svg ...></svg></div>
    <div class="bn">Cronos</div><span class="bt">BANCA FINAL · 15/09/2026</span>
    <div class="tag">Base elegível ao KPI · 2025</div>
  </div>
  <div class="body">
    <span class="eb"><span class="rv" style="--d:260ms">O problema</span></span>
    <h1 class="tt">...</h1>
    ...
  </div>
  <div class="ft"><span>procedência do dado</span></div>
</section>
```

- `data-slide` o número do slide, **igual nas duas variações**
- `data-var` `"a"` ou `"b"`
- `data-quem` `igor`, `ana` ou `hygor`. **Não escreva o marcador de quem
  apresenta:** o `_montar.py` injeta o retrato e o nome na primeira vaga do
  rodapé. Por isso o rodapé leva **um** `<span>`, com a procedência do dado.
- o `.bt` do cabeçalho é sempre `BANCA FINAL · 15/09/2026`
- copie a estrutura de cabeçalho de um bloco existente em
  `../video/blocos/` para o logo SVG sair igual. No slide `.dark` o traço do
  logo é `#0A0E17`, no `.light` é `#fff`.

### Classes compartilhadas, já prontas em `_estilo.css`

`.slide .light .dark .mesh .grid-bg .hd .body .ft .eb .tt .cartao .ic .num`
`.big` (número gigante rotulado) `.apres` (o marcador, injetado)
`.dv` (divisória escura)

### Camada de animação

| Classe | O que faz |
|---|---|
| `.rv` | entra subindo 14px, 0,6s |
| `.rv3` | entra com profundidade, rotateX de 8 graus, 0,8s |
| `.mask` com `<span>` dentro | tipografia entra por máscara de linha, 0,85s |
| `.ct` com `data-to` e `data-delay` | número que conta até o alvo |
| `--d` no `style` do elemento | atraso em ms |
| keyframe `corre` | barra ou trilho que enche, use `transform:scaleX` |

Exemplo: `<span class="rv" style="--d:640ms">`. Escalone os atrasos para a
leitura acontecer na ordem da fala, não tudo de uma vez.

**Altura de barra em pixel, nunca em porcentagem.** Porcentagem de altura não
resolve dentro deste flex e a barra sai com altura zero. Já aconteceu duas
vezes neste projeto.

### Ícones

SVG inline na classe `.ic`, traço 1,5, herdando a cor do contexto. Desenhe os
seus. **Zero emoji.**

---

## 5. Os números, todos medidos em `data/interim/incidentes_kpi.parquet`

**A base · o denominador tem que casar com o numerador**

| recorte | elegíveis ao KPI | perdas de prazo | taxa |
|---|---|---|---|
| 2023 | 87 | 4 | |
| 2024 | 357 | 6 | |
| **2025** | **25.156** | **238** | **0,95%** |
| base inteira, 2023 a 2025 | 25.600 | 248 | 0,97% |

122.543 incidentes no dataset, dos quais 25.600 elegíveis ao KPI, que é 21%.

**Se o slide fala de 2025, o denominador é 25.156 e a taxa é 0,95%.** Usar 238
perdas contra 25.600 elegíveis mistura um ano com três, e foi um erro real que
apareceu na construção deste deck.

**Perdas de prazo · ATENÇÃO AO PERÍODO**

A meta do KPI é **anual**, então o número que se compara com ela é o do ano
fechado. Medido no parquet:

| período | prioridade 2 | prioridade 3 |
|---|---|---|
| 2023 | 0 | 4 |
| 2024 | 0 | 6 |
| **2025** | **42** | **196** |
| base elegível inteira | 42 | 206 |

**Use 42 e 196, e escreva que é 2025.** O 206 é o total de três anos e não pode
ser comparado com uma meta anual: contra a régua do P3 ele cai na faixa de 201 a
230, que vale 125%, enquanto os 196 de 2025 caem abaixo de 201, que vale 150%.
Material antigo do projeto usa 206 como se fosse anual; está errado.

Quando o slide citar o número, deixe o período claro e diga a razão em uma
linha, tipicamente no rodapé: a meta é anual, e a base tem 248 perdas em três
anos.

**Volume não prevê perda de prazo** (261 dias úteis de 2025)
- os 68 dias de maior volume: 108 incidentes por dia, taxa de perda **0,75%**
- os 69 dias de menor volume: 56 incidentes por dia, taxa de perda **0,86%**
- o volume do dia explica **2,5%** da variação das perdas (r = 0,159; p = 0,011)

**Previsão de volume, Prophet**
- erro médio de **4** incidentes por dia na prioridade 2 e **11** na prioridade 3,
  média de D+1 a D+7, validado por backtest deslizante com re-treino por origem
- sazonalidade semanal ligada, anual desligada, feriados nacionais
- cobertura da banda de 80%: entre 86% e 88% no P2, entre 59% e 61% no P3

**Risco por incidente, regressão logística**
- ROC AUC **0,869** contra 0,868 do XGBoost
- PR-AUC **0,296** contra 0,253 do XGBoost
- calibração: prevê **48,1** perdas onde houve **50**
- escolhida por manter a calibração e ser explicável por construção

**Concentração, na base elegível inteira**

| grupo | volume | % da base | perdas | taxa |
|---|---|---|---|---|
| Team09 | 2.058 | 8,0% | 56 | 2,72% |
| Team11 | 8.702 | 34,0% | 114 | 1,31% |
| Team05 | 3.628 | 14,2% | 13 | 0,36% |
| Team14 | 8.973 | 35,1% | 10 | 0,11% |

- Team11 e Team14 atendem praticamente o mesmo volume, diferença de 3%, e a
  taxa do Team11 é **11,8 vezes** a do Team14
- os 30 itens de configuração com mais perdas concentram **61,7%** das perdas

**A stack**
- Django, Docker, Prophet, scikit-learn, pandas, e a Claude API só para redigir
  o texto do resumo diário
- agnóstica de provedor de nuvem, sem serviço proprietário de AWS, GCP ou Azure
- seis abas: Panorama, Previsão, Projeção, Fila de risco, Saúde por produto,
  Causas

**Nunca cite** ARIMA, SARIMA, Streamlit, clusterização por DTW nem detector de
cascata como parte da solução: os quatro foram testados e descartados.

---

## 6. Verificação obrigatória antes de entregar

O chromium que o playwright espera não existe nesta máquina. Use o que está em
disco:

```python
CHROME = r"C:\Users\igor.vignola\AppData\Local\ms-playwright\chromium-1217\chrome-win64\chrome.exe"
navegador = p.chromium.launch(executable_path=CHROME)
pagina = navegador.new_page(viewport={"width":1600,"height":900}, device_scale_factor=1)
```

Monte a sua página de teste em `blocos/_teste-NN.html` juntando o `_estilo.css`
com o seu bloco, e **olhe as imagens com a ferramenta Read**, em cada variação,
no estado final e em pelo menos dois instantes intermediários. Não julgue por
CSS lido.

Procure, e reporte com número:

- vão morto dentro de cartão, que é o defeito mais comum aqui
- texto transbordando o container
- elemento com altura ou largura zero que deveria ter tamanho
- qualquer coisa fora dos limites de 1600x900
- contraste insuficiente para leitura em chamada de vídeo
- as duas variações parecendo a mesma coisa, o que anula o propósito

E rode a varredura de texto: ocorrências de "turno", de travessão, de emoji, e
slide que cita prioridade 3 sem citar prioridade 2.
