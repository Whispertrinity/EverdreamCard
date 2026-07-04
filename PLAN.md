# Business Card Template — App Integration Plan

This document is the plan for connecting this single-page business card (digicard) template to your Smooth Sales app. The card is one HTML file plus assets; the app will supply **one JSON payload per business** so the same template can render any business’s card.

---

## 1. Purpose and scope

- **Template:** The existing `index.html` (and `fonts/`, `assets/`) is the visual and behavioural template. Styling, layout, flip behaviour, accordions, modals, and “Digital Business Card” messaging stay the same.
- **Per-business data:** Everything that varies by business is driven by a single **card data JSON** object. The app builds this JSON from Firestore (business, products, packs, contact, etc.) and either injects it into the HTML when serving the card or exposes it via an API the card page consumes.
- **Hosting:** The card is served **through** the app (e.g. `yourapp.com/card/{businessId}` or `/digicard/{slug}`). One deployment; many businesses via path + JSON.
- **Deliverable:** A portable folder (this directory) containing the template, this plan, and a **sample JSON file** (`sample-card-data.json`) so you can take it to the machine with the app and wire “build this JSON → serve template + data” without guessing the shape.

---

## 2. How the card works (reference)

- **Three “faces”:** Intro (front), Products (back left), Contact (back right). User swipes or uses arrows; the card flips and sections change.
- **Intro:** Logo, “Digital Business Card” (fixed), “swipe” hint.
- **Products section:** A single pricing line (e.g. “40g = $5, 80g = $10”), then an accordion of **flavours/products** (name + description). Below the jerky flavours, a divider, then optional rows such as **Pet treats** (class `flavour-panel-pet-treats`; roadmap: can add `--inactive-preview` for a transparent non-interactive state), then **Packs** (opens the wholesale modal).
- **Contact section:** Name (tappable for vCard), mobile, email, website, app link, divider, **about** text (business description), then Share and Wholesale buttons.
- **Share modal:** QR code (points at the card URL), “Copy link” (same URL). Optionally an “Open in app” link using the app URL.
- **Wholesale modal:** Title “Wholesale Packs”, then an accordion of **packs** (title, price, available/unavailable icon, contents list, was/now/save/savePct). Close button.
- **Accordions:** Only one panel open at a time in the flavours list and in the packs modal.

All variable content (business name, logo, products, prices, packs, contact, about, share URL, app URL) must come from the JSON. Fixed content (“Digital Business Card”, “swipe”, “Share”, “Wholesale”, “Wholesale Packs”, “Close”) stays in the template.

---

## 3. Data contract: JSON schema

The app must produce (or the card must receive) one object per business with the following shape. Field names and types are the contract between the app and the template.

### 3.1 Top-level fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `businessName` | string | Yes | Display name (e.g. “Everdream Jerky”). Used in `<h1>`, logo `alt`, and context. |
| `logoUrl` | string | Yes* | URL of the business logo. *App should fall back to a default logo URL if not set (e.g. from Firestore). |
| `shareUrl` | string | Yes | Public URL of **this** business’s card (e.g. `https://yourapp.com/card/everdream`). Used for QR code and “Copy link”. Must be stable per business. |
| `appUrl` | string | No | Link back to Smooth Sales (e.g. app store or web app). Used for “App” in contact and/or “Open in app” in share modal. |
| `about` | string | Yes | Business description. Can include multiple paragraphs (use `<br>` or newlines as in current card). No separate “pet treats” field—any such line is just part of this text. |
| `products` | array | Yes | List of products/flavours. Each item has `name` and `description`. Order = accordion order before the divider. Items with `afterDivider: true` render after the divider and before **Packs** (e.g. Pet treats). Optional `htmlDescription: true` means `description` is trusted HTML for that row only. |
| `productPrices` | array | Yes | List of size/price lines for the “pricing line” above the product list. Each item: `size` (e.g. "40g"), `price` (e.g. "$5"). Rendered as “40g = $5”, “80g = $10”, etc. |
| `packs` | array | Yes | List of wholesale packs. Each item: see § 3.2. Can be empty if a business has no packs. |
| `contact` | object | Yes | Contact block. See § 3.3. |

### 3.2 Pack object

Each element of `packs`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | e.g. “Pack 1” |
| `price` | string | Yes | e.g. “$150” |
| `available` | boolean | Yes | `true` = green tick, `false` = red X. |
| `contents` | array of strings | Yes | One string per bullet. Each string may include **trusted HTML** (e.g. `<strong>x 2</strong> … <span class="pack-bag-suffix">(x16 bags)</span>`). Totals must match pricing maths (e.g. ×2 per 40g flavour = 16 bags). Only the **Wholesale** modal list is rebuilt from JSON (`#wholesale-modal-content`); retail **Packs** modal stays static in the template. |
| `wasPrice` | string | Yes | e.g. “Was $160” |
| `nowPrice` | string | Yes | e.g. “Now $150” |
| `save` | string | Yes | e.g. “Save $10” |
| `savePct` | string | Yes | e.g. “6% saved” |

