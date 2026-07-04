# Business card template (digicard)

Single-page business card. Works standalone (hardcoded Everdream content) or **data-driven**: set `window.CARD_DATA` to a JSON payload before the script runs and the card fills from it.

**App integration:** See **PLAN.md** for the full plan, JSON schema, and injection steps. Use **sample-card-data.json** as the data contract and **card-data.schema.json** for validation or types.

**To drive from your app:** Inject one script before the main script, e.g.  
`<script>window.CARD_DATA = YOUR_JSON;</script>`
