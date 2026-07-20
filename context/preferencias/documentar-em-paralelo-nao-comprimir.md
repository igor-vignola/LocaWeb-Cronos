---
data: 2026-07-20
tipo: preferencia
status: ativo
relacionados: [prototipo-reflete-arquitetura, setup-ambiente-modelagem-windows]
---

# Documentar em paralelo à modelagem — e nunca comprimir o trabalho em poucos slides

## Contexto

Início da Sprint 3 (MVP Preliminar). Igor definiu como quer que a entrega seja
construída: à medida que treinamos os modelos, ir **documentando em paralelo** num
`.md` que depois vira os slides — pra não perder contexto do que foi feito e por quê.

## O que ficou definido

1. **Não comprimir.** O template oficial da Sprint 3 tem ~14 blocos, mas o MVP em si
   (slides "12–13" do template) deve **expandir para vários slides** — a entrega final
   deve ter na casa de **~20 slides**. Espremer o MVP em 2 slides **esconde o trabalho**
   e é proibido.
2. **Mostrar o processo, não só o número.** Não basta reportar acurácia. Tem que constar:
   quais **modelos/métodos** usamos, **visualizações** de cada etapa, e a **justificativa
   de cada escolha** (por que Prophet, por que DTW, por que essas features, etc.).
3. **Documentar em paralelo.** Enquanto construímos os notebooks, manter um `.md` de
   documentação vivo (candidato: `docs/sprint-3-mvp.md`) que registra o que fizemos e
   vira a base dos slides depois. O detalhe técnico fino vive no `.ipynb`; o `.md` é a
   narrativa que sobe pro PPT.
4. **Reaproveitar o que já existe.** Boa parte dos slides iniciais (contexto, problema,
   proposta) é repetição atualizada das Sprints 1 e 2 — manter quase igual, só atualizar.

## Por quê

A nota técnica da banca (peso 50% na Sprint 4) mede **domínio demonstrado**, não só
resultado. Um deck enxuto demais faz parecer que fizemos pouco; um deck que mostra cada
etapa, decisão e visualização comunica competência. Além disso, documentar em paralelo
evita o retrabalho de "reconstruir o raciocínio" na hora de montar o PPT no fim.

## Como aplicar

- Ao fechar cada bloco de modelagem (EDA, features, Prophet, XGBoost, DTW, SHAP),
  registrar no `.md`: o que foi feito, o gráfico/saída, e o porquê da escolha.
- Ao montar o PPT, expandir — 1 modelo pode virar 2-3 slides (setup, resultado, leitura).
- Nunca resumir "pra caber". Se está longo, é sinal de que tem trabalho pra mostrar.

## Conexões

- Reflexo visual dos modelos: `prototipo-reflete-arquitetura.md`
- Setup que viabiliza os modelos: `../conhecimento/setup-ambiente-modelagem-windows.md`

---

*Última atualização: 2026-07-20*
