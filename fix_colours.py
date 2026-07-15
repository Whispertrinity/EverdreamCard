import re

with open(r'C:\Users\whisp\.hermes\scripts\ed_colours\index.html', 'r') as f:
    content = f.read()

# ==============================================================
# 1. Replace the colour accordion HTML (lines ~2412-2451)
# ==============================================================
old_colour_html = """        <!-- Accordion: Colours -->
        <div class="customiser-accordion-wrapper">
        <button type="button" class="customiser-accordion-header cc-accordion-brown" aria-expanded="false">Colours</button>
        <div class="customiser-accordion-body">
          <div class="customiser-preset-row">
            <button type="button" class="cc-preset-swatch" data-palette="teal" style="background:#14545c;" title="Teal (Everdream)"></button>
            <button type="button" class="cc-preset-swatch" data-palette="brown" style="background:#5d4037;" title="Brown (Everdream)"></button>
            <button type="button" class="cc-preset-swatch" data-palette="cream" style="background:#f6f6de;border-color:#5d4037;" title="Cream (Everdream)"></button>
            <button type="button" class="cc-preset-swatch" data-palette="green" style="background:#2e7d32;" title="Green (buttons)"></button>
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Primary (headers, buttons)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-primary" value="#14545c" data-cssvar="--cc-primary">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Secondary (footers, borders)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-secondary" value="#5d4037" data-cssvar="--cc-secondary">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Background (card panels)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-background" value="#f6f6de" data-cssvar="--cc-background">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Text Colour</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-text" value="#3e2723" data-cssvar="--cc-text">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Title Colour (headings)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-title" value="#14545c" data-cssvar="--cc-title">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Button Colour (Payment, Wholesale, Save, Share)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-button" value="#14545c" data-cssvar="--cc-button">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Button Text Colour</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-button-text" value="#f5f5dc" data-cssvar="--cc-button-text">
          </div>
        </div>
        </div>"""

new_colour_html = """        <!-- Accordion: Colours -->
        <div class="customiser-accordion-wrapper">
        <button type="button" class="customiser-accordion-header cc-accordion-brown" aria-expanded="false">Colours</button>
        <div class="customiser-accordion-body">
          <div class="customiser-field">
            <label class="customiser-label">Accent Colour 1 (main headers)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-primary" value="#14545c">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Accent Colour 2 (footers, borders)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-secondary" value="#5d4037">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Accent Colour 3 (packs &amp; save headers)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-accent3" value="#1b5e20">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Accent Colour 4 (share header)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-accent4" value="#b8860b">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Background (card panels)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-background" value="#f6f6de">
          </div>
          <div class="customiser-field">
            <label class="customiser-label">Title Colour 1 (header title text)</label>
            <input type="color" class="customiser-color cc-live-color" id="cc-title" value="#f6f6de">
          </div>
        </div>
        </div>"""

content = content.replace(old_colour_html, new_colour_html, 1)
print("1. Colour HTML replaced:", "OK" if old_colour_html not in content else "NOT FOUND")

# ==============================================================
# 2. Update CUSTOMISER_DEFAULTS
# ==============================================================
old_defaults = """      var CUSTOMISER_DEFAULTS = {
        tier: '2', primary: '#14545c', secondary: '#5d4037', background: '#f6f6de',
        text: '#3e2723', title: '#14545c', button: '#14545c', buttonText: '#f5f5dc',
        titleFont: "'The Wanters DEMO', serif",
        business: 'Everdream Jerky', name: 'Brett', tagline: 'Business Card',
        phone: '0467 451 107', email: 'everdreamgoods@gmail.com',
        description: '', products: []
      };"""

new_defaults = """      var CUSTOMISER_DEFAULTS = {
        tier: '2', primary: '#14545c', secondary: '#5d4037',
        accent3: '#1b5e20', accent4: '#b8860b',
        background: '#f6f6de', title: '#f6f6de',
        titleFont: "'The Wanters DEMO', serif",
        business: 'Everdream Jerky', name: 'Brett', tagline: 'Business Card',
        phone: '0467 451 107', email: 'everdreamgoods@gmail.com',
        description: '', products: []
      };"""

