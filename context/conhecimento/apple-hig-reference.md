---
data: 2026-05-21
tipo: conhecimento
status: ativo
relacionados: [aesthetic-dark-glass-hibrido, brand-design-system-vs-prototipo]
---

# Apple Human Interface Guidelines — referência destilada (Materials, Motion, Toggles, Color, Buttons)

## Contexto

Em 21/05/2026 Igor decidiu refazer o design system do Cronos seguindo o **caminho Apple**. As guidelines oficiais (`developer.apple.com/design/human-interface-guidelines`) não puderam ser puxadas via WebFetch (SPA totalmente client-side). Igor copiou-e-colou manualmente as 5 páginas essenciais. Este arquivo destila os insights críticos pra aplicação no Cronos.

## Os 3 princípios fundamentais do HIG

1. **Hierarchy** — controles e interface elevam e distinguem o conteúdo abaixo
2. **Harmony** — design concêntrico alinha entre elementos, sistema e dispositivos
3. **Consistency** — convenções de plataforma, adapta a janelas/displays

> Aplicado ao Cronos: a paleta canônica `#2563EB` + neutros é a **harmony**, a separação visual entre chrome (sidebar/topbar) e content layer (KPIs/régua de risco) é a **hierarchy**, e a aderência aos padrões web (⌘K search, kbd hints, hover states) é a **consistency**.

---

## Liquid Glass (iOS 26, jun/2025) — a grande novidade

Material **dinâmico** que unifica a linguagem visual entre plataformas Apple. Forma uma camada funcional flutuando acima do conteúdo (controls/navigation), permitindo o conteúdo de fundo "espiar" através.

### Regras críticas do Liquid Glass

- ✅ **Use** Liquid Glass em **controls e navigation** (tab bars, sidebars, buttons proeminentes)
- ❌ **Não use** no content layer — vira confusão visual e complexidade desnecessária
- ⚠️ Exceção: controles transitórios no content (sliders, toggles) podem assumir aparência Liquid Glass durante interação
- ✅ Use **com parcimônia** em controles custom — overuse distrai do conteúdo
- ✅ Use a `clear` variant apenas sobre backgrounds visualmente ricos (media, photos)

### Dois variants do Liquid Glass

| Variant | Quando usar | Cronos applies onde |
|---|---|---|
| **Regular** | Quando background pode criar problema de legibilidade · componentes com muito texto (alerts, sidebars, popovers) | Sidebar, top bar, KPI cards, régua de meta |
| **Clear** | Sobre media/photos pra preservar visibilidade do conteúdo | Onboarding/hero rico, eventualmente over-chart overlays |

### Dimming layer pro Liquid Glass `clear`

- Se conteúdo de fundo é brilhante → adicionar camada escura 35% opacidade
- Se conteúdo é escuro o suficiente → não precisa

---

## Standard materials (4 thicknesses)

Pro **content layer** (NÃO Liquid Glass), iOS/iPadOS definem 4 materiais standard:

| Material | Translucência | Usar quando |
|---|---|---|
| `ultraThin` | Mais translúcido | Manter contexto do background (visible reminder) |
| `thin` | Translúcido | Overlays leves |
| `regular` (default) | Médio | Use padrão |
| `thick` | Mais opaco | Texto fino + features que precisam de mais contraste |

### Regras

- **Thicker = mais contraste** pra texto/elementos finos
- **Thinner = preserva contexto** do background
- Use **vibrant colors** sobre materials (não systemGray3 puro — contraste ruim)
- Vibrancy levels: `label` > `secondaryLabel` > `tertiaryLabel` > `quaternaryLabel`
- ⚠️ Evite `quaternaryLabel` sobre `thin`/`ultraThin` (contraste muito baixo)

---

## Motion — princípios HIG

Apple HIG **não dita durações/easings exatos** — foca em princípios:

