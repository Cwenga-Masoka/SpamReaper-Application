---
name: Surgical Utility
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#42474a'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#73787b'
  outline-variant: '#c2c7ca'
  surface-tint: '#4c616c'
  primary: '#2e434c'
  on-primary: '#ffffff'
  primary-container: '#455a64'
  on-primary-container: '#bad0dc'
  inverse-primary: '#b4cad6'
  secondary: '#b6171e'
  on-secondary: '#ffffff'
  secondary-container: '#da3433'
  on-secondary-container: '#fffbff'
  tertiary: '#673000'
  on-tertiary: '#ffffff'
  tertiary-container: '#8a4300'
  on-tertiary-container: '#ffbf95'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#cfe6f2'
  primary-fixed-dim: '#b4cad6'
  on-primary-fixed: '#071e27'
  on-primary-fixed-variant: '#354a53'
  secondary-fixed: '#ffdad6'
  secondary-fixed-dim: '#ffb3ac'
  on-secondary-fixed: '#410003'
  on-secondary-fixed-variant: '#930010'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311300'
  on-tertiary-fixed-variant: '#723600'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-margin: 16px
  gutter: 12px
  tap-target-min: 44px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

The design system is engineered for high-stakes inbox hygiene. It adopts a **Surgical Minimalism** style—prioritizing information density, rapid scanning, and decisive action. The aesthetic is professional, data-driven, and utilitarian, evoking the precision of a technical tool rather than a casual social app.

The UI relies on high-contrast typography and a strict functional color hierarchy to communicate urgency without clutter. Heavy use of whitespace ensures that even with dense data, the interface remains legible and calm under pressure. Elements are structured with mathematical precision to instill a sense of reliability and control.

## Colors

The color palette is strictly functional, mapping directly to the "time-to-expiry" of spam items. 

- **Primary (Neutral/Stable):** Slate Gray (#455A64) is used for standard UI elements, secondary text, and items with 4+ days remaining. It represents stability.
- **Secondary (Urgency):** Crimson Red (#D32F2F) is reserved for critical warnings, items expiring within 24 hours, and destructive actions. It demands immediate attention.
- **Tertiary (Mid-range):** Amber/Orange (#F57C00) signals caution for items with 2-3 days remaining.
- **Backgrounds:** Pure White (#FFFFFF) is the primary surface, with Light Gray (#F8F9FA) used for subtle grouping and sectioning to maintain maximum optical clarity.

## Typography

This design system utilizes **Hanken Grotesk** for its clean, contemporary, and highly legible character. It provides a professional "tech" feel that remains approachable. For data-heavy elements and timestamps, **JetBrains Mono** is used to provide a monospaced, systematic appearance that aids in scanning IDs and time durations.

- **Headlines:** Bold and tight-lettered for immediate recognition.
- **Labels:** Use monospaced fonts for "time remaining" and "sender address" to ensure numerical alignment across lists.
- **Contrast:** Maintain a minimum 7:1 contrast ratio for all critical data points.

## Layout & Spacing

The layout is optimized for single-handed mobile use. It follows a **Fluid Grid** model with a standard 16px lateral margin. 

- **Vertical Rhythm:** A strict 8px baseline grid is used to maintain consistent stacking.
- **Tap Targets:** Every interactive element must meet a minimum 44x44px clearance area to prevent mis-taps during rapid triage.
- **Structure:** Content is grouped into cards that span the full width of the viewport minus the 16px margins. Internal card padding is locked at 16px to ensure a spacious, readable environment for data points.

## Elevation & Depth

To maintain a "surgical" feel, the design system avoids heavy shadows or complex textures. Hierarchy is established through **Low-contrast outlines** and **Tonal layers**.

- **Surfaces:** Use 1px solid borders in #E0E0E0 for cards rather than shadows.
- **State Changes:** When an item is selected or active, use a subtle 2px border in the Primary Slate color.
- **Z-Axis:** The Bottom Tab Bar uses a light #F8F9FA background with a 1px top border to distinguish it from the content scroll area. Floating Action Buttons (if used) should have a crisp, 2px "hard" shadow for a tactile, utility-first look.

## Shapes

The shape language is **Soft** but disciplined. 0.25rem (4px) corner radii are used for primary cards and input fields to maintain a professional, structured appearance. Buttons may use a slightly larger 8px radius to differentiate them from static containers, but they never reach full "pill" roundness to preserve the serious, utility-driven aesthetic.

## Components

- **Spam Cards:** The central component. Contains a 16px internal padding, a JetBrains Mono "Time Remaining" label in the top right (color-coded by urgency), and large tap targets for "Delete" and "Restore" actions.
- **Action Buttons:** High-contrast backgrounds. Destruction buttons (Empty Spam) use #D32F2F with white text. Secondary actions use #455A64.
- **Bottom Tab Bar:** Persistent navigation with 24px minimalist line icons. The active state is indicated by a color shift to #455A64 and a 2px top-accent bar.
- **Urgency Badges:** Small, rectangular labels with #D32F2F backgrounds and white monospaced text for "1 DAY" warnings.
- **Checkboxes:** Square with a 2px radius, emphasizing the "technical checklist" nature of the task.
- **Empty States:** Use minimalist shield or trash can illustrations in light gray with clear, centered calls-to-action.