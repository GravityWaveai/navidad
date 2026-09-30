import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
import sys; sys.path.insert(0,'.')
from recolor import hsv, lum, SAND

def disk(r):
    y,x=np.ogrid[-r:r+1,-r:r+1]; return (x*x+y*y)<=r*r

def load(p, up=1.0):
    im=Image.open(p).convert('RGBA')
    if up!=1.0:
        im=im.resize((round(im.width*up),round(im.height*up)),Image.LANCZOS)
    return np.asarray(im).astype(np.float32)/255.0

def masks(rgba, has_alpha=True, hlo=95, hhi=210, smin=0.12, close_r=3, up=1.0):
    rgb=rgba[...,:3]; a=rgba[...,3]
    h,s,v=hsv(rgb)
    green=(h>=hlo)&(h<=hhi)&(s>smin)&(v>0.08)
    r=max(1,round(close_r*up))
    g2=ndi.binary_closing(green,structure=disk(r),iterations=1)
    g2=ndi.binary_fill_holes(g2)
    if has_alpha:
        sil=a>0.5
    else:
        sil=g2
    kraft=(h>=8)&(h<=62)&(s>0.16)&(v>0.22)
    kraft_d=ndi.binary_dilation(kraft,structure=disk(max(1,round(2*up))))
    mat=sil&g2&~kraft_d
    # drop tiny components (and stray blobs in the top band for scenes)
    lab,n=ndi.label(mat)
    if n>0:
        sizes=ndi.sum(np.ones(mat.shape),lab,range(1,n+1))
        cy=ndi.center_of_mass(np.ones(mat.shape),lab,range(1,n+1))
        keep=np.zeros(n+1,bool)
        for i in range(n):
            keep[i+1]=sizes[i]>(150*up*up) and (has_alpha or cy[i][0]>0.18*mat.shape[0])
        mat=keep[lab]
    # grow into the anti-aliased edge so no green fringe survives (alpha keeps the silhouette)
    edge=a>0.02 if has_alpha else ndi.binary_dilation(mat,structure=disk(1))
    mat=ndi.binary_dilation(mat,structure=disk(max(1,round(2.5*up))))&edge&~kraft
    # white print (logo text) inside silhouette
    pr=sil&(v>0.90)&(s<0.10)
    pr=ndi.binary_opening(pr,structure=disk(max(1,round(1*up))))&sil
    mat=mat&~pr
    soft=ndi.gaussian_filter(mat.astype(np.float32),0.5*up)
    return soft, mat, pr

def flecks(shape, seed=1, density=0.05, med=0.62, sigma=0.72, up=1.0, elong=2.4):
    """draw angular net-fragment flecks; returns alpha (0..1) and tone (0..1)"""
    H,W=shape
    rng=np.random.default_rng(seed)
    n=int(density*H*W/(up*up))
    layer=Image.new('L',(W,H),0); tone=Image.new('L',(W,H),0)
    d=ImageDraw.Draw(layer); dt=ImageDraw.Draw(tone)
    for i in range(n):
        cx,cy=rng.uniform(0,W),rng.uniform(0,H)
        faint=rng.random()<0.12
        s=rng.lognormal(math.log(med*up),sigma)
        if faint: s*=1.25
        s=min(s,2.9*up)
        k=int(rng.integers(3,7))
        ang=rng.uniform(0,2*math.pi)
        ex=rng.uniform(1.0,elong) if rng.random()<0.5 else 1.0
        pts=[]
        ca,sa=math.cos(ang),math.sin(ang)
        for j in range(k):
            t=2*math.pi*j/k+rng.uniform(-0.4,0.4)
            rr=s*rng.uniform(0.5,1.4)
            px=math.cos(t)*rr*ex; py=math.sin(t)*rr
            pts.append((cx+px*ca-py*sa, cy+px*sa+py*ca))
        if faint: tn=int(rng.uniform(1,60))
        else: tn=int(rng.uniform(70,255))
        d.polygon(pts,fill=255); dt.polygon(pts,fill=tn)
    al=np.asarray(layer.filter(ImageFilter.GaussianBlur(0.5*up))).astype(np.float32)/255
    tn=np.asarray(tone).astype(np.float32)/255
    return al, tn

