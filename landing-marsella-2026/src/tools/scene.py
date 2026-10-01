# closing scene: new product photos arranged on the catalogue table photo (original scene with the green products masked out)
import sys; sys.path.insert(0,'.')
from recolor2 import hsv, disk
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage as ndi
base=Image.open('img/p16_x862.png').convert('RGB').resize((1600,1200),Image.LANCZOS)
a=np.asarray(base).astype(np.float32)/255; h,s,v=hsv(a); green=(h>=120)&(h<=200)&(s>0.12)&(v>0.1)
m=ndi.binary_dilation(ndi.binary_closing(green,structure=disk(5)),structure=disk(14))
# inpaint the table where the products were
out=a.copy(); valid=(~m).astype(np.float32); mm=m.copy()
for sg in (4,8,16,32,64):
    for c in range(3):
        f=ndi.gaussian_filter(out[...,c]*valid,sg)/np.maximum(ndi.gaussian_filter(valid,sg),1e-3); sel=mm&(ndi.gaussian_filter(valid,sg)>0.02); out[sel,c]=f[sel]
    valid=np.maximum(valid,sel); mm=mm&~sel
# add wood grain from a clean table region
src=a[950:1150,100:500]; grain=src-ndi.gaussian_filter(src,(8,8,0)); H,W=a.shape[:2]
g=np.tile(grain,(H//200+1,W//400+1,1))[:H,:W]; out[m]+=g[m]*0.8
scene=Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8),'RGB').convert('RGBA')
def L(n): return Image.open(f'assets/{n}.webp').convert('RGBA')
def shadow(lay,blur=18,off=(10,22),st=0.45):
    al=np.asarray(lay)[...,3].astype(np.float32)/255; sh=ndi.shift(ndi.gaussian_filter(al,blur),(off[1],off[0]),order=1); sh=np.clip(sh*1.1,0,1)*st
    o=np.zeros((*al.shape,4),np.uint8); o[...,:3]=[40,35,30]; o[...,3]=(sh*255).astype(np.uint8); return Image.fromarray(o,'RGBA')
def put(im,x,y,h):
    im=im.resize((int(im.width*h/im.height),h),Image.LANCZOS); lay=Image.new('RGBA',scene.size,(0,0,0,0)); lay.alpha_composite(im,(x,y)); scene.alpha_composite(shadow(lay)); scene.alpha_composite(lay)
put(L('tree-logo'),880,330,560)      # tree back-centre
put(L('phone-ico-1'),330,470,470)    # packaged phone stand left
put(L('coaster-ico-pack'),1180,620,360)  # coaster pack right
put(L('star-logo'),560,760,300)      # star front-left
put(L('bola-pack'),1010,790,320)     # baubles front-right
scene.convert('RGB').save('assets/scene.jpg','JPEG',quality=86,optimize=True,progressive=True); print('scene ok')
