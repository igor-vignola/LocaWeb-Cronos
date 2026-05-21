# Console — 5-screen operational intelligence dashboard

> Spec for an AI-assisted design tool. Follow it literally. Every token, every duration, every sample data point. Avoid all AI design clichés (the "forbidden patterns" section is non-negotiable).

---

## 0. Persona

You are a senior design engineer with Emil Kowalski's craft sensibility. You ship interfaces where every detail compounds. You bias toward fewer, sharper choices over many decorative ones. You never animate things that get repeated 50 times a day.

---

## 1. Product context (no proper nouns)

An operational intelligence console for a cloud infrastructure team. It predicts SLA breaches before they happen, surfaces cascading incident patterns, and scores product health. Users are operations managers and on-call engineers who open this 20+ times per day.

The polish must hold up to repeated use. No flashy animation that users will hate after the 50th open.

---

## 2. Stack & engineering

- Next.js 14 App Router. Server Components by default.
- Tailwind CSS v3 + shadcn/ui primitives (customize all defaults — radii, shadows, colors must match the tokens in §3).
- Framer Motion only inside leaf `'use client'` components, isolated and `React.memo`'d.
- `@phosphor-icons/react` weight=duotone, size=18 standard.
- Fonts via `next/font/google`: `Outfit` (sans) and `JetBrains_Mono` (numbers only).
- Every numeric value wrapped in `font-mono tabular-nums`.

---

## 3. Design tokens

### Color — dark theme (default)

```
bg-base:    #0A0A0F     /* off-black — never #000 */
bg-1:       #0F0F16     /* panel base */
bg-2:       #14141B     /* nested panel */
glass-1:    rgba(255,255,255,0.04)
glass-2:    rgba(255,255,255,0.06)
hairline-1: rgba(255,255,255,0.08)
hairline-2: rgba(255,255,255,0.14)

text-1:     #F2F2F5     /* primary */
text-2:     #B5B5BD     /* secondary */
text-3:     #7A7A82     /* tertiary, axes */
text-4:     #4F4F57     /* disabled */

accent:     #2563EB     /* the ONLY accent — Cronos blue */
accent-soft:rgba(37,99,235,0.16)
danger:     #DC2626     /* never #F43F5E rose — use Cronos canonical */
danger-soft:rgba(220,38,38,0.16)
warning:    #D97706
warning-soft:rgba(217,119,6,0.16)
success:    #059669
success-soft:rgba(5,150,105,0.16)
```

### Color — light theme (toggle)

Mirror the dark tokens. `bg-base #F8F8FA`, `bg-1 #FFFFFF`, `text-1 #0A0A0F`, `hairline-1 rgba(0,0,0,0.06)`. Keep accent and semantic colors identical.

### Radii

panels 16px · cards 12px · chips 8px · inputs 8px · pills 9999px

### Shadows

- `glass-elev`: `inset 0 1px 0 rgba(255,255,255,0.06), 0 16px 40px rgba(0,0,0,0.30)`
- `card-rest`: `inset 0 1px 0 rgba(255,255,255,0.05)`
- `card-hover`: `inset 0 1px 0 rgba(255,255,255,0.10), 0 8px 24px rgba(0,0,0,0.32)`

Never use outer glows except on the single hero pulse dot.

### Motion easings

```
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1)
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)
```

Built-in CSS easings are too weak. Use these custom curves.

### Durations

| Element | Duration |
|---|---|
| Button press | 140ms |
| Hover state | 180ms |
| Popover/tooltip enter | 200ms |
| Popover/tooltip exit | 140ms |
| Panel enter | 280ms |
| Page block stagger | 50ms gap, 800ms total |

### Type scale (Outfit Sans)

