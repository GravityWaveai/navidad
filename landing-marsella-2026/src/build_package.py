# -*- coding: utf-8 -*-
"""Build the hand-over package for the web team / another AI:
   navidad-2026-web/
     navidad-2026.html            standalone page (no nav, no footer) using css/, js/, img/, fonts/
     fragmento-navidad-2026.html  only the <section> markup, to paste inside the site's own layout
     css/navidad-2026.css         scoped under #gw-navidad-2026
     js/navidad-2026.js           vanilla JS, no dependencies
     fonts/                       Cera Pro subsets (woff2)
     img/                         all images, descriptive names, grouped by use
     data/productos.json          product data ES/EN
     README.md, CONTENIDO-ES-EN.md (copied from the scratchpad)
"""
import os, re, sys, json, shutil, hashlib
HERE=os.path.dirname(os.path.abspath(__file__))
PKG=os.path.join(HERE,'pkg','navidad-2026-web')
WRAP_ID='gw-navidad-2026'

# ------------------------------------------------------------------ asset naming
NAMES=[ # (assets filename, package path). Earlier entries win for byte-identical files.
 ('logo-gravitec-navy.png','marca/logo-gravitec-by-gravity-wave-azul.png'),
 ('logo-gravitec-white.png','marca/logo-gravitec-by-gravity-wave-blanco.png'),
 ('boat.jpg','fondos/barco-gravity-wave-plastic-free-oceans.jpg'),
 ('net-bg.jpg','fondos/red-de-pesca-textura.jpg'),
 ('swatch.jpg','acabado/acabado-marsella-muestra.jpg'),
 ('proc-net.webp','proceso/redes-de-pesca-recuperadas.webp'),
 ('proc-granza.webp','proceso/granza-gravitec-reciclada.webp'),
 ('tree-logo.webp','productos/arbol/arbol-navidad-marsella-montado-tu-logo.webp'),
 ('tree-pack-std.webp','productos/arbol/arbol-navidad-pack-estandar.webp'),
 ('tree-pack-logo.webp','productos/arbol/arbol-navidad-pack-personalizado.webp'),
 ('tree-full.webp','productos/arbol/arbol-navidad-pack-mas-producto-personalizado.webp'),
 ('star-logo.webp','productos/estrellas/estrellas-navidad-marsella-tu-logo.webp'),
 ('star-pack-std.webp','productos/estrellas/estrellas-navidad-pack-estandar.webp'),
 ('star-pack.webp','productos/estrellas/estrellas-navidad-pack-personalizado.webp'),
 ('star-full.webp','productos/estrellas/estrellas-navidad-pack-mas-producto-personalizado.webp'),
 ('bola-real.webp','productos/bolas/bolas-navidad-marsella-tu-logo.webp'),
 ('bola-pack-std.webp','productos/bolas/bolas-navidad-pack-estandar.webp'),
 ('bola-pack.webp','productos/bolas/bolas-navidad-pack-personalizado.webp'),
 ('bola-full.webp','productos/bolas/bolas-navidad-pack-mas-producto-personalizado.webp'),
 ('phone-plain.webp','productos/portamovil/portamovil-marsella-3d.webp'),
 ('phone-ico-std.webp','productos/portamovil/portamovil-pack-estandar.webp'),
 ('phone-ico-1.webp','productos/portamovil/portamovil-pack-personalizado.webp'),
 ('phone-full.webp','productos/portamovil/portamovil-pack-mas-producto-personalizado.webp'),
 ('coaster-logo.webp','productos/posavasos/posavasos-marsella-tu-logo.webp'),
 ('coaster-ico-std.webp','productos/posavasos/posavasos-pack-estandar.webp'),
 ('coaster-ico-pack.webp','productos/posavasos/posavasos-pack-personalizado.webp'),
 ('coaster-pack.webp','productos/posavasos/posavasos-pack-mas-producto-personalizado.webp'),
]
def sha(p):
    h=hashlib.sha1()
    with open(p,'rb') as f: h.update(f.read())
    return h.hexdigest()