Your app’s pack-creation section should map naturally into this structure (title, price, availability, content lines, and computed was/now/save/savePct).

### 3.3 Contact object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name; also used for vCard. |
| `phone` | string | Yes | For display and `tel:` link. vCard uses this. |
| `email` | string | Yes | For display and `mailto:` link. vCard uses this. |
| `website` | string | No | URL. If empty, show “Coming Soon” or hide. |
| `app` | string | No | URL to app (Smooth Sales). If empty, show “Coming Soon” or hide. |

vCard is generated client-side from `name`, `phone`, and `email`; no extra fields required for the current template.

---

## 4. Fixed content (no swap)

- **Intro:** “Digital Business Card”, “swipe” — same for all businesses.
- **Labels:** “Name:”, “Mobile:”, “Email:”, “Website:”, “App:”, “Share”, “Wholesale”, “Wholesale Packs”, “Close”, “Copy link”, etc.
- **Packs button** in the products section: label “Packs”; opens the wholesale modal.
- **Accordion behaviour:** One open at a time in flavours and in packs.

---

## 5. What the app must do

1. **Build the JSON**  
   For a given business (by id or slug), assemble one object matching the schema above from:
   - Business doc (name, logo URL, description → `about`)
   - Products/flavours (name, description) → `products`
   - Product sizes/prices → `productPrices`
   - Packs (from your pack-creation section) → `packs` (title, price, available, contents, was/now/save/savePct)
   - Contact (from business or linked contact) → `contact`
   - Derived: `shareUrl` = your base URL + card path + business slug/id; `appUrl` = your Smooth Sales link

2. **Serve the card**  
   When a request hits the card route (e.g. `GET /card/:slug`):
   - Resolve the business.
   - Build the card JSON (step 1).
   - Either:
     - **A)** Inject it into the HTML (e.g. `window.CARD_DATA = <%= json %>`) and load the template so the page’s script reads `CARD_DATA` and fills the DOM, or  
     - **B)** Server-side render the template with placeholders replaced from the JSON, or  
     - **C)** Serve static HTML that fetches `/api/card/:slug/data` and gets this JSON, then fills the DOM.
   - Ensure the **shareUrl** you put in the JSON is exactly the URL you use for that request (so QR and “Copy link” are correct).

3. **QR code**  
   The template (or your served version) should build the QR image URL from `shareUrl`, e.g.  
   `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encodeURIComponent(shareUrl)}`.  
   As long as `shareUrl` is correct and stable per business, the QR is reliable.

4. **Logo fallback**  
   If `logoUrl` is missing in Firestore, the app should substitute a default logo URL (e.g. a generic Smooth Sales or “no logo” image) before putting it in the JSON.

---

## 6. Template changes required (on the HTML side)

Until the template is “data-driven,” the current HTML has hardcoded content. To connect it to the app:

1. **Single source of truth for runtime data**  
   The card’s script must read from one object (e.g. `window.CARD_DATA` or the result of a fetch). No hardcoded “Everdream Jerky”, “Brett”, “Barbecue”, etc.

2. **Replace all variable content**  
   On load (or when data is available), the script should:
   - Set document title and `<h1>` to `businessName`.
   - Set logo `src` and `alt` from `logoUrl` and `businessName`.
   - Build the pricing line from `productPrices`.
   - Build the flavour accordion from `products` (name + description).
   - Build the contact block from `contact` (name, phone, email, website, app; vCard from name/phone/email).
   - Set the about block from `about`.
   - Build the packs accordion from `packs` (title, price, available, contents, was/now/save/savePct).
   - Set `shareUrl` and `appUrl` for Share modal (QR, copy link, and optional “Open in app”).
   - Use `shareUrl` for the QR code image `src`.

3. **Keep structure and behaviour**  
   Section order, flip behaviour, accordion “one open at a time,” modals, and Packs button opening the wholesale modal stay as they are. Only the **content** of each block becomes dynamic.

4. **Optional**  
   If `packs` is empty, hide the Packs button and/or the Wholesale button in contact, or show a message—your product decision.

---

## 7. Suggested next steps

