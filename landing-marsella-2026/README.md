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
- `src/fotos-producto/` — las fotos de producto generadas (estrellas, árbol, bolas, portamóvil) y sus prompts (`PROMPTS.md`).
  Son la fuente de las piezas del hero, el selector y las fichas. Las variantes «estándar» (sin «TU LOGO AQUÍ» en el kraft)
  y la faja personalizada del árbol se derivan de ellas por retoque.
- `src/assets/` — imágenes ya recortadas para la landing. Los posavasos y la escena final siguen siendo fotos del catálogo
  con el material pasado a Marsella con `src/tools/` (textura real de la muestra).
- Sin formulario: la landing se envía por correo como catálogo. El bloque «Calcula tu pedido» deja añadir varios
  productos con nivel y unidades y genera un texto para pegar en la respuesta al correo (botón «Copiar el texto»).
- Fecha límite de pedidos de Navidad que figura en la landing: 6 de noviembre (la del catálogo).

## Restricciones de impresión UVI (formación Merch Navidad)
`docs-formacion-merch-navidad-uvi.pdf` recoge lo que hay que validar en cada logo antes de producir: siempre
vectorizado (svg/ai o png sin fondo, mín. 300 px / 80 mm), monocolor (negro packaging, blanco pieza), sin
degradados ni fondos, sin textos ni piezas < 1 mm, elementos con separación suficiente (la UVI añade un contorno
de 0,05 mm) y diseños simples porque la colocación es manual. Si el logo no es apto, pedir al cliente una versión
simplificada. Estos puntos aparecen resumidos en la sección Personalización de la landing.