BYHASH={}; BYNAME={}
for fn,pp in NAMES:
    src=os.path.join(HERE,'assets',fn)
    if os.path.exists(src):
        BYHASH.setdefault(sha(src),pp); BYNAME[fn]=pp
USED={}  # package path -> source path
def asset_url(path):
    """replacement for data_uri(): registers the file and returns its URL relative to the HTML"""
    h=sha(path); fn=os.path.basename(path)
    pp=BYHASH.get(h) or BYNAME.get(fn) or ('otros/'+fn)
    USED.setdefault(pp,path)
    return 'img/'+pp

# ------------------------------------------------------------------ run the page builder with external assets
src=open(os.path.join(HERE,'build_html.py'),encoding='utf-8').read()
src=src.replace('def data_uri(path):','def data_uri_inline(path):')
src=src.replace("tpl=tpl.replace('__CERA_BLACK__',b64(os.path.join(HERE,'fonts/merged/CeraPro-Black.woff2')))","tpl=tpl.replace('data:font/woff2;base64,__CERA_BLACK__','../fonts/CeraPro-Black.woff2')")
src=src.replace("tpl=tpl.replace('__CERA_REGULAR__',b64(os.path.join(HERE,'fonts/merged/CeraPro-Regular.woff2')))","tpl=tpl.replace('data:font/woff2;base64,__CERA_REGULAR__','../fonts/CeraPro-Regular.woff2')")
src=src[:src.index('head,body=tpl.split(')]
ns={'__file__':os.path.join(HERE,'build_html.py'),'__name__':'build_html_pkg','data_uri':asset_url}
sys.argv=[sys.argv[0]]
exec(compile(src,os.path.join(HERE,'build_html.py'),'exec'),ns)
tpl=ns['tpl']; PRODUCTS=ns['PRODUCTS']; VIEWIMG=ns['VIEWIMG']; A=ns['A']

# ------------------------------------------------------------------ strip nav + footer, split css / js
tpl=re.sub(r'\n<header class="nav".*?</header>\n','\n',tpl,flags=re.S)
m=re.search(r'<style>(.*?)</style>',tpl,flags=re.S); css=m.group(1); tpl=tpl[:m.start()]+tpl[m.end():]
m=re.search(r'<script>(.*?)</script>',tpl,flags=re.S); js=m.group(1); tpl=tpl[:m.start()]+tpl[m.end():]
# head bits (title, description, font links) are not part of the fragment
tpl=re.sub(r'^<title>.*?</title>\s*','',tpl,flags=re.S)
tpl=re.sub(r'<meta name="description"[^>]*>\s*','',tpl)
tpl=re.sub(r'<link [^>]*>\s*','',tpl)
tpl=tpl.replace('<main id="top">','<div class="gw-page">').replace('</main>','</div>')
# nav css + footer css blocks
css=re.sub(r'/\* ---------- nav ---------- \*/.*?(?=/\* ---------- hero)','',css,flags=re.S)
css=re.sub(r'/\* ---------- footer ---------- \*/.*?(?=/\* ---------- motion)','',css,flags=re.S)
css=css.replace('url(img/','url(../img/')
# nav js block
js=re.sub(r'\s*/\* ---- nav ---- \*/.*?(?=\s*/\* ---- product configurators)','\n',js,flags=re.S)
js=js.replace("  document.documentElement.classList.add('js');\n",'')

