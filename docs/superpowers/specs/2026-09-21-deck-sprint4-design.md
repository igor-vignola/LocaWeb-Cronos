# Deck da Sprint 4 · desenho

Data: 21/09/2026. Entrega no portal: 21/09/2026, 23h59. Decisões tomadas com o Igor nesta
sessão; onde este documento e a intuição discordarem, este documento ganha.

## O que é

O `.pptx` da Sprint 4 (`sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx`),
nos sete blocos do template oficial, construído sobre o deck da banca de 15/09/2026. O
rascunho atual, no estilo da Sprint 3, é descartado.

Duas saídas do mesmo builder:

- `prototipos/slides/sprint4/deck.html`, navegável por seta, para revisão no navegador.
- o `.pptx`: 13,333 × 7,5 in, um PNG por slide, fala nas notas do apresentador.

## Fontes

| Fonte | O que dá | Onde |
|---|---|---|
| Deck da banca | 33 slides, folha de estilo, contrato | `prototipos/slides/ao-vivo/` |
| Deck do pitch | o slide de objetivo, versão A | `prototipos/slides/pitch/blocos/06-objetivo.html` |
| Sprint 3 | o slide de código-fonte, como está | `prototipos/slides/mvp/abertura/12-codigo-C.html` |
| Prints da aplicação | dez capturas, 3200 × 2000 | `sprints/sprint-3/prints/` |
| Roteiro da banca | a fala de cada slide, vira nota | `prototipos/slides/ao-vivo/ROTEIRO.html` |
| Números | seção 5 e adendos | `prototipos/slides/ao-vivo/CONTRATO.md` |

## A ordem · 59 slides

| # | Bloco do template | Slides | Origem |
|---|---|---|---|
| 1 | Equipe e projeto | capa · **divisória** · equipe · Cronos, o nome · **descrição resumida** | banca 1, 2, 3 |
| 2 | Compreendendo o desafio | **divisória** · prazo · quebras 2025 · fila fora de ordem | banca 4, 5, 6 |
| 3 | Objetivo | **divisória** · objetivo | pitch A, mais linha de apoio que começa por verbo |
| 4 | Projeto realizado | **divisória** · **abordagem** · banca 7 a 30 · código-fonte | Sprint 3 como está |
| 5 | Demonstração | **divisória** · aplicação · **mapa das abas** · **10 telas com balões** · acesso com QR | banca 31 e 33 |
| 6 | Vídeo | **vídeo** | sem divisória: bloco de um slide |
| 7 | Conclusão | **divisória** · **síntese** · **aprendizados** · **limitações** · **próximos passos** · obrigado | banca 32 |

Em negrito, o que nasce agora: 6 divisórias e 13 slides de conteúdo. As sete divisórias de
seção da banca continuam dentro do bloco 4.

Decisões de ordem já fechadas: a divisória do bloco 1 vem depois da capa; fontes de dados
é um cartão do slide de abordagem, não um slide; o bloco 6 não tem divisória.

## Regras de forma

1. **Estilo da banca em tudo o que nasce agora.** `_estilo.css` lido de onde está, blocos
   novos em `prototipos/slides/sprint4/blocos/NN-nome.html`, no contrato do `CONTRATO.md`
   seção 4. Sem `data-quem`; o marcador de quem apresenta não existe neste deck.
2. **Divisória de bloco tem desenho próprio**, para não se confundir com a divisória de
   seção da banca. Duas propostas, uma clara e uma escura, escolhidas pelo Igor vendo.
   Nenhum slide de dentro leva rótulo de bloco.
3. **Telas na forma A** (layout da Sprint 3: moldura de navegador, coluna de texto), com
   balões numerados sobre o print apontando cada funcionalidade e legenda numerada que diz
   o que é e qual modelo está por trás. É a resposta ao único ponto negativo da Sprint 3
   ("faltou detalhar o funcionamento visual, prints funcionais do MVP em si").
4. **Slides da banca entram byte a byte**, com três ajustes: sem marcador; slide 2 troca
   "Quem apresenta" por "A equipe"; slide 31 troca a pastilha "Demonstração ao vivo" por
   "Demonstração da solução". Alguns ganham **linha de apoio** abaixo do título quando o
   título sozinho não fecha a mensagem; a lista é proposta ao Igor antes de entrar.
5. **Notas do apresentador em todo slide.** Banca: a fala do roteiro. Telas: o texto de
   uso real. Novos: escrita junto com o slide.
6. **Números só do `CONTRATO.md`.** Nenhuma conta nova. O erro da previsão escreve-se
   4,2 e 11,8, como no slide 18 da banca.
7. **Fora do deck:** testado e descartado (cascata, acúmulo, DTW, XGBoost), qualquer
   realizado depois de 01/10/2025 15h nas telas, a palavra "turno", travessão, emoji.
8. **P2 e P3 sempre juntos**, em todo slide novo.

## Como o builder funciona

`scripts/monta_deck_sprint4.py`, reescrito. Uma lista `ORDEM` com três tipos de item: número
de slide da banca, nome de bloco próprio em `sprint4/blocos/`, e caminho de HTML pronto (o
código-fonte da Sprint 3). Para cada item:

- lê a `<section>`, resolve contadores para o valor final, reancora caminhos de imagem;
- aplica os ajustes de texto e a linha de apoio, por mapa;
- escreve o `deck.html` com todos os slides, no visualizador do pitch;
- renderiza um PNG por slide em 1600 × 900 a 2×, com a animação congelada no estado final
  (o mesmo congelamento do `_comparar.py`), sem esperar os 4,2 s por slide;
- monta o `.pptx` com a nota de cada slide.

O slide da Sprint 3 e as dez telas usam a folha `mvp/abertura/base.css`; os demais, a da
banca. Cada `<section>` vai para o PNG a partir do próprio HTML, então as duas folhas não se
misturam na mesma página.

## Processo de revisão

1. **Esqueleto primeiro.** O deck inteiro com os 59 slides na ordem final: os reaproveitados
   já no lugar, e um slide de espera em cada posição nova dizendo "Aqui irá ficar: X", com
   uma linha do conteúdo e a origem. O Igor vê o que o espera.
2. **Lotes de três**, do início ao fim, só dos slides que precisam de trabalho. Cada lote
   é aberto no navegador dele (`deck.html`), avaliado, e só então vem o próximo.
3. **Fecho:** `deck.html` completo, `.pptx`, e o relatório da varredura.

## Verificação

- Cada slide novo: medição do `_verifica.py` (vão morto, fora do palco, invisível,
  dimensão zero), e o PNG olhado sozinho em 1600 × 900.
- Deck inteiro: varredura de texto por "turno", travessão, emoji, e P3 citado sem P2.
- `.pptx`: 59 slides, 13,333 × 7,5 in, uma imagem por slide, nota presente em todos, URL
  da aplicação e do vídeo iguais às publicadas.