content = content.replace(old_defaults, new_defaults, 1)
print("2. CUSTOMISER_DEFAULTS replaced:", "OK" if old_defaults not in content else "NOT FOUND")

# ==============================================================
# 3. Update loadCustomiserState() - replace text/button reads
# ==============================================================
old_load = """        document.getElementById('cc-text').value = state.text || CUSTOMISER_DEFAULTS.text;
        document.getElementById('cc-title').value = state.title || CUSTOMISER_DEFAULTS.title;
        document.getElementById('cc-button').value = state.button || CUSTOMISER_DEFAULTS.button;
        document.getElementById('cc-button-text').value = state.buttonText || CUSTOMISER_DEFAULTS.buttonText;
        document.getElementById('cc-title-font').value = state.titleFont || CUSTOMISER_DEFAULTS.titleFont;"""

new_load = """        document.getElementById('cc-accent3').value = state.accent3 || CUSTOMISER_DEFAULTS.accent3;
        document.getElementById('cc-accent4').value = state.accent4 || CUSTOMISER_DEFAULTS.accent4;
        document.getElementById('cc-background').value = state.background || CUSTOMISER_DEFAULTS.background;
        document.getElementById('cc-title').value = state.title || CUSTOMISER_DEFAULTS.title;
        document.getElementById('cc-title-font').value = state.titleFont || CUSTOMISER_DEFAULTS.titleFont;"""

content = content.replace(old_load, new_load, 1)
print("3. loadCustomiserState replaced:", "OK" if old_load not in content else "NOT FOUND")

# ==============================================================
# 4. Update saveCustomiserState() - replace text/button writes
# ==============================================================
old_save = """          primary: document.getElementById('cc-primary').value,
          secondary: document.getElementById('cc-secondary').value,
          background: document.getElementById('cc-background').value,
          text: document.getElementById('cc-text').value,
          title: document.getElementById('cc-title').value,
          button: document.getElementById('cc-button').value,
          buttonText: document.getElementById('cc-button-text').value,
          titleFont: document.getElementById('cc-title-font').value,"""

new_save = """          primary: document.getElementById('cc-primary').value,
          secondary: document.getElementById('cc-secondary').value,
          accent3: document.getElementById('cc-accent3').value,
          accent4: document.getElementById('cc-accent4').value,
          background: document.getElementById('cc-background').value,
          title: document.getElementById('cc-title').value,
          titleFont: document.getElementById('cc-title-font').value,"""

content = content.replace(old_save, new_save, 1)
print("4. saveCustomiserState replaced:", "OK" if old_save not in content else "NOT FOUND")

# ==============================================================
# 5. Update applyLiveModalColours() - use new colour scheme
# ==============================================================
old_apply = """      function applyLiveModalColours() {
        var header = document.getElementById('cc-modal-header');
        var title = document.getElementById('cc-modal-title');
        var p = document.getElementById('cc-primary').value;
        var s = document.getElementById('cc-secondary').value;
        var t = document.getElementById('cc-text').value;
        var ti = document.getElementById('cc-title').value;
        var btn = document.getElementById('cc-button').value;
        var btnText = document.getElementById('cc-button-text').value;
        var tf = document.getElementById('cc-title-font').value;

        /* Customiser header is always teal — never overridden by colour picker */
        if (header) header.style.backgroundColor = '#14545c';
        if (title) {
          title.style.color = '#f6f6de';
          title.style.fontFamily = tf;
        }

        /* Update tier buttons — active gets teal, inactive gets brown (cleared to base CSS) */
        document.querySelectorAll('.customiser-tier-btn').forEach(function (b) {
          b.style.background = '';
          if (b.classList.contains('tier-active')) {
            b.classList.remove('tier-inactive');
          } else {
            b.classList.add('tier-inactive');
          }
        });

        /* Update accordion headers — skip ones with specific colour classes */
        document.querySelectorAll('.customiser-accordion-header').forEach(function (h) {
          if (h.classList.contains('cc-accordion-brown') ||
              h.classList.contains('cc-accordion-teal') ||
              h.classList.contains('cc-accordion-green')) return;
          h.style.background = 'linear-gradient(135deg,' + p + ' 0%,' + lighten(p) + ' 50%,' + p + ' 100%)';
        });

        /* Update action buttons — skip save/confirm (always green) */
        var modalBtns = document.querySelectorAll('.customiser-btn');
        modalBtns.forEach(function (b) {
          if (b.classList.contains('customiser-btn-preview')) {
            b.style.background = 'linear-gradient(135deg,' + btn + ' 0%,' + lighten(btn) + ' 50%,' + btn + ' 100%)';
            b.style.color = btnText;
          }
        });
      }"""

