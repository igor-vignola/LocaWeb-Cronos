---
name: context-keeper
description: Mantém o contexto persistente do projeto Cronos em context/. Use SEMPRE que (a) Igor expressar uma preferência/feedback de processo, (b) tomarmos uma decisão técnica nova, (c) aprendermos algo novo sobre Locaweb/dataset/ferramentas, (d) acordarmos um marco de sprint, (e) Igor pedir explicitamente pra 'lembrar' algo, (f) você sentir que perderia informação útil se não documentasse. Cria ou atualiza o arquivo apropriado em context/ + atualiza o README.md como índice. Garante que toda conversa futura, mesmo perdendo memória de chat, consiga retomar o trabalho corretamente.
---

# Context Keeper

> Skill de manutenção do contexto persistente do projeto Cronos.
> O objetivo é simples: **toda informação importante vira arquivo no repo**, organizada, indexada, atualizada — e qualquer sessão futura (sua, do Igor, da Ana, do Hygor) consegue retomar exatamente de onde paramos.

---

## Quando invocar

Auto-trigger sempre que uma das situações abaixo acontecer na conversa:

1. **Decisão técnica nova** — escolhemos stack, biblioteca, abordagem, padrão (ex: "vamos usar Claude Design em vez de Figma", "Outfit + JetBrains Mono em vez de Geist")
2. **Preferência/feedback de Igor** — ele articula como quer trabalhar, o que evitar, o que reforçar (ex: "protótipo deve refletir arquitetura", "pushback bem-vindo", "não validar premissa falsa")
3. **Conhecimento novo sobre o domínio** — algo que aprendemos sobre Locaweb, sobre o dataset, sobre uma ferramenta, sobre um limite que descobrimos (ex: "Claude Design não tem seletor de framework", "design-system.html é light/operacional")
4. **Marco de sprint ou status change** — entrega feita, nota recebida, frente concluída, bloqueio resolvido, próximo passo redefinido
5. **Mentoria/conversa com Locaweb** — qualquer interação com Douglas ou time Locaweb
6. **Igor pede explicitamente** — "salva isso", "lembra disso", "adiciona no contexto"
7. **Sinto que perderia informação útil** — se em 2 semanas alguém retomar essa conversa, faria sentido encontrar esse fato? Se sim, documenta.

**Quando NÃO usar:** estado efêmero da conversa atual, debug de comandos, fatos triviais já documentados, tarefas em progresso (use TaskCreate pra isso).

---

## Estrutura de pastas

```
context/
├── README.md                  ← índice. SEMPRE atualizar quando criar/mover arquivo.
├── projeto.md                 ← identidade Cronos (rarely changes)
├── status.md                  ← estado AGORA + próximos passos (update frequente)
├── decisoes-tecnicas.md       ← resumo de stack e features (overview)
├── mentoria-locaweb.md        ← sumário das mentorias com Douglas
├── sprints/                   ← arquivo por sprint
│   ├── 01-ideacao.md
│   └── 02-arquitetura.md
├── decisoes/                  ← UMA decisão por arquivo, com data
│   └── YYYY-MM-DD-slug.md
├── preferencias/              ← como Igor trabalha, processo, comunicação
│   └── slug.md
└── conhecimento/              ← fatos aprendidos sobre Locaweb/dataset/ferramentas
    └── slug.md
```

### Quando salvar onde

| Tipo de informação | Pasta | Exemplo |
|---|---|---|
| Decisão técnica datada | `decisoes/` | "Adotamos Claude Design pra prototipagem" |
| Preferência de processo | `preferencias/` | "Protótipo deve refletir toda decisão da arquitetura" |
| Fato sobre domínio | `conhecimento/` | "Brand design-system é light/operacional, conflita com dark glass" |
| Estado de sprint | `sprints/0X-NOME.md` | Frentes da Sprint 2, progresso, blockers |
| Mudança no status geral | `status.md` | "AED iniciada, próximo bloco: setembro investigation" |
| Identidade do projeto | `projeto.md` | Equipe, tagline, cronograma |
| Mentoria/conversa Locaweb | `mentoria-locaweb.md` | Insights de live ou call |

### Quando criar arquivo novo vs atualizar existente

- **Decisão pontual, datada, com contexto único** → novo arquivo em `decisoes/`
- **Princípio de trabalho que aplica genericamente** → novo arquivo em `preferencias/` (ou atualiza se já existe)
- **Fato discreto sobre domínio** → novo arquivo em `conhecimento/` (ou atualiza)
- **Evolução de algo já documentado** → atualiza arquivo existente, adicionando seção com data
- **Mudança de estado de sprint** → atualiza `sprints/0X` + `status.md`

