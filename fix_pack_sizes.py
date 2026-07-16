# Fix per-size checkboxes in packs and wholesale accordions
# Also fix updatePackTotal/updateWholesaleTotal to use per-size pricing

with open(r'G:\EverdreamCard\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===== CHANGE A: Pack refreshProductCheckboxes - per-size rows =====
old_pack_refresh = """        function refreshProductCheckboxes() {
          var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
          prodList.innerHTML = '';
          if (!prods.length) {
            prodList.innerHTML = '<p style=\"font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#5d4037;\">Add products first.</p>';
            return;
          }
          prods.forEach(function (p, pi) {
            var row = document.createElement('div');
            row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
            var cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.className = 'cc-pack-prod-cb';
            cb.dataset.prodIdx = pi;
            /* Check if this product was previously in the pack */
            if (items && items[pi]) cb.checked = true;
            var qty = document.createElement('input');
            qty.type = 'number';
            qty.min = 1;
            qty.value = (items && items[pi] && items[pi].qty) ? items[pi].qty : 1;
            qty.style.width = '3rem';
            qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
            var nameSpan = document.createElement('span');
            nameSpan.textContent = p.name;
            row.appendChild(cb);
            row.appendChild(qty);
            row.appendChild(nameSpan);
            /* Update total on checkbox/qty change */
            cb.addEventListener('change', function () { saveCustomiserState(); updatePackTotal(_idx); });
            qty.addEventListener('input', function () { saveCustomiserState(); updatePackTotal(_idx); });
            prodList.appendChild(row);
          });
        }"""

new_pack_refresh = """        function refreshProductCheckboxes() {
          var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
          prodList.innerHTML = '';
          if (!prods.length) {
            prodList.innerHTML = '<p style=\"font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#5d4037;\">Add products first.</p>';
            return;
          }
          prods.forEach(function (p, pi) {
            var sizes = p.sizes && p.sizes.length ? p.sizes : [{ name: '', price: '' }];
            sizes.forEach(function (sz, si) {
              var key = pi + ':' + si;
              var row = document.createElement('div');
              row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
              var cb = document.createElement('input');
              cb.type = 'checkbox';
              cb.className = 'cc-pack-prod-cb';
              cb.dataset.key = key;
              /* Check if this size was previously in the pack */
              if (items && items[key]) cb.checked = true;
              var qty = document.createElement('input');
              qty.type = 'number';
              qty.min = 1;
              qty.value = (items && items[key] && items[key].qty) ? items[key].qty : 1;
              qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
              var nameSpan = document.createElement('span');
              var label = p.name;
              if (sz.name) label += ' - ' + sz.name;
              if (sz.price) label += ' - ' + sz.price;
              nameSpan.textContent = label;
              row.appendChild(cb);
              row.appendChild(qty);
              row.appendChild(nameSpan);
              /* Update total on checkbox/qty change */
              cb.addEventListener('change', function () { saveCustomiserState(); updatePackTotal(_idx); });
              qty.addEventListener('input', function () { saveCustomiserState(); updatePackTotal(_idx); });
              prodList.appendChild(row);
            });
          });
        }"""

if old_pack_refresh in html:
    html = html.replace(old_pack_refresh, new_pack_refresh)
    print("CHANGE A: Pack refreshProductCheckboxes per-size ✓")
else:
    print("CHANGE A FAIL: Pack refresh not found")

# ===== CHANGE B: Wholesale refreshWholesaleCheckboxes - per-size rows =====
old_wholesale_refresh = """        function refreshWholesaleCheckboxes() {
          /* Update total when checkboxes are re-rendered */
          var _idx = index;
          var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
          prodList.innerHTML = '';
          if (!prods.length) {
            prodList.innerHTML = '<p style=\"font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#5d4037;\">Add products first.</p>';
            return;
          }
          prods.forEach(function (p, pi) {
            var row = document.createElement('div');
            row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
            var cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.className = 'cc-wholesale-prod-cb';
            cb.dataset.prodIdx = pi;
            if (items && items[pi]) cb.checked = true;
            var qty = document.createElement('input');
            qty.type = 'number';
            qty.min = 1;
            qty.value = (items && items[pi] && items[pi].qty) ? items[pi].qty : 1;
            qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
            var nameSpan = document.createElement('span');
            nameSpan.textContent = p.name;
            row.appendChild(cb);
            row.appendChild(qty);
            row.appendChild(nameSpan);
            /* Update total on checkbox/qty change */
            cb.addEventListener('change', function () { saveCustomiserState(); updateWholesaleTotal(_idx); });
            qty.addEventListener('input', function () { saveCustomiserState(); updateWholesaleTotal(_idx); });
            prodList.appendChild(row);
          });
        }"""

new_wholesale_refresh = """        function refreshWholesaleCheckboxes() {
          /* Update total when checkboxes are re-rendered */
          var _idx = index;
          var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
          prodList.innerHTML = '';
          if (!prods.length) {
            prodList.innerHTML = '<p style=\"font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#5d4037;\">Add products first.</p>';
            return;
          }
          prods.forEach(function (p, pi) {
            var sizes = p.sizes && p.sizes.length ? p.sizes : [{ name: '', price: '' }];
            sizes.forEach(function (sz, si) {
              var key = pi + ':' + si;
              var row = document.createElement('div');
              row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
              var cb = document.createElement('input');
              cb.type = 'checkbox';
              cb.className = 'cc-wholesale-prod-cb';
              cb.dataset.key = key;
              if (items && items[key]) cb.checked = true;
              var qty = document.createElement('input');
              qty.type = 'number';
              qty.min = 1;
              qty.value = (items && items[key] && items[key].qty) ? items[key].qty : 1;
              qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
              var nameSpan = document.createElement('span');
              var label = p.name;
              if (sz.name) label += ' - ' + sz.name;
              if (sz.price) label += ' - ' + sz.price;
              nameSpan.textContent = label;
              row.appendChild(cb);
              row.appendChild(qty);
              row.appendChild(nameSpan);
              /* Update total on checkbox/qty change */
              cb.addEventListener('change', function () { saveCustomiserState(); updateWholesaleTotal(_idx); });
              qty.addEventListener('input', function () { saveCustomiserState(); updateWholesaleTotal(_idx); });
              prodList.appendChild(row);
            });
          });
        }"""

if old_wholesale_refresh in html:
    html = html.replace(old_wholesale_refresh, new_wholesale_refresh)
    print("CHANGE B: Wholesale refreshWholesaleCheckboxes per-size ✓")
else:
    print("CHANGE B FAIL: Wholesale refresh not found")

# ===== CHANGE C: getPacksArray - use prodIdx:sizeIdx keys =====
old_get_packs = """      function getPacksArray() {
        var wrappers = document.querySelectorAll('#cc-packs-container .cc-inner-product');
        var packs = [];
        wrappers.forEach(function (w) {
          var name = (w.querySelector('.cc-pack-name') || {}).value || '';
          var price = (w.querySelector('.cc-pack-price') || {}).value || '';
          var cbs = w.querySelectorAll('.cc-pack-prod-cb');
          var qtys = w.querySelectorAll('.cc-pack-prod-cb + input[type=\"number\"]');
          var items = {};
          cbs.forEach(function (cb, i) {
            if (cb.checked) {
              var qtyInput = qtys[i];
              items[cb.dataset.prodIdx] = { qty: parseInt(qtyInput ? qtyInput.value : 1) || 1 };
            }
          });
          packs.push({ name: name, price: price, items: items });
        });
        return packs;
      }"""

new_get_packs = """      function getPacksArray() {
        var wrappers = document.querySelectorAll('#cc-packs-container .cc-inner-product');
        var packs = [];
        wrappers.forEach(function (w) {
          var name = (w.querySelector('.cc-pack-name') || {}).value || '';
          var price = (w.querySelector('.cc-pack-price') || {}).value || '';
          var cbs = w.querySelectorAll('.cc-pack-prod-cb');
          var qtys = w.querySelectorAll('.cc-pack-prod-cb + input[type=\"number\"]');
          var items = {};
          cbs.forEach(function (cb, i) {
            if (cb.checked) {
              var qtyInput = qtys[i];
              items[cb.dataset.key] = { qty: parseInt(qtyInput ? qtyInput.value : 1) || 1 };
            }
          });
          packs.push({ name: name, price: price, items: items });
        });
        return packs;
      }"""

if old_get_packs in html:
    html = html.replace(old_get_packs, new_get_packs)
    print("CHANGE C: getPacksArray uses key ✓")
else:
    print("CHANGE C FAIL: getPacksArray not found")

# ===== CHANGE D: getWholesaleArray - use prodIdx:sizeIdx keys =====
old_get_wholesale = """      function getWholesaleArray() {
        var wrappers = document.querySelectorAll('#cc-wholesale-container .cc-inner-product');
        var wholesalePacks = [];
        wrappers.forEach(function (w) {
          var name = (w.querySelector('.cc-wholesale-name') || {}).value || '';
          var price = (w.querySelector('.cc-wholesale-price') || {}).value || '';
          var cbs = w.querySelectorAll('.cc-wholesale-prod-cb');
          var qtys = w.querySelectorAll('.cc-wholesale-prod-cb + input[type=\"number\"]');
          var items = {};
          cbs.forEach(function (cb, i) {
            if (cb.checked) {
              var qtyInput = qtys[i];
              items[cb.dataset.prodIdx] = { qty: parseInt(qtyInput ? qtyInput.value : 1) || 1 };
            }
          });
          wholesalePacks.push({ name: name, price: price, items: items });
        });
        return wholesalePacks;
              }"""

new_get_wholesale = """      function getWholesaleArray() {
        var wrappers = document.querySelectorAll('#cc-wholesale-container .cc-inner-product');
        var wholesalePacks = [];
        wrappers.forEach(function (w) {
          var name = (w.querySelector('.cc-wholesale-name') || {}).value || '';
          var price = (w.querySelector('.cc-wholesale-price') || {}).value || '';
          var cbs = w.querySelectorAll('.cc-wholesale-prod-cb');
          var qtys = w.querySelectorAll('.cc-wholesale-prod-cb + input[type=\"number\"]');
          var items = {};
          cbs.forEach(function (cb, i) {
            if (cb.checked) {
              var qtyInput = qtys[i];
              items[cb.dataset.key] = { qty: parseInt(qtyInput ? qtyInput.value : 1) || 1 };
            }
          });
          wholesalePacks.push({ name: name, price: price, items: items });
        });
        return wholesalePacks;
              }"""

if old_get_wholesale in html:
    html = html.replace(old_get_wholesale, new_get_wholesale)
    print("CHANGE D: getWholesaleArray uses key ✓")
else:
    print("CHANGE D FAIL: getWholesaleArray not found")

# ===== CHANGE E: updatePackTotal - use per-size pricing =====
old_update_pack = """              function updatePackTotal(index) {
                var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
                var containers = document.querySelectorAll('#cc-packs-container .cc-inner-product');
                var container = containers[index];
                if (!container) return;
                var cbs = container.querySelectorAll('.cc-pack-prod-cb');
                var qtys = container.querySelectorAll('.cc-pack-prod-cb + input[type=\"number\"]');
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
              }"""

new_update_pack = """              function updatePackTotal(index) {
                var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
                var containers = document.querySelectorAll('#cc-packs-container .cc-inner-product');
                var container = containers[index];
                if (!container) return;
                var cbs = container.querySelectorAll('.cc-pack-prod-cb');
                var qtys = container.querySelectorAll('.cc-pack-prod-cb + input[type=\"number\"]');
                var priceInput = container.querySelector('.cc-pack-price');
                var totalDiv = container.querySelector('.cc-pack-total');
                if (!totalDiv) return;

                var totalContents = 0;
                cbs.forEach(function (cb, i) {
                  if (cb.checked) {
                    var key = cb.dataset.key;
                    var parts = key.split(':');
                    var pi = parseInt(parts[0]);
                    var si = parseInt(parts[1] || 0);
                    var prod = prods[pi];
                    var qty = parseInt(qtys[i] ? qtys[i].value : 1) || 1;
                    if (prod && prod.sizes && prod.sizes.length > si) {
                      var price = parsePrice(prod.sizes[si].price);
                      totalContents += price * qty;
                    } else if (prod && prod.sizes && prod.sizes.length) {
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
              }"""

if old_update_pack in html:
    html = html.replace(old_update_pack, new_update_pack)
    print("CHANGE E: updatePackTotal per-size ✓")
else:
    print("CHANGE E FAIL: updatePackTotal not found")

# ===== CHANGE F: updateWholesaleTotal - use per-size pricing =====
old_update_wholesale = """              function updateWholesaleTotal(index) {
                var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
                var containers = document.querySelectorAll('#cc-wholesale-container .cc-inner-product');
                var container = containers[index];
                if (!container) return;
                var cbs = container.querySelectorAll('.cc-wholesale-prod-cb');
                var qtys = container.querySelectorAll('.cc-wholesale-prod-cb + input[type=\"number\"]');
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
              }"""

new_update_wholesale = """              function updateWholesaleTotal(index) {
                var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
                var containers = document.querySelectorAll('#cc-wholesale-container .cc-inner-product');
                var container = containers[index];
                if (!container) return;
                var cbs = container.querySelectorAll('.cc-wholesale-prod-cb');
                var qtys = container.querySelectorAll('.cc-wholesale-prod-cb + input[type=\"number\"]');
                var priceInput = container.querySelector('.cc-wholesale-price');
                var totalDiv = container.querySelector('.cc-wholesale-total');
                if (!totalDiv) return;

                var totalContents = 0;
                cbs.forEach(function (cb, i) {
                  if (cb.checked) {
                    var key = cb.dataset.key;
                    var parts = key.split(':');
                    var pi = parseInt(parts[0]);
                    var si = parseInt(parts[1] || 0);
                    var prod = prods[pi];
                    var qty = parseInt(qtys[i] ? qtys[i].value : 1) || 1;
                    if (prod && prod.sizes && prod.sizes.length > si) {
                      var price = parsePrice(prod.sizes[si].price);
                      totalContents += price * qty;
                    } else if (prod && prod.sizes && prod.sizes.length) {
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
              }"""

if old_update_wholesale in html:
    html = html.replace(old_update_wholesale, new_update_wholesale)
    print("CHANGE F: updateWholesaleTotal per-size ✓")
else:
    print("CHANGE F FAIL: updateWholesaleTotal not found")

# ===== Write =====
with open(r'G:\EverdreamCard\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\nAll changes applied")
