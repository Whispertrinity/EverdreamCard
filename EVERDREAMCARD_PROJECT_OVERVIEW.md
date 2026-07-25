# EverdreamCard — Project Overview

## What It Is
A **digital business card builder + live card website** for Everdream Jerky. One file (`index.html`) serves three things in one:

1. **The live/master card** — Brett's own digital business card (public face of Everdream Jerky). Lives at `everdreamcard.vercel.app`. Shows business name, tagline, logo, product list with prices, contact info, and action buttons (Payment, Wholesale, Save, Share). Allows 3D swipe navigation between pages (Intro → Products → Details).

2. **The customiser** — A design-your-own tool where a customer can pick a tier (2-page or 3-page card), customise colours, fonts, business info, products/packs, and preview their card live. When they save, it emails their design to everdreamgoods@gmail.com with a reference code.

3. **Customer cards (future/next phase)** — Once a design is paid for, a unique URL is generated with the customer's data baked in — a clone of the master card structure but with their custom colours, text, products, and no "Design Your Own" button.

## Why It Exists
- Brett needs a **digital business card** to share (tap-to-add-contact, share via link, etc.)
- Customers see it and want **their own version** — same card template, customised to their business
- The customiser lets them design and pay for their own card
- Every card shares the same core codebase — just different data per URL

## How It's Structured
**Single file:** `G:\EverdreamCard\index.html` (~5,500 lines, all inline)
- No frameworks, no build step, no separate CSS/JS files
- Deployed via **Vercel** from GitHub (`github.com/Whispertrinity/EverdreamCard.git`, main branch)
- Auto-deploys on `git push`

### Pages / Sections (the card's 3D flip carousel)
| Page | Content | Notes |
|------|---------|-------|
| **Intro** | Business name, logo, tagline | Always shown |
| **Products** | Accordion list of flavours with per-size pricing, plus Packs button | 3-page tier only |
| **Details (Contact)** | Description, Name, Mobile, Email, App, action buttons (Payment/Wholesale/Save/Share on master; Wholesale/Save/Share on preview), "Design Your Own" button | Always shown |

### The Customiser Sections
- **Details tab** — Business name, Name, Tagline, Phone, Email, Description (300 char max)
- **Text tab** — Title Font dropdown (The Wanters DEMO / Lemon Milk Light)
- **Colours tab** — Primary (header), Secondary (footer), Background (body), Accent 3, Accent 4, Title colour
- **Products tab** (3-page only) — Add products with sizes (name + weight + price), up to 30
- **Packs tab** (3-page only) — Multi-product bundles with per-size checkbox selection, live total/value/savings
- **Wholesale tab** (3-page only) — Same as Packs but for wholesale customers
- **Tier buttons:** 2 Pages ($20) or 3 Pages ($30)
- **Actions:** Preview, Save (sends design email with reference code), Reset (with confirmation modal)

### Key Architecture Decisions
- All modals share a consistent design: Teal/purple/green/red header, cream body, brown footer, red pill Close button
- Save/Confirm buttons always green (#1b5e20) — exempt from user colour customisation
- Footer colour brown (#4F362F) — not customisable
- Preview modal is an exact replica of the live card structure with the same sizes, 3D flip, and swipe navigation
- Preview contact body is scrollable — only the Details header is pinned; everything else (description, contact info, buttons, footer) scrolls together
- Customer cards (future) will be separate URLs served from the same file with different data, no "Design Your Own" button, and no functioning action buttons in preview

### What Hex Needs to Know
- The entire project is in **one file**: `G:\EverdreamCard\index.html`
- CSS is in `<style>` tags, JS is all in a single `<script>` at the bottom
- **No build tools, no npm, no dependencies** — just open index.html in a browser (or deploy via Vercel)
- The customiser saves state to `localStorage` under key `everdream-customiser`
- Live card data loads from URL params / a data object at the top of the JS
- Preview overlay is at z-index 400, customiser at ~300, modals at 500
- Desktop shortcut at `C:\Users\whisp\Desktop\EverdreamCard.lnk`

### Files on Disk
| Location | Purpose |
|----------|---------|
| `G:\EverdreamCard\index.html` | Single source of truth — all HTML, CSS, JS |
| `G:\EverdreamCard\assets/` | Images (icons, logo) |
| `G:\EverdreamCard\fonts/` | Font files (The Wanters DEMO, Lemon Milk Light) |
| `G:\EverdreamCard\icons/` | App icons (PWA manifest) |
| `G:\EverdreamCard\manifest.json` | PWA manifest |

### Colour System
| Role | Default | Customisable? |
|------|---------|:---:|
| Primary (header) | `#14545c` (teal) | ✅ |
| Secondary (footer) | `#5d4037` (brown) | ✅ |
| Background (body) | `#f6f6de` (cream) | ✅ |
| Accent 3 | `#1b5e20` (green) | ✅ |
| Accent 4 | `#b8860b` (gold) | ✅ |
| Title colour | `#f6f6de` (cream) | ✅ |
| Font face title | The Wanters DEMO | ✅ |
| Footer colour | `#4F362F` (brown) | ❌ fixed |
| Save buttons | `#1b5e20` (green) | ❌ fixed |
| Close buttons | `#c62828` (red) | ❌ fixed |
| Reset | `#7a0000` (deep red) | ❌ fixed |
