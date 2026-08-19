# Rodada 5 · o bloco analítico volta para a mesa

O Igor revisou o deck inteiro no PowerPoint e apontou slide por slide. Este arquivo é o
contrato desta rodada. **Leia inteiro antes de escrever qualquer linha.**

## O diagnóstico dele, em uma frase

> "tem muita coisa, parece protótipo, muito texto, estilo não muito legal"

E, sobre os títulos, uma instrução que vale para **todos** os slides:

> "tentar deixar o título de todos mais acadêmico e sério, sem ar de IA"

## As sete regras desta rodada

1. **Um slide, uma mensagem.** Antes de escrever, formule a mensagem do slide em uma frase.
   Bloco que não sustenta essa frase não entra. Se você precisa de duas frases, são dois
   slides ou é um slide errado.

2. **Corte metade do texto.** Alvo de **40 a 60 palavras de corpo**, fora título, rótulo de
   eixo e legenda de gráfico. Conte antes de entregar e reporte a contagem.

3. **O gráfico é o protagonista.** Onde existe figura matplotlib, ela ocupa a maior área do
   slide e nada compete com ela. Cartão lateral vira anotação curta, não parágrafo. Se o
   slide tem gráfico e o gráfico não é a primeira coisa que o olho encontra, refaça.

4. **Título descritivo e neutro.** O título nomeia o assunto como cabeçalho de relatório
   acadêmico. Proibidos os moldes que ele reprovou:
   - veredito com verbo forte: "Rigor também é saber o que cortar", "A causa mais comum não é
     a mais perigosa", "O que a operação já viu, ela resolve"
   - inversão espirituosa e paralelismo de slogan: "não é X, é Y", "X, mas não Y"
   - frase de efeito com número no meio: "Uma quebra a cada 103 incidentes"

   Bons: "Taxa de violação de OLA por familiaridade do problema", "Comparação entre regressão
   logística e XGBoost", "Erro do Prophet por horizonte de previsão".

5. **Sem cara de protótipo.** Fora: selo de situação colorido repetido em toda linha, chip
   tracejado de placeholder, ícone decorativo sem função, cartão escuro com "o que isso muda
   na decisão", rodapé explicando como ler o próprio slide.

6. **Nenhum número novo.** Todo número já está nos slides atuais ou na folha de fatos em
   `prototipos/slides/mvp/abertura/BRIEFING.md`. Você está reorganizando apresentação, não
   produzindo análise. Se precisar de um número que não existe, **não invente**: escreva
   `[verificar]` e reporte no relatório final.

7. **P2 e P3 sempre juntos.** Todo bloco que fala de uma prioridade mostra a outra do lado.

## Vocabulário

- **"turno" está proibido.** Trocar por "início do dia", "durante o dia", "no dia".
- Nada de "em um relance", "o terreno", "o gabarito", "a conta aparece".
- Sem travessão em texto corrido. Vírgula, ponto ou dois-pontos.
- Sem emoji.

## Estilo visual, que não muda

Está tudo em `prototipos/slides/mvp/abertura/base.css` e nos slides atuais. Resumo:

- Fonte **Outfit**. Nunca Inter, nunca system-ui como escolha.
- Um azul só, `#2563EB`. Vermelho só para perigo real, verde para resultado bom, âmbar para
  atenção. Sem roxo, sem neon, sem preto puro.
- Slide de 1600 por 900, com topo e rodapé iguais aos atuais.
- Números com `font-variant-numeric: tabular-nums` (classe `.num`).
- Proibido cartão com barra colorida grossa na esquerda.

**Referência aprovada:** o Igor gosta de `d02a` (cartões largos com ícone e número grande),
`d13a` (três cartões com numeral fantasma) e `d24a` (figura grande com anotações curtas ao
lado). Puxe dessas composições.

## O que entregar

Para **cada** slide da sua lista, **duas versões novas**, com sufixo `-r5a` e `-r5b`:

    d03m-r5a.html
    d03m-r5b.html

**Não sobrescreva o arquivo original.** O Igor vai comparar antes e depois.

As duas versões precisam ser **composições diferentes**, não a mesma coisa com outra cor.
Uma delas pode ser conservadora, mantendo a estrutura atual mas cortando texto e arrumando
o título. A outra tem de arriscar uma composição nova.

Renderize e **olhe a imagem** antes de entregar:

    .venv/Scripts/python scripts/renderiza_slides.py --saida _r5 prototipos/slides/mvp/deck/d03m-r5a.html

O script avisa se o conteúdo transborda o quadro. Transbordo reprova a entrega.

## Relatório final

Devolva, por slide: o arquivo original, a mensagem em uma frase, o título antigo e o novo de
cada versão, a contagem de palavras de corpo, e o que muda entre `-r5a` e `-r5b`. Liste
qualquer `[verificar]` que você tenha deixado.
