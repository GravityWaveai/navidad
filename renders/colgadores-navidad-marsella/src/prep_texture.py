from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
im = Image.open('ref_muestra.png').convert('RGB')
W,H = im.size  # 990x1350
# square crop avoiding the MUESTRA badge (bottom-left)
crop = im.crop((0, 60, 990, 1050))
a = np.asarray(crop).astype(np.float32)
# flatten illumination: divide by heavily blurred luminance of the white background
lum = Image.fromarray(a.mean(axis=2).astype(np.uint8)).filter(ImageFilter.GaussianBlur(70))
l = np.asarray(lum).astype(np.float32)
# background estimate from the bright pixels only: blur a max-filtered version
bright = Image.fromarray(a.mean(axis=2).astype(np.uint8)).filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(60))
b = np.asarray(bright).astype(np.float32)
gain = (b.mean()/np.maximum(b,1))[...,None]
a2 = np.clip(a*gain, 0, 255)
# white point: map 92nd percentile of brightness to a warm white
p = np.percentile(a2.mean(axis=2), 92)
target = np.array([243, 242, 237], dtype=np.float32)
scale = target / np.array([np.percentile(a2[...,i], 92) for i in range(3)])
a3 = np.clip(a2*scale, 0, 255).astype(np.uint8)
out = Image.fromarray(a3).resize((1024,1024), Image.LANCZOS)
out = ImageEnhance.Color(out).enhance(1.12)
out.save('marsella_face.png')
# bump map: specks slightly recessed/satin -> grayscale, blurred a touch
g = ImageOps.grayscale(out).filter(ImageFilter.GaussianBlur(0.8))
g.save('marsella_bump.png')
# roughness map: specks a bit glossier (lower roughness) than the white grain
r = ImageOps.autocontrast(g)
r = Image.fromarray((np.asarray(r).astype(np.float32)*0.25+170).astype(np.uint8))
r.save('marsella_rough.png')
# fine grain for the white recycled plastic (sparkly micro-texture)
rng = np.random.default_rng(3)
noise = rng.normal(0, 1, (1024,1024)).astype(np.float32)
noise = np.asarray(Image.fromarray(np.clip(noise*40+128,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)))
Image.fromarray(noise).save('grain.png')
# kraft paper texture 1024x1024
k = rng.normal(0,1,(1024,1024)).astype(np.float32)
kb = np.asarray(Image.fromarray(np.clip(k*30+128,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)
fib = rng.normal(0,1,(1024,1024)).astype(np.float32)
fib = np.asarray(Image.fromarray(np.clip(fib*40+128,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur((6,0.6)))).astype(np.float32)
base = np.array([196,154,108],dtype=np.float32)  # kraft
mix = ((kb-128)*0.35 + (fib-128)*0.45)[...,None]
kr = np.clip(base + mix*np.array([1.0,0.9,0.75]), 0, 255).astype(np.uint8)
Image.fromarray(kr).save('kraft.png')
print(out.size, 'ok', a3.reshape(-1,3).mean(axis=0))
