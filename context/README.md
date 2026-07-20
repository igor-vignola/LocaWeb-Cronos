# Pasta `context/`

Contexto persistente do projeto Cronos. Versionado no Git — todo mundo do time (Ana, Hygor, Igor) vê o mesmo. Qualquer sessão do Claude Code consegue retomar o trabalho lendo daqui, mesmo perdendo memória de chat.

## Como funciona

A skill `.claude/skills/context-keeper/` mantém esta pasta **automaticamente atualizada** sempre que tomarmos uma decisão, definirmos uma preferência, ou aprendermos algo importante sobre o projeto. Quando isso acontece:

1. Arquivo novo é criado na pasta correta (`decisoes/` / `preferencias/` / `conhecimento/`)
2. Este README é atualizado adicionando o link
3. Frontmatter completo (data, tipo, status, relacionados) garante busca futura

**Contexto desatualizado é pior que sem contexto.** Se algo mudou, atualizar agora — não depois.

---

## Estrutura

### Arquivos raiz — visão geral do projeto

| Arquivo | O que tem | Quando consultar |
|---|---|---|
| `projeto.md` | Identidade Cronos: tagline, equipe, cronograma | Apresentar projeto, conferir dados oficiais |
| `status.md` | Onde estamos AGORA, próximos passos imediatos | Retomar trabalho, planejar próximo bloco |
| `decisoes-tecnicas.md` | Resumo da stack, features, restrições, 3 diferenciais | Antes de decidir abordagem técnica |
| `mentoria-locaweb.md` | Sumário das mentorias com Douglas/Locaweb | Antes de decisões de produto/arquitetura |

### `sprints/` — arquivo por sprint

| Arquivo | Status |
|---|---|
| [Sprint 1 — Ideação](sprints/01-ideacao.md) | ✅ Entregue · nota 5/5 |
| [Sprint 2 — Arquitetura](sprints/02-arquitetura.md) | ✅ Entregue · nota 5/5 |
| Sprint 3 — MVP Preliminar | 🚧 Iniciada 20/07 (entrega 23/08) |

### `decisoes/` — uma decisão por arquivo, datada

Decisões pontuais com contexto único. Nome do arquivo: `YYYY-MM-DD-slug.md`.

| Decisão | Data |
|---|---|
| [Prototipagem via Claude Design (não Figma)](decisoes/2026-05-21-prototipagem-claude-design.md) | 2026-05-21 |
| [Aesthetic dark glass híbrido V1+V5](decisoes/2026-05-21-aesthetic-dark-glass-hibrido.md) | 2026-05-21 |
| [Alvo dos modelos: série elegível ao KPI (não volume total)](decisoes/2026-07-20-alvo-modelagem-serie-kpi.md) | 2026-07-20 |

### `preferencias/` — como Igor trabalha, princípios, processo

Regras genéricas que aplicamos em todo trabalho do projeto.

| Preferência | Última atualização |
|---|---|
| [Protótipo deve refletir toda decisão da arquitetura](preferencias/prototipo-reflete-arquitetura.md) | 2026-05-21 |
| [Documentar em paralelo — não comprimir o MVP em poucos slides](preferencias/documentar-em-paralelo-nao-comprimir.md) | 2026-07-20 |

### `conhecimento/` — fatos aprendidos sobre Locaweb/dataset/ferramentas

Coisas que descobrimos no caminho e queremos preservar pra próxima sessão.

| Conhecimento | Última atualização |
|---|---|
| [Apple HIG — referência destilada](conhecimento/apple-hig-reference.md) | 2026-05-21 |
| [Claude Design — limites e quirks](conhecimento/claude-design-limites-quirks.md) | 2026-05-21 |
| [Brand canônico (light) vs Protótipo (dark)](conhecimento/brand-design-system-vs-prototipo.md) | 2026-05-21 |
| [Setup ambiente modelagem Windows (Prophet/tslearn/SHAP)](conhecimento/setup-ambiente-modelagem-windows.md) | 2026-07-20 |
| [Regras de KPI + causa da anomalia de setembro/2025](conhecimento/regras-kpi-e-anomalia-setembro.md) | 2026-07-20 |

---

## Formato dos arquivos

Todo arquivo desta pasta segue:

```markdown
---
data: YYYY-MM-DD
tipo: decisao | preferencia | conhecimento | mentoria
status: ativo | superado | em-revisao
relacionados: [outros-slugs]
---

# Título

## Contexto
O que motivou.

## O que ficou definido
A regra/decisão/fato.

## Por quê
Justificativa pra ser entendido 6 meses depois.

## Como aplicar
Quando isso se manifesta no trabalho.

## Conexões
Links cruzados com [[outros-arquivos]].
```

Atualizações posteriores viram seção:

```markdown
## Atualização YYYY-MM-DD
O que mudou e por quê.
```

**Nunca apagar histórico** — só marcar superado.

---

## Convenções de manutenção

1. **Commit junto** — toda mudança em `context/` vira commit `docs:` (ver skill `commit-style`)
2. **Linkar liberalmente** — `[[slug]]` mesmo que o arquivo destino ainda não exista (vira TODO pra criar)
3. **Granularidade > consolidação** — preferir 30 arquivos pequenos a 3 enormes
4. **Frontmatter é não-negociável** — sem data + tipo + status, o arquivo não serve pra busca
5. **Atualizar este README** — toda vez que criar/mover/marcar superado um arquivo
