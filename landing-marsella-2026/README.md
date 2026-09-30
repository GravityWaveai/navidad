# Landing · Regalos corporativos Navidad 2026 · Acabado Marsella

Landing en HTML autocontenida (imágenes y fuentes incrustadas) construida a partir del catálogo
`Marsella 2026 - Catálogo Regalos Corporativos`. Toda la colección aparece en acabado **Marsella**.

- `index.html` — la landing lista para publicar en cualquier hosting (un solo archivo, ~2,2 MB).
  Necesita internet solo para Poppins y Sacramento (Google Fonts); Cera Pro va incrustada.
- `src/page.html` — plantilla (textos, CSS y JS). Los bloques de producto y la calculadora se generan desde `src/build_html.py`.
- `src/build_html.py` — datos de los 5 productos (fichas, precios por tramo, MOQ, tamaño de logo) y generador.
  Para cambiar precios o textos de producto, edita `PRODUCTS` y ejecuta `python3 src/build_html.py .`
  (escribe `index.html` y `artifact.html`). El script comprueba que los titulares en Cera Pro solo usen
  glifos disponibles en el subconjunto incrustado (el que venía en el PDF).
- `src/assets/` — fotos del catálogo: las reales en Marsella tal cual, y las verdes recoloreadas a Marsella
  con `src/tools/` (máscara del material + moteado sintético calibrado con las fotos reales).
- Enlace de pedido: el formulario Typeform del catálogo (`ORDER_URL` en `build_html.py`).
- Fecha límite de pedidos de Navidad que figura en la landing: 6 de noviembre (la del catálogo).
