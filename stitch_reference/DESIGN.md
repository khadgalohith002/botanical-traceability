---
name: PhytoTrace Precision Architecture
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#424845'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#727974'
  outline-variant: '#c1c8c3'
  surface-tint: '#486458'
  primary: '#00180f'
  on-primary: '#ffffff'
  primary-container: '#112d23'
  on-primary-container: '#789688'
  inverse-primary: '#aecdbf'
  secondary: '#2c694e'
  on-secondary: '#ffffff'
  secondary-container: '#aeeecb'
  on-secondary-container: '#316e52'
  tertiary: '#00180d'
  on-tertiary: '#ffffff'
  tertiary-container: '#002f1d'
  on-tertiary-container: '#39a173'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#caeada'
  primary-fixed-dim: '#aecdbf'
  on-primary-fixed: '#032017'
  on-primary-fixed-variant: '#314c41'
  secondary-fixed: '#b1f0ce'
  secondary-fixed-dim: '#95d4b3'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#0e5138'
  tertiary-fixed: '#92f7c3'
  tertiary-fixed-dim: '#75daa8'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005235'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  body-semibold:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system serves high-stakes agricultural analytics and botanical supply chain intelligence. The interface represents absolute forensic auditability, scientific precision, and industrial botanical provenance. Users range from chief compliance officers and supply chain directors to biological data scientists navigating multi-tier provenance graphs.

The visual narrative rejects generic tech tropes and hollow skeuomorphism. It combines **Corporate Modern** rigor with **Tactile Scientific Minimalism**—characterized by crisp structural bounding boxes, tabular information density, deep botanical forest hues, and immediate node status clarity. 

The emotional tone balances institutional authority with natural biology: calm, unyielding, forensic, and clean. Visual clarity is prioritized over ornamentation to ensure complex graph visualizations (Neo4j subgraphs, sankey diagrams, genomic lot trees) integrate seamlessly alongside tabular ledger panels.

## Colors

The palette establishes deliberate semantic tiers anchored in agricultural deep canopy tones and botanical verification markers:

### Surface & Canvas Architecture
- **Canvas Base:** `#F4F6F4` provides a calibrated, anti-glare botanical tint that prevents optical fatigue during continuous forensic monitoring.
- **Surface Elevation (Cards/Sheets):** `#FFFFFF` pure white, bordered strictly with cool sage hairlines `#D8E2DC` or structural dividers `#E2E8F0`.
- **Primary Chrome / Top Navigation:** `#112D23` deep evergreen base with `#1B4332` secondary navigation rails and command bars.

### Botanical & Graph Accents
- **Action / Primary Interactive:** `#2D6A4F` (deep sage foliage) for stable states; `#1B4332` for hovered controls.
- **Verification & Accent Highlights:** `#52B788` for verified ledger states, active network routes, and primary graph focal nodes; `#74C69D` for secondary active node rings and highlight badges.
- **Audit Alert System:** Functional status uses strict, restrained chromatic indicators: Warning `#D97706` (amber), Error/Contamination `#DC2626` (crimson), Information/Query `#2563EB` (cyan blue).

### Graph Ontology Node Tokens
To guarantee instant parsing within Neo4j and Plotly canvas projections, graph taxonomy nodes are mapped directly to dedicated chromatic tags:
- **Farm:** `#2D6A4F` (deep foliage)
- **Botanical:** `#52B788` (crisp sage)
- **Batch:** `#0284C7` (specimen cobalt)
- **Processor:** `#7C3AED` (extraction violet)
- **Manufacturer:** `#D97706` (transformation amber)
- **Distributor:** `#0D9488` (logistics teal)
- **Retailer:** `#64748B` (end-node slate)

### Typography Chromatics
- **Text Headings / Crucial Metrics:** `#0F172A` (deepest slate black).
- **Body & Tabular Values:** `#1E293B` (high-contrast charcoal slate).
- **Secondary / Meta / Units:** `#64748B` (refined muted slate).
- **Disabled / Structural Outlines:** `#CBD5E1`.

## Typography

The typographic hierarchy implements a tripartite system tailored for scientific SaaS:

1. **Space Grotesk** serves as the architectural headline voice. Its engineered geometric structure mirrors network topology, analytical machinery, and contemporary biotechnology without sacrificing formal legibility.
2. **Hanken Grotesk** delivers clean, low-distortion continuous reading across complex metadata grids, ledger tables, parameter inspectors, and analytical dialogues.
3. **JetBrains Mono** is reserved for forensic tracing strings: Lot IDs, Global Location Numbers (GLN), cryptographic batch hashes, Cypher queries, timestamps, and ontology node chips.

Tabular figures (`font-variant-numeric: tabular-nums`) must be enforced for all data grids, financial totals, and geographic coordinates.

## Layout & Spacing

The layout utilizes a structured **12-column fluid grid** system optimized for multi-pane analytical dashboards, property panels, and network visualization viewports:

- **Desktop (1440px+):** 12 columns with 24px (`1.5rem`) gutters, 32px (`2rem`) page margin. Accommodates a fixed 260px collapsible command rail, a fluid graph canvas, and a fixed 380px contextual entity inspector.
- **Tablet (768px – 1439px):** 8 columns with 16px (`1rem`) gutters, 20px page margin. Contextual inspector converts to an overlay sheet or collapsible bottom drawer.
- **Mobile (<768px):** 4 columns with 12px gutters, 16px page margin. Visualizer renders within dedicated cards or full-screen modal contexts with collapsed control panels.

