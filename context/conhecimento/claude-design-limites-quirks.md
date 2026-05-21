---
data: 2026-05-21
tipo: conhecimento
status: ativo
relacionados: [prototipagem-claude-design]
---

# Claude Design — limites, quirks e fluxo prático

## Contexto

Em 21/05/2026 começamos a usar `claude.ai/design` como rota de prototipagem da Sprint 2. Documentando os quirks que descobrimos no caminho pra próxima sessão não tropeçar nos mesmos.

## O que ficou definido (fatos sobre a ferramenta)

### Interface

- Layout: split — esquerda "Start with context" + textbox de prompt; direita "Design Files" com previews
- 4 botões em "Start with context": **Design System**, **Add screenshot**, **Attach codebase**, **Drag in a Figma file**
- Drop area: aceita "Images, docs, references, Figma links, or folders"
- Tags pré-prontas no prompt: "Hi-fi design", "Interactive prototype", "Design System (design system)"
- **NÃO tem seletor de framework/stack** — ele decide sozinho (default: React via Babel no browser, multi-arquivo)

### Comportamento

- **Ignora "pergunta antes de seguir"** — instrução "Comece pela Tela 1 e pergunte antes da Tela 2" foi ignorada, batch-executou pelas telas em sequência. Tratar como esperado.
- Multi-arquivo: cria `styles.css`, `sidebar.jsx`, `topbar.jsx`, etc. (organizado, < 1000 linhas por arquivo)
- Declara o "sistema" antes de começar (tema, fontes, ícones, decisões de layout, fonte dos dados) — útil pra auditar antes dele commitar
- Output exportável como PPTX (botão "Export as PPTX (editable)")

### Limites

- Custo: usa cota da conta Anthropic. Igor bateu 100% do extra limit em 21/05 — reseta em domingo 31/mai
- Se travar no meio, parece não ter botão de "pause" — só dá pra esperar terminar ou abrir nova sessão (perdendo contexto)

## Por quê documentar

Pra próxima sessão (Igor, Ana, Hygor ou outro Claude) saber:
- Não desperdiçar prompt instruindo "pergunte antes" — ele ignora
- Esperar terminar tudo antes de aplicar iteração
- Não tentar configurar stack/framework — não tem seletor
- Cuidar com custo: cada geração consome cota agressivamente

## Como aplicar

**Fluxo ótimo aprendido:**

1. **Spec completo upfront** — não vale a pena fragmentar. Anexa o `.md` inteiro, deixa ele rodar tudo.
2. **Iteração em batch após terminar** — quando ele acabar todas as telas, manda UM prompt aplicando todas as melhorias em todas as telas. Mais barato que ir tela-por-tela.
3. **Validação local com `preview-style.html`** — antes de gastar cota gerando, abre o sniff test e bate olho na direção.
4. **Screenshots como referência** — anexar prints dos V1 e V5 (`prototipos/dashboard-v{1,5}-*.html`) ajuda muito mais que descrever em texto.
5. **NÃO anexar `brand/design-system.html`** — ver [[brand-design-system-vs-prototipo]].

**Prompt textbox curto:** o `.md` carrega o spec. A textbox só serve pra direção operacional ("Comece pela Tela 1, rode pre-flight ao final").

## Conexões

- [[prototipagem-claude-design]] — a decisão de adotar
- [[brand-design-system-vs-prototipo]] — o que NÃO anexar

---

*Última atualização: 2026-05-21*
