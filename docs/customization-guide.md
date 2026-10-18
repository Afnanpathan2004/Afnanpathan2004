# 🍁 AUTUMN Profile — Architecture & Customization Guide

This guide documents the design tokens, visual assets, automation workflows, and maintenance procedures for the **Autumn** developer profile.

---

## 🎨 1. Autumn Design Tokens & Palette

The design system is built from handpicked natural autumn pigments:

| Token Name | HEX Code | Role & Usage |
| :--- | :--- | :--- |
| **Autumn Ivory** | `#FBFBF5` | Light highlights, high-contrast readable text, clean surfaces |
| **Pale Golden Cream** | `#FEED9F` | Monospace tags, subheadings, soft golden terminal text |
| **Sunlit Yellow** | `#F7D327` | Primary visual accents, active highlights |
| **Harvest Gold** | `#D0A823` | Outer card borders, botanical branches, command prompts |
| **Bark Charcoal** | `#504C41` | Subtle divider rules, terminal control borders, card frames |
| **Deep Chestnut** | `#54280D` | Forest ridge silhouettes, deep background shadows |
| **Burnt Sienna** | `#A83A0A` | Crimson maple accents, section markers |
| **Rustic Ochre** | `#9A7807` | Grounding tones, secondary leaf elements |
| **Golden Sand** | `#F8CB78` | Warm badges, tag fills, secondary borders |
| **Warm Amber** | `#EBAA32` | Horizon bloom, mid-layer foliage, gradient blends |
| **Earth Brown** | `#40271D` | Deep silhouette hills, window headers |
| **Muted Bark** | `#9B704B` | Timestamps, metadata annotations, subtle labels |
| **Apricot Gold** | `#F0B562` | Subheading highlights, category headers |
| **Autumn Orange** | `#EB7134` | Branch nodes, terminal markers, peak activity dots |
| **Deep Autumn Slate** | `#18130E` | High-contrast dark card backdrop for all lighting conditions |

---

## 🏛️ 2. Repository Architecture & Asset Catalog

```text
.
├── .github/
│   └── workflows/
│       ├── metrics.yml             # Generates metrics.svg daily (lowlighter/metrics)
│       ├── profile-3d-contrib.yml  # Generates 3D contribution SVGs daily
│       ├── snake.yml               # Generates Autumn contribution snake SVGs
│       └── validate-profile.yml    # CI test suite for SVGs, links, and workflows
├── assets/
│   ├── autumn-divider.svg          # Botanical branch divider with golden embers
│   ├── autumn-footer.svg           # Silhouette forest floor with reflection quote
│   ├── autumn-hero.svg             # Main animated golden-hour banner with falling leaves
│   ├── autumn-leaf.svg             # Maple leaf vector marker
│   ├── autumn-terminal.svg         # Animated zsh terminal with CS domains overview
│   ├── typing-headline.svg         # Smooth rotating computer science domains SVG
│   └── profile/
│       └── contribution-snake-autumn.svg # Pre-rendered autumn contribution grid fallback
├── docs/
│   └── customization-guide.md      # This guide
├── scripts/
│   └── validate-assets.py          # Local & CI validation script
└── README.md                       # Main GitHub profile document
```

---

## 🛠️ 3. How to Customize Components

### A. Customizing the Hero Banner (`assets/autumn-hero.svg`)
- **Title & Name:** Open `assets/autumn-hero.svg` and locate `<text id="goldTextGrad">AFNAN PATHAN</text>`.
- **Tagline:** Modify the text under `<!-- Core Tagline -->`.
- **Disciplines:** Update the subtitle under `<!-- Technical Disciplines Subhead -->`.
- **Falling Leaves:** Adjust durations in `<animateTransform>` tags to change drifting patterns.

### B. Customizing the Autumn Terminal (`assets/autumn-terminal.svg`)
- Domain lines are structured in `<g transform="translate(32, 75)">`.
- Each category `[01_CLOUD_INFRASTRUCTURE]` through `[04_DISTRIBUTED_SYSTEMS]` displays technical focus areas.
- Keep text width within the terminal boundary (860px viewBox).

### C. Updating Computer Science Domains & Technologies
Open `README.md` and navigate to the **Computer Science Domains** section.
Each domain card organizes concepts and technical tools without personal plans or unverified claims.

---

## ⚡ 4. Automation & GitHub Actions

### Contribution Snake (`.github/workflows/snake.yml`)
The workflow utilizes `Platane/snk@v3` with custom query parameters:
- **Light output:**
  `color_snake=#D0A823&color_dots=#FBFBF5,#FEED9F,#F8CB78,#EBAA32,#A83A0A`
- **Dark output:**
  `color_snake=#F7D327&color_dots=#231D16,#54280D,#9A7807,#D0A823,#EB7134`
- Pushes directly to the `output` branch.
- **Permissions required:** `contents: write` must be enabled under **Repository Settings > Actions > General > Workflow permissions** (`Read and write permissions`).

### CI Validation Suite (`.github/workflows/validate-profile.yml`)
- Executes on every push or pull request touching `main`.
- Validates:
  1. SVG XML parsing (prevents undefined entities like unescaped `&` or unclosed tags).
  2. Image references (prevents broken local paths).
  3. Security check (ensures zero hardcoded secrets or access keys).
  4. Privacy check (ensures zero private project disclosures).
  5. Workflow permissions check.

To run the validator locally:
```bash
python3 scripts/validate-assets.py
```

---

## 🔒 5. Privacy & Security Guidelines

- **Public technical identity only:** No personal roadmaps, private project names, unreleased features, or future career milestones.
- **No `<script>` tags:** GitHub strictly strips JavaScript from SVGs in READMEs. All animations use SVG SMIL (`<animate>`, `<animateTransform>`).
- **No external fonts via `@import`:** Text elements declare system fallbacks (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'SF Mono', monospace`).
- **Pre-rendered fallbacks:** All dynamic services have local SVGs (`assets/profile/contribution-snake-autumn.svg`) to prevent empty boxes when external services experience latency.