### Density Strategy
This system adopts an industrial **compact-to-medium density scale**. Spacing tokens prioritize zero wasted space while protecting legibility:
- `space-xs` (4px): Used for chip icon-to-label separation and status indicator margins.
- `space-sm` (8px): Inner table cell padding, input field vertical gutters, badge padding.
- `space-md` (16px): Standard component interior padding (card bodies, list groups).
- `space-lg` (24px): Card headers, drawer borders, layout module stack margins.
- `space-xl` (40px): Section divisions, major dashboard row separators.

## Elevation & Depth

To maximize visual clarity for complex property graphs, the design system avoids heavy shadows, blurring, and skeuomorphic gradients. Depth is established through **tonal layering and low-contrast outlines**:

- **Level 0 (Canvas):** `#F4F6F4`. Continuous matte foundation.
- **Level 1 (Panels & Cards):** `#FFFFFF` background bound by a crisp 1px stroke of `#D8E2DC` (or `#E2E8F0` for interior subdivisions). Zero drop-shadow in resting state.
- **Level 2 (Hover / Elevated Cards / Context Flyouts):** `#FFFFFF` paired with an ultra-diffused, cool tinted ambient shadow: `0 4px 12px -2px rgba(17, 45, 35, 0.06), 0 2px 6px -1px rgba(17, 45, 35, 0.04)`.
- **Level 3 (Modal Dialogs / Cytoscape/Plotly Control Palettes):** `#FFFFFF` elevated with `0 12px 28px -4px rgba(17, 45, 35, 0.12), 0 4px 10px -2px rgba(17, 45, 35, 0.06)` with a crisp 1px stroke of `#CBD5E1`.
- **Level 4 (Sticky Graph HUDs & Floating Action Bars):** Elevated floating surfaces using crisp borders `#1B4332` on dark mode or `#CBD5E1` on light mode with crisp 24px ambient bounds.

## Shapes

The design system maintains a **Soft (Level 1)** structural silhouette to reflect scientific precision and equipment hardware aesthetics:

- **Standard Containers / Cards:** `0.25rem` (4px) border radius. Gives components a crisp, technical edge.
- **Form Inputs / Action Buttons:** `0.25rem` (4px) corner radius, reinforcing an engineering-grade control aesthetic.
- **Inspection Sheets & Modals:** `0.5rem` (8px) corner radius (`rounded-lg`).
- **Ontology & Status Badges:** `0.25rem` (4px) subtle chamfered corners for technical tags, or absolute pills (`9999px`) purely for micro numeric counters and live ledger indicators.

## Components

### Buttons
- **Primary:** Filled `#2D6A4F` text in pure `#FFFFFF`, 4px radius, 36px standard height (`8px 16px` padding). Hover shifts to `#1B4332`. Active scale down `0.99`.
- **Secondary / Technical:** Crisp outline with 1px `#D8E2DC` stroke, background `#FFFFFF`, text `#1E293B`. Hover shifts background to `#F4F6F4` and border to `#52B788`.
- **Destructive / Flag Contamination:** Background `#FEE2E2`, border 1px `#FCA5A5`, text `#991B1B`.

### Graph Ontology Node Badges
Ontology tokens must immediately identify the botanical entity type:
- Form: Inline flex container, 20px height, uppercase `label-sm` font, 4px border radius.
- Includes a 6px solid circular indicator matching the ontological category color:
  - *Farm:* Outline `#2D6A4F`, background `#EBF5F0`, text `#1B4332`.
  - *Botanical:* Outline `#52B788`, background `#EDFAF3`, text `#1B4332`.
  - *Batch:* Outline `#0284C7`, background `#F0F9FF`, text `#0369A1`.
  - *Processor:* Outline `#7C3AED`, background `#F5F3FF`, text `#5B21B6`.
  - *Manufacturer:* Outline `#D97706`, background `#FFFBEB`, text `#B45309`.
  - *Distributor:* Outline `#0D9488`, background `#F0FDFA`, text `#0F766E`.
  - *Retailer:* Outline `#64748B`, background `#F8FAFC`, text `#334155`.

### Verification Badges
- **Verified / DNA Confirmed:** Background `#EDFAF3`, border 1px `#74C69D`, text `#1B4332`. Accompanied by a leading checkmark icon.
- **Pending Review:** Background `#FFFBEB`, border 1px `#FCD34D`, text `#B45309`.
- **Quarantine / Discrepancy:** Background `#FEF2F2`, border 1px `#FCA5A5`, text `#B91C1C`.

### Cards & Analytical Panels
- Background `#FFFFFF`, 1px solid `#D8E2DC` outer border.
- Card Header: 44px fixed height with 1px border-bottom `#E2E8F0`, padding `0 16px`. Left contains `headline-sm` title; right houses secondary control icons or export tools.
- Body: `16px` padding, default `#1E293B` text.

### Form Inputs & Query Builders
- Height: 36px. Border: 1px `#CBD5E1`. Background: `#FFFFFF`. Corner radius: 4px.
- Focus state: Border transitions to `#2D6A4F` with a 2px outer ring in `#52B788` at 20% opacity. No standard browser glow.
- Monospaced query inputs (Cypher syntax or Lot lookup) utilize `JetBrains Mono` at `label-lg` sizing.

### Checkboxes & Radios
- Size: 16px × 16px. Border: 1.5px `#64748B`. Corner radius: 3px (checkbox) / 50% (radio).
- Checked: Background `#2D6A4F`, border `#2D6A4F`, check/dot rendered in pure `#FFFFFF`.

### Specialized Domain Component: Graph Traceability Ledger
- Interactive hybrid table that maps each hop across the botanical graph.
- Every ledger row displays: Hop sequence number, Timestamp, Origin Node Badge, Destination Node Badge, Verified Batch Hash (monospaced), and Action trigger (Inspect / Isolate).
- Alternating row zebra banding with `#FFFFFF` and `#F8F9FA`; row hover state uses `#EDFAF3` with a left border accent in `#52B788`.