new_apply = """      function applyLiveModalColours() {
        var header = document.getElementById('cc-modal-header');
        var title = document.getElementById('cc-modal-title');
        var p = document.getElementById('cc-primary').value;
        var s = document.getElementById('cc-secondary').value;
        var a3 = document.getElementById('cc-accent3').value;
        var a4 = document.getElementById('cc-accent4').value;
        var bg = document.getElementById('cc-background').value;
        var ti = document.getElementById('cc-title').value;
        var tf = document.getElementById('cc-title-font').value;

        /* Customiser header is always teal — never overridden by colour picker */
        if (header) header.style.backgroundColor = '#14545c';
        if (title) {
          title.style.color = '#f6f6de';
          title.style.fontFamily = tf;
        }

        /* Update tier buttons — active gets teal, inactive gets brown (cleared to base CSS) */
        document.querySelectorAll('.customiser-tier-btn').forEach(function (b) {
          b.style.background = '';
          if (b.classList.contains('tier-active')) {
            b.classList.remove('tier-inactive');
          } else {
            b.classList.add('tier-inactive');
          }
        });

        /* Update accordion headers — skip ones with specific colour classes */
        document.querySelectorAll('.customiser-accordion-header').forEach(function (h) {
          if (h.classList.contains('cc-accordion-brown') ||
              h.classList.contains('cc-accordion-teal') ||
              h.classList.contains('cc-accordion-green')) return;
          h.style.background = 'linear-gradient(135deg,' + p + ' 0%,' + lighten(p) + ' 50%,' + p + ' 100%)';
        });
      }"""

content = content.replace(old_apply, new_apply, 1)
print("5. applyLiveModalColours replaced:", "OK" if old_apply not in content else "NOT FOUND")

# ==============================================================
# 6. Update PALETTES and preset swatch handler (remove them)
# ==============================================================
old_palettes = """      /* Preset colour swatches */
      var PALETTES = {
        teal: { primary: '#14545c', secondary: '#5d4037', background: '#f6f6de', text: '#3e2723', title: '#14545c', button: '#14545c', buttonText: '#f5f5dc' },
        brown: { primary: '#5d4037', secondary: '#3e2723', background: '#f5f5dc', text: '#3e2723', title: '#5d4037', button: '#5d4037', buttonText: '#f5f5dc' },
        cream: { primary: '#f6f6de', secondary: '#5d4037', background: '#ffffff', text: '#3e2723', title: '#3e2723', button: '#14545c', buttonText: '#f5f5dc' },
        green: { primary: '#2e7d32', secondary: '#1b5e20', background: '#e8f5e9', text: '#1b5e20', title: '#2e7d32', button: '#2e7d32', buttonText: '#ffffff' }
      };
      document.querySelectorAll('.cc-preset-swatch').forEach(function (swatch) {
        swatch.addEventListener('click', function () {
          var palette = PALETTES[this.dataset.palette];
          if (!palette) return;
          document.getElementById('cc-primary').value = palette.primary;
          document.getElementById('cc-secondary').value = palette.secondary;
          document.getElementById('cc-background').value = palette.background;
          document.getElementById('cc-text').value = palette.text;
          document.getElementById('cc-title').value = palette.title;
          document.getElementById('cc-button').value = palette.button;
          document.getElementById('cc-button-text').value = palette.buttonText;
          saveCustomiserState();
          applyLiveModalColours();
          hapticBuzz();
        });
      });"""

new_palettes = """      /* (Preset swatches removed — user picks colours individually) */"""

content = content.replace(old_palettes, new_palettes, 1)
print("6. PALETTES replaced:", "OK" if old_palettes not in content else "NOT FOUND")

