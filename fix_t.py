with open(r'G:\EverdreamCard\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace remaining t references for contact labels
html = html.replace(
    "color:' + t + ';\\\"><span class=\\\"preview-contact-label\\\"",
    'color:#3e2723;\\\"><span class=\\"preview-contact-label\\"'
)

with open(r'G:\EverdreamCard\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