| Role | Size / Letter-spacing / Weight |
|---|---|
| display (used ONCE per page, on the hero number) | 96px / -0.05em / 800 |
| h1 | 28px / -0.026em / 700 |
| h2 | 17px / -0.022em / 700 |
| h3 | 13.5px / -0.012em / 600 |
| body | 14px / -0.01em / 400 |
| caption | 11.5px / 0.06em uppercase / 600 |
| mono-num | JetBrains Mono, tabular-nums, applied to **every** number |

---

## 4. Shared chrome (present on all 5 screens)

### 4.1. Background

- Fixed full-viewport pseudo-element, z-0, `pointer-events:none`.
- **Two STATIC radial gradients** (no animation — performance):
  - 600×600 blob, `radial-gradient(circle, #2563EB 0%, transparent 70%)`, `blur(80px)`, opacity 0.18, positioned top-left at `-200px -150px`.
  - 500×500 blob, `radial-gradient(circle, #DC2626 0%, transparent 70%)`, `blur(80px)`, opacity 0.12, positioned bottom-right at `-150px -100px`.
- Grain texture overlay: fixed pseudo-element, SVG fractal noise, opacity 0.05, `mix-blend-mode: overlay`.
- Light theme: drop both blob opacities to 0.06.

### 4.2. Sidebar — 240px expanded / 64px collapsed

- Glass surface: `bg-glass-1` + `backdrop-filter: blur(32px) saturate(160%)` + 1px right hairline.
- **Top section** (18px padding):
  - 34×34 logo mark — off-black square, 9px radius, white abstract glyph inside (a checkmark-trending-up shape with a small circle at the apex).
  - Wordmark "Cronos" — 17px / 700 / -0.035em.
  - Tagline "Veja antes. Aja antes." — 8px / 0.18em uppercase / `text-4`.
- **Search input** (14px horizontal padding, below brand):
  - Full-width, `bg-glass-2`, 8px radius.
  - Placeholder "Buscar produto, alerta..."
  - `⌘K` kbd hint on right — 4px padding, 1px border, `text-3`, JetBrains Mono 10px.
- **Nav sections** with 10px / 0.12em uppercase / `text-4` headers:

  **Operação**
  - Dashboard (squares icon)
  - Previsões (line-chart icon)
  - Tendências (trend-up icon)
  - Cascatas (shield icon) — badge `3` (8px font, danger bg, white text, opacity pulse 1→0.5→1 on 2s loop)
  - Saúde · Produto (target icon)
  - Probabilidade KPI (cube icon)

  **Diferenciais**
  - Morning brief (sun icon) — badge `06:00` (text-3, no pulse, neutral)
  - Alertas (bell icon) — badge `8` (warning bg)

  **Análise**
  - Produtos (briefcase icon)
  - Equipes (users icon)
  - Configurações (gear icon)

- **Active item**: `bg-glass-2`, 3px left bar (accent, no outer glow), icon in accent color, font-weight 600.
- **Hover**: `bg-glass-2`, transition background 160ms ease-out.
- **Active click**: `scale(0.98)` for 100ms.
- **Footer** (top hairline divider):
  - 32×32 avatar — initials "IV", blue→neutral gradient (NOT blue→purple), white text 11px 700.
  - Name "Igor Vignola", role "Operações · Locaweb".
  - 3-dot menu icon on the right.

### 4.3. Top bar — 60px

- **Breadcrumb left**: "Operação / Dashboard" — slashes in `text-4`, current page in `text-1` 600.
- **Spacer**.
- **Live status pill**: 6px green dot (`#10B981`, opacity pulse 1→0.5→1 on 1.6s ease) + "Live" + "16:42:08" mono — wrapped in pill: 5px 9px padding, `bg-glass-2`, hairline border, 9999px radius, 11.5px 600.
- **⌘K trigger button**: 240×34, `bg-glass-1`, search icon left, "Buscar" placeholder text, ⌘K kbd right.
- **34×34 notification button**: bell icon + 7px danger dot top-right.
- **52×30 theme toggle**: sun icon on left (active when dark), moon on right (active when light). Knob slides via `translateX(22px)` in 360ms `cubic-bezier(0.16, 1, 0.3, 1)`.