# ------------------------------------------------------------------ ids: avoid collisions with the host site
IDMAP={'porque':'navidad-por-que','proceso':'navidad-proceso','marsella':'navidad-acabado-marsella','productos':'navidad-productos',
 'personalizacion':'navidad-personalizacion','calculadora':'navidad-calcula-tu-pedido','pedido':'navidad-cierre-pedidos',
 'respuesta':'navidad-respuesta-correo','elige':'navidad-elige-producto',
 'cart':'gw-cart','replyText':'gw-reply-text','toast':'gw-toast','outCount':'gw-out-count','outUnits':'gw-out-units','outTotal':'gw-out-total',
 'outCap':'gw-out-cap','copyReply':'gw-copy-reply','emailTxt':'gw-email','copyBtn':'gw-copy-email'}
def rename_ids(t):
    for a,b in IDMAP.items():
        t=re.sub(r'id="%s"'%re.escape(a),'id="%s"'%b,t)
        t=re.sub(r'href="#%s"'%re.escape(a),'href="#%s"'%b,t)
        t=re.sub(r"getElementById\('%s'\)"%re.escape(a),"getElementById('%s')"%b,t)
    for a,b in {'id="prod-':'id="gw-prod-','href="#prod-':'href="#gw-prod-',"'#prod-'":"'#gw-prod-'","'prod-'+":"'gw-prod-'+",
                "'cart-'+":"'gw-cart-'+","\"cq-'":"\"gw-cq-'",'"tbl-':'"gw-tbl-','"qty-':'"gw-qty-'}.items():
        t=t.replace(a,b)
    return t
tpl=rename_ids(tpl); js=rename_ids(js)
assert "getElementById('cart')" not in js and 'id="cart"' not in tpl

# ------------------------------------------------------------------ scope the css under the wrapper id
def split_sel(h):
    out=[]; depth=0; cur=''
    for ch in h:
        if ch=='(': depth+=1
        if ch==')': depth-=1
        if ch==',' and depth==0: out.append(cur); cur=''
        else: cur+=ch
    out.append(cur); return [s.strip() for s in out if s.strip()]
def scope_css(c,prefix):
    out=[]; i=0; n=len(c)
    while i<n:
        if c.startswith('/*',i):
            j=c.find('*/',i)+2; out.append(c[i:j]); i=j; continue
        if c[i].isspace(): i+=1; continue
        j=c.find('{',i)
        if j<0: break
        header=c[i:j].strip(); depth=1; k=j+1
        while k<n and depth>0:
            if c[k]=='{': depth+=1
            elif c[k]=='}': depth-=1
            k+=1
        body=c[j+1:k-1]; i=k
        if header.startswith('@media') or header.startswith('@supports'):
            out.append(header+'{'+scope_css(body,prefix)+'}')
        elif header.startswith('@'):
            out.append(header+'{'+body+'}')
        else:
            new=[]
            for s in split_sel(header):
                if s=='html': continue
                if s in (':root','body'): new.append(prefix)
                else: new.append(prefix+' '+s)
            if new: out.append(','.join(new)+'{'+body+'}')
    return '\n'.join(out)
css_scoped=scope_css(css,'#'+WRAP_ID)
css_scoped=('/* Gravitec by Gravity Wave · Regalos corporativos Navidad 2026 · acabado Marsella\n'
            '   Todo el CSS está acotado bajo #%s para no interferir con la web anfitriona.\n'
            '   Fuentes: Poppins + Sacramento (Google Fonts, enlace en el <head>) y Cera Pro (fonts/, subconjunto). */\n'%WRAP_ID)+css_scoped
js_out=('/* Gravitec by Gravity Wave · Navidad 2026 · selector de nivel, tablas plegables, pedido y texto para el correo.\n'
        '   Sin dependencias. Cargar con defer o al final del body, después del HTML de la sección. */\n'+js.strip()+'\n')

