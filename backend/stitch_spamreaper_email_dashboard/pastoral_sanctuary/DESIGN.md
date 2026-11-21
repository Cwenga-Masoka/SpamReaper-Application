---
name: Pastoral Sanctuary
colors:
  surface: '#f1fcf1'
  surface-dim: '#d2ddd2'
  surface-bright: '#f1fcf1'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#ebf7ec'
  surface-container: '#e5f1e6'
  surface-container-high: '#e0ebe0'
  surface-container-highest: '#dae5db'
  on-surface: '#141e17'
  on-surface-variant: '#414941'
  inverse-surface: '#29332c'
  inverse-on-surface: '#e8f4e9'
  outline: '#727970'
  outline-variant: '#c1c9bf'
  surface-tint: '#3b6845'
  primary: '#265332'
  on-primary: '#ffffff'
  primary-container: '#3e6b48'
  on-primary-container: '#b7e9be'
  inverse-primary: '#a1d2a8'
  secondary: '#755b00'
  on-secondary: '#ffffff'
  secondary-container: '#fed977'
  on-secondary-container: '#785d00'
  tertiary: '#7f301b'
  on-tertiary: '#ffffff'
  tertiary-container: '#9e4730'
  on-tertiary-container: '#ffd3c9'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bcefc3'
  primary-fixed-dim: '#a1d2a8'
  on-primary-fixed: '#00210b'
  on-primary-fixed-variant: '#23502f'
  secondary-fixed: '#ffe08f'
  secondary-fixed-dim: '#e6c363'
  on-secondary-fixed: '#241a00'
  on-secondary-fixed-variant: '#584400'
  tertiary-fixed: '#ffdbd2'
  tertiary-fixed-dim: '#ffb4a1'
  on-tertiary-fixed: '#3c0800'
  on-tertiary-fixed-variant: '#7c2e19'
  background: '#f1fcf1'
  on-background: '#141e17'
  surface-variant: '#dae5db'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-md: 1.5rem
  gutter-lg: 2rem
  margin: 1rem
  margin-md: 2rem
  margin-lg: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

The design system establishes a restorative, tactile sanctuary for inbox stewardship. Rather than treating spam management as an anxiety-inducing triage or high-intensity security task, the UI transforms cleaning the inbox into an unhurried walk across sunlit, rolling hills. 

The aesthetic marries **Tactile Softness** with **Pastoral Minimalism**:
- **Atmosphere:** Sun-drenched, breathable, and serene. Whitespace acts as open air; elements feel like smooth river pebbles, polished wood, and fresh grass.
- **Tone:** Reassuring, forgiving, and protective without being punitive. Permanent deletion and quarantine ("purgatory") are handled with gentle clarity rather than jarring alarms.
- **Tactility:** Micro-interactions mimic organic physics—gentle spring curves, soft depressions on press, and diffuse shadows tinted with warm amber and moss undertones.

## Colors

The palette derives from the natural balance of meadow foliage, earth, and golden daylight. High-contrast harsh blacks and clinical cool grays are forbidden in favor of warm stone, foliage pigments, and sunlit yellows.

### Color Roles & Application
- **Primary (`#3E6B48` - Forest Moss):** Anchors core brand actions, primary buttons, confirmed states, and safe sender endorsements. Darker shade (`#2D4F35`) serves hover and pressed states.
- **Secondary (`#F4D06F` - Golden Sunlight):** Highlights status changes, active triage banners, unread indicators, and celebratory completion marks.
- **Tertiary (`#E07A5F` - Terracotta Clay):** Used strictly for purgatory countdowns, permanent expulsions, blocklists, and critical spam flags, replacing abrasive alert reds with an earthy, decisive signal.
- **Neutral Foreground (`#232D26` - Forest Charcoal):** Replaces pure black to deliver deep, readable contrast without sterile harshness. Muted variations include Sage Mud (`#5C6B60`) for secondary prose and Dried Grass (`#849488`) for metadata and borders.
- **Canvas & Containers:** Base canvas is Off-White Alabaster (`#FAF9F6`), with elevated surfaces layered using Hill Stone Warm Gray (`#F3EFEA`), Sage Tint (`#E8F0EC`), and Mint Mist (`#D5E5DB`).

## Typography

The typography system relies on **Plus Jakarta Sans** across all levels, taking advantage of its rounded geometric forms, warm terminals, and exceptional clarity at micro scale.

- **Headlines & Display:** Set with tight tracking (`-0.02em` to `-0.01em`) and firm weights (600–700) to feel grounded, confident, and hospitable.
- **Body Text:** Uses generous line heights (`1.57` to `1.625`) to preserve an open, breathable reading rhythm, preventing dense email preview listings from feeling cluttered.
- **Labels & Microcopy:** Enhanced with slight positive tracking (`0.01em` to `0.04em`) to maintain legibility inside small pill badges, countdown tags, and status chips.

## Layout & Spacing

