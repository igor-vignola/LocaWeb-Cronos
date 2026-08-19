# Auditoria de consistência do deck · Sprint 3

Feita em 19/08/2026, sobre os 51 slides que entram no `.pptx`. O método foi extrair todo
número de todo slide com o texto em volta, agrupar por valor, e conferir cada divergência
contra `data/interim/incidentes_kpi.parquet`.

**Nenhum número do deck está errado.** O problema é outro, e é mais perigoso: o deck usa
quatro recortes diferentes da base e quase nunca diz qual está usando. Dois slides fazem a
mesma afirmação com números diferentes, e quem cruzar os dois conclui que um deles mente.

## A raiz: quatro bases sem rótulo

| Recorte | Incidentes | Violações | Taxa | Onde é usado |
|---|---|---|---|---|
| 2023 a 2025, base elegível inteira | 25.600 | 248 | 0,97% | abertura, `d02a`, `d10a`, `d21a`, `d22a` |
| Só 2025 | 25.156 | 238 | 0,95% | `04-problema-D`, `d35a` |
| Jan a set/2025, treino do modelo | 19.973 | 188 | 0,94% | `d30a`, `d31a`, `d32a`, `d33a` |
| Out a dez/2025, teste do modelo | 5.183 | 50 | 0,96% | `d24a`, `d25a`, `d26a` |

Os quatro são legítimos e a divisão tem razão de ser: descrição na base cheia, treino e teste
no recorte de 2025. O defeito é não declarar o recorte em cada slide que publica uma taxa.

## As contradições encontradas

### 1. Mesma afirmação, dois números · `d22a` contra `d33a`

Os dois slides publicam a leitura de que a prioridade alta parecia proteger contra o estouro:

| | `d22a` | `d33a` |
|---|---|---|
| Taxa no agregado, P2 | 0,81% | 0,84% |
| Taxa no agregado, P3 | 1,01% | 0,97% |
| Em caso inédito, P2 | 2,27% | 2,11% |
| Em caso inédito, P3 | 1,54% | 1,40% |

Conferido no dado: `d22a` está certo para 25.600 e `d33a` está certo para 19.973. É a mesma
análise em bases diferentes.

**Correção:** a leitura pertence ao `d33a`, que é o slide dedicado a ela. Tirar o cartão
escuro do `d22a`. Isso resolve a contradição e ainda atende o "MUITA COISA MESMO" do Igor.

### 2. Mesmo achado, dois números · `d22a` contra `d31a`

O gradiente de familiaridade aparece nos dois slides:

| | `d22a` | `d31a` |
|---|---|---|
| Caso inédito | 1,60% | 1,46% |
| Rotina conhecida | 0,35% | 0,31% |
| Queda | 4,6 vezes | 4,7 vezes |
| Base | 25.600 | 19.973 |

**Correção:** o achado pertence ao `d31a`. Tirar o gráfico de familiaridade do `d22a`.

### 3. O slide de fechamento contradiz o slide do achado

`d39a` publica **4,6x** para o gradiente. `d31a` publica **4,7x**. O fechamento resume o
bloco, então tem de repetir o número do bloco.

**Correção:** `d39a` passa a 4,7x, ou o slide sai, conforme a decisão do Igor.

### 4. Um slide diz que o modelo de risco ainda não existe

`d17a` traz o modelo de risco em um cartão com o selo **"em desenvolvimento"** e o rótulo
"Modelo 2 · próxima entrega". O modelo foi entregue nesta sprint e ocupa oito slides depois
desse. É a contradição mais cara do deck: ela desmente o próprio MVP.

**Correção:** o selo sai.

### 5. Períodos misturados nas violações por prioridade

O caso que o Igor pegou sozinho. Conferido no dado:

| Período | P2 | P3 | Total |
|---|---|---|---|
| 2023 | 0 | 4 | 4 |
| 2024 | 0 | 6 | 6 |
| 2025 | 42 | 196 | 238 |
| 2023 a 2025 | 42 | 206 | **248** |

`d10a` publica 42 e 206, que é o triênio. `04-problema-D` publica 42 e 196, que é 2025. Como
o P2 tem zero violação em 2023 e 2024, o 42 se repete e parece erro de soma.

**Correção:** rotular o período nos dois. Nenhum número muda.

### 6. Arredondamento do erro do Prophet

O erro médio do Prophet aparece como **4,2 e 11,8** na maioria dos slides, como **4/dia e
11/dia** no `d17a`, e como **4 e 11** no `d39a`.

**Correção:** um formato só, 4,2 e 11,8, com o arredondado permitido apenas em texto corrido
desde que o slide não seja o que publica a métrica.

### 7. Uma figura tinha sido editada à mão

`figs/41_volume_mensal.png`, o gráfico do salto de setembro, não era produzido por nenhum
script. Ele saiu da célula 18 do `notebooks/01_eda.ipynb` e **foi editado depois**: a
anotação dizia "~4 mil" onde o notebook imprime **3.996**. Ou seja, havia um número no deck
sem célula que o reproduzisse, que é justamente o que a regra do projeto proíbe.

**Corrigido** com `scripts/figura_volume_mensal.py`, que lê o Excel oficial e regrava a
figura. Saída conferida: ago/2025 = 3.996, set/2025 = 21.561, salto de 5,4 vezes.

