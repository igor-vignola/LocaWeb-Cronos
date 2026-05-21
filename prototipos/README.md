# Protótipos — Cronos

Mockups HTML/CSS/JS das 5 telas principais do Cronos. Cada tela vira **screenshot** que cola num slide do PPT da Sprint 2 (bloco 3 do template oficial — "Protótipos da Solução", o maior bloco com 5 slides).

---

## Estado atual

✅ `assets/style.css` — identidade visual Cronos completa (paleta, tipografia, componentes base: KPIs, cards, tabelas, sparklines, alertas, badges, score bars)

⏳ Telas a construir:
1. `dashboard.html` — Dashboard Geral
2. `morning-brief.html` — Resumo + ações
3. `cascata.html` — Detector de cascata
4. `saude-produto.html` — Score de saúde
5. `kpi-probabilidade.html` — Probabilidade de KPI
6. `index.html` — landing com nav entre as telas

---

## Como usar o CSS base

Toda tela importa o `style.css` e usa as classes utilitárias + componentes prontos:

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Cronos · Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <div class="app">
    <!-- topnav vai aqui -->
    <header class="header">...</header>
    <main class="content">...</main>
  </div>
</body>
</html>
```

### Paleta (variáveis CSS prontas)

| Variável | Hex | Uso |
|---|---|---|
| `--c-accent` | `#2563EB` | Azul Cronos — destaque, série principal |
| `--c-danger` | `#DC2626` | Vermelho — APENAS perigo/crítico (OLA estourado, KPI em risco) |
| `--c-warning` | `#D97706` | Amarelo — atenção |
| `--c-success` | `#16A34A` | Verde — sucesso |
| `--c-ink` | `#111827` | Texto principal |
| `--c-mid` | `#888888` | Texto secundário, eixos |
| `--c-border` | `#E5E7EB` | Bordas, separadores |
| `--c-bg` | `#F9FAFB` | Fundo geral da tela |

> **Regra de ouro:** se a cor não comunica algo específico, use cinza. Vermelho NUNCA é decorativo.

### Componentes já prontos no CSS

- `.header`, `.brand`, `.brand-logo`, `.brand-name`, `.brand-tag`, `.head-right`, `.head-live`, `.avatar`
- `.kpi-row`, `.kpi-card`, `.kpi-label`, `.kpi-value`, `.kpi-sub`, `.spark` + `.bar`
- `.card`, `.card-head`, `.card-title`, `.card-sub`, `.legend`, `.chip`
- `.alerts`, `.alert`, `.alert-icon`, `.alert-body`, `.badge`
- `table`, `th`, `td`, `.spark-tbl`, `.score-cell`, `.score-bar`, `.score-fill`, `.action-btn`
- `.topnav` (navegação entre os 5 mockups)

---

## Por que HTML e não Figma

Tentamos Figma em 20/05 (arquivo de teste em https://www.figma.com/design/OEBIG7Bh1P6z6TFi8FufSd) mas batemos no limite do plano Starter do Figma MCP. HTML/CSS/JS é mais flexível, sem teto, e ainda vira esqueleto dos templates Django na Sprint 3.

---

## Como gerar os screenshots pro PPT

Cada tela renderizada no navegador → print da tela (Win+Shift+S) ou print da página inteira via DevTools → cola no slide correspondente do template oficial.

---

## Identidade visual de referência

Estilo inspirado em **TIM / Unifique** (referência da mentoria com Douglas): dashboard de consumo, near real-time, 2-3 abas, clean e focado. Visão clara do estado atual no topo, drill-down quando precisa de detalhe.

> Detalhes completos da identidade visual: `.claude/skills/viz-style/SKILL.md`