### 4.4. Page enter animation

Each block (hero, KPI row, side panels) uses a stagger cascade:
`opacity: 0 → 1`, `translateY: 12px → 0`, duration 800ms `cubic-bezier(0.16, 1, 0.3, 1)`, delays `80 / 140 / 200 / 260 / 320 / 400ms` for blocks in DOM order.

Isolate this in a single client component that uses Framer Motion `staggerChildren`. NEVER spread it across multiple client components — `staggerChildren` requires shared parent.

---

## 5. Screen 1 — Dashboard

**Route**: `/`

**Grid**: `1fr | 320px` right rail (rail spans full height). Below the hero: 4-column KPI strip. Below: cascata signature card (full width). Below: alerts list (1fr) | heatmap (1fr).

### 5.1. Hero panel (glass + glass-elev shadow, 24×28 padding)

Three-column layout: massive number | text | sparkline.

**LEFT — the number**
- Single number `73` at 96px font (NOT bigger), font-weight 800, letter-spacing -0.05em, line-height 0.85, JetBrains Mono tabular-nums.
- Gradient text fill: `linear-gradient(135deg, #F2F2F5 0%, #B5B5BD 50%, #DC2626 100%)`.
- Unit `%` at 32px, `text-3` color, baseline-aligned.
- 7px danger pulse dot at bottom-right of the number — THIS IS THE ONLY ALLOWED OUTER GLOW: `box-shadow: 0 0 12px rgba(220,38,38,0.45)`. Opacity pulse 1→0.5→1 on 1.4s ease infinite.

**MIDDLE — the message**
- Eyebrow pill: 6px red pulse dot + "PROBABILIDADE KPI · EM RISCO" (10.5px / 0.12em uppercase / 700, danger color) wrapped in `bg-danger-soft` pill with hairline border, 5px 10px padding.
- H1: `A meta de maio está [se inclinando contra você].` — bracketed text in gradient fill `linear-gradient(120deg, #DC2626, #D97706)`, rest in `text-1`. 28px / -0.026em / 700, max-width 32ch.
- Body: `Queda de **12 pp em 7 dias**. Para reverter, **nenhuma nova violação** até dia 31 — e o detector identificou **3 cascatas** em formação agora.` 13px `text-3`, bold parts in `text-2` 600.
- Two CTAs:
  - **Primary**: "Plano de mitigação" + arrow icon. Solid `bg-accent`, white text, 10×16 padding, 10px radius. Hover: `translateY(-2px)` + `box-shadow: 0 8px 24px rgba(37,99,235,0.32)`. Press: `scale(0.97)`.
  - **Secondary**: "Cenários Monte Carlo" + clock icon. `glass-1` bg, hairline border, white text.

**RIGHT — the sparkline**
- Top pill: "↓ 12pp em 7d" in danger-soft pill.
- Sparkline panel: 70px tall, `glass-2` bg, hairline border, 10px radius, 10px padding.
  - White solid line (2px) for past 30 days, falling.
  - Dashed danger line (2px, stroke-dasharray 3 3) for next 11 days, continuing to fall.
  - Single circle marker at "today" point — danger fill, the same single `box-shadow: 0 0 6px` allowed only here.
  - Area fill under line: linear-gradient danger 40% opacity → transparent.
- Footer caption: "Meta OLA **99.5%** · 11 dias".

### 5.2. KPI strip — 4 equal cards (glass surface)

Each card: 18×20 padding, 12px radius, `glass-1` bg, `card-rest` shadow.

**Card 1 — Incidentes hoje**
- Label "INCIDENTES HOJE" (11px uppercase 600 `text-3`) + 26×26 icon chip `accent-soft` bg + clock icon in accent.
- Value `127` — 36px / -0.04em / 700, JetBrains Mono, `text-1`.
- Bottom row: delta pill `↑ 12%` (`danger-soft` bg, danger text, 11.5px 600) + sparkline 78×26 — 8 bars, last 2 solid accent, prior 6 `accent-soft`.

