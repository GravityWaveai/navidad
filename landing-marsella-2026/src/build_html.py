import base64, json, os, re, sys, html as H
HERE=os.path.dirname(os.path.abspath(__file__))
ORDER_URL="https://hj0yzvepfbz.typeform.com/to/Ursb0tCA"
OUT_DIR=sys.argv[1] if len(sys.argv)>1 else HERE

def b64(path):
    with open(path,'rb') as f: return base64.b64encode(f.read()).decode()
def data_uri(path):
    ext=path.rsplit('.',1)[1].lower()
    mime={'webp':'image/webp','jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png'}[ext]
    return f"data:{mime};base64,{b64(path)}"

A=lambda n: os.path.join(HERE,'assets',n)
IMG={
 'logo_navy':A('logo-gravitec-navy.png'),'logo_white':A('logo-gravitec-white.png'),'logo_gw':A('logo-gw-white.png'),
 'boat':A('boat.jpg'),'net':A('net-bg.jpg'),'scene':A('scene.jpg'),'swatch':A('swatch.jpg'),
 'cover_stars':A('cover-stars.webp'),
 'row_star':A('row-star.webp'),'row_tree':A('row-tree.webp'),'row_coaster':A('row-coaster.webp'),'row_phone':A('row-phone.webp'),
 'proc_net':A('proc-net.webp'),'proc_granza':A('proc-granza.webp'),
 'star_real':A('star-real.webp'),'phone_real':A('phone-real.webp'),'bola_real':A('bola-real.webp'),'tree_real':A('tree-real.webp'),'coaster_real':A('coaster-real.webp'),
 'star_pack_std':A('star-pack-std.webp'),'star_pack':A('star-pack.webp'),'star_logo':A('star-logo.webp'),
}
VIEWIMG={ # view images for product galleries
 'coaster-logo':A('coaster-logo.webp'),'coaster-pack':A('coaster-pack.webp'),'coaster-real':A('coaster-real.webp'),
 'phone-real':A('phone-real.webp'),'phone-tag':A('phone-tag.webp'),'phone-ico-2':A('phone-ico-2.webp'),
 'star-real':A('star-real.webp'),'star-logo':A('star-logo.webp'),'star-pack':A('star-pack.webp'),
 'tree-real':A('tree-real.webp'),'tree-logo':A('tree-logo.webp'),'tree-pack':A('tree-pack.webp'),
 'bola-real':A('bola-real.webp'),
}