---

## Formato de arquivo

Todo arquivo criado por esta skill segue este padrão:

```markdown
---
data: YYYY-MM-DD
tipo: decisao | preferencia | conhecimento | mentoria
status: ativo | superado | em-revisao
relacionados: [outros-slugs-relacionados]
---

# Título curto e descritivo

## Contexto
1-3 frases explicando o que motivou esta decisão/preferência/aprendizado.

## O que ficou definido
A regra/decisão/fato, em uma frase clara. Sem ambiguidade.

## Por quê
A justificativa. Quem precisa entender 6 meses depois deve conseguir ler isso e concordar (ou discordar com base sólida).

## Como aplicar
Quando esta regra/decisão se manifesta no trabalho. Exemplos concretos.

## Conexões
Links para outros arquivos relacionados (ex: `[[2026-05-21-claude-design]]`).

---

*Última atualização: YYYY-MM-DD*
```

Se o arquivo for atualizado depois, adicionar seção:

```markdown
## Atualização YYYY-MM-DD
O que mudou e por quê.
```

NUNCA apagar histórico — só anotar override/superação.

---

## Manutenção do README.md (índice)

O `context/README.md` é o índice. SEMPRE atualizar quando:
- Criar arquivo novo
- Mover/renomear arquivo
- Marcar arquivo como superado

Formato do índice: tabela por categoria, linha por arquivo, com título + 1 frase + data da última atualização.

---

## Relação com auto-memory

Esta skill é **complementar** ao sistema de auto-memory em `~/.claude/projects/.../memory/`:

| Vai em `memory/` (local) | Vai em `context/` (repo) |
|---|---|
| Informação sobre Igor como pessoa (role, estilo, goals) | Decisão técnica do projeto Cronos |
| Preferências aplicáveis a qualquer projeto dele | Princípio de trabalho específico deste challenge |
| Fatos rápidos que precisam estar quentes na próxima conversa | Conhecimento que a Ana e o Hygor também precisam ver |

**Regra simples:** se a informação seria útil pra outra pessoa do time abrir o repo e entender, vai em `context/`. Se é só sobre como você (Claude) deve se comportar com o Igor, vai em `memory/`.

Quando ambos se aplicam — duplicar é OK. Os dois sistemas coexistem.

---

## Checklist ao invocar a skill

Antes de fechar a invocação, validar:

- [ ] Identifiquei o tipo correto (decisao / preferencia / conhecimento / status)
- [ ] Escolhi a pasta correta (`decisoes/` / `preferencias/` / `conhecimento/` / arquivo raiz)
- [ ] Arquivo tem frontmatter completo (data, tipo, status, relacionados)
- [ ] Título descritivo e nome do arquivo segue `YYYY-MM-DD-slug.md` (para `decisoes/`) ou `slug.md` (demais)
- [ ] Conteúdo segue o template (Contexto / O que ficou definido / Por quê / Como aplicar / Conexões)
- [ ] README.md atualizado com link pro novo arquivo
- [ ] Se a informação afeta `status.md` ou um arquivo de sprint, esses também foram atualizados
- [ ] Se aplicável, também salvei em `memory/` (regra acima)
- [ ] Commitei? (lembrar Igor de commitar, ou commitar se ele autorizou)

---

## Princípios

1. **Contexto desatualizado é pior que sem contexto.** Se algo mudou, atualizar agora, não depois.
2. **Granularidade > consolidação.** Melhor 30 arquivos pequenos e específicos que 3 enormes.
3. **Frontmatter é não-negociável.** Sem data + tipo + status, o arquivo não serve pra busca futura.
4. **Slug bem feito é metade do trabalho.** Nome do arquivo deve descrever conteúdo em 2-4 palavras.
5. **Toda decisão tem `Por quê`.** Sem isso, em 6 meses ninguém sabe se ainda vale.
6. **Conexões > silos.** Linkar entre arquivos liberalmente, mesmo com `[[slug]]` que ainda não existe.

---

## Comando rápido

Quando Igor disser "salva isso no contexto" ou similar, sem mais detalhes:

1. Identificar a informação principal da conversa recente
2. Categorizar (decisao / preferencia / conhecimento)
3. Escolher pasta + slug
4. Aplicar template
5. Atualizar README.md
6. Reportar pra Igor: "Salvei em `context/[pasta]/[arquivo]`. Quer que eu commite?"