**Card 2 — OLA do mês**
- Icon chip `warning-soft` + clipboard-check icon.
- Value `96.2%` — unit `%` in `text-3` 18px.
- Delta `↓ 1.3pp da meta` (warning pill).
- Sparkline: first 3 bars success, last 5 warning (visualizes the decline).

**Card 3 — Cascatas ativas**
- Icon chip `danger-soft` + shield-warning icon.
- Value `3`.
- Delta `↑ 2 em 24h` (danger pill).
- Sparkline: 8 bars all danger gradient.

**Card 4 — Score saúde médio**
- Icon chip purple-soft + target icon.
- Value `82` — unit `/100` in `text-3`.
- Delta `↓ 4` (warning pill).
- Sparkline: mixed, declining.

**Hover state per card**: lift `translateY(-2px)`, border → `hairline-2`, sparkline bars `scaleY(1.1)`, 280ms ease-out. The hover gradient origin should track the mouse — implement via CSS vars `--mx`, `--my` updated by a `mousemove` handler in an isolated client component.

### 5.3. Cascata signature card (full width below KPI strip, 22×24 padding)

Top 1.5px gradient bar `linear-gradient(90deg, danger, warning, transparent)`. No outer glow.

**HEADER ROW**
- LEFT: 38×38 rounded chip `danger-soft` with a shield icon. Next to it: eyebrow (red pulse dot + "ALERTA · CASCATA EM FORMAÇÃO" 10.5px / 0.12em uppercase / 700 / danger) + product name `MySQL Compartilhado *— Região SP*` (22px / -0.028em / 700, regional suffix in `text-3` 500 14px).
- RIGHT: `Elapsed **02h 14min** · próximo evento em **38min**` (11px `text-3`, bold in `text-1`).

**FLOW VISUALIZATION** — 8 nodes horizontal

| # | Type | Border | Fill | Inside | Time below |
|---|---|---|---|---|---|
| 1 | p5 | text-2 | neutral | `P5` | 14:28 |
| 2 | p5 | text-2 | neutral | `P5` | 14:46 |
| 3 | p5 | text-2 | neutral | `P5` | 15:04 |
| 4 | p4 | warning | warning-soft | `P4` | 15:22 |
| 5 | p4 | warning | warning-soft | `P4` | 15:38 |
| 6 | p3 | danger | danger-soft | `P3` | 15:54 |
| 7 | p3 | danger | danger-soft | `P3` | 16:12 |
| 8 | **predicted** | dashed danger | transparent | `P2` | **~17:20** (bold) |

Each node is a 42×42 circle. Times below in JetBrains Mono 10.5px 600 `text-3`.

The **predicted** node has a pinging ring: pseudo-element `inset(-4px)`, 2px danger border, animation `0% opacity 0.6 scale 0.85 → 70% opacity 0 scale 1.5 → 100% opacity 0 scale 1.5`, 1.6s ease infinite. This is the SECOND allowed glow exception.

**Links between nodes** — 2px height repeating dashes:
- Links 1–3: neutral `hairline-2` dashes.
- Links 4–5: warning dashes, opacity 0.7.
- Links 6–7: danger dashes, opacity 0.9, with a 5×4px traveling bullet pulsing left→right in 1.8s linear infinite (this signals "flow is happening right now").

**FOOTER ROW** (above hairline divider, 12px padding-top)
- LEFT: caption "PROBABILIDADE DE ESCALAR" + value `84%` (22px / 800, gradient text danger→pink) + context "nas próximas 2h".
- RIGHT: primary CTA "Abrir runbook" + arrow icon.

### 5.4. Alerts list (left half of bottom row, glass panel, 14×22 padding)

Header inside panel: "Alertas · últimas 24h" (h2) + "ver todos →" link button right.

Use `divide-y hairline-1` between rows — no card-in-card.

