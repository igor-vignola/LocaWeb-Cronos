# Rodada 3 · registro acadêmico e os cinco slides que voltam

Leia junto com `BRIEFING.md` (folha de fatos, todo número permitido) e `BRIEFING-2.md`
(contrato de saída, assets locais, sprite de ícones). Aqui está só o que muda.

O Igor escolheu seis dos onze: capa B, equipe B, proposta A, desenho B, descrição A,
tecnologias A. **Não mexa nesses arquivos**, exceto o título, quando esta folha mandar.
Voltam para a mesa: **03, 04, 06, 07 e 08**.

## 1. Registro de escrita, a regra que atravessa tudo

Palavras dele: *"esses títulos não tão legais"*, *"o que eu falei de título direto e
neutro?"*, *"precisamos cuidar com a escrita anti IA, isso é acadêmico, profissional"*.

O defeito não é gramatical, é de **registro**. Os títulos foram construídos como frase de
efeito, em três moldes que se repetem:

- `X, e Y` — "Duas fontes entram, e um campo decide o que conta"
- `Do A ao B` — "Do arquivo da Locaweb ao gestor, dentro de um contêiner"
- veredito com verbo forte — "A nota do ano cai num único mês"

**Substitua por título descritivo**, que nomeia o assunto do slide como cabeçalho de
relatório. Sem inversão, sem aposto espirituoso, sem verbo de impacto, sem vírgula
retórica. O punch continua permitido no bloco de modelagem, onde mora achado; **na abertura,
que é a parte formal da entrega, o título nomeia.**

Vale para o corpo também: nada de "é aqui que a conta aparece", "o que compensa", "quem tem
o volume não tem o risco". Frase declarativa, sujeito e predicado, sem ironia.

**Os títulos aprovados, use exatamente estes:**

| Arquivo | Título |
|---|---|
| `03-contexto-A` e `-B` | Contexto da operação e causas do estouro de OLA |
| `04-problema-A` e `-B` | Atingimento do KPI em 2025 e objetivos para 2026 |
| `05-solucao-A` | Componentes da solução e a métrica de cada um |
| `06-gestao-doc-A` e `-B` | Documentação do gerenciamento e quadro do projeto |
| `07-gestao-plano-A` e `-B` | Cronograma das sprints e divisão do trabalho |
| `08-arquitetura-A` e `-B` | Fontes de dados e regra de elegibilidade ao KPI |
| `09-desenho-B` | Arquitetura da solução em quatro etapas |
| `10-descricao-A` | Descrição dos elementos da arquitetura |
| `11-tecnologias-A` | Tecnologias utilizadas e o papel de cada uma |

## 2. O teto de 45 palavras estava errado

Eu impus 45 palavras de corpo na rodada 2 e o resultado foi o oposto do desejado: o slide 03
ficou *"estranho de ler"* e *"só tem número"*. O problema da rodada 1 nunca foi a quantidade
de palavras, foi **parágrafo sem hierarquia e cartão repetido**.

**Novo alvo: 60 a 90 palavras de corpo**, organizadas. Frase curta com sujeito e verbo é
melhor que rótulo solto. Um número sem uma frase que diga o que ele significa não comunica
nada, e foi exatamente o que aconteceu.

---

# Slide 03 · Contextualização · refazer as duas versões

**A dica do template pede quatro coisas, e hoje o slide faz uma.** Leia a dica inteira:

> "Defina claramente o problema. Qual é a questão a ser resolvida. Considere o contexto em
> que o problema está ocorrendo. Isso pode incluir fatores históricos, sociais, econômicos,
> culturais e políticos que podem estar influenciando a situação. Tente identificar as causas
> raiz do problema. Entenda os fatores que podem contribuir para o problema (podem ser usadas
> ferramentas de análise como: análise SWOT, matriz de impacto e viabilidade, diagrama de
> Ishikawa). Aqui você pode inserir notícias, gráficos, informações da empresa parceira."

As duas versões precisam cobrir, na ordem:

1. **O problema, definido em uma frase.** A operação é medida por um indicador anual de
   violação de OLA por faixa, e a apuração só fecha em dezembro, quando o resultado do ano já
   está formado.
2. **O contexto.** Operação 24 por 7 de hospedagem e cloud para pequeno e médio negócio.
   122.543 incidentes em três anos, dos quais 25.600 contam para a meta. Prazo de 4 horas no
   P2 e 12 no P3.
3. **O fator histórico**, que a dica pede explicitamente: em setembro de 2025 a expansão do
   monitoramento automático multiplicou o volume registrado, de 3.996 para 21.561 no mês, sem
   alterar a série que conta para a meta, que foi de 2.330 para 2.324. Isso separa volume
   registrado de volume relevante, e é um fato de contexto, não um achado nosso.
4. **As causas raiz**, no Ishikawa que já existe. Mas **cada espinha volta a ter uma frase
   curta**, de 6 a 10 palavras, junto do número. Só ícone e número não se lê.

- **A** · Ishikawa como elemento central, com as espinhas voltando a ter frase curta, e uma
  faixa no alto com a definição do problema em uma frase e três números de contexto.
