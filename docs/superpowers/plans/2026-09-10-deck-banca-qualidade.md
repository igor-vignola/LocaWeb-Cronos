# Deck da banca · rodada de qualidade e ajustes

> **Para agentes:** cada tarefa abaixo é fechada em si. Leia a tarefa inteira antes de
> começar, e não toque em arquivo fora da lista **Arquivos** da sua tarefa — há outros
> agentes trabalhando em paralelo.

**Objetivo:** fechar todos os ajustes que o dono do projeto pediu em 10/09/2026 e passar o
deck inteiro por uma revisão de legibilidade, para nenhum slide parecer "print mal tirado".

**Arquitetura:** deck HTML/CSS em `prototipos/slides/ao-vivo/`. Cada slide é um arquivo em
`blocos/NN-nome.html` com um `<style>` e uma `<section>`. O `_montar.py` concatena tudo em
`deck.html`; o `_verifica.py` tira print de cada composição em 1600x900 e acusa defeito.

**Stack:** HTML, CSS, `.venv/Scripts/python.exe` (pandas, matplotlib, playwright).

**Spec:** as mensagens do dono do projeto de 10/09/2026, transcritas em cada tarefa.

---

## Restrições globais

Valem para **toda** tarefa deste plano.

1. Um arquivo de bloco contém, nesta ordem: um `<style>` e uma ou mais `<section
   class="slide light|dark PREFIXO" data-slide="N" data-var="a|b|c" data-quem="igor|ana|hygor">`.
   Nada mais. Sem `<!doctype>`, `<html>`, `<head>`, `<body>`, `<script>` — o montador
   descarta silenciosamente o que não for `<style>` ou `<section class="slide...`.
2. O palco é **1600x900 px fixo**.
3. **Todo o CSS dos blocos vira um arquivo só.** Prefixo de classe é único por bloco;
   confira com `grep -rn "PREFIXO" blocos/*.html`. Nome de `@keyframes` é global; confira
   com `grep -ho "@keyframes [a-zA-Z0-9_-]*" blocos/*.html _estilo.css | sort -u`. Toda
   regra começa pelo prefixo do bloco.
4. Camada de animação pronta: `.rv`, `.rv3`, `.mask`, `.ct` (`data-to`/`data-delay`/`data-dec`),
   keyframes globais `corre` (scaleX), `sobe` (scaleY), `tracar`. Atraso via
   `style="--d:800ms"`. Easing `var(--out)` e `var(--spring)`. Animação presa ao slide
   ativo: `.pref.is-active .coisa{animation:...}`.
5. **Nada termina depois de ~3,4 s** — o verificador tira o print aos 4200 ms.
6. Use `>` no seletor quando o alvo for filho direto.
7. **Contraste mínimo em superfície escura** (fundo `#0A0E17` ou cartão escuro):
   - texto corrido e rótulo: `#B7C0CB` ou mais claro
   - texto secundário: `#A6B0BD` ou mais claro
   - o mais apagado que se admite, e só em rótulo de 10-11px: `#9CA6B4`
   - **proibido** abaixo disso: `#7A8494`, `#5B647A`, `#5F6B7C`, `#4B5563`, `#6B7686`
8. **Tamanho mínimo de texto:** 11px para rótulo em caixa alta com `letter-spacing`, 12,5px
   para qualquer texto de leitura. Nada abaixo disso.
9. Português do Brasil, registro neutro e acadêmico. **Sem copy com cara de IA**: sem
   "Eleve/Descubra/Transforme", sem frase de efeito, sem tríade retórica, sem travessão
   decorativo, sem "ou seja" explicando o próprio número. Sem emoji.
10. A palavra **"turno" é proibida**.
11. **Regra 10 do projeto:** todo bloco que fala de P3 mostra P2 do lado, com o mesmo peso.
12. Todo número precisa sair de uma fonte real do repositório. Não invente número.
13. **Olhe o print.** Depois de montar e verificar, abra `_png/NNv.png` com a ferramenta
    Read e olhe. Não é opcional.
