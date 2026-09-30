import numpy as np, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as ndi
A='assets'
FONT=ImageFont.truetype('fonts/merged/CeraPro-Black.ttf', 40)
def load(n): return Image.open(f'{A}/{n}.webp').convert('RGBA')
def save(im,n,q=88): p=f'{A}/{n}.webp'; im.save(p,'WEBP',quality=q,method=6); print(n,im.size,os.path.getsize(p)//1024,'KB')
def shadow_of(im, blur=14, off=(10,16), strength=0.55):
    """soft cast shadow layer from the alpha silhouette"""
    a=np.asarray(im)[...,3].astype(np.float32)/255
    sh=ndi.gaussian_filter(a,blur); sh=ndi.shift(sh,(off[1],off[0]),order=1)
    sh=np.clip(sh*1.15,0,1)*strength
    out=np.zeros((*a.shape,4),np.uint8); out[...,0:3]=[20,40,70]; out[...,3]=(sh*255).astype(np.uint8)
    return Image.fromarray(out,'RGBA')
def add_logo(im, center, size, rot=0, lines=('TU','LOGO','AQUÍ')):
    """white 'TU LOGO AQUÍ' with soft relief, like a UVI print"""
    W,H=im.size; layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    f=ImageFont.truetype('fonts/merged/CeraPro-Black.ttf', size)
    lh=int(size*0.98); y0=center[1]-lh*len(lines)/2
    for i,t in enumerate(lines):
        w=d.textlength(t,font=f); d.text((center[0]-w/2, y0+i*lh), t, font=f, fill=(255,255,255,255))
    if rot: layer=layer.rotate(rot,resample=Image.BICUBIC,center=center)
    a=np.asarray(layer)[...,3].astype(np.float32)/255
    # relief: soft dark shadow offset below-right, only outside the letters
    sh=ndi.shift(ndi.gaussian_filter(a,1.6),(2,1.5),order=1); sh=np.clip(sh*1.3,0,1)*(1-a)
    shl=np.zeros((H,W,4),np.uint8); shl[...,0:3]=[30,55,60]; shl[...,3]=(sh*0.55*255).astype(np.uint8)
    base=np.asarray(im).copy()
    # print only where the piece exists
    mask=(base[...,3]>200)
    shl[...,3]=(shl[...,3]*mask).astype(np.uint8)
    L=np.asarray(layer).copy(); L[...,3]=(L[...,3]*mask).astype(np.uint8)
    out=Image.fromarray(base,'RGBA'); out.alpha_composite(Image.fromarray(shl,'RGBA')); out.alpha_composite(Image.fromarray(L,'RGBA'))
    return out
def stack(pieces, size, margin=40):
    """compose pieces (img, x, y, rotation, scale) back-to-front with cast shadows between them"""
    canvas=Image.new('RGBA',size,(0,0,0,0))
    for i,(im,x,y,rot,sc) in enumerate(pieces):
        p=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
        if rot: p=p.rotate(rot,resample=Image.BICUBIC,expand=True)
        lay=Image.new('RGBA',size,(0,0,0,0)); lay.alpha_composite(p,(x,y))
        if i>0:
            sh=shadow_of(lay,blur=9,off=(6,10),strength=0.6)
            # shadow only over the pieces already placed
            under=np.asarray(canvas)[...,3]>0
            s=np.asarray(sh).copy(); s[...,3]=(s[...,3]*under).astype(np.uint8)
            canvas.alpha_composite(Image.fromarray(s,'RGBA'))
        canvas.alpha_composite(lay)
    return canvas.crop(canvas.getbbox())
star=load('star-real'); phone=load('phone-real'); tree=load('tree-real'); bola=load('bola-real'); coaster=load('coaster-real')
# logo on the real pieces
star_logo=add_logo(star,(star.width*0.50,star.height*0.58),int(star.width*0.11),rot=-6)
save(star_logo,'star-logo')
phone_logo=add_logo(phone,(phone.width*0.40,phone.height*0.48),int(phone.width*0.06),rot=-4,lines=('TU LOGO','AQUÍ'))
save(phone_logo,'phone-logo')
tree_logo=add_logo(tree,(tree.width*0.50,tree.height*0.80),int(tree.width*0.11),lines=('TU','LOGO','AQUÍ'))
save(tree_logo,'tree-logo')
# hero: two real stars, one in front, with a real cast shadow between them
hero=stack([(star,60,0,-14,0.96),(star_logo,150,120,4,1.0)],(900,720))
save(hero,'cover-stars')
# coasters pair for the product view: two real coasters offset, front one with logo
c2=coaster.resize((coaster.width*2,coaster.height*2),Image.LANCZOS)
pair=stack([(c2,0,40,0,1.0),(c2,150,0,0,1.0)],(700,560))
save(pair,'coaster-logo')
# composed 'full' views
def side(name,left,right,h=520,gap=-20):
    L=load(left); R=load(right)
    L=L.resize((int(L.width*h/L.height),h),Image.LANCZOS); R=R.resize((int(R.width*h*0.9/R.height),int(h*0.9)),Image.LANCZOS)
    c=Image.new('RGBA',(L.width+R.width+gap+30,h+30),(0,0,0,0)); c.alpha_composite(L,(0,15)); c.alpha_composite(R,(L.width+gap+30,15+h-R.height)); save(c,name)
side('star-full','star-pack','star-logo')
side('phone-full','phone-ico-1','phone-logo',gap=0)
side('tree-full','tree-pack-std','tree-logo',gap=-10)
# row / chooser images = real photos
for src,dst in [('star-real','row-star'),('tree-real','row-tree'),('coaster-real','row-coaster'),('phone-real','row-phone')]:
    save(load(src),dst)