1. **Add motion purposefully** — não anime "porque sim". Animação gratuita distrai/causa desconforto físico
2. **Make motion optional** — sempre tenha alternativa (haptics, audio, texto)
3. **Realistic feedback** — movimento deve casar com expectativa do gesto (se desliza pra baixo, dismiss volta pra baixo)
4. **Brevity & precision** — feedback animation deve ser breve e precisa
5. **Avoid motion in frequent interactions** — sistema já tem subtle animations padrão; custom só pra momentos especiais
6. **Let people cancel** — não obrigue esperar animação completar
7. Considere **SF Symbols animados** (Apple's animated icon system)

### Durações Apple-aware (do meu treinamento, não do HIG texto)

| Interação | Duração |
|---|---|
| Button press feedback | 100-160ms |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects | 150-250ms |
| Modals, drawers | 280-500ms |
| Spring (toggle knob) | natural, ~400ms |

### Easing Apple-aware

- `cubic-bezier(0.25, 1, 0.5, 1)` — ease-out forte (Apple feel)
- `cubic-bezier(0.32, 0.72, 0, 1)` — iOS drawer / sheet
- `cubic-bezier(0.34, 1.56, 0.64, 1)` — spring com leve overshoot (toggle)
- `cubic-bezier(0.76, 0, 0.24, 1)` — ease-in-out forte (transitions on screen)

---

## Toggles

### Switch (capsule + knob)

- ✅ Use **switch** em **list rows** (iOS) — context é o row, não precisa label
- ✅ Default green (`#34C759`) ou app accent (use a Cronos `#2563EB` se quiser)
- ❌ Não use switch fora de list rows em iOS — use **button-that-behaves-like-toggle** (cor de fundo muda no estado active)
- ✅ Diferenças visuais entre on/off devem ser óbvias (cor + shape + dot/checkmark)
- ⚠️ Nunca confie SÓ em cor (alguns usuários não percebem diferenças)

### Checkbox (square)

- ✅ Use checkbox **se hierarquia de settings** (subordinados indentados)
- States: **on** (azul + white checkmark), **off** (vazio), **mixed** (azul + dash)
- Mostrar mixed quando subordinados têm states diferentes
- Use radio buttons se mais de 2 opções mutuamente exclusivas

### Radio button (circular)

- States: **selected** (filled dark + white center), **deselected** (empty)
- Grupo de 2-5 opções mutuamente exclusivas
- Mais de 5 opções → pop-up button

---

## Color

### System colors (iOS exact RGB)

| Cor | Default (light) | Default (dark) |
|---|---|---|
| Red | `255,56,60` | `255,66,69` |
| Orange | `255,141,40` | `255,146,48` |
| Yellow | `255,204,0` | `255,214,0` |
| Green | `52,199,89` | `48,209,88` |
| Mint | `0,200,179` | `0,218,195` |
| Teal | `0,195,208` | `0,210,224` |
| Cyan | `0,192,232` | `60,211,254` |
| Blue | `0,136,255` | `0,145,255` |
| Indigo | `97,85,245` | `109,124,255` |
| Purple | `203,48,224` | `219,52,242` |
| Pink | `255,45,85` | `255,55,95` |
| Brown | `172,127,94` | `183,138,102` |

### iOS system grays

| Gray | Light | Dark |
|---|---|---|
| systemGray | `142,142,147` | `142,142,147` |
| systemGray2 | `174,174,178` | `99,99,102` |
| systemGray3 | `199,199,204` | `72,72,74` |
| systemGray4 | `209,209,214` | `58,58,60` |
| systemGray5 | `229,229,234` | `44,44,46` |
| systemGray6 | `242,242,247` | `28,28,30` |

### Cores semânticas iOS (foreground)

- **label** — primary text
- **secondaryLabel** — secondary text
- **tertiaryLabel** — tertiary text
- **quaternaryLabel** — quaternary text
- **placeholderText** — placeholder
- **separator** — separator (permite background passar)
- **opaqueSeparator** — separator sólido
- **link** — link text

### Backgrounds iOS

**System set:**
- systemBackground — primary
- secondarySystemBackground — grouping content
- tertiarySystemBackground — grouping within secondary

**Grouped set** (para grouped table views):
- systemGroupedBackground
- secondarySystemGroupedBackground
- tertiarySystemGroupedBackground

### Regras de uso

- ❌ **Não hard-code system colors** — eles mudam entre releases
- ✅ **Sempre forneça light AND dark variants**, mesmo se app for single-mode (pra Liquid Glass adaptivity)
- ✅ **Increased contrast variants** — Apple tem específicos pra cada cor
- ✅ Test em **True Tone** e diferentes lighting
- ❌ Não use mesma cor com significados diferentes
- ❌ Não dependa só de cor pra diferenciar (acessibilidade)

### Liquid Glass color

- Por padrão **sem cor própria** — herda do conteúdo atrás
- Pode aplicar cor pra emphasis (primary CTA)
- **Apply color sparingly** — reserve pra status indicators e primary actions
- ❌ Evite color em vários controles na mesma view
- Pra emphasize primary actions, **aplique cor no background**, não no símbolo/texto

---

## Buttons

### 3 atributos compõem um button

1. **Style** — visual baseado em size, color, shape
2. **Content** — symbol, text, ou ambos
3. **Role** — semantic meaning que afeta aparência

### Roles

| Role | Comportamento | Aparência |
|---|---|---|
| Normal | Sem significado especial | Default |
| Primary | Button default (mais provável) | Accent color |
| Cancel | Cancela ação atual | Default neutral |
| Destructive | Ação destrutiva (deletar) | System red |

### Hit region mínimo

- iOS/iPadOS/macOS: **44×44 pt** mínimo
- visionOS: **60×60 pt** mínimo

### Princípios

- ✅ **Press state OBRIGATÓRIO** em custom buttons (sem ele, parece unresponsive)
- ✅ Use **style (não size)** pra distinguir preferred choice
- ✅ Use **prominent style + accent color** no primary CTA da view
- ⚠️ Limite a **1-2 prominent buttons por view** — overuse aumenta carga cognitiva
- ❌ **Não atribua primary role a button destrutivo** — usuário às vezes clica sem ler

### macOS button types

- **Push button** (default)
- **Square button** (= gradient button) — para actions related to a view (add/remove rows)
- **Help button** — circular com `?` — abre help docs
- **Image button** — exibe image/symbol/icon

### visionOS button shapes & states

**Shapes:**
- **Circular** — icon-only
- **Capsule** — text-only ou text+icon (preferred default)
- **Rounded rectangle** — text only

**States:**
1. **Idle** — background dark, outline white
2. **Hover** — background medium dark
3. **Selected** — background white, outline black
4. **Unavailable** — background very dark, outline light

**Sizes (visionOS):** mini 28pt · small 32pt · regular 44pt · large 52pt · extra large 64pt

### Outras observações

- Activity indicator inside button (iOS) quando ação não é instantânea
- Trailing ellipsis (`...`) quando button abre outra window/view (macOS)
- visionOS buttons NÃO suportam custom hover effects
- watchOS: capsule shape padrão pra inline buttons

---

## Como aplicar no Cronos

### Materials → Glass tokens
- Glass-regular (Liquid Glass regular) → sidebar, top bar, KPI cards, panels
- Glass-clear → reservado pra hero overlay sobre chart cheio
- Standard materials (ultraThin/thin/regular/thick) → BG layers pra content layer (atualmente não usamos muito; possível em modais futuros)

### Motion → durations + easings em `tokens.css`
- 4 easing curves definidas
- 5 duration tokens (instant, fast, quick, base, slow)
- Spring suave com overshoot mínimo pra toggles

### Toggles → 3 componentes
- Switch (capsule + knob com slide animation + spring + color transition)
- Checkbox (rounded square + check icon)
- Radio button (circle + dot center)

### Color → tokens hierárquicos
- Label hierarchy (4 levels) ao invés de só "text-1/2/3"
- Background hierarchy (system + grouped sets)
- Fills + separators tokens
- Increased contrast variants pra accessibility

### Buttons → roles + sizes
- 4 roles (Normal · Primary · Cancel · Destructive)
- 3 sizes (sm 32pt · md 40pt · lg 48pt) — adaptado pra web
- Hit region 44px mínimo
- Press state obrigatório (scale 0.97 + 140ms)

## Conexões

- [[aesthetic-dark-glass-hibrido]] — superado, agora light + Liquid Glass-influenced
- [[brand-design-system-vs-prototipo]] — brand canônico continua, refinado com Apple-tier polish

---

*Última atualização: 2026-05-21*
*Fontes: developer.apple.com/design/human-interface-guidelines/{materials,motion,toggles,color,buttons} (extraído manualmente)*