8 alert rows. Each row:
- 36×36 priority chip:
  - P2 = solid `text-1` bg with `bg-base` text
  - P3 = `danger-soft` bg, danger text
  - P4 = `warning-soft` bg, warning text
  - P5 = `accent-soft` bg, accent text
  - Priority text: JetBrains Mono 11.5px 700
- Body: title (13.5px / -0.012em / 600 / `text-1`) + 1-line description (12px `text-3`).
- Right: timestamp (11px Mono `text-3`) + optional `CASCATING` tag (9.5px uppercase 600, `danger-soft` pill).
- Hover: `bg-glass-2`. Press: `scale(0.995)`.

### 5.5. Heatmap (right half of bottom row, glass panel, 14×22 padding)

GitHub-contributions-style: 7 rows × 24 cols of cells, aspect 1:1, 3px gap, 2.5px radius.

- Row labels: Dom / Seg / Ter / Qua / Qui / Sex / Sáb (10px uppercase 600 `text-3`).
- Col labels: 00, 03, 06, 09, 12, 15, 18, 21 (9px `text-3`).
- 7 intensity levels:
  - `h0` = `bg-glass-2`
  - `h1` = `accent` 22% opacity
  - `h2` = `accent` 40% opacity
  - `h3` = `accent` 60% opacity
  - `h4` = `accent` 80% opacity
  - `h5` = `accent` solid
  - `h6` = `danger` — used ONLY for the September incident peaks
- Hover per cell: `scale(1.35)` + `box-shadow: 0 0 0 1.5px accent, card-hover`, 160ms ease-out, raise z-index to 5.
- Legend below (above hairline divider): "menos ←  ░ ░ ▒ ▒ ▓ ▓ → mais".

---

## 6. Screen 2 — Morning Brief

**Route**: `/morning-brief`

Different layout: single centered column, `max-width: 760px`, generous vertical rhythm. This is a daily executive summary — readability beats density.

### 6.1. Layout

- Sidebar **collapses to 64px icon-only** on this screen.
- Top header bar stays full.
- Content centered, no right rail.

### 6.2. Top header inside content

Date pill `Quinta · 21 maio · 06:00` with sun icon, caption style, centered.

### 6.3. Block 1 — Ontem

- Eyebrow `ONTEM · 20 MAI` (caption).
- H1: `127 incidentes, [3 quase cascataram].` — bracketed text in danger gradient.
- Inline mini-stats separated by 1px vertical hairlines (`divide-x`) — NO cards:
  - `127` incidentes
  - `96.2%` OLA
  - `12min` MTTR
- 2-sentence prose summary: 15px `text-2`, line-height 1.55, max-width 60ch.

### 6.4. Block 2 — Hoje

- Eyebrow `HOJE · 21 MAI`.
- H1 with the gradient treatment when there's risk.
- 3 numbered list items. Each: 28×28 circle number badge (accent bg, white text, Mono) + body paragraph.
- Items stagger-enter with 80ms delay between.

### 6.5. Block 3 — Ações sugeridas

- Eyebrow `AÇÕES SUGERIDAS · IA`.
- 3 action cards in vertical stack (NOT a grid). Each card: 16×20 padding, `glass-1`, 12px radius.
  - Action title (h3 600).
  - Body (13px `text-3`, max 2 lines).
  - Bottom row: `Impacto: alto / médio / baixo` pill + `Designar →` link button on right.

### 6.6. Block 4 — CTA strip

`Ver relatório completo` (primary) + `Compartilhar com equipe` (secondary). Centered.

Motion: blocks fade-in with 150ms stagger. NO horizontal motion on this page.

---

## 7. Screen 3 — Cascata (detalhe)

**Route**: `/cascatas/[id]`

Reuses the Dashboard's cascata signature card AS THE HERO but expanded full width. Below it, three columns:

### 7.1. Column A — Eventos do gatilho (timeline)