The layout is built mobile-first, prioritizing thumb-zone ergonomics for rapid spam triage, expanding gracefully into a centered, spacious dashboard on desktop.

- **Grid Strategy:** A fluid 4-column layout on mobile (`< 768px`), 8-column layout on tablet (`768px - 1024px`), and a 12-column layout capped at `1280px` maximum width on desktop.
- **Margins & Safe Zones:** Mobile devices utilize `margin` (16px) with dynamic viewport edge safe-padding. Desktop layouts embrace broad landscape whitespace via `margin-lg` (48px) to reinforce an unhurried, pastoral cadence.
- **Vertical Spacing Cadence:** Stacks and sections adhere strictly to multiples of 8px (via `space-sm`, `space-md`, `space-lg`, and `space-xl`). Dense stacking is prohibited; items in triage lists must have ample separation to reduce visual fatigue.

## Elevation & Depth

Visual hierarchy rejects harsh, dark drop-shadows. Instead, elevation mirrors soft afternoon sunlight filtering through tree leaves onto the grass:

- **Tonal Layering:** The primary depth mechanism. The canvas rests on `#FAF9F6`, background panels use `#F3EFEA`, and interactive cards lift into `#FFFFFF`.
- **Sunlit Ambient Shadows:** Shadows carry a subtle moss-tinted warm hue (`rgba(45, 79, 53, 0.05)` and `rgba(224, 122, 95, 0.04)` for destructive surfaces).
  - *Resting Card:* `0 4px 20px -2px rgba(45, 79, 53, 0.04), 0 2px 6px -1px rgba(45, 79, 53, 0.02)`
  - *Floating / Hover:* `0 12px 32px -4px rgba(45, 79, 53, 0.08), 0 4px 12px -2px rgba(45, 79, 53, 0.03)`
  - *Modal / Popover:* `0 24px 48px -8px rgba(35, 45, 38, 0.12), 0 8px 16px -4px rgba(35, 45, 38, 0.04)`
- **Organic Outlines:** Elevated surfaces are framed by a 1px soft border in `#E5DFD7` (Sand border) or `#E8F0EC` (Sage tint) to preserve edge definition against light backdrops without visual noise.

## Shapes

The design system employs a **Pill-shaped (Level 3)** geometry to evoke organic river stones, pebbles, and natural curves. 

- **Interactive Controls:** Buttons, chips, search bars, and countdown tags use full pill geometry (`border-radius: 9999px`).
- **Cards & Surfaces:** Content containers utilize pebble radii:
  - Base cards: `1.5rem` (24px)
  - Modals and prominent dashboard sections: `2rem` (32px)
- **Nested Child Proportions:** When an element is placed inside a container, inner corners follow concentric harmony (e.g., a card with 24px radius containing a pill button with 9999px radius or secondary element with 12px radius).

## Components

### Buttons
- **Primary:** Solid Forest Green (`#3E6B48`) with off-white text (`#FAF9F6`). Full pill shape, padding `0.75rem 1.75rem`. Hover deepens to `#2D4F35` with an organic lift (`-1px` transform).
- **Secondary / Warm:** Sunlit Amber outline or soft wash (`#F4D06F` background with `#232D26` text).
- **Destructive ("Reap / Purge"):** Earth Terracotta (`#E07A5F`) fill or border. Communicates decisive action with warmth rather than anger.

### Pebble Cards (Email & Sender Items)
- **Container:** Rounded `1.5rem`, `#FFFFFF` surface, `1px solid #E5DFD7` border, ambient moss shadow.
- **Layout:** High horizontal padding (`1.25rem`), flexible stack on mobile.
- **Interactive State:** Slides gently horizontally on swipe or reveals inline tactile actions (Keep, Purgatory, Banish).

### Purgatory Countdown Badges
- **Visuals:** Pill-shaped badge with soft Terracotta or Sunlit wash (`#E07A5F` at 12% opacity or `#F4D06F` at 20% opacity).
- **Typography:** `label-sm` in bold `#E07A5F` or `#232D26`.
- **Content:** Formatted friendly text (e.g., `🌿 3 days left in purgatory`) accompanied by a subtle miniature circular progress ring.

### Chips & Filters
- **Default:** Pill shape, background `#EEF5F0`, text `#5C6B60`, border `1px solid transparent`.
- **Selected:** Background `#3E6B48`, text `#FFFFFF`, with a gentle spring transition upon toggle.

### Form Inputs & Search Fields
- **Container:** Generous pill structure (`border-radius: 9999px`), background `#F3EFEA`, border `1.5px solid transparent`.
- **Focus:** Border transitions smoothly to `#4A7C59` accompanied by a soft glow ring (`0 0 0 4px rgba(74, 124, 89, 0.15)`). Placeholder set in `#849488`.

### Checkboxes & Radios
- **Design:** Organic leaf-like softening on corners (`6px` radius for checkboxes, full circle for radios).
- **Active State:** Forest Green fill with an off-white rounded checkmark or dot.