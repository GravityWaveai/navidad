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
 ('cover-stars','img/p01_x34.png',1.6,11,{}),
 ('row-tree','img/p03_x47.png',1.6,12,{}),
 ('row-star','img/p03_x48.png',1.6,13,{}),
 ('row-coaster','img/p03_x49.png',1.6,14,{}),
 ('row-phone','img/p03_x50.png',1.6,15,{}),
 ('coaster-pack','img/p06_x71.png',1.5,21,{}),
 ('coaster-logo','img/p07_x77.png',1.5,22,{}),
 ('coaster-ico-std','img/p07_x76.png',2.0,23,{}),
 ('coaster-ico-pack','img/p07_x78.png',2.0,24,{}),
 ('phone-plain','img/p08_x88.png',1.5,31,{}),
 ('phone-tag','img/p08_x89.png',1.5,32,{}),
 ('phone-ico-1','img/p09_x96.png',1.5,33,{}),
 ('phone-ico-2','img/p09_x97.png',1.5,34,{}),
 ('phone-ico-3','img/p09_x100.png',1.5,35,{}),
 ('star-logo','img/p10_x112.png',1.5,41,{}),
 ('star-pack','img/p11_x119.png',1.5,42,{}),
 ('star-pack-std','img/p11_x120.png',1.8,43,{}),
 ('star-pack-2','img/p11_x124.png',1.8,44,{}),
 ('tree-pack','img/p13_x142.png',1.5,52,{}),
 ('tree-pack-std','img/p13_x143.png',1.8,53,{}),
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
    o=recolor(a,ms,m,pr,seed=seed,up=up)
    if name in FRONT:
        union,M=fit_front(a,FRONT[name],up)
        if M is not None:
            M=ndi.binary_dilation(M,structure=disk(max(1,round(1.5*up))))
            o[...,:3]*=front_shadow(union,M,up=up)[...,None]; print('   front shadow', name, int(M.sum()))
    im=Image.fromarray((np.clip(o,0,1)*255).astype(np.uint8),'RGBA'); im.save(f'test2/{name}.png'); return im
meta={}
for name,srcp,up,seed,extra in REC:
    im=process2(srcp,name,up,seed,extra)
    im=crop_alpha(im,pad=int(8*up))
    meta[name]=save_webp(im,name)
# scene (no alpha)
im,m,pr=process('img/p16_x862.png','test2/scene.png',has_alpha=False,up=1.5,seed=7,hlo=140,hhi=210,smin=0.10,close_r=4)
meta['scene']=save_jpg(im,'scene',q=84)
# real marsella photos (no recolor)
def real(name,srcp,box=None,pad=6):
    im=Image.open(srcp).convert('RGBA')
    im=im.crop(box) if box else crop_alpha(im,pad)
    meta[name]=save_webp(im,name,q=86)
real('star-real','img/p10_x113.png')
real('phone-real','img/p08_x90.png')
real('bola-real','img/p14_x160.png')
real('coaster-real','img/p06_x72.png')
real('tree-real','img/p12_x136.png')
im,m,pr=process('img/p12_x135.png','test2/tree-logo.png',has_alpha=True,up=1.5,seed=51)
im=im.crop((int(255*1.5),0,im.width,im.height))
# keep only the largest connected object (the tree)
al=np.asarray(im)[...,3]>10; lab,n=ndi.label(ndi.binary_dilation(al,iterations=3)); sizes=ndi.sum(np.ones(al.shape),lab,range(1,n+1)); big=(lab==(int(np.argmax(sizes))+1))
arr=np.asarray(im).copy(); arr[...,3]=np.where(big,arr[...,3],0); im=Image.fromarray(arr,'RGBA'); im=crop_alpha(im,12); meta['tree-logo']=save_webp(im,'tree-logo')
im=Image.open('test2/coaster-logo.png').convert('RGBA'); aa=np.asarray(im)[...,3]>10; occ=aa.sum(0)
xs=np.where(occ>3)[0]; gaps=[x for x in range(xs.min(),xs.max()) if occ[x]<=3]; cut=(gaps[0]+gaps[-1])//2
meta['coaster-logo']=save_webp(crop_alpha(im.crop((0,0,cut,im.height)),12),'coaster-logo')
# process crops from p04_x56 (net / granza / panel)
im=Image.open('img/p04_x56.png').convert('RGBA'); al=np.asarray(im)[...,3]>10
occ=al.sum(0)>3
segs=[]; inseg=False
for x,o in enumerate(occ):
    if o and not inseg: start=x; inseg=True
    if not o and inseg: segs.append((start,x)); inseg=False
if inseg: segs.append((start,len(occ)))
segs=[s for s in segs if s[1]-s[0]>40]; print('segments', segs)
for nm,(x0,x1) in zip(['proc-net','proc-granza','proc-panel'],segs):
    c=im.crop((x0-4,0,x1+4,im.height)); c=crop_alpha(c,6); meta[nm]=save_webp(c,nm,q=86)
# swatch, net bg, boat
sw=Image.open('img/p05_x67.png').convert('RGBA').crop((79,120,456,683)); meta['swatch']=save_jpg(flat(sw),'swatch',q=86)
meta['net-bg']=save_jpg(Image.open('img/p04_x636.png'),'net-bg',q=72)
meta['boat']=save_jpg(Image.open('img/p02_x618.png'),'boat',q=78)
# composed 'full' views: packaging + piece with logo side by side
def compose(name,left,right,h=520,gap=-30):
    L=Image.open(f'assets/{left}.webp').convert('RGBA'); R=Image.open(f'assets/{right}.webp').convert('RGBA')
    L=L.resize((int(L.width*h/L.height),h),Image.LANCZOS); R=R.resize((int(R.width*h*0.92/R.height),int(h*0.92)),Image.LANCZOS)
    c=Image.new('RGBA',(L.width+R.width+gap+20,h+20),(0,0,0,0)); c.alpha_composite(L,(0,10)); c.alpha_composite(R,(L.width+gap+20,10+h-R.height)); meta[name]=save_webp(c,name)
compose('star-full','star-pack','star-logo')
compose('phone-full','phone-ico-1','phone-tag',gap=-10)
json.dump(meta,open('assets/meta.json','w'),indent=1)
print('total KB', sum(os.path.getsize(f'assets/{f}') for f in os.listdir('assets'))//1024)