# lazy-load every image except the hero piece and the brand logos
tpl=re.sub(r'<img (?![^>]*loading=)',lambda m:'<img loading="lazy" decoding="async" ',tpl)
tpl=re.sub(r'(<div class="hero-visual">\s*)<img loading="lazy" decoding="async" ',r'\1<img fetchpriority="high" ',tpl)
tpl=re.sub(r'<img loading="lazy" decoding="async" (src="img/marca/)',r'<img \1',tpl)
fragment='<section id="%s" class="gw-navidad" lang="es">\n%s\n</section>\n'%(WRAP_ID,tpl.strip())
# only copy the images the page really references (IMG dict replacement registers unused ones too)
refs=set(re.findall(r'img/([A-Za-z0-9_./-]+)',fragment))|set(re.findall(r'\.\./img/([A-Za-z0-9_./-]+)',css))
USED={k:v for k,v in USED.items() if k in refs}
HEAD_LINKS=('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Sacramento&display=swap">\n')
standalone=('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
 '<title>Regalos corporativos de Navidad 2026 con redes de pesca recicladas | Gravitec by Gravity Wave</title>\n'
 '<meta name="description" content="Árbol, estrellas, bolas, portamóvil y posavasos fabricados con redes de pesca recuperadas del Mediterráneo, en el nuevo acabado Marsella y con el logo de tu empresa. Precios por volumen y tres niveles de personalización.">\n'
 '<meta name="theme-color" content="#D9D0C6">\n'+HEAD_LINKS+
 '<link rel="stylesheet" href="css/navidad-2026.css">\n<style>body{margin:0;background:#D9D0C6}</style>\n</head>\n<body>\n'+fragment+
 '<script src="js/navidad-2026.js" defer></script>\n</body>\n</html>\n')

# ------------------------------------------------------------------ write package
if os.path.exists(PKG): shutil.rmtree(PKG)
for d in ('css','js','fonts','img','data'): os.makedirs(os.path.join(PKG,d),exist_ok=True)
open(os.path.join(PKG,'navidad-2026.html'),'w',encoding='utf-8').write(standalone)
open(os.path.join(PKG,'fragmento-navidad-2026.html'),'w',encoding='utf-8').write(
 '<!-- Fragmento para insertar dentro de la plantilla de la web (menú y footer los pone la web). Requiere css/navidad-2026.css, js/navidad-2026.js y el enlace a Google Fonts (ver README). -->\n'+fragment)
open(os.path.join(PKG,'css','navidad-2026.css'),'w',encoding='utf-8').write(css_scoped)
open(os.path.join(PKG,'js','navidad-2026.js'),'w',encoding='utf-8').write(js_out)
for f in ('CeraPro-Black.woff2','CeraPro-Regular.woff2','CeraPro-Black.chars.txt','CeraPro-Regular.chars.txt'):
    shutil.copy(os.path.join(HERE,'fonts','merged',f) if os.path.exists(os.path.join(HERE,'fonts','merged',f)) else os.path.join(HERE,'fonts',f),os.path.join(PKG,'fonts',f))
for pp,srcp in USED.items():
    dst=os.path.join(PKG,'img',pp); os.makedirs(os.path.dirname(dst),exist_ok=True); shutil.copy(srcp,dst)
for f in ('README.md','CONTENIDO-ES-EN.md'):
    p=os.path.join(HERE,'pkg_docs',f)
    if os.path.exists(p): shutil.copy(p,os.path.join(PKG,f))