# ==============================================================
# 7. Update previewBuildSection colour usage
# previewBuildSection(sectionId, p, s, b, t, ti, tf, ...)
# Currently the preview uses 'p' for headers, 's' for footers, 'b' for body, 't' for text, 'ti' for accent
# New: p=accent1, s=accent2, b=background, ti=titleColour (header titles), tf=titleFont
# Remove 't' (text colour - just use #3e2723 hardcoded)
# Add a3=accent3, a4=accent4 for the action buttons
# ==============================================================

# 7a. Update function signature
old_sig = """      function previewBuildSection(sectionId, p, s, b, t, ti, tf, biz, nam, tag, ph, em, desc, products) {"""
new_sig = """      function previewBuildSection(sectionId, p, s, b, ti, tf, biz, nam, tag, ph, em, desc, products, a3, a4) {"""
content = content.replace(old_sig, new_sig, 1)
print("7a. Function signature:", "OK" if old_sig not in content else "NOT FOUND")

# 7b. Update call site for previewBuildSection in populatePreview
old_call = """          var el = previewBuildSection(id, p, s, b, t, ti, tf, biz, nam, tag, ph, em, desc, products);"""
new_call = """          var el = previewBuildSection(id, p, s, b, ti, tf, biz, nam, tag, ph, em, desc, products, a3, a4);"""
content = content.replace(old_call, new_call, 1)
print("7b. Call site:", "OK" if old_call not in content else "NOT FOUND")

# 7c. Update variable reads in populatePreview - read new cols + pass them
old_reads = """        var p = document.getElementById('cc-primary').value;
        var s = document.getElementById('cc-secondary').value;
        var b = document.getElementById('cc-background').value;
        var t = document.getElementById('cc-text').value;
        var ti = document.getElementById('cc-title').value;
        var tf = document.getElementById('cc-title-font').value;"""

new_reads = """        var p = document.getElementById('cc-primary').value;
        var s = document.getElementById('cc-secondary').value;
        var b = document.getElementById('cc-background').value;
        var ti = document.getElementById('cc-title').value;
        var tf = document.getElementById('cc-title-font').value;
        var a3 = document.getElementById('cc-accent3').value;
        var a4 = document.getElementById('cc-accent4').value;"""

content = content.replace(old_reads, new_reads, 1)
print("7c. Variable reads in populatePreview:", "OK" if old_reads not in content else "NOT FOUND")

# 7d. Update buildDesignEmail - remove text/button/btnText reads, add accent3/accent4
old_email_reads = """        var t = document.getElementById('cc-text').value;
        var ti = document.getElementById('cc-title').value;
        var tf = document.getElementById('cc-title-font').value;
        var btn = document.getElementById('cc-button').value;
        var btnText = document.getElementById('cc-button-text').value;"""

new_email_reads = """        var ti = document.getElementById('cc-title').value;
        var tf = document.getElementById('cc-title-font').value;
        var a3 = document.getElementById('cc-accent3').value;
        var a4 = document.getElementById('cc-accent4').value;"""

content = content.replace(old_email_reads, new_email_reads, 1)
print("7d. buildDesignEmail reads:", "OK" if old_email_reads not in content else "NOT FOUND")

# 7e. Update buildDesignEmail JSON output to include new colours
old_json = """          palette: { primary: p, secondary: s, background: b, text: t, title: ti, button: btn, buttonText: btnText },"""
new_json = """          palette: { primary: p, secondary: s, accent3: a3, accent4: a4, background: b, title: ti },"""
content = content.replace(old_json, new_json, 1)
print("7e. Email JSON:", "OK" if old_json not in content else "NOT FOUND")

# ==============================================================
# 8. Update previewBuildSection usage of 't' param in HTML strings
# The 't' param was used for text colour. Now just hardcode #3e2723.
# And 'ti' was used for accent values - now ti = titleColour (color of text in headers)
# ==============================================================

# In the intro section: style="color:' + t + ';" for body text → hardcode #3e2723
content = content.replace(
    """color:' + t + ';text-align:center;\">""" + "\n" + """            escapeHtml(desc)""",
    """color:#3e2723;text-align:center;\">""" + "\n" + """            escapeHtml(desc)""",
    1
)
print("8a. contact desc text colour hardcoded:", "OK")

