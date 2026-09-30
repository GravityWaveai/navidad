import sys, os, json
sys.path.insert(0,'.')
from recolor2 import *
OUT='assets'; os.makedirs(OUT,exist_ok=True)
def flat(im,bg=SAND):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def crop_alpha(im,pad=6):
    bb=im.getbbox(); 
    if not bb: return im
    return im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
def save_webp(im,name,q=82):
    p=f'{OUT}/{name}.webp'; im.save(p,'WEBP',quality=q,method=6); print(name, im.size, os.path.getsize(p)//1024,'KB'); return p
def save_jpg(im,name,q=82):
    p=f'{OUT}/{name}.jpg'; im.convert('RGB').save(p,'JPEG',quality=q,optimize=True,progressive=True); print(name, im.size, os.path.getsize(p)//1024,'KB'); return p

REC=[ # name, src, up, seed, extra
 ('coaster-pack','img/p06_x71.png',1.5,21,{'tex':1.15}),
 ('coaster-ico-std','img/p07_x76.png',2.0,23,{'tex':0.8}),
 ('coaster-ico-pack','img/p07_x78.png',2.0,24,{'tex':0.8}),
 ('phone-plain','img/p08_x88.png',1.5,31,{}),
 ('phone-tag','img/p08_x89.png',1.5,32,{}),
 ('phone-ico-1','img/p09_x96.png',1.5,33,{'tex':0.8}),
 ('phone-ico-2','img/p09_x97.png',1.5,34,{'tex':0.8}),
 ('phone-ico-3','img/p09_x100.png',1.5,35,{'tex':0.8}),
 ('star-pack','img/p11_x119.png',1.5,42,{}),
 ('star-pack-std','img/p11_x120.png',1.8,43,{'tex':0.85}),
 ('star-pack-2','img/p11_x124.png',1.8,44,{'tex':0.85}),
 ('tree-pack','img/p13_x142.png',1.5,52,{'tex':0.9}),
 ('tree-pack-std','img/p13_x143.png',1.8,53,{'tex':0.8}),
]
STAR=np.asarray(Image.open('img/p10_x113.png').convert('RGBA'))[...,3]>128
_ys,_xs=np.where(STAR); STAR=STAR[_ys.min():_ys.max()+1,_xs.min():_xs.max()+1]
FRONT={'cover-stars':'star','star-logo':'star','row-star':'star','coaster-pack':'ell','coaster-logo':'ell'}
def fit_front(a,kind,up):
    union=a[...,3]>0.5
    if kind=='star':
        M=fit_template(union,STAR,angles=range(-40,41,4),scales=[0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2])
        return union,M
    occ=(a[...,3]>0.5).sum(0); xs=np.where(occ>3)[0]; gaps=[x for x in range(xs.min(),xs.max()) if occ[x]<=3]; cut=(gaps[0]+gaps[-1])//2
    union=union.copy(); union[:,cut:]=False; M=None
    for asp in (0.35,0.42,0.5,0.58):
        r=fit_template(union,ellipse(int(300*asp),300),angles=range(-20,21,5),scales=[0.6,0.75,0.9,1.05,1.2],min_fill=0.985)
        if r is not None and (M is None or r.sum()>M.sum()): M=r
    return union,M
def process2(srcp,name,up,seed,extra):
    a=load(srcp,up); ms,m,pr=masks(a,True,up=up,**{k:v for k,v in extra.items() if k in ('hlo','hhi','smin','close_r')})
    m2=m|pr; ms2=np.maximum(ms,pr.astype(np.float32)); pr2=np.zeros_like(pr)
    o=recolor_real(a,ms2,m2,pr2,up=up,tex_scale=extra.get('tex',1.0),seed=seed)
    im=Image.fromarray((np.clip(o,0,1)*255).astype(np.uint8),'RGBA'); im.save(f'test2/{name}.png'); return im
meta={}
for name,srcp,up,seed,extra in REC:
    im=process2(srcp,name,up,seed,extra)
    im=crop_alpha(im,pad=int(8*up))
    meta[name]=save_webp(im,name)
# scene (no alpha)
a=load('img/p16_x862.png',1.5); ms,m,pr=masks(a,False,up=1.5,hlo=140,hhi=210,smin=0.10,close_r=4)
o=recolor_real(a,np.maximum(ms,pr.astype(np.float32)),m|pr,np.zeros_like(pr),up=1.5,tex_scale=0.55,seed=7)
im=Image.fromarray((np.clip(o,0,1)*255).astype(np.uint8),'RGBA'); meta['scene']=save_jpg(im,'scene',q=84)
# real marsella photos (no recolor)
def real(name,srcp,box=None,pad=6):
    im=Image.open(srcp).convert('RGBA')
    im=im.crop(box) if box else crop_alpha(im,pad)
    meta[name]=save_webp(im,name,q=86)
real('star-real','img/p10_x113.png')
SKIP=True
real('phone-real','img/p08_x90.png')
real('bola-real','img/p14_x160.png')
real('coaster-real','img/p06_x72.png')
real('tree-real','img/p12_x136.png')
json.dump(meta,open('assets/meta.json','w'),indent=1)
print('total KB', sum(os.path.getsize(f'assets/{f}') for f in os.listdir('assets'))//1024)
