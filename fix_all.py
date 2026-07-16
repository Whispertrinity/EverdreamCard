# Changes:
# 1. Make cc-ip-save-btn green instead of teal
# 2. Change "Remove pack" → "Remove", "Remove product" → "Remove", "Remove wholesale" → "Remove"
# 3. Add total value + % diff calculation to pack and wholesale accordions

with open(r'G:\EverdreamCard\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# === CHANGE 1: cc-ip-save-btn green ===
old = '''    .cc-ip-save-btn {
      display: block;
      margin: 0.6rem auto 0;
      padding: 0.4rem 1.2rem;
      font-family: 'The Wanters DEMO', serif;
      font-size: 0.85rem;
      font-weight: 600;
      color: #f5f5dc;
      background: linear-gradient(135deg,#14545c 0%,#1a6b75 50%,#14545c 100%);
      border: 2px solid #0a1a1d;
      border-radius: 9999px;
      cursor: pointer;
      -webkit-text-stroke: 0.6px #000;
      text-stroke: 0.6px #000;
      paint-order: stroke fill;
      -webkit-paint-order: stroke fill;
    }
    .cc-ip-save-btn:hover { transform: translateY(-1px); }'''

new = '''    .cc-ip-save-btn {
      display: block;
      margin: 0.6rem auto 0;
      padding: 0.4rem 1.2rem;
      font-family: 'The Wanters DEMO', serif;
      font-size: 0.85rem;
      font-weight: 600;
      color: #f5f5dc;
      background: linear-gradient(135deg,#1b5e20 0%,#2e7d32 50%,#1b5e20 100%);
      border: 2px solid #0d3b0f;
      border-radius: 9999px;
      cursor: pointer;
      -webkit-text-stroke: 0.6px #000;
      text-stroke: 0.6px #000;
      paint-order: stroke fill;
      -webkit-paint-order: stroke fill;
    }
    .cc-ip-save-btn:hover { transform: translateY(-1px); }'''

if old in html:
    html = html.replace(old, new)
    changes += 1
    print(f"CHANGE 1: cc-ip-save-btn → green ✓")
else:
    print("CHANGE 1 FAIL: cc-ip-save-btn CSS not found")

# === CHANGE 2: "Remove pack" → "Remove", etc ===
for old_text, new_text in [
    ("removeBtn.textContent = 'Remove pack';", "removeBtn.textContent = 'Remove';"),
    ("removeBtn.textContent = 'Remove wholesale';", "removeBtn.textContent = 'Remove';"),
    ("removeBtn.textContent = 'Remove product';", "removeBtn.textContent = 'Remove';"),
]:
    count = html.count(old_text)
    if count > 0:
        html = html.replace(old_text, new_text)
        changes += count
        print(f"CHANGE 2: '{old_text}' → '{new_text}' ({count} occurrences) ✓")
    else:
        print(f"CHANGE 2: '{old_text}' NOT FOUND ✗")

# === CHANGE 3: Add total value + % diff to packs accordion ===
# We need to insert a total-value div after the prodList in createPackAccordion
# and update refreshProductCheckboxes to update the total on checkbox/qty change

# First, find and enhance the pack accordion body assembly
# After `body.appendChild(prodList);` add the total value div
old_body = '''body.appendChild(prodListLabel);
        body.appendChild(prodList);
        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:0.5rem;margin-top:0.6rem;';
        saveBtn.style.flex = '1';
        removeBtn.style.flex = '1';
        btnRow.appendChild(saveBtn);
        btnRow.appendChild(removeBtn);
        body.appendChild(btnRow);'''

new_body = '''body.appendChild(prodListLabel);
        body.appendChild(prodList);
        /* Total value line */
        var totalDiv = document.createElement('div');
        totalDiv.className = 'cc-pack-total';
        totalDiv.id = 'cc-pack-total-' + index;
        totalDiv.style.cssText = 'margin-top:0.5rem;padding:0.4rem 0.5rem;border-top:1px dashed #5d4037;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#3e2723;text-align:center;';
        totalDiv.textContent = 'Total contents value: —';
        body.appendChild(totalDiv);
        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:0.5rem;margin-top:0.6rem;';
        saveBtn.style.flex = '1';
        removeBtn.style.flex = '1';
        btnRow.appendChild(saveBtn);
        btnRow.appendChild(removeBtn);
        body.appendChild(btnRow);'''

if old_body in html:
    html = html.replace(old_body, new_body)
    changes += 1
    print(f"CHANGE 3: Pack total value div added ✓")
else:
    print("CHANGE 3 FAIL: Pack body assembly not found")

# Same for wholesale accordion
old_body_w = '''body.appendChild(prodListLabel);
        body.appendChild(prodList);
        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:0.5rem;margin-top:0.6rem;';
        saveBtn.style.flex = '1';
        removeBtn.style.flex = '1';
        btnRow.appendChild(saveBtn);
        btnRow.appendChild(removeBtn);
        body.appendChild(btnRow);'''

new_body_w = '''body.appendChild(prodListLabel);
        body.appendChild(prodList);
        /* Total value line */
        var totalDiv = document.createElement('div');
        totalDiv.className = 'cc-wholesale-total';
        totalDiv.id = 'cc-wholesale-total-' + index;
        totalDiv.style.cssText = 'margin-top:0.5rem;padding:0.4rem 0.5rem;border-top:1px dashed #5d4037;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#3e2723;text-align:center;';
        totalDiv.textContent = 'Total contents value: —';
        body.appendChild(totalDiv);
        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:0.5rem;margin-top:0.6rem;';
        saveBtn.style.flex = '1';
        removeBtn.style.flex = '1';
        btnRow.appendChild(saveBtn);
        btnRow.appendChild(removeBtn);
        body.appendChild(btnRow);'''

if old_body_w in html:
    html = html.replace(old_body_w, new_body_w)
    changes += 1
    print(f"CHANGE 3b: Wholesale total value div added ✓")
else:
    print("CHANGE 3b FAIL: Wholesale body assembly not found")

# === CHANGE 4: Add a calculatePackTotal function and update refreshProductCheckboxes ===
# Add the helper function before the "/* Add pack button */" comment
# Find the pack refreshProductCheckboxes to add total calculation
# We need to modify the refreshProductCheckboxes within createPackAccordion
# to recalculate total after any checkbox/qty change

# Let's add a parsePrice helper and the recalculation logic
# First find the priceInput event listeners and add update on change
old_price_listeners = '''[nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', saveCustomiserState);
          el.addEventListener('change', saveCustomiserState);
        });'''

# There are two of these — one for pack (line ~3884), one for wholesale (line ~4027)
# We'll modify both to also update the total

# For packs — this snippet appears first in the pack function
new_price_listeners = '''[nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', function() { saveCustomiserState(); updatePackTotal(index); });
          el.addEventListener('change', function() { saveCustomiserState(); updatePackTotal(index); });
        });'''

# We'll replace the first occurrence (packs) but there are two identical blocks
# Let me use more context to be precise

# Actually, the block [nameInput, priceInput].forEach appears:
# - In createProductAccordion (product - line 3711) — no price input, just name/desc
# - In createPackAccordion (pack - line 3884) — nameInput + priceInput
# - In createWholesaleAccordion (wholesale - line 4027) — nameInput + priceInput

# For product (no price):
old_product_listeners = '''[nameInput, descInput].forEach(function (el) {
          el.addEventListener('input', saveCustomiserState);
          el.addEventListener('change', saveCustomiserState);
        });'''

# This is fine — leave it

# For pack — the one right before return wrapper
# Need to find the last occurrence of [nameInput, priceInput].forEach in the file
# Let me search for both
count = html.count('''[nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', saveCustomiserState);
          el.addEventListener('change', saveCustomiserState);
        });''')

print(f"Found {count} occurrences of [nameInput, priceInput].forEach")

# Replace the pack one (check context: depends on which function it's in)
# Let me replace all pack/wholesale specific ones with extra context

# Find the pack-specific one (near return wrapper after body.appendChild(btnRow))
old_pack_return = '''body.appendChild(btnRow);

        header.addEventListener('click', function () {
          var expanded = this.getAttribute('aria-expanded') === 'true';
          this.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          body.classList.toggle('open');
        });

        wrapper.appendChild(header);
        wrapper.appendChild(body);
        container.appendChild(wrapper);

        [nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', saveCustomiserState);
          el.addEventListener('change', saveCustomiserState);
        });

        return wrapper;
      }

      function renumberPackAccordions()'''

new_pack_return = '''body.appendChild(btnRow);

        header.addEventListener('click', function () {
          var expanded = this.getAttribute('aria-expanded') === 'true';
          this.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          body.classList.toggle('open');
        });

        wrapper.appendChild(header);
        wrapper.appendChild(body);
        container.appendChild(wrapper);

        [nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', function() { saveCustomiserState(); updatePackTotal(index); });
          el.addEventListener('change', function() { saveCustomiserState(); updatePackTotal(index); });
        });

        return wrapper;
      }

      function renumberPackAccordions()'''

if old_pack_return in html:
    html = html.replace(old_pack_return, new_pack_return)
    changes += 1
    print(f"CHANGE 4a: Pack event listeners include updatePackTotal ✓")
else:
    print("CHANGE 4a FAIL: Pack return wrapper pattern not found")

# Same for wholesale
old_wholesale_return = '''body.appendChild(btnRow);

        header.addEventListener('click', function () {
          var expanded = this.getAttribute('aria-expanded') === 'true';
          this.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          body.classList.toggle('open');
        });

        wrapper.appendChild(header);
        wrapper.appendChild(body);
        container.appendChild(wrapper);

        [nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', saveCustomiserState);
          el.addEventListener('change', saveCustomiserState);
        });

        return wrapper;
      }

      function renumberWholesaleAccordions()'''

new_wholesale_return = '''body.appendChild(btnRow);

        header.addEventListener('click', function () {
          var expanded = this.getAttribute('aria-expanded') === 'true';
          this.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          body.classList.toggle('open');
        });

        wrapper.appendChild(header);
        wrapper.appendChild(body);
        container.appendChild(wrapper);

        [nameInput, priceInput].forEach(function (el) {
          el.addEventListener('input', function() { saveCustomiserState(); updateWholesaleTotal(index); });
          el.addEventListener('change', function() { saveCustomiserState(); updateWholesaleTotal(index); });
        });

        return wrapper;
      }

      function renumberWholesaleAccordions()'''

if old_wholesale_return in html:
    html = html.replace(old_wholesale_return, new_wholesale_return)
    changes += 1
    print(f"CHANGE 4b: Wholesale event listeners include updateWholesaleTotal ✓")
else:
    print("CHANGE 4b FAIL: Wholesale return wrapper pattern not found")

# === CHANGE 5: Add the calculation helper function ===
# Insert after getWholesaleArray function (before "function renumberWholesaleAccordions" section)
# Find the closing brace of getWholesaleArray

old_wholesale_getter_end = '''return wholesalePacks;
      }

      function renumberWholesaleAccordions()'''

new_helpers = '''return wholesalePacks;
      }

      /* Parse a price string like "$5" or "10" or "$150" to a number */
      function parsePrice(priceStr) {
        if (!priceStr) return 0;
        var cleaned = priceStr.replace(/[^\\d.]/g, '');
        var val = parseFloat(cleaned);
        return isNaN(val) ? 0 : val;
      }

      /* Update the total contents value for a pack accordion */
      function updatePackTotal(index) {
        var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
        var container = document.querySelectorAll('#cc-packs-container .cc-inner-product')['' + index];
        if (!container) return;
        var cbs = container.querySelectorAll('.cc-pack-prod-cb');
        var qtys = container.querySelectorAll('.cc-pack-prod-cb + input[type="number"]');
        var priceInput = container.querySelector('.cc-pack-price');
        var totalDiv = container.querySelector('.cc-pack-total');
        if (!totalDiv) return;

        var totalContents = 0;
        cbs.forEach(function (cb, i) {
          if (cb.checked) {
            var pi = parseInt(cb.dataset.prodIdx);
            var prod = prods[pi];
            var qty = parseInt(qtys[i] ? qtys[i].value : 1) || 1;
            if (prod && prod.sizes && prod.sizes.length) {
              /* Use the first size's price for calculation */
              var price = parsePrice(prod.sizes[0].price);
              totalContents += price * qty;
            }
          }
        });

        var packPrice = parsePrice(priceInput ? priceInput.value : '');
        if (totalContents > 0) {
          var diff = totalContents - packPrice;
          var pct = ((diff / totalContents) * 100).toFixed(1);
          var sign = diff >= 0 ? '-' : '+';
          totalDiv.textContent = 'Total value: $' + totalContents.toFixed(2) + '  |  Pack price: $' + (packPrice > 0 ? packPrice.toFixed(2) : '—') +
            (packPrice > 0 ? '  |  ' + sign + pct + '% ($' + Math.abs(diff).toFixed(2) + ')' : '');
        } else {
          totalDiv.textContent = 'Total contents value: —';
        }
      }

      /* Update the total contents value for a wholesale accordion */
      function updateWholesaleTotal(index) {
        var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
        var container = document.querySelectorAll('#cc-wholesale-container .cc-inner-product')['' + index];
        if (!container) return;
        var cbs = container.querySelectorAll('.cc-wholesale-prod-cb');
        var qtys = container.querySelectorAll('.cc-wholesale-prod-cb + input[type="number"]');
        var priceInput = container.querySelector('.cc-wholesale-price');
        var totalDiv = container.querySelector('.cc-wholesale-total');
        if (!totalDiv) return;

        var totalContents = 0;
        cbs.forEach(function (cb, i) {
          if (cb.checked) {
            var pi = parseInt(cb.dataset.prodIdx);
            var prod = prods[pi];
            var qty = parseInt(qtys[i] ? qtys[i].value : 1) || 1;
            if (prod && prod.sizes && prod.sizes.length) {
              var price = parsePrice(prod.sizes[0].price);
              totalContents += price * qty;
            }
          }
        });

        var packPrice = parsePrice(priceInput ? priceInput.value : '');
        if (totalContents > 0) {
          var diff = totalContents - packPrice;
          var pct = ((diff / totalContents) * 100).toFixed(1);
          var sign = diff >= 0 ? '-' : '+';
          totalDiv.textContent = 'Total value: $' + totalContents.toFixed(2) + '  |  Pack price: $' + (packPrice > 0 ? packPrice.toFixed(2) : '—') +
            (packPrice > 0 ? '  |  ' + sign + pct + '% ($' + Math.abs(diff).toFixed(2) + ')' : '');
        } else {
          totalDiv.textContent = 'Total contents value: —';
        }
      }

      function renumberWholesaleAccordions()'''

if old_wholesale_getter_end in html:
    html = html.replace(old_wholesale_getter_end, new_helpers)
    changes += 1
    print(f"CHANGE 5: parsePrice + updatePackTotal + updateWholesaleTotal helpers added ✓")
else:
    print("CHANGE 5 FAIL: getWholesaleArray closing pattern not found")

# === CHANGE 6: Also update refreshProductCheckboxes in packs to call updatePackTotal ===
# This is for pack accordion
old_refresh_end = '''refreshProductCheckboxes();'''

# Replace the one in createPackAccordion — need to identify it uniquely
# It's preceded by "/* Products in pack */" in pack, and "/* Products in wholesale pack */" in wholesale

old_pack_refresh_start = '''        /* Products in pack */
        var prodListLabel = document.createElement('label');
        prodListLabel.className = 'customiser-label';
        prodListLabel.textContent = 'Products in this pack';
        var prodList = document.createElement('div');
        prodList.className = 'cc-pack-product-list';
        prodList.id = 'cc-pack-prods-' + index;

        function refreshProductCheckboxes() {'''

new_pack_refresh_start = '''        /* Products in pack */
        var prodListLabel = document.createElement('label');
        prodListLabel.className = 'customiser-label';
        prodListLabel.textContent = 'Products in this pack';
        var prodList = document.createElement('div');
        prodList.className = 'cc-pack-product-list';
        prodList.id = 'cc-pack-prods-' + index;

        function refreshProductCheckboxes() {
          /* Update total when checkboxes are re-rendered */
          var _idx = index;'''

# And add the total update call after refreshProductCheckboxes() call
old_refresh_call = '''        }
        refreshProductCheckboxes();

        /* Save button */'''

new_refresh_call = '''        }
        refreshProductCheckboxes();
        /* Calculate initial total */
        setTimeout(function() { updatePackTotal(_idx); }, 10);

        /* Save button */'''

if old_refresh_call in html:
    html = html.replace(old_refresh_call, new_refresh_call)
    changes += 1
    print(f"CHANGE 6: Initial pack total calculation ✓")
else:
    print("CHANGE 6 FAIL: refreshProductCheckboxes call not found")

# Same for wholesale
old_wholesale_refresh_start = '''        /* Products in wholesale pack */
        var prodListLabel = document.createElement('label');
        prodListLabel.className = 'customiser-label';
        prodListLabel.textContent = 'Products in this wholesale pack';
        var prodList = document.createElement('div');
        prodList.className = 'cc-wholesale-product-list';
        prodList.id = 'cc-wholesale-prods-' + index;

        function refreshWholesaleCheckboxes() {'''

new_wholesale_refresh_start = '''        /* Products in wholesale pack */
        var prodListLabel = document.createElement('label');
        prodListLabel.className = 'customiser-label';
        prodListLabel.textContent = 'Products in this wholesale pack';
        var prodList = document.createElement('div');
        prodList.className = 'cc-wholesale-product-list';
        prodList.id = 'cc-wholesale-prods-' + index;

        function refreshWholesaleCheckboxes() {
          /* Update total when checkboxes are re-rendered */
          var _idx = index;'''

if old_wholesale_refresh_start in html:
    html = html.replace(old_wholesale_refresh_start, new_wholesale_refresh_start)
    changes += 1
    print(f"CHANGE 6b: Wholesale refresh _idx var added ✓")
else:
    print("CHANGE 6b FAIL: Wholesale refresh start not found")

old_wholesale_refresh_call = '''        }
        refreshWholesaleCheckboxes();

        var saveBtn = document.createElement('button');'''

new_wholesale_refresh_call = '''        }
        refreshWholesaleCheckboxes();
        /* Calculate initial total */
        setTimeout(function() { updateWholesaleTotal(_idx); }, 10);

        var saveBtn = document.createElement('button');'''

if old_wholesale_refresh_call in html:
    html = html.replace(old_wholesale_refresh_call, new_wholesale_refresh_call)
    changes += 1
    print(f"CHANGE 6c: Initial wholesale total calculation ✓")
else:
    print("CHANGE 6c FAIL: Wholesale refresh call not found")

# Also update the checkbox+priceInput change listeners within refreshProductCheckboxes
# to recalculate total on any qty/checkbox change
# Find the cb/qty elements in refreshProductCheckboxes and add change handlers

print(f"\nTotal changes: {changes}")

with open(r'G:\EverdreamCard\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("File written")