# ------------------------------------------------------------------ data/productos.json (ES + EN)
EN={
 'arbol':dict(name='Christmas Tree',short='Trees',pitch='A tabletop tree made of two panels that slot together, no tools needed. It assembles in seconds, stores flat and takes pride of place on the desk or at reception every Christmas.',
   spec=[('Contents','1 tree (2 interlocking panels)'),('Weight','500 g'),('Dimensions','250 × 150 × 10 mm'),('Finish','Marsella')],
   alts={'std':'Flat tree panel with the standard Gravity Wave kraft band','pack':'Flat tree panel with the kraft band customised with your logo','full':'Customised kraft band and assembled tree with your logo printed in white','real':'Assembled Christmas tree in Marsella finish'}),
 'estrellas':dict(name='Christmas Stars (Pack of 2)',short='Stars',pitch='Two hanging stars with cord, in kraft packaging. The ornament that goes back on the tree every December, with your logo at its centre.',
   spec=[('Contents','Pack of 2 stars'),('Pack weight','150 g'),('Pack dimensions','110 × 105 × 10 mm'),('Finish','Marsella')],
   alts={'std':'Pack of stars in the standard Gravity Wave kraft sleeve','pack':'Pack of stars in the kraft sleeve customised with your logo','full':'Customised sleeve and star with your logo printed in white','real':'Christmas star in Marsella finish'}),
 'bolas':dict(name='Christmas Bauble (Pack of 2)',short='Baubles',pitch='Two flat hanging baubles with your logo in the centre. Light, simple and highly visible: the most direct way to put your brand on the tree.',
   spec=[('Contents','Pack of 2 baubles'),('Pack weight','120 g'),('Pack dimensions','110 × 90 × 10 mm'),('Finish','Marsella')],
   alts={'std':'Pack of two baubles with the standard Gravity Wave kraft cross band','pack':'Pack of two baubles with the kraft cross band customised with your logo','full':'Customised band and bauble with your logo printed in white','real':'Two Christmas baubles in Marsella finish with the text Your logo here'}),
 'portamovil':dict(name='Phone Stands',short='Phone stands',pitch='A solid, stable desktop stand for your phone that stays on the desk in plain sight all year round. With kraft tag and cord, ready to hand over.',
   spec=[('Contents','1 phone stand'),('Weight','300 g'),('Dimensions','130 × 80 × 18 mm'),('Finish','Marsella')],
   alts={'std':'Phone stand with the standard Gravity Wave kraft tag','pack':'Phone stand with the kraft tag customised with your logo','full':'Customised kraft tag and phone stand with your logo printed on the piece','real':'Phone stand in Marsella finish, 3D render'}),
 'posavasos':dict(name='Coasters (Pack of 4)',short='Coasters',pitch='Four Gravitec® coasters in Marsella finish, presented in kraft packaging. The desk classic that gets used every day, at home and at the office, and reminds people who gave it.',
   spec=[('Contents','Pack of 4 coasters'),('Pack weight','240 g'),('Pack dimensions','90 × 90 × 20 mm'),('Finish','Marsella')],
   alts={'std':'Pack of coasters with the standard Gravity Wave kraft band','pack':'Pack of coasters with the kraft band customised with your logo','full':'Customised kraft band and your logo printed on each coaster','real':'Coasters in Marsella finish with the text Your logo here'}),
}
LEVELS=[('std','Estándar','Standard'),('pack','Packaging personalizado','Customised packaging'),('full','Packaging + producto personalizado','Customised packaging + product')]
data={
 'campaign':{'name_es':'Regalos corporativos Navidad 2026 · Acabado Marsella','name_en':'Corporate Christmas gifts 2026 · Marsella finish',
   'brand':'Gravitec® by Gravity Wave','material_es':'Gravitec®, fabricado con redes de pesca recuperadas del Mediterráneo','material_en':'Gravitec®, made from fishing nets recovered from the Mediterranean',
   'finish':'Marsella','order_deadline':'2026-11-06','order_deadline_es':'6 de noviembre de 2026','order_deadline_en':'6 November 2026',
   'prices_note_es':'Precios sin IVA ni gastos de envío','prices_note_en':'Prices exclude VAT and shipping','currency':'EUR','max_units_online':1000,
   'contact_email':'info@thegravitywave.com','contact_place':'Gravity Wave · Calpe, Alicante','website':'https://thegravitywave.com',
   'customisation_es':'Impresión del packaging kraft personalizado en tinta negra e impresión UVI con tu logo en blanco en cada pieza.',
   'customisation_en':'Customised kraft packaging printed in black ink and UV print of your logo in white on each piece.'},
 'levels':[{'key':k,'name_es':es,'name_en':en} for k,es,en in LEVELS],
 'products':[]}