Vertical timeline, glass panel. Each event = 36×36 priority circle + body + timestamp. Connect events with a 2px vertical `hairline-2` line on the left side of the column.

### 7.2. Column B — Produtos correlatos

5 mini-product rows. Each row:
- Rank `#1`–`#5` (Mono `text-4`)
- Name + region (stacked, `text-1` and `text-3`)
- Score (15px 800 Mono) — color-coded crit/warn/ok, gradient text on crit only.

### 7.3. Column C — Playbook sugerido

3-step expandable accordion. Each step:
- 28×28 number badge + step title.
- Click expands a `glass-2` inner card containing a code-block or checklist.
- Expansion via `clip-path: inset(0 0 100% 0) → inset(0)`, 280ms ease-out. Height NOT animated. Use `transform: scaleY` from `transform-origin: top` for the content reveal.

### 7.4. Bottom strip — historical cascata table

shadcn-style table, 8 rows. Columns: Data | Duração | Escalou para | Produtos afetados | Resolução. Hover row: `bg-glass-2`. Click row navigates.

---

## 8. Screen 4 — Score saúde por produto

**Route**: `/saude`

Two-column workspace: 240px filter rail on the left, data viz on the right.

### 8.1. Filter rail (left, glass panel)

Filter groups separated by hairline + 12px gap.

- **Período**: segmented pill control `24h | 7d | 30d | 90d`. Active pill `bg-glass-2` + hairline border, others transparent `text-3`.
- **Região**: vertical checkbox list. Custom checkbox: 14×14, 3px radius, accent fill when checked.
- **Categoria**: same checkbox pattern.
- **Severidade mínima**: range slider P5 → P2 with custom-styled accent track.

### 8.2. Main area

Top: ranking title `Score de saúde · todos os produtos` (h2) + count `(47 produtos · 8 críticos)` in `text-3`.

Below: a **card-less** wide list using `divide-y hairline-1`. Each row 64px tall, 4-column grid:

1. Rank `01` — Mono 18px 800 `text-4`.
2. Product name + region (stacked).
3. Score bar: 200px wide × 6px tall, `rounded-full` `bg-glass-2`. Filled by color rule:
   - ok = success solid
   - warn = warning solid
   - crit = `linear-gradient(90deg, danger, #EC4899)`
   - Fill width animates from 0 to actual value on enter, 600ms `cubic-bezier(0.16, 1, 0.3, 1)`.
4. Score number 28px 800 Mono — gradient text on crit, solid color on others.
5. Trend chip `↑ 4 / ↓ 7 / →` — color-coded.

Row hover: `bg-glass-2`. Row click: navigate to detail.

**Explicit rule**: no card containers on this screen. The "anti-card overuse" pattern.

---

## 9. Screen 5 — Probabilidade KPI

**Route**: `/kpi`

The executive cockpit screen. Single big chart + 3 scenario cards.

### 9.1. Hero (full width, asymmetric)

- H2 eyebrow `PROJEÇÃO · META DE MAIO`.
- 96px hero number `73%` same treatment as Dashboard, but positioned to the **right** of the chart (NOT left — asymmetric per layout-variance).
- Below number: pill `INCLINAÇÃO NEGATIVA · -12pp em 7d` danger.

### 9.2. Big chart (left 2/3)

Plotly-style line chart, 380px tall, glass panel.

- **X-axis**: days 01 to 31 of May. Current day highlighted with a vertical guide.
- **Y-axis**: 0 → 100% probability.
- **Three lines**:
  - Past — solid white `#F2F2F5`, 2.5px, opacity 1. Historical actual.
  - Forecast median — solid accent, 2.5px. Prophet-style prediction.
  - Forecast 90% CI — accent fill, opacity 0.10, between upper/lower bands.
- **Goal line** at 99.5% — dashed success, 1.5px, with "META OLA" label right-aligned.
- **Today vertical guide** — 1px dashed `hairline-2`, "HOJE" label at top.
- **Hover tooltip**: glass popover, 9×11 padding, `transform-origin: cursor`, scale-in 0.95 → 1 with 180ms ease-out.

