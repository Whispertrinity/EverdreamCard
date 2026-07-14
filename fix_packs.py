import re
import os

os.chdir(r'C:\Users\whisp\.hermes\scripts\everdream_work')

with open('index.html', 'r') as f:
    content = f.read()

old_refresh = """        function refreshProductCheckboxes() {
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
            prodList.appendChild(row);
          });
        }"""

new_refresh = """        function refreshProductCheckboxes() {
          var prods = getProductsArray().filter(function (p) { return p.name.trim(); });
          prodList.innerHTML = '';
          if (!prods.length) {
            prodList.innerHTML = '<p style=\"font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;color:#5d4037;\">Add products first.</p>';
            return;
          }
          var rowIdx = 0;
          prods.forEach(function (p, pi) {
            if (!p.sizes || !p.sizes.length) {
              var row = document.createElement('div');
              row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
              var cb = document.createElement('input');
              cb.type = 'checkbox';
              cb.className = 'cc-pack-prod-cb';
              cb.dataset.prodIdx = pi;
              cb.dataset.sizeIdx = '-1';
              if (items && items[rowIdx]) cb.checked = true;
              var qty = document.createElement('input');
              qty.type = 'number';
              qty.min = 1;
              qty.value = (items && items[rowIdx] && items[rowIdx].qty) ? items[rowIdx].qty : 1;
              qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
              var nameSpan = document.createElement('span');
              nameSpan.textContent = p.name;
              row.appendChild(cb);
              row.appendChild(qty);
              row.appendChild(nameSpan);
              prodList.appendChild(row);
              rowIdx++;
            } else {
              p.sizes.forEach(function (sz, si) {
                if (!sz.name && !sz.price) return;
                var row = document.createElement('div');
                row.style.cssText = 'display:flex;align-items:center;gap:0.35rem;margin-bottom:0.25rem;font-family:Verdana,Geneva,sans-serif;font-size:0.85rem;color:#3e2723;';
                var cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.className = 'cc-pack-prod-cb';
                cb.dataset.prodIdx = pi;
                cb.dataset.sizeIdx = si;
                if (items && items[rowIdx]) cb.checked = true;
                var qty = document.createElement('input');
                qty.type = 'number';
                qty.min = 1;
                qty.value = (items && items[rowIdx] && items[rowIdx].qty) ? items[rowIdx].qty : 1;
                qty.style.cssText = 'width:3rem;padding:0.2rem 0.3rem;border:1px solid #5d4037;border-radius:6px;font-family:Verdana,Geneva,sans-serif;font-size:0.8rem;';
                var nameSpan = document.createElement('span');
                var label = p.name;
                if (sz.name) label += ' - ' + sz.name;
                if (sz.price) label += ' - ' + sz.price;
                nameSpan.textContent = label;
                row.appendChild(cb);
                row.appendChild(qty);
                row.appendChild(nameSpan);
                prodList.appendChild(row);
                rowIdx++;
              });
            }
          });
        }"""

content = content.replace(old_refresh, new_refresh, 1)
print("1. refreshProductCheckboxes:", "OK" if old_refresh not in content else "NOT FOUND")

old_getpacks = """      function getPacksArray() {
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

new_getpacks = """      function getPacksArray() {
        var wrappers = document.querySelectorAll('#cc-packs-container .cc-inner-product');
        var packs = [];
        wrappers.forEach(function (w) {
          var name = (w.querySelector('.cc-pack-name') || {}).value || '';
          var price = (w.querySelector('.cc-pack-price') || {}).value || '';
          var cbs = w.querySelectorAll('.cc-pack-prod-cb');
          var items = {};
          cbs.forEach(function (cb) {
            if (cb.checked) {
              var qtyInput = cb.parentNode.querySelector('input[type="number"]');
              var pi = cb.dataset.prodIdx;
              var si = cb.dataset.sizeIdx;
              var key = pi + ':' + si;
              items[key] = { qty: parseInt(qtyInput ? qtyInput.value : 1) || 1 };
            }
          });
          packs.push({ name: name, price: price, items: items });
        });
        return packs;
      }"""

content = content.replace(old_getpacks, new_getpacks, 1)
print("2. getPacksArray:", "OK" if old_getpacks not in content else "NOT FOUND")

old_email = """            var allProds = getProductsArray();
            Object.keys(pack.items).forEach(function (idx) {
              var prod = allProds[parseInt(idx)];
              if (prod) body += '      x' + pack.items[idx].qty + ' ' + prod.name + '\\n';
            });"""

new_email = """            var allProds = getProductsArray();
            Object.keys(pack.items).forEach(function (key) {
              var parts = key.split(':');
              var pi = parseInt(parts[0]);
              var si = parseInt(parts[1]);
              var prod = allProds[pi];
              if (prod) {
                var label = prod.name;
                if (!isNaN(si) && si >= 0 && prod.sizes && prod.sizes[si]) {
                  var sz = prod.sizes[si];
                  if (sz.name) label += ' - ' + sz.name;
                  if (sz.price) label += ' - ' + sz.price;
                }
                body += '      x' + pack.items[key].qty + ' ' + label + '\\n';
              }
            });"""

content = content.replace(old_email, new_email, 1)
print("3. buildDesignEmail:", "OK" if old_email not in content else "NOT FOUND")

with open('index.html', 'w') as f:
    f.write(content)
print("Done")
