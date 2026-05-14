# Pasta `context/`

Esta pasta concentra o contexto persistente do projeto Cronos. Os arquivos aqui não são carregados automaticamente — o Claude (ou qualquer integrante da equipe) consulta sob demanda quando precisa de informação específica.

## Por que existe

Substitui localmente o que antes vivia na "memória" do chat do Claude.ai. Sendo versionado no Git:

- Ana, Hygor e Igor compartilham o mesmo contexto.
- Histórico de decisões fica rastreável (via `git log`).
- O Claude Code lê os arquivos quando precisa.

## Arquivos

| Arquivo | O que tem | Quando consultar |
|---------|-----------|------------------|
| `projeto.md` | Identidade Cronos: tagline, equipe, cronograma | Para apresentar o projeto, conferir dados oficiais |
| `decisoes-tecnicas.md` | Stack, features, restrições, os 3 diferenciais | Antes de decidir abordagem técnica |
| `mentoria-locaweb.md` | Insights da live com Douglas/Locaweb | Antes de decisões de produto/arquitetura |
| `status.md` | Onde estamos AGORA, próximos passos imediatos | Para retomar o trabalho, planejar próximo bloco |
| `sprints/01-ideacao.md` | Sprint 1 entregue, nota 5/5, feedback | Para referenciar o que foi entregue |
| `sprints/02-arquitetura.md` | Sprint 2 em andamento, 8 frentes, checklist | Durante toda a Sprint 2 |

## Como manter atualizado

**Regra simples:** se você decidir algo importante, anote no arquivo correspondente e commit com mensagem `docs: ...`.

Exemplos:
- Mudou a stack? → atualiza `decisoes-tecnicas.md`
- Nova reunião com Locaweb? → adiciona em `mentoria-locaweb.md`
- Terminou um entregável de sprint? → marca em `sprints/0X.md` e atualiza `status.md`

Contexto desatualizado é pior que sem contexto — vira fonte de confusão.