def recolor(rgba, mat_soft, mat, pr, seed=1, up=1.0, density=0.05, med=0.62,
            base=(0.885,0.88,0.855), dark=(0.14,0.30,0.26), mid=(0.31,0.45,0.40), faint=(0.66,0.73,0.70),
            blur=14.0, shade_lo=0.74, shade_hi=1.0, hf_amt=0.06, shadow_gain=1.8, print_relief=True):
    rgb=rgba[...,:3]; L=lum(rgb)
    W=(mat&~pr).astype(np.float32)
    num=ndi.gaussian_filter(L*W,blur*up); den=ndi.gaussian_filter(W,blur*up)
    bl=np.where(den>1e-3,num/np.maximum(den,1e-3),L)
    sel=mat&~pr
    lo,hi=np.percentile(bl[sel],4),np.percentile(bl[sel],96)
    sh=np.clip((bl-lo)/max(hi-lo,1e-3),0,1)
    shade=shade_lo+(shade_hi-shade_lo)*sh
    # recover cast shadows: only the darkest, contiguous regions of the original (overlap shadows, deep edges)
    Ls=ndi.gaussian_filter(L*W,2.5*up)/np.maximum(ndi.gaussian_filter(W,2.5*up),1e-3)
    Ln=(Ls-lo)/max(hi-lo,1e-3)
    thr=np.percentile(Ln[sel],5)
    occ=np.clip(thr-Ln,0,0.6)*sel
    lab_,n_=ndi.label(occ>0.01)
    if n_:
        sz=ndi.sum(np.ones(occ.shape),lab_,range(1,n_+1)); keep=np.zeros(n_+1,bool); keep[1:]=sz>(1400*up*up); occ=occ*keep[lab_]
    occ=ndi.gaussian_filter(occ,2*up)
    shade=shade*np.clip(1-shadow_gain*occ,0.5,1)
    hf=np.clip((L-bl)*hf_amt,-0.05,0.05)
    fa,ft=flecks(L.shape,seed,density,med,up=up)
    isfaint=(ft<0.25)
    col=np.array(dark)[None,None,:]*(1-ft[...,None])+np.array(mid)[None,None,:]*ft[...,None]
    col=np.where(isfaint[...,None],np.array(faint)[None,None,:],col)
    basec=np.array(base)[None,None,:]
    new=basec*(shade[...,None]+hf[...,None])
    new=new*(1-fa[...,None])+col*(0.85*shade[...,None]+0.15)*fa[...,None]
    if print_relief and pr.any():
        # printed logo: pure white with a soft dark relief shadow so it reads on the light base
        prf=pr.astype(np.float32)
        shd=ndi.shift(ndi.gaussian_filter(prf,1.3*up),(1.6*up,1.2*up),order=1,mode='constant')
        shd=np.clip(shd*1.4,0,1)*(1-prf)
        new=new*(1-0.42*shd[...,None])
        new=np.where(pr[...,None],np.array([0.985,0.985,0.975])[None,None,:]*np.clip(shade[...,None]*0.3+0.7,0,1),new)
        mat_soft=np.maximum(mat_soft,prf)
    m=mat_soft[...,None]
    out=rgba.copy(); out[...,:3]=np.clip(rgb*(1-m)+new*m,0,1)
    return out

def process(path, out, has_alpha=True, up=1.5, seed=1, **kw):
    a=load(path,up)
    ms,m,pr=masks(a,has_alpha,up=up,**{k:v for k,v in kw.items() if k in ('hlo','hhi','smin','close_r')})
    o=recolor(a,ms,m,pr,seed=seed,up=up,**{k:v for k,v in kw.items() if k not in ('hlo','hhi','smin','close_r')})
    im=Image.fromarray((np.clip(o,0,1)*255).astype(np.uint8),'RGBA')
    im.save(out)
    return im, m, pr