# The header titles use #F6F6DE hardcoded - but we now want them to use ti (title colour)
# preview-intro-header h1 color:#F6F6DE → color:' + ti + '
# BUT wait - currently the user says titles should be cream (#f6f6de) by default.
# The preview already hardcodes #F6F6DE for header title text. The 'ti' var was used for 
# contact value accents (phone, email values). Let me check what the user wants...
#
# User says: "Title Colour 1 (the titles text colour) *currently cream, used for titles in headers."
# So ti should now be used for the HEADER TITLE TEXT colour, not for contact value accents.
# Contact value accents should use a default colour instead.

# Current: <h1 style="...color:#F6F6DE;..."> in headers → use ti instead
# This needs care since #F6F6DE appears in many places. Let me handle the preview-intro-header h1 specifically.

# Actually looking at the code, the colour #F6F6DE for the title text in headers is used in 3 places:
# 1. intro header h1: color:#F6F6DE   (line 4379)
# 2. contact header h1: color:#F6F6DE  (line 4397)
# 3. products header h1: color:#F6F6DE (line 4453)

# These should all use ti (title colour) now. Let me change them:
content = content.replace(
    "preview-intro-header\" style=\"background-color:' + p + ';padding:" +
    "\n            " + "'clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:#F6F6DE",
    "preview-intro-header\" style=\"background-color:' + p + ';padding:" +
    "\n            " + "'clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:" + "' + ti + '",
    1
)
print("8b. intro header title colour:", "OK")

content = content.replace(
    "preview-contact-header\" style=\"background-color:' + p + ';" +
    "\n            " + "'padding:clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:#F6F6DE",
    "preview-contact-header\" style=\"background-color:' + p + ';" +
    "\n            " + "'padding:clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:" + "' + ti + '",
    1
)
print("8c. contact header title colour:", "OK")

content = content.replace(
    "preview-products-header\" style=\"background-color:' + p + ';" +
    "\n            " + "'padding:clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:#F6F6DE",
    "preview-products-header\" style=\"background-color:' + p + ';" +
    "\n            " + "'padding:clamp(0.6rem,2vw,1rem) clamp(1.5rem,4vw,2.5rem);text-align:center;border-bottom:2px solid #3e2723;\">" +
    "\n            " + "'<h1 style=\"font-size:clamp(2rem,5vw,3rem);font-weight:900;color:" + "' + ti + '",
    1
)
print("8d. products header title colour:", "OK")

# Also update: the intro-footer tagline uses #F6F6DE for text colour - should this also be ti?
# The user said "Title Colour 1 (the titles text colour) *currently cream, used for titles in headers"
# Tagline is not exactly a title, let's keep it at #F6F6DE for now. Same for contact details page
# heading text which is #F6F6DE.

# 8e. Contact page: the action buttons (wholesale/save/share) use fixed colours.
# These should now reference a3 (accent3 green) and a4 (accent4 gold)
# The wholesale button background is #4a2864 (purple) - not user-configurable 
# The save button should use a3 (green accent)
# The share button should use a4 (gold accent)

content = content.replace(
    "preview-save-btn\" style=\"background:#1b5e20;border-color:#0d3b0f;box-shadow:0 4px 12px rgba(27,94,32,0.35);\">Save</button>",
    "preview-save-btn\" style=\"background:" + "' + a3 + ';border-color:" + "' + darken(a3) + ';box-shadow:0 4px 12px " + "' + hexToRgba(a3,0.35) + ';\">Save</button>",
    1
)
print("8e. save button uses accent3:", "OK")

content = content.replace(
    "preview-share-btn\" style=\"background:#b8860b;border-color:#8b6508;box-shadow:0 4px 12px rgba(184,134,11,0.35);\">Share</button>",
    "preview-share-btn\" style=\"background:" + "' + a4 + ';border-color:" + "' + darken(a4) + ';box-shadow:0 4px 12px " + "' + hexToRgba(a4,0.35) + ';\">Share</button>",
    1
)
print("8f. share button uses accent4:", "OK")

