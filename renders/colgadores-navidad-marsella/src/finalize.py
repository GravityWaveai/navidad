import json, subprocess, shutil, os
OUT = '/home/user/navidad/renders/colgadores-navidad-marsella'
os.makedirs(OUT, exist_ok=True)
shots = [
 {"shot":"pack_gw","w":2048,"h":2048,"elev":62,"dist":262,"out":"out/r_gw.png"},
 {"shot":"pack_co","w":2048,"h":2048,"elev":62,"dist":262,"out":"out/r_co.png"},
 {"shot":"pack_co_unboxed","w":2400,"h":1500,"elev":52,"dist":400,"out":"out/r_un.png"},
]
subprocess.run(['node','render.js',json.dumps(shots)], check=True)
names = {"pack_gw":"02_packaging-gravity-wave","pack_co":"03_packaging-tu-logo-gravity-wave","pack_co_unboxed":"04_packaging-tu-logo-colgadores-personalizados"}
for s in shots:
    j = json.load(open(s['out'].replace('.png','.json'))); W,H = s['w'],s['h']; arrows=[]
    if s['shot']=='pack_co':
        px,py = j['anchors']['print']
        arrows.append({"p0":[px-0.21*W,py-0.30*H],"c":[px-0.02*W,py-0.31*H],"p1":[px-0.012*W,py-0.058*H],"w":0.011*W})
    if s['shot']=='pack_co_unboxed':
        ax,ay = j['anchors']['orn']; px,py = j['anchors']['print']
        arrows.append({"p0":[ax-0.10*W,ay-0.30*H],"c":[ax+0.03*W,ay-0.27*H],"p1":[ax-0.004*W,ay-0.085*H],"w":0.0085*W})
        arrows.append({"p0":[px-0.13*W,py-0.31*H],"c":[px-0.005*W,py-0.31*H],"p1":[px-0.008*W,py-0.08*H],"w":0.0085*W})
    base = os.path.join(OUT, names[s['shot']])
    subprocess.run(['python3','composite.py',json.dumps({"render":s['out'],"out":base,"arrows":arrows})], check=True)
# image 1: the one the user supplied
from PIL import Image
im = Image.open('ref_pack.png').convert('RGB'); im.save(os.path.join(OUT,'01_pack-2-colgadores-marsella.png')); im.save(os.path.join(OUT,'01_pack-2-colgadores-marsella.jpg'), quality=94)
print(sorted(os.listdir(OUT)))