def internal_edge_shadow(rgba, mat, up=1.0, gsig=1.2, thr_pct=97.5, minlen=70, width=9.0, strength=0.42):
    """cast shadow along internal edges between overlapping pieces: strong, long luminance edges inside the material.
    The shadow is drawn on the darker side of the edge (the piece behind). Returns a multiplier map (0..1)."""
    L=lum(rgba[...,:3]); a=rgba[...,3]
    Ls=ndi.gaussian_filter(L,gsig*up)
    gy=ndi.sobel(Ls,0); gx=ndi.sobel(Ls,1); g=np.hypot(gx,gy)
    inner=ndi.binary_erosion(mat,structure=disk(max(2,round(4*up))))
    g=g*inner
    thr=np.percentile(g[inner],thr_pct) if inner.any() else 1e9
    e=g>thr
    lab,n=ndi.label(e,structure=np.ones((3,3)))
    mult=np.ones(L.shape,np.float32)
    if not n: return mult
    sz=ndi.sum(np.ones(e.shape),lab,range(1,n+1))
    keep=np.zeros(n+1,bool); keep[1:]=sz>(minlen*up); e=keep[lab]
    if not e.any(): return mult
    # shadow on the darker side: shift edge pixels along -gradient (toward darker) and blur
    ys,xs=np.where(e); nx=gx[ys,xs]; ny=gy[ys,xs]; nn=np.hypot(nx,ny)+1e-6; nx/=nn; ny/=nn
    sh=np.zeros(L.shape,np.float32)
    for d in np.linspace(0.5,width*up,int(width*up*2)):
        yy=np.clip(np.round(ys-ny*d).astype(int),0,L.shape[0]-1); xx=np.clip(np.round(xs-nx*d).astype(int),0,L.shape[1]-1)
        sh[yy,xx]=np.maximum(sh[yy,xx],1-d/(width*up))
    sh=ndi.gaussian_filter(sh,1.5*up)*mat
    sh=np.clip(sh*1.6,0,1)
    return 1-strength*sh

def fit_template(union, tmpl, angles, scales, min_fill=0.97):
    """find (angle, scale, y, x) placing binary template fully inside union with maximal area; returns mask or None"""
    from numpy.fft import rfft2, irfft2
    H,W=union.shape; U=union.astype(np.float32); FU=rfft2(U)
    best=None
    for ang in angles:
        for sc in scales:
            t=ndi.zoom(tmpl.astype(np.float32),sc,order=1)>0.5
            t=ndi.rotate(t,ang,order=0,reshape=True)
            th,tw=t.shape
            if th>=H or tw>=W: continue
            area=t.sum()
            if area<50: continue
            T=np.zeros((H,W),np.float32); T[:th,:tw]=t
            corr=irfft2(FU*np.conj(rfft2(T)),s=(H,W))  # corr[y,x] = overlap of template shifted by (y,x)
            y,x=np.unravel_index(np.argmax(corr),corr.shape)
            fill=corr[y,x]/area
            if fill>=min_fill and (best is None or area>best[0]):
                best=(area,ang,sc,y,x,t)
    if best is None: return None
    area,ang,sc,y,x,t=best
    M=np.zeros((H,W),bool); th,tw=t.shape
    yy=np.arange(th)+y; xx=np.arange(tw)+x
    M[np.ix_(yy%H,xx%W)]=t
    return M

def front_shadow(union, front, up=1.0, offset=(5,6), spread=9, strength=0.5, edge=0.18):
    """multiplier map: soft cast shadow of the front piece onto the rest of the union"""
    sh=ndi.gaussian_filter(front.astype(np.float32),spread*up*0.5)
    sh=ndi.shift(sh,(offset[0]*up,offset[1]*up),order=1)
    sh=np.clip(sh*1.3,0,1)*(~front)*union
    core=ndi.binary_dilation(front,structure=disk(max(1,round(2*up))))&~front&union
    sh=np.maximum(sh,ndi.gaussian_filter(core.astype(np.float32),1.0*up)*1.2)
    sh=np.clip(sh,0,1)
    return 1-strength*sh

def ellipse(h,w):
    y,x=np.ogrid[-1:1:complex(0,h),-1:1:complex(0,w)]; return (x*x+y*y)<=1