14. Não faça commit. Não rode o verificador no deck inteiro (use os números da sua tarefa).

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `blocos/21-desempenho.html` | **novo** · o resultado do modelo de risco: ROC, PR-AUC, calibração |
| `blocos/20-fila.html` | perde a tira de métricas do pé, fica só com a curva e o painel |
| `blocos/22..33-*.html` | renumerados a partir do 21 antigo |
| `blocos/27-saude.html` | (ex-26) refeito: mais limpo, foco em produto e nota |
| `_estilo.css` | contraste do escuro e o grão que quebra a banda |

---

## Tarefa 1 — Novo slide do desempenho do modelo, e renumeração

**Responsável:** eu (bloqueia as demais; não despachar em paralelo).

**Arquivos:**
- Criar: `blocos/21-desempenho.html`
- Modificar: `blocos/20-fila.html`
- Renomear e renumerar: todos os blocos de `data-slide` 21 em diante
- Modificar: `CONTRATO.md`, `PERGUNTAS.md`

**O pedido, literal:** *"[a tira de métricas do slide 20] texto com cara de IA ein, dá para
melhorar também, não sei, tenta fazer um slide separado para isso, tipo, cada slide terá no
máximo 30 segundos a 1 minuto de apresentação"*.

**Números, todos de `notebooks/04_risco_ola.ipynb` e do `CLAUDE.md`:**

| | regressão logística | gradient boosting |
|---|---|---|
| ROC AUC | 0,869 | 0,868 |
| PR-AUC | 0,2958 | 0,2526 |
| quebras previstas, onde houve 50 | 48,1 | 1.007 com `scale_pos_weight` |

A taxa da base no período de teste é **0,0096** — a PR-AUC de referência. 0,2958 é **31
vezes** isso. O intervalo da PR-AUC entre cortes é **0,2702 a 0,3177**, então o resultado
não depende da escolha de 01/10/2025.

**Passos:**
- [ ] Criar o slide novo, prefixo `.dsp`
- [ ] Tirar `.metrica` do `20-fila.html` e devolver o `.fecho` com a frase da regra simples
- [ ] Renumerar 21→22 … 32→33, arquivos e `data-slide`
- [ ] Corrigir referências em prosa a números de slide
- [ ] Montar, verificar 20 e 21, olhar os dois prints

---

## Tarefa 2 — Slide da nota de saúde, refeito limpo

**Responsável:** agente.

**Arquivo:** `blocos/27-saude.html` (era `26-saude.html`; a Tarefa 1 renomeia antes).

**O pedido, literal:** *"misericórdia, mais um, qualidade horrível, parece pixelado, e tipo,
seja mais objetivo, clean, foco no produto e nota, não parece que tá dando para entrar nele e
ver o que justifica a nota, não parece leal com o que usamos de fato, e tá confuso, cheio
demais, pouco espaço, pesado"*.

Antes disso ele já tinha pedido: *"podemos manter simples, um negócio que mostra a saúde do
produto e destrincha o motivo da nota ao expandir"*.

**O que está errado hoje:** quinze linhas em duas colunas, mais um painel escuro de cinco
colunas embaixo, mais uma linha de conta, mais um rodapé. Sete blocos de informação num
slide só. O painel escuro usa cinza apagado sobre preto e some na projeção.

**O alvo:** dois blocos, não sete. Um lado mostra **o ranking**; o outro mostra **um produto
aberto**, com as cinco medidas que produzem a nota dele. Muito branco. O leitor tem de
entender em dez segundos que a nota tem ranking e tem motivo.

Sugestões, você decide: mostrar os quinze como pontos numa régua de 0 a 100 em vez de quinze
linhas; ou mostrar só os cinco piores com os dez restantes resumidos numa linha. O que não
pode é a densidade de hoje.

**"Leal com o que usamos de fato"** quer dizer: a linha aberta é a tela do produto. Leia
`webapp/painel/servicos.py`, função `saude_lista()` e a constante `COMPONENTES`, e reproduza
o que ela entrega — os cinco componentes com o rótulo oficial, e a posição relativa de cada
um. Rótulos oficiais, sem inventar outros: **Taxa de violação**, **Problemas inéditos**,
**Fechados sem causa**, **Duração mediana**, **Tendência da taxa**.