PRODUCTS=[
 dict(id='posavasos', name='Posavasos (Pack 4)', short='Posavasos', xmas=False, unit='pack', unitPl='packs', moq=80, logo='40 × 40 mm',
      pitch='Cuatro posavasos de Gravitec® en acabado Marsella, presentados en packaging kraft. El clásico de mesa que se usa cada día, en casa y en la oficina, y que recuerda quién lo regaló.',
      spec=[('Contenido','Pack de 4 posavasos'),('Peso del pack','240 g'),('Dimensiones del pack','90 × 90 × 20 mm'),('Acabado','Marsella')],
      head_small='(4 uds/pack)',
      tiers=[(80,200,[18.2,19.5,21.5]),(201,500,[13.1,14.0,14.9]),(501,1000,[12.5,13.5,14.4])],
      views=[('Con tu logo','coaster-logo','Dos posavasos en acabado Marsella con el texto Tu logo aquí impreso en blanco'),
             ('Packaging','coaster-pack','Pack de cuatro posavasos con su faja de packaging kraft personalizada'),
             ('Muestra real','coaster-real','Fotografía real de un posavasos en acabado Marsella')]),
 dict(id='portamovil', name='Portamóviles', short='Portamóviles', xmas=False, unit='ud', unitPl='uds', moq=150, logo='30 × 30 mm',
      pitch='Un soporte de sobremesa para el móvil, macizo y estable, que se queda en la mesa de trabajo a la vista todo el año. Con etiqueta kraft y cordel, listo para entregar.',
      spec=[('Contenido','1 portamóvil'),('Peso','300 g'),('Dimensiones','130 × 80 × 18 mm'),('Acabado','Marsella')],
      head_small='',
      tiers=[(150,200,[12.6,13.0,13.6]),(201,500,[10.3,10.6,11.1]),(501,1000,[9.3,9.6,10.0])],
      views=[('Pieza','phone-real','Portamóvil en acabado Marsella, fotografía real'),
             ('Con tu logo','phone-tag','Portamóvil con etiqueta kraft personalizada y el texto Tu logo aquí impreso en blanco'),
             ('Etiqueta kraft','phone-ico-2','Portamóvil con la etiqueta kraft estándar de Gravity Wave')]),
 dict(id='estrellas', name='Estrellas de Navidad (Pack 2)', short='Estrellas', xmas=True, unit='pack', unitPl='packs', moq=80, logo='30 × 30 mm',
      pitch='Dos estrellas para colgar, con cordel, en packaging kraft. El adorno que vuelve al árbol cada diciembre, con tu logo en el centro.',
      spec=[('Contenido','Pack de 2 estrellas'),('Peso del pack','150 g'),('Dimensiones del pack','110 × 105 × 10 mm'),('Acabado','Marsella')],
      head_small='(2 uds/pack)',
      tiers=[(80,200,[15.6,17.0,18.5]),(201,500,[14.8,15.5,16.3]),(501,1000,[14.4,14.9,15.9])],
      views=[('Pieza','star-real','Estrella de Navidad en acabado Marsella, fotografía real'),
             ('Con tu logo','star-logo','Estrella con el texto Tu logo aquí impreso en blanco'),
             ('Packaging','star-pack','Pack de estrellas con packaging kraft personalizado')]),
 dict(id='arbol', name='Árboles de Navidad', short='Árboles', xmas=True, unit='ud', unitPl='uds', moq=80, logo='30 × 30 mm',
      pitch='Un árbol de sobremesa formado por dos piezas que se encajan sin herramientas. Se monta en segundos, se guarda plano y preside la mesa o la recepción cada Navidad.',
      spec=[('Contenido','1 árbol (2 piezas encajables)'),('Peso','500 g'),('Dimensiones','250 × 150 × 10 mm'),('Acabado','Marsella')],
      head_small='',
      tiers=[(80,200,[26.4,27.0,28.0]),(201,500,[22.6,22.9,23.3]),(501,1000,[20.7,21.0,21.4])],
      views=[('Pieza','tree-real','Árbol de Navidad en acabado Marsella montado, fotografía real'),
             ('Con tu logo','tree-logo','Árbol con el texto Tu logo aquí impreso en blanco'),
             ('Packaging','tree-pack','Árbol plano con su faja de packaging kraft personalizada')]),
 dict(id='bolas', name='Bola de Navidad (Pack 2)', short='Bolas', xmas=True, unit='pack', unitPl='packs', moq=80, logo='30 × 30 mm',
      pitch='Dos bolas planas para colgar, con tu logo en el centro. Ligeras, sencillas y muy visibles: el formato más directo para llevar tu marca al árbol.',
      spec=[('Contenido','Pack de 2 bolas'),('Peso del pack','120 g'),('Dimensiones del pack','110 × 90 × 10 mm'),('Acabado','Marsella')],
      head_small='(2 uds/pack)',
      tiers=[(80,200,[15.6,17.0,18.5]),(201,500,[14.8,15.5,16.3]),(501,1000,[14.4,14.9,15.9])],
      views=[('Con tu logo','bola-real','Dos bolas de Navidad en acabado Marsella con el texto Tu logo aquí impreso en blanco, fotografía real')]),
]

def price(v):
    s=f"{v:.1f}".replace('.',',')
    if s.endswith(',0'): s=s[:-2]
    return s

ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def product_html(p, i):
    alt=' alt' if i%2==1 else ''
    ribbon='<div class="ribbon" aria-hidden="true">Edición <b>Navidad</b></div>' if p['xmas'] else ''
    imgs=[]; thumbs=[]
    for j,(label,key,alttext) in enumerate(p['views']):
        src=data_uri(VIEWIMG[key])
        imgs.append(f'<img data-view="v{j}" src="{src}" alt="{H.escape(alttext)}"{"" if j==0 else " hidden"}>')
        thumbs.append(f'<button class="thumb" type="button" data-view="v{j}" aria-pressed="{"true" if j==0 else "false"}"><img src="{src}" alt=""><span>{label}</span></button>')
    thumbs_html=f'<div class="thumbs" role="group" aria-label="Vistas de {H.escape(p["name"])}">{"".join(thumbs)}</div>' if len(thumbs)>1 else ''
    spec=''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in p['spec'])
    rows=''
    for (lo,hi,pr) in p['tiers']:
        cells=''.join(f'<td><span data-cera="black">{price(x)} €</span><span class="u">/{p["unit"]}</span></td>' for x in pr)
        rows+=f'<tr><td>{lo}-{hi}</td>{cells}</tr>'
    small=f'<small>{p["head_small"]}</small>' if p['head_small'] else ''
    unit_word='pack' if p['unit']=='pack' else 'unidad'
    return f'''
    <article class="product{alt}" id="prod-{p['id']}">
      {ribbon}
      <div class="product-grid">
        <div class="gallery rv">
          <div class="stage">{''.join(imgs)}</div>
          {thumbs_html}
        </div>
        <div class="pinfo rv">
          <div class="h3"><h3 class="h3 cera" data-cera="black">{p['name']}</h3><span class="sub cera-r" data-cera="regular">Personalizables</span></div>
          <p class="pitch">{p['pitch']}</p>
          <dl class="spec">{spec}</dl>
          <div class="perso"><h4>Personalización</h4><p>Impresión del packaging kraft personalizado en <b>tinta negra</b> e impresión <b>UVI con tu logo en blanco</b> en cada pieza, hasta <b>{p['logo']}</b>.</p></div>
          <span class="deadline"><span class="dot" aria-hidden="true"></span>Fecha límite para pedidos de Navidad: 6 de noviembre</span>
        </div>
      </div>
      <div class="pricing rv">
        <div class="pricing-head"><h4>Precio por {unit_word} según cantidad y nivel de personalización</h4><span class="moq">Pedido mínimo: <b>{p['moq']} {p['unitPl']}</b></span></div>
        <div class="tablewrap"><table class="prices">
          <thead><tr><th scope="col">Nº {p['unitPl']}{small}</th><th scope="col">Estándar</th><th scope="col">Packaging<br>personalizado</th><th scope="col">Packaging + producto<br>personalizado</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
        <div class="pricing-foot">
          <span class="note">*Precios sin IVA ni gastos de envío.</span>
          <div class="hero-ctas"><a class="btn btn-teal" href="{ORDER_URL}" target="_blank" rel="noopener">Hacer pedido {ARROW}</a><a class="btn btn-ghost" href="#calculadora" data-calc="{p['id']}">Calcular mi pedido</a></div>
        </div>
      </div>
    </article>'''