for p in PRODUCTS:
    e=EN[p['id']]
    views={}
    for k,(key,alt_es) in p['views'].items():
        views[k]={'image':asset_url(VIEWIMG[key]),'alt_es':alt_es,'alt_en':e['alts'].get(k,'')}
    main_img=asset_url(VIEWIMG[p['chooser']] if p['chooser'] in VIEWIMG else A(p['chooser']+'.webp'))
    data['products'].append({
      'id':p['id'],'order':len(data['products'])+1,'christmas_edition':p['xmas'],
      'name_es':p['name'],'name_en':e['name'],'short_es':p['short'],'short_en':e['short'],
      'unit_es':p['unit'],'unit_en':'pack' if p['unit']=='pack' else 'unit','units_label_es':p['unitPl'],'units_label_en':'packs' if p['unit']=='pack' else 'units',
      'moq':p['moq'],'logo_max_size_mm':p['logo'],
      'pitch_es':p['pitch'],'pitch_en':e['pitch'],
      'spec_es':[{'label':a,'value':b} for a,b in p['spec']],'spec_en':[{'label':a,'value':b} for a,b in e['spec']],
      'price_tiers':[{'min':lo,'max':hi,'prices':{'std':pr[0],'pack':pr[1],'full':pr[2]}} for lo,hi,pr in p['tiers']],
      'main_image':main_img,'views':views})
json.dump(data,open(os.path.join(PKG,'data','productos.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)

# ------------------------------------------------------------------ img manifest
man=['# Imágenes del paquete (ruta · uso en la página)','']
USE={'marca/logo-gravitec-by-gravity-wave-azul.png':'Logo Gravitec by Gravity Wave en azul marino (cita del barco). Sobre fondos claros.',
 'marca/logo-gravitec-by-gravity-wave-blanco.png':'Logo Gravitec en blanco (cabecera/hero). Sobre fondos oscuros o con contraste.',
 'fondos/barco-gravity-wave-plastic-free-oceans.jpg':'Foto de fondo de la cita (barco de Gravity Wave, Plastic Free Oceans). Va con velo arena por encima.',
 'fondos/red-de-pesca-textura.jpg':'Foto de fondo de la sección El proceso (red de pesca), opacidad baja.',
 'acabado/acabado-marsella-muestra.jpg':'Muestra del acabado Marsella (primer plano del material).',
 'proceso/redes-de-pesca-recuperadas.webp':'Paso 1 del proceso: redes recuperadas.','proceso/granza-gravitec-reciclada.webp':'Paso 2 del proceso: granza Gravitec.',
}
for pp in sorted(USED):
    note=USE.get(pp)
    if not note:
        if 'tu-logo' in pp or '-3d' in pp: note='Pieza suelta: hero (estrellas), selector de producto, fila de piezas, paso 3 del proceso (árbol) y vista «pieza» de la ficha.'
        elif 'estandar' in pp: note='Nivel 1 · Estándar: imagen grande de la ficha y miniatura del selector de nivel. También tarjeta 1 de Personalización (estrellas).'
        elif 'pack-personalizado' in pp: note='Nivel 2 · Packaging personalizado: imagen grande y miniatura. También tarjeta 2 de Personalización (estrellas).'
        elif 'mas-producto' in pp: note='Nivel 3 · Packaging + producto personalizado: imagen grande y miniatura. También tarjeta 3 de Personalización (estrellas).'
        else: note=''
    man.append('- `img/%s` · %s'%(pp,note))
open(os.path.join(PKG,'img','INDICE-IMAGENES.md'),'w',encoding='utf-8').write('\n'.join(man)+'\n')
sizes=sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(PKG) for f in fs)
print('package written:',PKG,'files:',sum(len(fs) for _,_,fs in os.walk(PKG)),'size: %.1f MB'%(sizes/1e6))
print('images:',len(USED))