- **B** · duas colunas. À esquerda o contexto em prosa curta e organizada (o que é a
  operação, como ela é medida, o que mudou em setembro de 2025). À direita o Ishikawa
  compacto com as seis causas.

# Slide 04 · Problema a ser resolvido · refazer as duas versões

Ele disse *"aqui também ficou difícil entender qual a mensagem"*. A régua de doze meses está
aprovada como elemento, o que falta é dizer o que ela mostra e o que se pretende alcançar.

O slide precisa deixar legível, sem o leitor ter que decifrar:

1. **que a régua é a régua oficial da Locaweb**, com seis faixas de nota por prioridade, e que
   a cor da célula é a faixa em que o ano estava naquele mês
2. **o que aconteceu**: o P2 acumulou 35 violações até outubro e 41 em novembro, saindo da
   faixa de 125% para a de 75%. O P3 fechou em 196 e permaneceu na faixa de 150% nos doze meses
3. **o que se pretende alcançar**, que é o que a dica do template cobra: fechar o ano dentro
   de 39 violações no P2 e 200 no P3, e conhecer a faixa projetada antes de novembro, e não na
   apuração de dezembro

Escreva isso em frase declarativa, não em rótulo solto. Uma legenda explicando a leitura da
régua vale mais que três cartões de número sem contexto.

- **A** · régua de células, uma frase de leitura abaixo dela, e os objetivos em bloco próprio
- **B** · régua em barras com a linha da meta atravessando, mesma estrutura de texto

# Slides 06 e 07 · Gerenciamento · refazer as duas versões de cada

Ele não escolheu nenhuma das quatro: *"as de gerenciamento não escolhi, acho que pode
melhorar e ficar menos cara de IA"*.

O que dá cara de material gerado nestes dois hoje:

- **selo de situação colorido em toda linha** (`Entregue`, `Em curso`, `Planejada`), que é
  padrão de dashboard e não de documento de projeto
- **chip tracejado com `[responsável]`**, que parece formulário não preenchido
- **ícone decorativo ao lado de cada frente de trabalho**, sem função
- **título contando quantidade** ("Quatro sprints em um quadro", "Quatro entregas em cadência")
- área reservada gigante e vazia dominando o slide

Como resolver:

- **Tabela sóbria em vez de selo colorido.** Coluna de situação em texto, com peso tipográfico
  marcando o que está em andamento. Cor semântica só onde há risco, e aqui não há.
- **`[responsável]` sai do chip** e vira uma linha de texto abaixo do nome da frente, ou uma
  coluna de tabela vazia. Precisa parecer campo a preencher por uma pessoa, não placeholder de
  template.
- **Ícone só onde carrega significado.** Numa tabela de cronograma, nenhum.
- O slide **06** leva o quadro completo e a documentação das sprints. O slide **07** leva o
  cronograma, a divisão do trabalho e o cartão em andamento. Mantenha as áreas reservadas, mas
  **equilibre**: a área não deve passar de metade da largura do slide.

# Slide 08 · Fontes de dados · refazer as duas versões

Veredito dele: *"esse de fonte dos dados tá bemmm feio, muito feio mesmo, pensa em alguma
forma mais interessante de mostrar isso"*.

O conteúdo está certo, a apresentação não. Hoje são duas fichas retangulares com números
soltos e uma faixa embaixo, o que lê como formulário.

O assunto do slide é **de onde o dado vem e o que sobra depois da regra**. Sugestões de
tratamento, escolha duas e desenvolva de verdade:

- **Anatomia do registro.** Mostrar um incidente real do dataset como objeto, com as 19
  colunas nomeadas em volta, destacando as quatro que a regra de elegibilidade lê
  (`Prioridade`, `Incidente Pai`, `Status`, `Entrou para KPI?`). Isso mostra a fonte e a regra
  no mesmo desenho, e é concreto.
- **Duas entradas e um portão.** As duas fontes chegando por caminhos distintos e passando por
  um portão que é o campo oficial, com o que entra e o que fica de fora quantificado. Não como
  funil genérico de três barras, e sim com o campo nomeado no portão.
- **Escala comparada.** 122.543 registrados contra 25.600 elegíveis desenhados em proporção
  real de área, para a diferença ser visível antes de ser lida, com os 107.416 do filtro
  errado marcados como o erro que se evita.

Use as placas locais (`python.png`, `pandas.png`, `holidays.png`) e a placa CSS `xl` para
openpyxl. Uma amostra de linha do dataset é permitida: `INC8654075 · 2 - Alta · lrel ·
31/12/2025 18:06 · 5.443 s · KPI violado NAO`, que está na base.

---

## Verificação

Renderize cada arquivo a 1600x900 com playwright (`channel="chrome"`) e olhe a imagem. Conte
as palavras de corpo, que agora devem ficar entre **60 e 90**. Confira que nenhum título usa
os moldes proibidos, que não sobrou fonte mono, e que nenhuma imagem quebrou.

No relatório final diga, por arquivo: a ideia da versão, a contagem de palavras, e o título
usado.
