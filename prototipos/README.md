# Protótipos — Cronos

## Estado atual (21/05/2026)

🔄 **Reset.** A direção dark-glass via Claude Design foi descartada — o resultado ficou genérico, com termos inventados, e fugiu da identidade Cronos.

Novo caminho:
1. **Calibrar personalidade** via `personalidade.html` — 4 flavors do mesmo dashboard, todos light + brand canônico, variando o tom (operacional crisp · iOS-refined · editorial · tático).
2. **Explorar `data/raw/LWDATASET.xlsx`** pra extrair vocabulário real da Locaweb (produtos, categorias, padrões) → vira input do protótipo, zero invenção.
3. **Spec consolidado** com personalidade escolhida + vocabulário real.
4. **Novo protótipo** uma tela por vez, HTML manual (mais controle, sem limite de cota).

## Arquivos ativos

| Arquivo | Função |
|---|---|
| `personalidade.html` | Showcase visual de 4 personalidades pra Igor escolher (passo 1) |
| `README.md` | Este arquivo |

## Arquivos arquivados / descartados

A iteração dark-glass via Claude Design foi removida (`dashboard-v1-command.html`, `dashboard-v5-glass.html`, `preview-style.html`, `claude-design-prompt*.md`, `Claude Design/*`). Permanece em git history (commits `ceb729f`, `5ac1b88`) caso seja preciso revisitar.

## Identidade visual ativa

A canônica: `brand/design-system.html`.

**Tokens-chave:**
- Accent único: `#2563EB`
- Neutros: escala `#000` → `#FFF` (11 cinzas)
- Semânticas: `#DC2626` danger · `#059669` success · `#D97706` warning — **APENAS em badges, dots e barras de progresso**, nunca em números grandes ou títulos
- Tipografia: `Outfit` (site/dashboard) + `Sora` (slides) + `JetBrains Mono` (números tabulares)
- Radii: 14px panels, 10px small, 6px xs

> **Regra de ouro do brand:** Números grandes, títulos e textos são sempre preto/cinza. Cor semântica é informação, não decoração.