**Dados:** `data/app/painel.json`, campo `saude`, corte de 01/10/2025. Leia o JSON e confira
cada número. A nota é a média das cinco posições relativas (0 = melhor dos quinze, 1 = pior),
invertida: lvps = (1,000 + 0,533 + 1,000 + 0,400 + 1,000) / 5 = 0,7866 → **21,3**.

O produto a abrir é o **lvps**, o pior dos quinze. Nas duas prioridades: **125 incidentes na
2 com 2 violações, e 185 na 3 com 7** — isso é a regra 10 e não sai.

**Cuidado:** o `lcsi` tem duração mediana de **451,28 h**. Não é erro. Se entrar numa barra
junto com os outros catorze, a escala morre. Deixe a duração fora do ranking ou trate a
escala; não distorça e não esconda.

**Passos:**
- [ ] Ler `servicos.py`, o JSON e o arquivo atual
- [ ] Reescrever o bloco inteiro
- [ ] `_montar.py`, `_verifica.py 27`, abrir `_png/27a.png` e olhar
- [ ] Repetir até o print ficar limpo e legível

---

## Tarefa 3 — Varredura de legibilidade no deck inteiro

**Responsável:** agente.

**Arquivos:** `_estilo.css` e todos os `blocos/*.html`, **exceto** `20-fila.html`,
`21-desempenho.html` e `27-saude.html`, que estão com outros.

**O pedido, literal:** *"todos os slides terão que passar por esse review de qualidade, os
slides devem ser super legíveis, não pixelados, se quiser, usa um agente, mas precisamos
disso"*. E antes: *"esses divisores parecem com baixa qualidade... parece um print mal tirado
que tirou a qualidade"*, *"aqui também, o que aconteceu que parece que tem lugares onde a
qualidade tá ruim? quase nem leio o texto"*.

**O que já foi feito e você não precisa refazer:** a tabela de cinzas do item 7 das
restrições globais já foi aplicada em massa, e `_estilo.css` já tem o grão
(`.dark .grid-bg::after`) que quebra a banda dos degradês.

**O que fazer:** para **cada uma das 48 composições**, abrir `_png/NNv.png` e procurar:

1. texto que você não lê confortavelmente a três metros — cinza fraco sobre escuro, cinza
   fraco sobre branco, azul sobre azul;
2. texto abaixo de 12,5px que não seja rótulo em caixa alta;
3. barra, ponto ou filete que sumiu no fundo;
4. borda de cartão que não separa nada porque tem contraste de menos;
5. texto encostando na borda do cartão, ou em outro texto;
6. número que não terminou de contar, ou elemento que não apareceu.

Corrija subindo cor, corpo ou peso — **sem mudar layout, sem mudar número e sem mudar
texto**. Se um defeito exigir mudar layout, **não mexa**: anote no relatório.

**Passos:**
- [ ] `.venv/Scripts/python.exe prototipos/slides/ao-vivo/_verifica.py` (deck inteiro, uma vez)
- [ ] Abrir os PNG em lotes e anotar cada defeito com arquivo e seletor
- [ ] Corrigir em lote
- [ ] Remontar, reverificar, reabrir os PNG dos que você tocou
- [ ] Relatar: o que corrigiu, e o que precisa de mudança de layout

---

## Tarefa 4 — Fechamento

**Responsável:** eu.

- [ ] `_montar.py` e `_verifica.py` no deck inteiro
- [ ] Conferir que não sobrou referência a número de slide errado
- [ ] Atualizar `CONTRATO.md` §7.9 e o registro das decisões
- [ ] Commit

---

## Fora deste plano, esperando decisão do dono do projeto

- **Slide 25 (agora 26)** — "A meta do ano vai fechar?" segue com quatro composições e ele
  nunca escolheu.
- **`ROTEIRO.html`** — escrito para 25 slides, o deck tem 33.
- **GitHub Pages** — o QR do último slide aponta para `igor-vignola.github.io/LocaWeb-Cronos`,
  que responde 404: falta o push e falta habilitar o Pages.
- **Duração** — ele estimou 20 a 25 minutos com a demo de 5. A banca é de ~15.