### 9.3. Scenario stack (right 1/3)

Three vertically-stacked scenario cards, 14px gap stack:

**Card 1 — Otimista** (success accent on 3px left border)
- Eyebrow + title `Nada falha até dia 31`
- Big Mono percentage `94%` in success color.
- 1-line body explaining condition.

**Card 2 — Atual** (accent border, currently selected, `glass-2` slightly elevated)
- `Trajetória atual mantida`
- `73%` in accent gradient text.

**Card 3 — Pessimista** (danger border)
- `Mais 2 cascatas escalam`
- `41%` in danger gradient text.

**Interaction**: each card clickable. Click updates the chart's forecast line to that scenario via Framer Motion `layoutId`. Line redraws with `stroke-dashoffset` animation from old path to new, 600ms `cubic-bezier(0.77, 0, 0.175, 1)`.

---

## 10. Motion specification (apply globally)

| Element | Property | Duration | Easing |
|---|---|---|---|
| Button `:active` | `scale(0.97)` | 140ms | ease-out |
| Card hover lift | `translateY(-2px)` | 260ms | ease-out |
| Nav item hover | bg-color | 160ms | ease-out |
| Popover/tooltip enter | opacity + `scale(0.95 → 1)` | 180ms | ease-out |
| Popover/tooltip exit | opacity + `scale(1 → 0.95)` | 140ms | ease-out |
| Page block stagger | opacity + `translateY(12 → 0)` | 800ms total / 80ms gap | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Theme toggle knob | `translateX` | 360ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Cascata predicted ring | scale + opacity | 1.6s loop | ease |
| Heatmap cell hover | `scale(1 → 1.35)` | 160ms | ease-out |
| Sparkline bars on card hover | `scaleY(1 → 1.1)` | 220ms | ease-out |
| Live dot pulse | opacity 1 → 0.5 → 1 | 1.6s loop | ease |
| Cascata travelling pulse | `translateX` | 1.8s loop | linear |

### Hard rules

- All animations on `transform` and `opacity` only — NEVER `width`, `height`, `top`, `left`, `padding`, `margin`.
- Tooltips opened within 300ms of closing the previous one skip the enter animation (set `data-instant`).
- Buttons triggered by keyboard (Enter, Space) skip the hover animation.
- `prefers-reduced-motion: reduce` disables all infinite loops and reduces durations to 0.01ms — keep opacity, kill movement.
- All hover-only effects gated behind `@media (hover: hover) and (pointer: fine)`.
- Use CSS transitions (not @keyframes) for any interruptible state. Only use @keyframes for infinite loops (pulse, traveling bullet, predicted ring).
- Popovers/tooltips/dropdowns must set `transform-origin` to the trigger location (not center). Modals are the exception — they stay centered.
- Never animate from `scale(0)`. Start from `scale(0.95) opacity 0`.

---

## 11. Forbidden patterns (NON-NEGOTIABLE)

- ❌ `Inter` font anywhere. Use Outfit + JetBrains Mono only.
- ❌ `#000000` — use `#0A0A0F`.
- ❌ Purple+blue gradient buttons or accents. Single accent only (`#2563EB`). Gradient text allowed only on hero numbers and crit scores.
- ❌ Outer-glow shadows on cards or buttons. Two exceptions ONLY: the hero pulse dot, and the cascata predicted ring.
- ❌ Emojis in UI text, alt text, or icons. Use Phosphor icons.
- ❌ Three-equal-column feature card row. Use 2-column zig-zag or asymmetric grids.
- ❌ Centered hero text. Always asymmetric.
- ❌ `transition: all`. Specify exact properties.
- ❌ `scale(0)` entrance animations.
- ❌ `ease-in` on any UI element. Always `ease-out` or custom curves.
- ❌ `transform-origin: center` on popovers.
- ❌ Generic names ("John Doe", "Sarah Chan", "Acme Corp"). Use the sample data in §12.
- ❌ Round-number fakes (99.9%, 50%, 1000). Use the messy realistic data in §12.
- ❌ Unsplash. If avatars are needed, use initials-over-gradient blocks.
- ❌ "Elevate / Seamless / Unleash / Next-gen" copywriting. Use concrete verbs.
- ❌ `h-screen` — use `min-h-[100dvh]` to prevent iOS Safari layout jumps.
- ❌ `w-[calc(...)]` math — use CSS Grid.
- ❌ Card containers on dense data screens (Score Saúde, Cascata table). Prefer `divide-y` with hairlines.

