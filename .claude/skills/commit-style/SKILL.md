---
name: commit-style
description: "Padrão de mensagens de commit do projeto Cronos. SEMPRE consulte antes de sugerir, escrever ou revisar mensagens de commit. Use quando o usuário mencionar: commit, git commit, git add, mensagem de commit, conventional commits, ou pedir para 'commitar', 'subir', 'mandar pro git'. Use também quando estiver revisando o histórico do repositório ou propondo agrupar mudanças em commits."
---

# Padrão de Commits — Cronos

Convenção do projeto baseada em **Conventional Commits**, em português, formato simplificado.

## Formato

```
<tipo>: <descrição>
```

- **Sem escopo obrigatório** — `feat: ...` está correto. Escopo é opcional e só usado se realmente clarificar.
- **Descrição** pode ser um resumo completo do que foi feito — não precisa ser curtíssima. Mas deve caber em uma linha legível (idealmente até ~100 caracteres).
- **Imperativo, minúsculo, sem ponto final** na descrição.

## Tipos válidos

| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade do produto (código novo que entrega valor) |
| `fix` | Correção de bug ou problema |
| `docs` | Documentação (README, `context/`, comentários, docstrings) |
| `chore` | Manutenção, configuração, dependências, build, gitignore |
| `refactor` | Refatoração de código sem mudança de comportamento |
| `test` | Adição ou ajuste de testes |
| `style` | Formatação, espaços em branco, ponto e vírgula — não muda lógica |

> Não use outros tipos (`update`, `change`, `add`...). Mantenha-se nestes 7.

## Exemplos bons

```
feat: adiciona detector de cascata para incidentes P4/P5 que escalam para P3
fix: corrige filtro de incidente pai que estava ignorando NaN em vez de string vazia
docs: atualiza decisoes-tecnicas.md com a escolha de tslearn DTW para clusterização
chore: adiciona regras de gitignore para *.pkl e diretório data/processed
refactor: extrai logica de geração de features temporais para módulo features.py
test: adiciona teste de regressão para função de cálculo de OLA estourado
docs: documenta achados da AED sobre anomalia de setembro/2025 no notebook
```

Note: a descrição pode ser **bem explicativa**. Não precisa caber em 5 palavras.

## Exemplos ruins (e o motivo)

```
❌ Update files                              → vago, não diz o quê
❌ feat: Implementou função X.               → "Implementou" (passado) e ponto final
❌ FIX: bug                                  → tipo em maiúsculo, descrição vazia
❌ feat(modelagem)(features): adiciona X     → escopo duplo, complica sem ajudar
❌ feat: várias coisas                       → comitar várias coisas juntas. Quebra em commits separados.
```

## Quando usar corpo do commit (opcional)

Para mudanças grandes ou com contexto importante, adicione corpo após uma linha em branco:

```
feat: implementa pipeline completo de AED do dataset LWDATASET

- Adiciona limpeza de tipos e datas
- Identifica anomalia de queda de incidentes em setembro/2025
- Gera gráficos de distribuição temporal, por produto e por OLA
- Salva relatório consolidado em notebooks/01_eda.ipynb
```

Use corpo quando:
- A mudança afeta vários arquivos ou conceitos
- Há contexto importante (porquê, decisão técnica) que não cabe no título
- É uma mudança que outros do time precisam entender em detalhe

## Regras adicionais

1. **Um commit = uma mudança lógica.** Não juntar AED + correção de gitignore + atualização de README em um commit só.
2. **Commits pequenos e frequentes** são preferíveis a commits gigantes.
3. **Não commitar código quebrado** na branch `main`.
4. **Não commitar dados sensíveis** (credenciais, .env, tokens). Se acontecer, falar com o time imediatamente.
5. **Mensagens em português** — todo o projeto está em PT-BR, manter consistência.

## Fluxo recomendado antes de commitar

1. `git status` — confere o que vai entrar
2. `git diff --staged` — revisa as mudanças
3. Pergunta: "essa mudança é UMA coisa só?". Se não, separa em commits diferentes.
4. Escolhe o tipo correto
5. Escreve descrição que **explica o quê e o porquê**, não só o quê

## Padrão de mensagem por tipo de mudança

| Mudança | Tipo provável |
|---------|--------------|
| Criou novo notebook de AED | `feat` ou `docs` (se for puramente exploratório/documental) |
| Atualizou `context/status.md` | `docs` |
| Corrigiu coluna errada em filtro | `fix` |
| Adicionou nova dependência ao requirements | `chore` |
| Renomeou função sem mudar comportamento | `refactor` |
| Atualizou cores no `viz-style` | `style` (ou `docs` se for em arquivo de doc) |
| Mudou logo, fonte ou padrão visual do brand | `style` |
