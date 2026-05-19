import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/OpenClawData/workspace/potolki-chernivtsi/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Length:', len(c))
print('Has Chernivtsi:', 'Чернівці' in c)

# 1. Replace CSS variables — more yellow, grays instead of black
old_root = """  --bg:        #0a0b0d;
  --bg-2:      #111316;
  --panel:     #181b1f;
  --line:      #232730;
  --line-2:    #2f343e;
  --text:      #f0f2f5;
  --text-dim:  #8a909a;
  --accent:    #e8eaef;
  --accent-2:  #c9ccd2;
  --accent-d:  #8a8e96;
  --gold:      #F5C518;
  --red:       #e63946;
  --gold-old:   #d4af6f;
  --green:     #2ecc71;"""

new_root = """  --bg:        #2a2a2a;
  --bg-2:      #333333;
  --panel:     #3a3a3a;
  --line:      #4a4a4a;
  --line-2:    #666666;
  --text:      #f5f5f5;
  --text-dim:  #cccccc;
  --accent:    #F5C518;
  --accent-2:  #e8b810;
  --accent-d:  #d4a600;
  --gold:      #F5C518;
  --red:       #e63946;
  --gold-old:   #F5C518;
  --green:     #2ecc71;"""

if old_root in c:
    c = c.replace(old_root, new_root)
    print('1. CSS variables replaced')
else:
    print('1. CSS variables NOT found - checking...')
    # Try to find the actual content
    idx = c.find('--bg:')
    if idx >= 0:
        print('Found --bg at', idx)
        print('Context:', c[idx:idx+200])

# 2. Hero background and border
c = c.replace(
    'border-bottom:1px solid var(--line);\n}\n.hero-bg{',
    'border-bottom:3px solid var(--gold);\n  background:linear-gradient(135deg, #2a2a2a 0%, #333333 40%, #3a3a00 100%);\n}\n.hero-bg{'
)
print('2. Hero border/gradient done')

# 3. Hero glow colors
c = c.replace('rgba(232,234,239,.08)', 'rgba(245,197,24,.12)')
c = c.replace('rgba(212,175,111,.05)', 'rgba(245,197,24,.08)')
print('3. Hero glow colors done')

# 4. Section numbers
c = c.replace(
    'font-size:12px;\n  letter-spacing:.14em;\n  margin-bottom:14px;\n  display:flex;align-items:center;gap:10px;\n}\n.section-num::before{\n  content:"";width:28px;height:1px;background:var(--gold);',
    'font-size:13px;\n  font-weight:700;\n  letter-spacing:.14em;\n  margin-bottom:14px;\n  display:flex;align-items:center;gap:10px;\n}\n.section-num::before{\n  content:"";width:32px;height:2px;background:var(--gold);'
)
print('4. Section nums done')

# 5. Selection color
old_font_m = "  --font-m:    'JetBrains Mono', monospace;\n}"
new_font_m = "  --font-m:    'JetBrains Mono', monospace;\n}\n::selection{background:var(--gold);color:#111}"
c = c.replace(old_font_m, new_font_m)
print('5. Selection done')

# 6. hero-benefits CSS
c = c.replace(
    '.hero-lead{\n  font-size:18px;\n  color:var(--text-dim);\n  max-width:540px;\n  margin-bottom:36px;\n  line-height:1.55;\n}',
    '.hero-lead{\n  font-size:18px;\n  color:var(--text-dim);\n  max-width:540px;\n  margin-bottom:20px;\n  line-height:1.55;\n}\n\n.hero-benefits{\n  list-style:none;\n  margin-bottom:36px;\n  max-width:540px;\n}\n.hero-benefits li{\n  font-family:var(--font-m);\n  font-size:16px;\n  color:var(--text);\n  padding:8px 0;\n  display:flex;\n  align-items:center;\n  gap:12px;\n  border-bottom:1px solid rgba(245,197,24,.15);\n}\n.hero-benefits li::before{\n  content:"—";\n  color:var(--gold);\n  font-weight:700;\n  font-size:20px;\n}'
)
print('6. hero-benefits CSS done')

