# 🍁 AUTUMN Profile — Architecture & Customization Guide

This guide documents the design tokens, visual assets, automation workflows, and maintenance procedures for the **Golden Autumn** developer profile.

---

## 🎨 1. Autumn Light-Theme Design Tokens & Palette

The visual design captures warm golden sunlight filtering through autumn trees:

| Token Name | HEX Code | Role & Usage |
| :--- | :--- | :--- |
| **Autumn Ivory** | `#FBFBF5` | Page background, clean light surfaces, high contrast |
| **Main Card Background** | `#FFFDF5` | Primary card background for metrics, graphs, and terminal |
| **Secondary Card Surface**| `#FEED9F` | Pale golden cream accents and secondary surfaces |
| **Soft Golden Surface** | `#FFF6D8` | Badges, pills, terminal header, legend containers |
| **Primary Text** | `#40271D` | Earth Brown — high-contrast headings, main numbers, body |
| **Secondary Text** | `#504C41` | Bark Charcoal — list items, section descriptions, labels |
| **Muted Text** | `#9B704B` | Timestamps, footnote annotations, subtitle metadata |
| **Supporting Text** | `#6F604B` | Medium contrast supporting text, axis numbers |
| **Primary Border** | `#D0A823` | Harvest Gold — outer card borders, hero frame, dividers |
| **Soft Border** | `#E8DDB9` | Subtle internal card borders, gridlines, pill outlines |
| **Primary Highlight** | `#D0A823` | Harvest Gold — botanical accents, command prompts |
| **Bright Highlight** | `#F7D327` | Sunlit Yellow — ember sparkles, fire icon, bright accents |
| **Secondary Highlight**| `#EBAA32` | Warm Amber — mid-layer foliage, streak ring |
| **Warm Orange** | `#EB7134` | Autumn Orange — graph data nodes, active prompt icons |
| **Deep Accent** | `#A83A0A` | Burnt Sienna — peak activity dots, category emphasis |
| **Dark Accent** | `#54280D` | Deep Chestnut — headline gradient start, bold labels |

---

## 🏛️ 2. Repository Architecture & Asset Catalog

```text
.
├── .github/
│   └── workflows/
│       ├── metrics.yml             # Generates metrics.svg & activity-graph-autumn.svg daily
│       ├── profile-3d-contrib.yml  # Generates 3D contribution SVGs daily
│       ├── snake.yml               # Generates light & dark autumn contribution snakes
│       └── validate-profile.yml    # CI test suite for SVGs, links, workflows & privacy
├── assets/
│   ├── autumn-divider.svg          # Botanical branch divider with golden embers
│   ├── autumn-footer.svg           # Silhouette forest floor with reflection quote (light theme)
│   ├── autumn-hero.svg             # Animated golden sunlight banner with falling leaves
│   ├── autumn-leaf.svg             # Maple leaf vector marker
│   ├── autumn-terminal.svg         # Animated zsh terminal with CS domains overview (light theme)
│   ├── typing-headline.svg         # Smooth rotating computer science domains SVG (high contrast)
│   └── profile/
│       ├── activity-graph-autumn.svg       # Generated light golden contribution activity graph
│       └── contribution-snake-autumn.svg   # Pre-rendered autumn light contribution grid fallback
├── docs/
│   └── customization-guide.md      # This guide
├── scripts/
│   ├── generate-activity-graph.py  # Generates activity-graph-autumn.svg from GitHub API
│   └── validate-assets.py          # Local & CI validation script (checks SVG, links, privacy)
└── README.md                       # Main GitHub profile document
```

---

## 🛠️ 3. How to Customize Components

### A. Customizing the Hero Banner (`assets/autumn-hero.svg`)
- **Title & Name:** Open `assets/autumn-hero.svg` and locate `<text id="warmTitleGrad">AFNAN PATHAN</text>`.
- **Tagline:** Modify the text under `<!-- Core Tagline -->`.
- **Disciplines:** Update the subtitle under `<!-- Technical Disciplines Subhead -->`.
- **Falling Leaves:** Adjust durations in `<animateTransform>` tags to change drifting patterns.

### B. Customizing the Autumn Terminal (`assets/autumn-terminal.svg`)
- Domain lines are structured in `<g transform="translate(32, 75)">`.
- Each category `[01_CLOUD_INFRASTRUCTURE]` through `[04_DISTRIBUTED_SYSTEMS]` displays technical focus areas.
- Keep text width within the terminal boundary (860px viewBox).

### C. Updating Computer Science Domains & Technologies
Open `README.md` and navigate to the **Computer Science Domains** section.
Organized into:
- **Primary Technical Domains:** Cloud & Infrastructure, DevOps & Systems Engineering, AI & Machine Learning, Backend & API Engineering, Site Reliability & Observability, Networking & Distributed Systems.
- **Specialized Disciplines:** AI Agents & Tool Integration, Data Engineering & Analytics, Databases & Data Management, Security & Privacy Engineering, Software & Mobile Development, Systems, Storage & Virtualization.

### D. Generating the Contribution Activity Graph Locally
To regenerate the activity graph locally using your current GitHub contribution history:
```bash
python3 scripts/generate-activity-graph.py
```

---

## ⚡ 4. Automation & GitHub Actions

### Contribution Snake (`.github/workflows/snake.yml`)
The workflow utilizes `Platane/snk@v3` with custom query parameters:
- **Light output:**
  `color_snake=#D0A823&color_dots=#F2E8CF,#FEED9F,#F8CB78,#EBAA32,#A83A0A`
- **Dark output:**
  `color_snake=#F7D327&color_dots=#231D16,#54280D,#9A7807,#D0A823,#EB7134`
- Pushes directly to the `output` branch.

### Daily Metrics & Activity Graph (`.github/workflows/metrics.yml`)
- Runs daily at midnight UTC.
- Executes `scripts/generate-activity-graph.py` to refresh `assets/profile/activity-graph-autumn.svg` with authentic contribution data.
- Generates `metrics.svg` via `lowlighter/metrics`.

### CI Validation Suite (`.github/workflows/validate-profile.yml`)
- Executes on every push or pull request touching `main`.
- Validates:
  1. SVG XML parsing (prevents undefined entities like unescaped `&` or unclosed tags).
  2. Image references (prevents broken local paths).
  3. Security check (ensures zero hardcoded secrets or access keys).
  4. Privacy check (ensures zero private project disclosures or personal roadmap claims).
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
- **Pre-rendered fallbacks:** All dynamic services have verified local SVGs (`assets/profile/activity-graph-autumn.svg`, `assets/profile/contribution-snake-autumn.svg`) to prevent empty boxes or broken third-party dependencies.