---

## 12. Sample data (use verbatim — no fabrication)

### Products
MySQL Compartilhado · WordPress Cloud · Email Business · Cloud Server Standard · CDN Edge · Painel de Controle · Postgres Dedicado · Backup Vault

### Regions
SP · RJ · POA · FOR · BSB

### People
- Igor Vignola — Operações (avatar `IV`)
- Douglas Gouveia — Gerente Executivo (avatar `DG`)
- Marina Schettini — SRE Lead (avatar `MS`)
- Tiago Asakawa — On-call (avatar `TA`)

### Realistic numbers
- 122,543 incidentes (base 3 anos)
- 47 produtos ativos
- 96.2% OLA do mês
- 99.5% meta OLA
- 73% probabilidade KPI
- 12 pp queda em 7 dias
- 3 cascatas ativas
- 84% probabilidade de escalar
- 02h 14min elapsed na cascata atual
- 38min até próximo evento previsto
- 06:00 horário do morning brief
- 127 incidentes hoje
- 82/100 score saúde médio

### Realistic incident titles (Portuguese)
- Latência elevada · MySQL SP — 14:28
- Pool de conexões saturado · WordPress — 15:04
- OLA em risco · Email Business — pico de 89%
- Detector de cascata: P5 → P4 em curso · CDN Edge
- Backup falhou · Vault POA — 03:14
- Pico de erros 5xx · Painel — 11:47
- Timeout em queries lentas · Postgres Dedicado — 09:22
- Resposta degradada · CDN Edge FOR — 17:03

---

## 13. Output requirements

Generate as a Next.js 14 App Router project:

- One route per screen under `app/`.
- Shared `components/` for: `sidebar.tsx`, `top-bar.tsx`, `kpi-card.tsx`, `glass-panel.tsx`, `priority-chip.tsx`, `sparkline.tsx`, `cascata-flow.tsx`, `heatmap.tsx`, `score-row.tsx`.
- Theme provider in `app/providers.tsx` (client component) wrapping `app/layout.tsx`.
- Each screen file is a Server Component that imports client-component leaves only where motion or state is required.
- Tailwind config in `tailwind.config.ts` with all tokens from §3 mapped to theme extensions.
- Phosphor icons imported per-component (tree-shaking).

### Pre-flight checklist (run at the end, report each line)

- [ ] `min-h-[100dvh]` instead of `h-screen` everywhere
- [ ] No `transition: all`
- [ ] No purple+blue gradients (only single accent + allowed gradient-text)
- [ ] All numbers in `font-mono tabular-nums` (JetBrains Mono)
- [ ] Empty / loading / error states for every list and chart
- [ ] Mobile collapse: sidebar → top drawer at `< 768px`, KPI strip → 2×2 grid, hero number scales to 64px
- [ ] Stagger animations isolated in client leaves with `React.memo`
- [ ] All popovers/tooltips set `transform-origin` to trigger
- [ ] `prefers-reduced-motion` handled

Confirm at the end: **"Pre-flight passed."**

---

## 14. Order of generation

Generate **Screen 1 (Dashboard)** first and complete it fully — including the sidebar, top bar, hero, KPI strip, cascata, alerts, heatmap. Run the pre-flight checklist.

Then **ask me** before generating Screen 2. Each screen is one full pass with checklist.
