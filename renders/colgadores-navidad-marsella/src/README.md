# Renders colgadores Navidad · acabado Marsella

Escena 3D en three.js renderizada con Chromium headless (Playwright). La textura
`marsella_face.png` sale de la foto real de la muestra (`ref_muestra.png`), con la
iluminación aplanada; `kraft.png` es el cartón de la faja en cruz.

Regenerar:

```bash
cd renders/colgadores-navidad-marsella/src
npm install            # three + playwright-core (usa el Chromium de /opt/pw-browsers)
python3 finalize.py    # renderiza 02, 03 y 04 y los compone con las flechas
```

Parámetros clave en `scene.html`: `R`, `T` (disco Ø80 × 5 mm), `LOBE_*`/`HOLE_*`
(pestaña y agujero), `BAND_W`/`BAND_T` (faja), `TAB_ANGLE` (−45° = pestaña entre el
brazo superior y el derecho de la cruz). La cámara se pasa por query (`elev`, `dist`, `fov`).