tpl=open(os.path.join(HERE,'page.html'),encoding='utf-8').read()
products=''.join(product_html(p,i) for i,p in enumerate(PRODUCTS))
tpl=tpl.replace('__PRODUCTS__',products)
data=[dict(id=p['id'],short=p['short'],unit=p['unit'],unitPl=p['unitPl'],moq=p['moq'],tiers=[dict(min=lo,max=hi,prices=pr) for lo,hi,pr in p['tiers']]) for p in PRODUCTS]
tpl=tpl.replace('__DATA__',json.dumps(data,ensure_ascii=False))
tpl=tpl.replace('__ORDER_URL__',ORDER_URL)
FONTS=os.path.join(HERE,'fonts') if os.path.exists(os.path.join(HERE,'fonts','CeraPro-Black.woff2')) else os.path.join(HERE,'fonts','merged')
tpl=tpl.replace('__CERA_BLACK__',b64(os.path.join(FONTS,'CeraPro-Black.woff2')))
tpl=tpl.replace('__CERA_REGULAR__',b64(os.path.join(FONTS,'CeraPro-Regular.woff2')))
for k,path in IMG.items():
    tpl=tpl.replace(f'__IMG_{k}__',data_uri(path))
left=re.findall(r'__[A-Z_a-z0-9]+__',tpl)
assert not left, f'unreplaced placeholders: {set(left)}'

# ---- Cera glyph checker: every element marked data-cera must only use glyphs the embedded subset has
sets={w:set(open(os.path.join(FONTS,f'CeraPro-{w.capitalize()}.chars.txt'),encoding='utf-8').read()) for w in ('black','regular')}
problems=[]
for m in re.finditer(r'<([a-z0-9]+)[^>]*data-cera="(black|regular)"[^>]*>(.*?)</\1>',tpl,flags=re.S):
    w=m.group(2); text=re.sub(r'<[^>]+>','',m.group(3)); text=H.unescape(text)
    bad=sorted({c for c in text if not c.isspace() and c not in sets[w]})
    if bad: problems.append((w,text.strip()[:60],bad))
if problems:
    for w,t,b in problems: print('CERA MISSING',w,repr(t),b)
    sys.exit('fix the copy above (glyphs missing in the embedded Cera subset)')
print('Cera glyph check OK')

# ---- outputs
head,body=tpl.split('\n<header class="nav"',1); body='<header class="nav"'+body
os.makedirs(OUT_DIR,exist_ok=True)
open(os.path.join(OUT_DIR,'artifact.html'),'w',encoding='utf-8').write(tpl)
standalone=('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#D9D0C6">\n'
            +head+'\n</head>\n<body>\n'+body+'\n</body>\n</html>\n')
open(os.path.join(OUT_DIR,'index.html'),'w',encoding='utf-8').write(standalone)
print('artifact.html',os.path.getsize(os.path.join(OUT_DIR,'artifact.html'))//1024,'KB · index.html',os.path.getsize(os.path.join(OUT_DIR,'index.html'))//1024,'KB')
