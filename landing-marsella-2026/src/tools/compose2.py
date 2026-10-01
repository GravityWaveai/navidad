from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os
from scipy import ndimage as ndi
A='assets'
def load(n): return Image.open(f'{A}/{n}.webp' if os.path.exists(f'{A}/{n}.webp') else f'{A}/{n}.png').convert('RGBA')
def save(im,n,q=84):
    p=f'{A}/{n}.webp'; im.save(p,'WEBP',quality=q,method=6); print(n,im.size,os.path.getsize(p)//1024,'KB')
def crop(im,pad=10):
    bb=im.getbbox(); return im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
def shadow(layer, blur=10, off=(8,12), strength=0.55, only_over=None):
    a=np.asarray(layer)[...,3].astype(np.float32)/255
    sh=ndi.shift(ndi.gaussian_filter(a,blur),(off[1],off[0]),order=1); sh=np.clip(sh*1.2,0,1)*strength
    if only_over is not None: sh=sh*(np.asarray(only_over)[...,3]>0)
    out=np.zeros((*a.shape,4),np.uint8); out[...,0:3]=[25,45,70]; out[...,3]=(sh*255).astype(np.uint8)
    return Image.fromarray(out,'RGBA')
def band_on(base, cross, center, size):
    """put a kraft cross band over a piece, centred, with a cast shadow onto the piece"""
    c=cross.resize((size,int(cross.height*size/cross.width)),Image.LANCZOS)
    lay=Image.new('RGBA',base.size,(0,0,0,0)); lay.alpha_composite(c,(center[0]-c.width//2,center[1]-c.height//2))
    out=base.copy(); out.alpha_composite(shadow(lay,blur=8,off=(5,9),strength=0.5,only_over=base)); out.alpha_composite(lay); return out
def logo_text(lines, size, fill=(255,255,255,255), spacing=0.98):
    f=ImageFont.truetype('fonts/merged/CeraPro-Black.ttf',size); d0=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    w=int(max(d0.textlength(t,font=f) for t in lines))+8; lh=int(size*spacing); im=Image.new('RGBA',(w,lh*len(lines)+10),(0,0,0,0)); d=ImageDraw.Draw(im)
    for i,t in enumerate(lines): tw=d.textlength(t,font=f); d.text(((w-tw)/2,i*lh),t,font=f,fill=fill)
    return im
def print_on(base, txt, pos, mask_alpha=True):
    """white UV print with soft relief; only where the piece exists"""
    lay=Image.new('RGBA',base.size,(0,0,0,0)); lay.alpha_composite(txt,pos)
    a=np.asarray(lay)[...,3].astype(np.float32)/255
    sh=ndi.shift(ndi.gaussian_filter(a,1.5),(2,1.5),order=1); sh=np.clip(sh*1.3,0,1)*(1-a)
    piece=np.asarray(base)[...,3]>200
    shl=np.zeros((*a.shape,4),np.uint8); shl[...,0:3]=[30,55,60]; shl[...,3]=(sh*0.5*255*piece).astype(np.uint8)
    L=np.asarray(lay).copy(); L[...,3]=(L[...,3]*piece).astype(np.uint8)
    out=base.copy(); out.alpha_composite(Image.fromarray(shl,'RGBA')); out.alpha_composite(Image.fromarray(L,'RGBA')); return out
def side(name,L,R,h=520,gap=-10):
    L=L.resize((int(L.width*h/L.height),h),Image.LANCZOS); R=R.resize((int(R.width*h*0.92/R.height),int(h*0.92)),Image.LANCZOS)
    c=Image.new('RGBA',(L.width+R.width+gap+30,h+30),(0,0,0,0)); c.alpha_composite(L,(0,15)); c.alpha_composite(R,(L.width+gap+30,15+h-R.height)); save(c,name)

cross_logo=load('cross-logo'); cross_std=load('cross-std')

# ---------- BOLAS: pack = two baubles with the kraft cross over the front one
bola=load('bola-real')
bola_std=band_on(bola,cross_std,(515,620),700); save(bola_std,'bola-pack-std')
bola_pack=band_on(bola,cross_logo,(515,620),700); save(bola_pack,'bola-pack')
side('bola-full',bola_pack,bola,h=560,gap=-40)

# ---------- POSAVASOS: from the catalogue coaster photo (upscaled)
co=load('coaster-real'); co=co.resize((co.width*3,co.height*3),Image.LANCZOS)
# soften upscale artefacts a touch
co=co.filter(ImageFilter.SMOOTH)
W,H=co.width+60,co.height+120
def stack4(cross):
    c=Image.new('RGBA',(W,H),(0,0,0,0))
    for i in range(4):
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); lay.alpha_composite(co,(30,90-i*28))
        if i>0: c.alpha_composite(shadow(lay,blur=6,off=(0,10),strength=0.45,only_over=c))
        c.alpha_composite(lay)
    cx,cy=30+co.width//2, 90-3*28+co.height//2
    return crop(band_on(c,cross,(cx,cy),int(co.width*1.05)))
save(stack4(cross_std),'coaster-ico-std'); cp=stack4(cross_logo); save(cp,'coaster-ico-pack')
save(crop(co),'coaster-logo')
side('coaster-pack',cp,crop(co),h=520,gap=-20)

# ---------- ÁRBOL: logo printed in the plane of the right panel
tree=load('tree-logo'); a=np.asarray(tree).astype(np.float32)
L=a[...,:3].mean(-1); box=(265,845,440,1015); x0,y0,x1,y1=box
m=np.zeros(L.shape,bool); m[y0:y1,x0:x1]=(L[y0:y1,x0:x1]>236)&(a[y0:y1,x0:x1,3]>200); m=ndi.binary_dilation(m,iterations=2)
out=a.copy(); valid=(~m).astype(np.float32)
for s in (3,6,12):
    for c in range(3):
        f=ndi.gaussian_filter(out[...,c]*valid,s)/np.maximum(ndi.gaussian_filter(valid,s),1e-3); sel=m&(ndi.gaussian_filter(valid,s)>0.02); out[sel,c]=f[sel]
    valid=np.maximum(valid,(sel).astype(np.float32)); m=m&~sel
# add real grain from the same panel (above the text)
src=a[690:840,300:450,:3]; grain=src-ndi.gaussian_filter(src,(5,5,0)); g=np.tile(grain,(2,2,1))[:y1-y0,:x1-x0]
mm=np.zeros(L.shape,bool); mm[y0:y1,x0:x1]=True; diff=(np.abs(out[...,:3]-a[...,:3]).sum(-1)>6)&mm
out[y0:y1,x0:x1,:3]+=g*diff[y0:y1,x0:x1,None]
clean=Image.fromarray(np.clip(out,0,255).astype(np.uint8),'RGBA')
txt=logo_text(('TU','LOGO','AQUÍ'),46)
# perspective of the right panel: foreshorten and tilt up to the right
tw,th=txt.size; k=0.16; sx=0.82
coeffs=(1/sx,0,0, k/sx,1,0, 0,0)  # inverse map for PIL: x=a*x'+b*y'+c ; y=d*x'+e*y'+f
newW=int(tw*sx)+int(th*0)+2; newH=int(th+ k*tw)+2
# build with explicit inverse mapping: source x = x'/sx ; source y = y' - k*(x')/sx ... use AFFINE with data (a,b,c,d,e,f)
aff=txt.transform((newW,newH),Image.AFFINE,(1/sx,0,0,-k/sx,1,0),resample=Image.BICUBIC)
aff=aff.transform(aff.size,Image.AFFINE,(1,0,0,0,1,-k*tw),resample=Image.BICUBIC) if False else aff
aff=crop(aff,4)
tree2=print_on(clean,aff,(352-aff.width//2,930-aff.height//2))
save(tree2,'tree-logo'); save(tree2,'tree-real'); save(tree2,'row-tree')
side('tree-full',load('tree-pack-std'),tree2,h=520,gap=-10)