# 7. Add hero-benefits HTML
old_tag = 'class="hero-lead">'
idx = c.find(old_tag)
if idx > 0:
    end_p = c.find('</p>', idx)
    if end_p > 0:
        p_tag_close = c.find('>', idx)
        before_p_content = c[:p_tag_close+1]
        p_content = c[p_tag_close+1:end_p]
        after = c[end_p+4:]
        
        # Check if benefits already exist
        if 'hero-benefits' not in c[idx:idx+500]:
            new_html = before_p_content + 'Преміальні натяжні стелі в Чернівцях — глянцеві, матові, з трековою системою, світловими лініями та ромб-підсвіткою. Безкоштовний замір, монтаж за 1 день, гарантія до 12 років.</p>\n          <ul class="hero-benefits">\n            <li>Доступні ціни — від 700 грн за м² з роботою</li>\n            <li>Висока якість — сертифіковані матеріали</li>\n            <li>Гарантія до 12 років письмова</li>\n            <li>Безкоштовний замір по Чернівцях та області</li>\n          </ul>'
            c = before_p_content + after.replace(after, after, 1)  # placeholder
            c = c[:p_tag_close+1] + 'Преміальні натяжні стелі в Чернівцях — глянцеві, матові, з трековою системою, світловими лініями та ромб-підсвіткою. Безкоштовний замір, монтаж за 1 день, гарантія до 12 років.</p>\n          <ul class="hero-benefits">\n            <li>Доступні ціни — від 700 грн за м² з роботою</li>\n            <li>Висока якість — сертифіковані матеріали</li>\n            <li>Гарантія до 12 років письмова</li>\n            <li>Безкоштовний замір по Чернівцях та області</li>\n          </ul>' + c[end_p+4:]
            print('7. hero-benefits HTML done!')
        else:
            print('7. hero-benefits already exist')
else:
    print('7. hero-lead class NOT found')

# 8. Price highlights — add gold color to prices
c = c.replace('class="price">', 'class="price" style="color:var(--gold)">')
print('8. Price highlights done')

# 9. Top bar gold
c = c.replace(
    '.top-bar{\n  background:var(--accent);\n  color:#0a0b0d;',
    '.top-bar{\n  background:var(--gold);\n  color:#111;'
)
print('9. Top bar gold done')

# 10. Logo mark gold
c = c.replace(
    '.logo-mark{\n  width:42px;height:42px;\n  background:var(--accent);\n  color:#0a0b0d;',
    '.logo-mark{\n  width:42px;height:42px;\n  background:var(--gold);\n  color:#111;'
)
print('10. Logo mark gold done')

# 11. Nav CTA gold
c = c.replace(
    '.nav-cta{\n  display:inline-flex;align-items:center;gap:10px;\n  padding:13px 22px;\n  background:var(--accent);\n  color:#0a0b0d;',
    '.nav-cta{\n  display:inline-flex;align-items:center;gap:10px;\n  padding:13px 22px;\n  background:var(--gold);\n  color:#111;'
)
print('11. Nav CTA gold done')

# 12. Button accent gold
c = c.replace(
    '.btn-accent{\n  display:inline-flex;align-items:center;gap:12px;\n  padding:18px 28px;\n  background:var(--accent);\n  color:#0a0b0d;',
    '.btn-accent{\n  display:inline-flex;align-items:center;gap:12px;\n  padding:18px 28px;\n  background:var(--gold);\n  color:#111;'
)
print('12. Button accent gold done')

# 13. Gallery overlay tag gold
c = c.replace('color:var(--gold);\n  margin-bottom:8px;\n}\n.gallery-title{', 'color:var(--gold);\n  font-weight:700;\n  margin-bottom:8px;\n}\n.gallery-title{')
print('13. Gallery tags done')

# Write back
with open('C:/OpenClawData/workspace/potolki-chernivtsi/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('\nALL DONE!')
print('Final length:', len(c))