1. **Use the sample JSON**  
   `sample-card-data.json` in this folder is one valid payload (Everdream-style) matching the schema. Use it to:
   - Validate the schema in your app (e.g. TypeScript interface or Zod).
   - Test the template once you’ve made the HTML data-driven (inject this file or serve it from the app).

2. **Implement “build JSON” in the app**  
   From Firestore (and your pack builder), implement a function or endpoint: “given business id/slug, return the card data object.” Reuse the same field names as in this plan and the sample.

3. **Make the template data-driven**  
   On the machine where you have the app (or in a branch), update the card’s HTML/JS so it reads from `CARD_DATA` (or fetched JSON) and fills the DOM as in § 6. No need to change layout or styles for the first version.

4. **Wire the route**  
   Add the card route (e.g. `card/:slug`). On request, build JSON, serve the template with the JSON injected (or serve template + API for JSON). Set `shareUrl` to the actual URL of that card (e.g. `https://yourapp.com/card/everdream`).

5. **Test with one business**  
   Use Everdream (or one test business) end-to-end: open the card URL, check logo, products, packs, contact, about, Share (QR + copy), and app link if present.

---

## 8. Files in this folder (portable package)

| File | Purpose |
|------|--------|
| `index.html` | Current template (to be made data-driven when integrating). |
| `PLAN.md` | This plan. |
| `sample-card-data.json` | Example card data matching the schema. Use as reference and for testing. |
| `fonts/` | Font files referenced by the template. |
| `assets/` | Logo placeholder, availability icons, etc. |

Take this whole folder to the computer with the app. The plan + sample JSON are enough to implement “build this JSON in the app” and “serve the card with this data” without guessing the structure.

---

## 9. Easiest way for the app to interface: inject once

The template is **data-driven**: if the page loads with `window.CARD_DATA` set, the script will fill the card from it. The app only has to inject the JSON in one place.

### 9.1 Injection point in the HTML

Inject a single script **before** the main card script runs (e.g. right after `<body>` or before the closing `</body>`), so that when the main script runs, `window.CARD_DATA` is already defined:

```html
<script>window.CARD_DATA = YOUR_JSON_OBJECT;</script>
```

If you server-render the HTML, replace `YOUR_JSON_OBJECT` with the JSON string (escaped for HTML). Example in Node/Express:

```js
const cardData = getCardDataForBusiness(req.params.slug); // build from Firestore
const html = template
  .replace('__CARD_DATA__', JSON.stringify(cardData).replace(/</g, '\\u003c'));
```

In the template HTML, include this exactly once where the script should run first:

```html
<script>window.CARD_DATA = __CARD_DATA__;</script>
```

Then your build or server replaces `__CARD_DATA__` with the stringified JSON (with `<` escaped to avoid breaking out of the script tag).

### 9.2 Alternative: fetch from API

If you prefer not to inject into HTML:

1. Serve the card HTML as a static file (no per-request injection).
2. The page loads, then fetches e.g. `GET /api/card/:slug/data` and gets the same JSON.
3. Set `window.CARD_DATA = responseJson` and then call the same apply function the template uses (see § 6), or reload / re-run the card init after setting `CARD_DATA`.

The template expects `CARD_DATA` to be available when its main script runs; so if you use fetch, either delay the main script until after the fetch, or expose a small `window.applyCardData(data)` and call it after fetch.

### 9.3 Files to take to the app machine

| File | Use |
|------|-----|
| `index.html` | Template; already reads `window.CARD_DATA` when present and fills the card. |
| `PLAN.md` | Full plan and injection steps. |
| `README.md` | Short pointer to PLAN.md and injection. |
| `sample-card-data.json` | Example payload; use for tests and schema reference. |
| `card-data.schema.json` | JSON Schema; use for validation or TypeScript types (e.g. quicktype, or manual interface). |
| `fonts/`, `assets/` | Required by the template. |

No build step is required on the card side. On the app side: build the JSON (matching the schema), then inject it as above or serve it from an API.

---

## 10. Summary

- **One JSON per business** with: `businessName`, `logoUrl`, `shareUrl`, `appUrl`, `about`, `products`, `productPrices`, `packs`, `contact`.
- **Products = flavours:** array of `{ name, description }`.
- **Packs:** array of objects with title, price, available, contents (two lines), was/now/save/savePct.
- **Contact:** name, phone, email, website, app (vCard from name/phone/email).
- **About:** single business description (any “pet treats” or similar is just part of that text).
- **Fixed:** “Digital Business Card”, “swipe”, and all UI labels.
- **QR:** Built from `shareUrl`; reliable as long as the app sends the correct card URL.
- **Next:** Implement JSON build in app → make template read from that JSON → serve card route with injected data; use `sample-card-data.json` and this plan as the contract.