A mesma auditoria vale para `figs/08_comparacao_final.png`, cuja legenda cobria as curvas: a
causa está na célula 4.9 do `notebooks/03_previsao_volume.ipynb`, na linha
`ax.legend(loc='upper left')`. Os valores foram reproduzidos e conferem.

### 8. Um número que nenhuma conta reproduz · `42.155`

O funil de elegibilidade do `d03m` publica três degraus: 122.543 registrados, **42.155 com
tratamento**, 25.600 elegíveis. O primeiro e o terceiro conferem. O do meio não.

Testado contra o Excel oficial:

| Definição | Resultado |
|---|---|
| `Status` diferente de "Sem Intervenção" | 42.170 |
| `Status` em Encerrado ou Encerrado Automaticamente | 42.169 |
| `Status` diferente de "Sem Intervenção", com data de abertura válida | 42.170 |
| `Status` diferente de "Sem Intervenção", com duração preenchida | 42.170 |
| **Publicado no slide** | **42.155** |

Nenhuma leitura razoável chega a 42.155, e a diferença de 15 registros não tem explicação.
O número está dentro da imagem `figs/funil.png`, então corrigir exige regerar a figura.

**Duas saídas.** Trocar por **42.170**, que é reproduzível e vem com definição declarada. Ou
tirar o degrau do meio: o `CLAUDE.md` já determina que o campo oficial `Entrou para KPI?`
codifica as três regras juntas, e exibir um passo intermediário convida exatamente à
confusão que essa regra existe para evitar. A segunda saída é a mais segura.

Aproveitando a mesma verificação: aplicar as três regras à mão devolve **25.751**, contra os
**25.600** do campo oficial. São 151 registros de diferença. Isso reforça a regra do projeto
de usar sempre o campo oficial, e é mais um motivo para não desenhar o filtro como se fosse
uma sequência de peneiras nossas.

### 9. Dois slides davam veredito oposto sobre a mesma projeção

A divisória da seção de projeção e a aba Projeção da aplicação publicavam conclusões
invertidas sobre os mesmos dois números:

| | P2, projeta 43,5 | P3, projeta 208,0 |
|---|---|---|
| Divisória da projeção | **dentro**, contra meta 45 | **acima**, contra meta 200 |
| Aba Projeção | **acima**, contra limite 39 | **dentro** |

Os dois estavam aritmeticamente certos, porque a régua da Locaweb tem seis faixas e cada
slide escolheu uma diferente: 45 é o limite dos 75% no P2, e 200 é o limite dos 150% no P3.

O slide do problema, que é o que define o objetivo do ano, usa **39 no P2 e 263 no P3**, que
é a faixa de 100% nas duas prioridades. **Corrigido:** a divisória passou a usar os mesmos
limites, e o veredito virou *P2 acima, P3 dentro*.

### 10. Multiplicador proibido pela própria folha de fatos

A folha de fatos diz, sobre a concentração por equipe: *"são participações medidas em bases
diferentes. Apresente lado a lado, nunca como múltiplo do tipo 19 vezes"*. O slide de
estrutura operacional publicava exatamente **19×** e **5,7×**.

A verificação mostrou por que a regra existe. Sobre a base cheia de 122.543 registros, o
Team14 tem 75,7% e o Team11 tem 8,0%. Sobre os 25.600 elegíveis, que é a base do indicador,
as parcelas são **35,1% e 34,0%**, praticamente iguais. O múltiplo de 19 vezes nascia de
dividir uma participação medida numa base por outra medida em base diferente.

**Corrigido:** o slide passou a comparar as duas equipes sobre a mesma base, com a taxa de
violação de cada uma, **0,11% contra 1,31%**. A comparação ficou mais forte e passou a ser
metodologicamente defensável.

### 11. Registro informal em quarenta pontos do texto

Levantamento automático de marcas de linguagem informal nos slides que entram no `.pptx`:
44 ocorrências, das quais 40 foram corrigidas. As restantes são vocabulário técnico legítimo
(`baseline`, `rolling backtest`) e um falso positivo.

O que saiu: a contração `pra` em lugar de `para a`, primeira pessoa do plural (*"as decisões
que tomamos"*, *"como validamos, sem enganar a nós mesmos"*, *"não inventamos o que não dá
pra ver"*), coloquialismos (*"enxurrada de alertas"*, *"o grosso do volume"*, *"raio-x"*,
*"furar o prazo"*, *"bater o trivial"*, *"fecham sozinhos"*), o anglicismo *insight*, e nove
paralelismos negativos do tipo *"não é X, é Y"*.

Também foram reescritos os títulos dos slides que não tinham passado pela rodada 5, que ainda
usavam veredito com verbo forte: *"Quem tem o volume não tem o risco"*, *"A operação é grande,
mas estruturada"*, *"O que muda o volume é o dia útil, não o dia da semana"*, *"Usar os 3 anos
ensinaria um crescimento que não existe"*, *"Testar como se fosse a operação real"*.

## A regra que evita a recaída

**Todo slide que publica uma taxa declara a base sobre a qual ela foi calculada**, num rótulo
curto junto do número ou no eixo do gráfico. Exemplos: `base 2023 a 2025 · 25.600 elegíveis`,
`treino: jan a set/2025 · 19.973`, `teste: out a dez/2025 · 5.183`.

E **o mesmo achado aparece uma vez só**. Se dois slides precisam do mesmo número, o segundo
cita o primeiro em vez de recalcular sobre outro recorte.
