import sys, json, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
BG = (216, 208, 196)
def arrow(layer_draw, S, p0, c, p1, width):
    pts = [(( (1-t)**2*p0[0] + 2*(1-t)*t*c[0] + t*t*p1[0])*S, ((1-t)**2*p0[1] + 2*(1-t)*t*c[1] + t*t*p1[1])*S) for t in np.linspace(0,1,80)]
    w = width*S
    layer_draw.line(pts, fill=(255,255,255,255), width=int(w), joint='curve')
    for p in (pts[0], pts[-1]): layer_draw.ellipse([p[0]-w/2,p[1]-w/2,p[0]+w/2,p[1]+w/2], fill=(255,255,255,255))
    # head: chevron
    tx, ty = pts[-1][0]-pts[-4][0], pts[-1][1]-pts[-4][1]; L = math.hypot(tx,ty); tx,ty = tx/L, ty/L
    hl = width*4.2*S
    for sgn in (1,-1):
        a = math.radians(32)*sgn
        bx = pts[-1][0] - hl*(tx*math.cos(a) - ty*math.sin(a)); by = pts[-1][1] - hl*(tx*math.sin(a) + ty*math.cos(a))
        layer_draw.line([pts[-1], (bx,by)], fill=(255,255,255,255), width=int(w))
        layer_draw.ellipse([bx-w/2,by-w/2,bx+w/2,by+w/2], fill=(255,255,255,255))
def main(render_png, out_base, arrows):
    im = Image.open(render_png).convert('RGBA'); W,H = im.size
    # background with a very soft radial lift under the product
    yy,xx = np.mgrid[0:H,0:W].astype(np.float32)
    d = np.sqrt(((xx-W/2)/W)**2 + ((yy-H/2)/H)**2)
    lift = np.clip(1 - d/0.75, 0, 1)**2 * 7
    bg = np.stack([np.clip(BG[i] + lift, 0, 255) for i in range(3)], axis=2).astype(np.uint8)
    out = Image.fromarray(bg).convert('RGBA')
    out.alpha_composite(im)
    if arrows:
        S = 3; layer = Image.new('RGBA', (W*S, H*S), (0,0,0,0)); dr = ImageDraw.Draw(layer)
        for a in arrows: arrow(dr, S, a['p0'], a['c'], a['p1'], a['w'])
        layer = layer.resize((W,H), Image.LANCZOS)
        out.alpha_composite(layer)
    out = out.convert('RGB')
    # subtle photographic grain
    arr = np.asarray(out).astype(np.float32); g = np.random.default_rng(11).normal(0, 1.6, arr.shape[:2])[...,None]
    out = Image.fromarray(np.clip(arr + g, 0, 255).astype(np.uint8))
    out.save(out_base + '.png', optimize=True)
    out.save(out_base + '.jpg', quality=93, subsampling=0)
    print('saved', out_base, W, H)
if __name__ == '__main__':
    cfg = json.loads(sys.argv[1]); main(cfg['render'], cfg['out'], cfg.get('arrows', []))