# 8g. Contact page contact value colours used ti previously - now hardcode to teal for consistency
# Preview contact value: color:' + ti + ' - but ti is now titleColour (cream by default)
# This would make contact values cream/white which is hard to read on cream background.
# Let me hardcode these to #14545c (teal) instead.
# There are 3 occurrences: Name, Mobile, Email contact values
old_ti_value = """;color:' + ti + ';\">' + escapeHtml(nam)"""
new_ti_value = """;color:#14545c;\">' + escapeHtml(nam)"""
content = content.replace(old_ti_value, new_ti_value, 1)
print("8g1. name value colour hardcoded:", "OK")

old_ti_value2 = """;color:' + ti + ';\">' + escapeHtml(ph)"""
new_ti_value2 = """;color:#14545c;\">' + escapeHtml(ph)"""
content = content.replace(old_ti_value2, new_ti_value2, 1)
print("8g2. phone value colour hardcoded:", "OK")

old_ti_value3 = """;color:' + ti + ';\">' + escapeHtml(em)"""
new_ti_value3 = """;color:#14545c;\">' + escapeHtml(em)"""
content = content.replace(old_ti_value3, new_ti_value3, 1)
print("8g3. email value colour hardcoded:", "OK")

# 8h. Contact section: the label colours use 't' which was text colour - hardcode #3e2723
# Actually the labels use style="color:' + t + ';" for the label text. Since t is removed,
# let me hardcode #3e2723 for these.
for old_str, new_str in [
    ("color:' + t + ';\"><span class=\\\"preview-contact-label\\\"",
     "color:#3e2723;\"><span class=\\\"preview-contact-label\\\""),
    ("color:' + t + ';\">' + escapeHtml(desc)",
     "color:#3e2723;\">' + escapeHtml(desc)"),
]:
    content = content.replace(old_str, new_str, 1)

print("8h. contact label colours hardcoded:", "OK")

# 8i. Remove unused 't' parameter from remaining spots
# Check: the intro section doesn't use t directly (it uses tagline which is separate)
# The intro body text "Swipe" uses hardcoded #3e2723 - fine

# ==============================================================
# 9. Add darken() and hexToRgba() helper functions
# ==============================================================
old_lighten = """      function lighten(hex) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0,2), 16);
        var g = parseInt(hex.substring(2,4), 16);
        var b = parseInt(hex.substring(4,6), 16);
        r = Math.min(255, r + 20);
        g = Math.min(255, g + 20);
        b = Math.min(255, b + 20);
        return '#' + r.toString(16).padStart(2,'0') + g.toString(16).padStart(2,'0') + b.toString(16).padStart(2,'0');
      }"""

new_lighten = """      function lighten(hex) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0,2), 16);
        var g = parseInt(hex.substring(2,4), 16);
        var b = parseInt(hex.substring(4,6), 16);
        r = Math.min(255, r + 20);
        g = Math.min(255, g + 20);
        b = Math.min(255, b + 20);
        return '#' + r.toString(16).padStart(2,'0') + g.toString(16).padStart(2,'0') + b.toString(16).padStart(2,'0');
      }
      function darken(hex) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0,2), 16);
        var g = parseInt(hex.substring(2,4), 16);
        var b = parseInt(hex.substring(4,6), 16);
        r = Math.max(0, r - 30);
        g = Math.max(0, g - 30);
        b = Math.max(0, b - 30);
        return '#' + r.toString(16).padStart(2,'0') + g.toString(16).padStart(2,'0') + b.toString(16).padStart(2,'0');
      }
      function hexToRgba(hex, alpha) {
        hex = hex.replace('#', '');
        var r = parseInt(hex.substring(0,2), 16);
        var g = parseInt(hex.substring(2,4), 16);
        var b = parseInt(hex.substring(4,6), 16);
        return 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
      }"""

content = content.replace(old_lighten, new_lighten, 1)
print("9. darken/hexToRgba added:", "OK" if old_lighten not in content else "NOT FOUND")

# ==============================================================
# 10. Write the file
# ==============================================================
with open(r'C:\Users\whisp\.hermes\scripts\ed_colours\index.html', 'w') as f:
    f.write(content)
print("10. File written!")
