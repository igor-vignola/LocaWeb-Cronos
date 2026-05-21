---
data: 2026-05-21
tipo: conhecimento
status: ativo
relacionados: [aesthetic-dark-glass-hibrido, prototipagem-claude-design]
---

# Brand canônico (light) vs Protótipo (dark) — dois sistemas conscientes

## Contexto

A pasta `brand/` contém o sistema canônico do Cronos:
- `design-system.html` — paleta light (`#2563EB` accent sobre fundo branco), fontes Outfit + Sora, identidade pública/operacional usada na Sprint 1
- `guia-equipe.html` — guia do projeto, fontes DM Sans + JetBrains Mono
- `template-slides.pptx` — template oficial dos slides

O protótipo da Sprint 2 vai num caminho aesthetic diferente: **dark glass híbrido V1+V5** (ver [[aesthetic-dark-glass-hibrido]]).

## O que ficou definido

Cronos opera com **dois sistemas visuais coexistindo**, cada um pra contexto diferente:

| Sistema | Onde | Quando usar |
|---|---|---|
| **Brand canônico (light)** | `brand/design-system.html`, slides PPTX, Sprint 1, Sprint 3 (Django) | Identidade pública, apresentações, produto final operacional |
| **Protótipo dark glass** | `prototipos/*.html`, Claude Design output | Mockup pra Sprint 2 — demonstrar capacidade de design + impressionar banca |

Ambos compartilham o accent canônico `#2563EB` (consistência de marca) e as cores semânticas `#DC2626` / `#D97706` / `#059669`. O que muda é base (light vs dark), tipografia (Outfit+Sora vs Outfit+JetBrains Mono) e estética geral.

## Por quê

**Por que dois sistemas?**

- A Sprint 1 (ideação) usou identidade light/operacional — alinhado com slide deck FIAP
- A Sprint 2 (arquitetura+protótipo) precisa impressionar com polish visual — dark glass entrega isso melhor
- A Sprint 3+ (MVP Django) volta pra identidade light pra ser operacional/profissional

**Por que NÃO anexar `brand/design-system.html` no Claude Design?**

Se anexar junto com o spec dark glass, o Claude Design tenta reconciliar dois sistemas conflitantes (light vs dark, Sora vs JetBrains Mono, surface white vs glass) e o resultado fica morno — meio light, meio dark, sem identidade clara em nenhum.

A solução: o spec do Claude Design (`prototipos/claude-design-prompt.md`) já redeclara os tokens dark glass de forma completa e auto-contida. Não precisa do brand como input.

## Como aplicar

**Sprint 2 (atual):**
- Spec do protótipo é fonte única de verdade
- `brand/` fica reservado, não anexar no Claude Design
- Tokens dark glass têm precedência

**Sprint 3 (MVP Django):**
- Voltar pra `brand/design-system.html` como base
- O dark glass do protótipo NÃO migra 1:1
- O esqueleto React/Tailwind do Claude Design serve de referência estrutural, não de paleta

**Geral:**
- Quando alguém da equipe perguntar "qual paleta usar?" — depende do contexto. Sprint 2 + protótipo = dark glass. Slide/Django/produção = brand canônico.
- Accent `#2563EB` é o ponto de continuidade entre os dois mundos.

## Conexões

- [[aesthetic-dark-glass-hibrido]] — o spec do protótipo
- [[prototipagem-claude-design]] — ferramenta da Sprint 2

---

*Última atualização: 2026-05-21*
