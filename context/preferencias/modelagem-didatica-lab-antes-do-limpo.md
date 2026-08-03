---
data: 2026-07-21
tipo: preferencia
status: ativo
relacionados: [documentar-em-paralelo-nao-comprimir]
---

# Modelagem é didática: laboratório primeiro, notebook limpo depois

## Contexto

Em 21/07/2026, ao começar a modelagem dos modelos, Igor redefiniu o modo de trabalho. O foco desta fase é o **aprendizado dele** (entender como cada modelo funciona, por que se escolhe cada ferramenta, como treinar/testar/validar), não só a evolução do modelo.

## O que ficou definido

- Para cada modelo, existe um **notebook de laboratório NÃO comitado** em `notebooks/lab/` (gitignored): bagunçado, didático, com experimentos, testes e explicações. É onde se aprende e evolui o modelo.
- Ao finalizar, esse laboratório é **destilado** no notebook limpo e comitado (`notebooks/0X_*.ipynb`), com texto profissional/neutro (ver [[escrita-neutra-deliverables]] no memory).
- Conduzir como **professor**: explicar o conceito, **checar o que Igor já sabe antes** de aplicar, sem pressa, instigando-o a rodar código e entender o porquê.

## Por quê

A nota técnica da banca pesa 50% e exige domínio demonstrado. Igor precisa entender de verdade o que foi feito para defender na apresentação. Além disso, um MVP construído com compreensão é mais robusto que um copiado.

## Como aplicar

- Não despachar modelagem como tarefa; não treinar/plotar sem acompanhar o Igor.
- Explicar termos antes de usá-los (ex: baseline, treino/teste, validação).
- Manter no `.ipynb` só texto sério; explicações conversacionais ficam no chat.

## Conexões

- [[documentar-em-paralelo-nao-comprimir]] — o notebook limpo alimenta o PPT.

---

*Última atualização: 2026-07-21*
