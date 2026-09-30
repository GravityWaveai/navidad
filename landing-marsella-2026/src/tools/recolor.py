import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

SAND=(217,208,198)

def load_rgba(p):
    return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)/255.0

def hsv(rgb):
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    mx=rgb.max(-1); mn=rgb.min(-1); d=mx-mn
    s=np.where(mx>1e-6, d/np.maximum(mx,1e-6), 0)
    h=np.zeros_like(mx)
    m=d>1e-6
    rc=np.where(m,(mx-r)/np.maximum(d,1e-6),0); gc=np.where(m,(mx-g)/np.maximum(d,1e-6),0); bc=np.where(m,(mx-b)/np.maximum(d,1e-6),0)
    h=np.where(mx==r, bc-gc, np.where(mx==g, 2.0+rc-bc, 4.0+gc-rc))
    h=(h/6.0)%1.0
    return h*360, s, mx

def lum(rgb):
    return 0.299*rgb[...,0]+0.587*rgb[...,1]+0.114*rgb[...,2]

def soft_mask(rgba, hlo=100, hhi=200, smin=0.14, ssoft=0.10, vmin=0.06):
    """soft mask of the green/teal Gravitec material"""
    h,s,v=hsv(rgba[...,:3]); a=rgba[...,3]
    hm=((h>=hlo)&(h<=hhi)).astype(np.float32)
    sm=np.clip((s-smin)/ssoft,0,1)
    vm=(v>vmin).astype(np.float32)
    return hm*sm*vm*np.clip(a*4,0,1)

def build_lut(swatch_path):
    sw=np.asarray(Image.open(swatch_path).convert('RGB')).astype(np.float32)/255
    L=lum(sw).ravel(); px=sw.reshape(-1,3)
    lo,hi=np.percentile(L,2),max(np.percentile(L,98),np.percentile(L,2)+1e-3)
    idx=np.clip(np.round((L-lo)/(hi-lo)*255),0,255).astype(int)
    lut=np.zeros((256,3)); cnt=np.zeros(256)
    np.add.at(lut,idx,px); np.add.at(cnt,idx,1)
    xs=np.where(cnt>0)[0]
    for c in range(3):
        lut[:,c]=np.interp(np.arange(256),xs,lut[xs,c]/cnt[xs])
    return lut

def recolor_lut(rgba, mask, lut, gamma=1.0):
    rgb=rgba[...,:3].copy(); L=lum(rgb)
    sel=mask>0.5
    lo,hi=np.percentile(L[sel],3),np.percentile(L[sel],97)
    t=np.clip((L-lo)/max(hi-lo,1e-3),0,1)**gamma
    idx=np.clip(np.round(t*255),0,255).astype(int)
    new=lut[idx]
    m=mask[...,None]
    out=rgba.copy(); out[...,:3]=rgb*(1-m)+new*m
    return out

def speckle_field(shape, seed=1, scale=1.0, coverage=0.16):
    """procedural Marsella fleck pattern: returns (fleck mask 0..1, darkness variation 0..1)"""
    rng=np.random.default_rng(seed)
    n1=ndi.gaussian_filter(rng.standard_normal(shape), 1.6*scale)
    n2=ndi.gaussian_filter(rng.standard_normal(shape), 3.2*scale)
    n3=ndi.gaussian_filter(rng.standard_normal(shape), 0.9*scale)
    f=n1*0.55+n2*0.35+n3*0.25
    thr=np.percentile(f,100*(1-coverage))
    # soft threshold
    fl=np.clip((f-thr)/(0.12*f.std()+1e-6),0,1)
    var=ndi.gaussian_filter(rng.random(shape), 6*scale)
    var=(var-var.min())/(var.max()-var.min()+1e-6)
    return fl, var

def recolor_synthetic(rgba, mask, seed=1, scale=1.0, coverage=0.16, base=(0.93,0.92,0.885), dark=(0.10,0.33,0.29), mid=(0.20,0.47,0.42), blur=4.0, shade_lo=0.62, shade_hi=1.0):
    rgb=rgba[...,:3]; L=lum(rgb)
    sel=mask>0.5
    # shading from low-passed luminance (within the masked region only, to avoid bleeding of bg)
    Lm=np.where(sel,L,0); W=sel.astype(np.float32)
    num=ndi.gaussian_filter(Lm,blur); den=ndi.gaussian_filter(W,blur)
    bl=np.where(den>1e-3,num/np.maximum(den,1e-3),L)
    lo,hi=np.percentile(bl[sel],4),np.percentile(bl[sel],96)
    sh=np.clip((bl-lo)/max(hi-lo,1e-3),0,1)
    shade=shade_lo+(shade_hi-shade_lo)*sh
    # fine texture: keep a little of the high-frequency detail for realism
    hf=np.clip((L-bl)*0.6+0.0,-0.08,0.08)
    fl,var=speckle_field(L.shape,seed,scale,coverage)
    col=np.array(dark)[None,None,:]*(1-var[...,None])+np.array(mid)[None,None,:]*var[...,None]
    basec=np.array(base)[None,None,:]
    new=basec*(shade[...,None]+hf[...,None])
    new=new*(1-fl[...,None])+col*(shade[...,None]*0.9+0.1)*fl[...,None]
    m=mask[...,None]
    out=rgba.copy(); out[...,:3]=np.clip(rgb*(1-m)+new*m,0,1)
    return out

def save(arr, path, bg=None):
    im=Image.fromarray((np.clip(arr,0,1)*255).astype(np.uint8),'RGBA')
    if bg is not None:
        b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); im=b.convert('RGB')
    im.save(path)
    return im
