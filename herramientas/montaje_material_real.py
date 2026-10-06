"""Montaje determinista: geometría de un render Codex (PNG con alfa) + textura REAL del acabado
Marsella (foto recortada) + pieza trasera completa. Sin IA, sin créditos.

Uso:
  python3 herramientas/montaje_material_real.py fuentes/arbol-02-pack-gravity-wave.png \
      fuentes/muestra-acabado-marsella-recortada.jpg fuentes/arbol-02-montaje-material-real

Genera <salida>.png (alfa) y <salida>-blanco.jpg (fondo blanco, para el pase foto en Magnific).
Opciones: --sin-trasera (una sola pieza), --escala 0.75 (tamaño de escama), --offset 16,-14.
"""
import sys, random, argparse
from PIL import Image, ImageFilter
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("codex"); ap.add_argument("textura"); ap.add_argument("salida")
ap.add_argument("--escala", type=float, default=0.75)
ap.add_argument("--offset", default="0,0")
ap.add_argument("--sin-trasera", action="store_true")
ap.add_argument("--semilla", type=int, default=7)
A = ap.parse_args()
random.seed(A.semilla)

src = Image.open(A.codex).convert("RGBA"); W, H = src.size
a = np.array(src).astype(np.int32)
r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
opaque = al > 20
# Cartón kraft + logo negro: se conservan tal cual del render
kraft = opaque & ((r - b) > 70) & (r > 140) & (g > 95) & (g < 210)
lum = 0.299 * r + 0.587 * g + 0.114 * b
if kraft.sum() > 500:
    ys, xs = np.where(kraft)
    by0, by1 = np.percentile(ys, [0.5, 99.5]).astype(int); bx0, bx1 = np.percentile(xs, [0.5, 99.5]).astype(int)
    bandbox = np.zeros_like(opaque); bandbox[by0:by1 + 1, bx0:bx1 + 1] = True
    keep = (kraft & bandbox) | (bandbox & (lum < 90))
    keep = (np.array(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))) > 0) & opaque
else:
    by1 = int(H * 0.55); keep = np.zeros_like(opaque)
panel = opaque & ~keep
# Sombreado de cantos del render, sin las motas
speck = panel & (g >= r - 4) & (lum < 218)
speck = (np.array(Image.fromarray((speck * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0) & panel
base = np.percentile(lum[panel & ~speck], 60)
lf = lum.astype(np.float32).copy(); lf[speck] = base
Lm = np.array(Image.fromarray(lf.clip(0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(15))).astype(np.float32)
shade = np.clip(Lm / base, 0.93, 1.03)
# Textura real, parches aleatorios fundidos (sin costuras)
tex = Image.open(A.textura).convert("RGB")
tex = tex.resize((int(tex.width * A.escala), int(tex.height * A.escala)), Image.LANCZOS)
T = np.array(tex).astype(np.float32)
def quilt(W, H, patch=220, step=150, feather=50):
    out = np.zeros((H, W, 3), np.float32); ws = np.zeros((H, W, 1), np.float32)
    yy, xx = np.mgrid[0:patch, 0:patch]
    d = np.minimum(np.minimum(yy, patch - 1 - yy), np.minimum(xx, patch - 1 - xx)).astype(np.float32)
    wgt = np.clip(d / feather, 0, 1)[..., None] + 1e-3
    for y in range(-patch // 2, H, step):
        for x in range(-patch // 2, W, step):
            ty = random.randint(0, T.shape[0] - patch); tx = random.randint(0, T.shape[1] - patch)
            p = np.rot90(T[ty:ty + patch, tx:tx + patch], random.randint(0, 3))
            if random.random() < 0.5: p = p[:, ::-1]
            y0, x0 = max(y, 0), max(x, 0); y1, x1 = min(y + patch, H), min(x + patch, W)
            if y1 <= y0 or x1 <= x0: continue
            out[y0:y1, x0:x1] += p[y0 - y:y1 - y, x0 - x:x1 - x] * wgt[y0 - y:y1 - y, x0 - x:x1 - x]
            ws[y0:y1, x0:x1] += wgt[y0 - y:y1 - y, x0 - x:x1 - x]
    return out / ws
front = np.zeros((H, W, 4), np.float32)
front[..., 0:3] = quilt(W, H) * shade[..., None]; front[..., 3] = al
front[keep, 0:3] = a[keep, 0:3]
frontimg = Image.fromarray(front.clip(0, 255).astype(np.uint8), "RGBA")
canvas = Image.new("RGBA", (W + 60, H + 60), (0, 0, 0, 0))
if not A.sin_trasera:
    mask = opaque.copy(); cx = W // 2
    for y in range(by1, H):  # rellenar la ranura inferior entre las dos patas
        row = mask[y]; L = np.where(row[:cx])[0]; R = np.where(row[cx:])[0]
        if len(L) and len(R): mask[y, L.max():cx + R.min() + 1] = True
    mask = np.array(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))) > 0
    back = np.zeros((H, W, 4), np.float32); random.seed(A.semilla + 92)
    back[..., 0:3] = quilt(W, H) * 0.90; back[..., 3] = mask * 255
    dx, dy = map(int, A.offset.split(","))
    canvas.alpha_composite(Image.fromarray(back.clip(0, 255).astype(np.uint8), "RGBA"), (30 + dx, 30 + dy))
canvas.alpha_composite(frontimg, (30, 30))
canvas.save(A.salida + ".png")
white = Image.new("RGBA", canvas.size, (255, 255, 255, 255)); white.alpha_composite(canvas)
white.convert("RGB").save(A.salida + "-blanco.jpg", quality=95)
print("ok", A.salida + ".png", A.salida + "-blanco.jpg")
