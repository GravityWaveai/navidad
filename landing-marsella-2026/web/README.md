# Regalos corporativos Navidad 2026 · Acabado Marsella — paquete para integrar en la web

Catálogo-landing de la campaña de Navidad 2026 de **Gravitec® by Gravity Wave** (regalos corporativos fabricados con redes de pesca recuperadas del Mediterráneo, todos en el nuevo acabado **Marsella**). Este paquete está preparado para que otra persona o IA lo instale dentro de **thegravitywave.com** con SEO en español e inglés.

**La web ya tiene menú y footer: este paquete no los incluye.** Es solo el contenido de la página, con su CSS y su JS, pensado para vivir dentro de la plantilla del sitio.

---

## 1. Contenido del paquete

```
navidad-2026-web/
├── navidad-2026.html            Página completa y autónoma (para previsualizar en local o publicar tal cual)
├── fragmento-navidad-2026.html  SOLO la <section> de contenido, para pegar dentro de la plantilla de la web
├── css/navidad-2026.css         Estilos. Todo acotado bajo #gw-navidad-2026
├── js/navidad-2026.js           Interacciones. JavaScript puro, sin dependencias
├── fonts/                       Cera Pro Black y Regular (woff2, SUBCONJUNTO, ver §5) + lista de glifos disponibles
├── img/                         Todas las imágenes, con nombres descriptivos y agrupadas por uso (índice en img/INDICE-IMAGENES.md)
│   ├── marca/                   Logos Gravitec by Gravity Wave (azul y blanco)
│   ├── acabado/                 Muestra del acabado Marsella
│   ├── fondos/                  Fotos de fondo (barco, red de pesca)
│   ├── proceso/                 Redes recuperadas, granza
│   ├── productos/{arbol,estrellas,bolas,portamovil,posavasos}/   Pieza con «Tu logo aquí» + los 3 niveles de packaging
│   └── seo/og-navidad-2026.jpg  Imagen Open Graph 1200×630
├── data/productos.json          Datos de los 5 productos en ES y EN: nombres, textos, fichas, precios por tramo, mínimos, imágenes y alt
├── CONTENIDO-ES-EN.md           Todos los textos de la página en español con su traducción al inglés
└── README.md                    Este documento
```

Rutas relativas: el HTML referencia `img/...`; el CSS referencia `../img/...` y `../fonts/...`. Si se cambia la estructura de carpetas, hay que ajustar esas rutas (búsqueda y sustitución).

---

## 2. Cómo integrarlo en la web

1. **Subir** las carpetas `css/`, `js/`, `img/` y `fonts/` al servidor (por ejemplo a `/navidad-2026/`), manteniendo la estructura interna.
2. **En el `<head>`** de la página:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Sacramento&display=swap">
   <link rel="stylesheet" href="/navidad-2026/css/navidad-2026.css">
   ```
   Si la web ya carga Poppins desde Google Fonts, basta con asegurarse de que incluya los pesos 400, 500, 600, 700 y 800 y añadir Sacramento.
3. **Pegar el contenido de `fragmento-navidad-2026.html`** donde deba ir la página (entre el menú y el footer de la plantilla). Es una única `<section id="gw-navidad-2026">`.
4. **Cargar el JS** después del HTML: `<script src="/navidad-2026/js/navidad-2026.js" defer></script>`.
5. Comprobar con la lista de QA del §8.

En WordPress funciona pegando el fragmento en un bloque «HTML personalizado» de una página a ancho completo y encolando el CSS y el JS (`wp_enqueue_style` / `wp_enqueue_script` con `defer`). Algunos editores reescriben el HTML pegado: comprobar que conservan los atributos `data-view`, `data-level`, `data-calc`, `hidden` y `aria-*`, porque el JS depende de ellos.

### Aislamiento respecto a la web anfitriona
- **Todo el CSS está acotado** bajo `#gw-navidad-2026`. El contenedor define su propio fondo (arena `#D9D0C6`), tipografía y colores, así que no depende de los estilos del sitio ni los pisa.
- **Los ids están prefijados** (`gw-…` para los elementos funcionales, `navidad-…` para las anclas de sección) para no chocar con los del sitio.
- El JS es una función autoejecutada: no deja variables globales ni usa librerías.
- No se incluye `html{scroll-behavior:smooth}`; si se quiere desplazamiento suave en las anclas, añadirlo en el CSS global del sitio.
- Enlaces internos de la página (todos son anclas dentro de la misma sección): `#navidad-elige-producto`, `#navidad-por-que`, `#navidad-proceso`, `#navidad-acabado-marsella`, `#navidad-productos`, `#gw-prod-arbol`, `#gw-prod-estrellas`, `#gw-prod-bolas`, `#gw-prod-portamovil`, `#gw-prod-posavasos`, `#navidad-personalizacion`, `#navidad-calcula-tu-pedido`, `#navidad-respuesta-correo`, `#navidad-cierre-pedidos`. Si la web quiere enlazar a ellas desde el menú, usar esas anclas.

---

## 3. Qué hace el JavaScript

- **Selector de nivel por producto** (Estándar / Packaging personalizado / Packaging + producto): cambia la imagen grande de la ficha y muestra el precio por unidad del tramo, el total para las unidades indicadas y la diferencia frente a estándar. Botón «Ver la foto real de la pieza» para alternar con la pieza suelta (en Portamóviles la ficha abre con el render 3D sin logos).
- **Campo de unidades** por producto, con mínimo (MOQ) y máximo 1.000 (más, con presupuesto).
- **«Ver toda la tabla de precios»**: despliega y oculta la tabla completa de cada producto (va oculta por defecto).
- **«Calcula tu pedido»**: el cliente añade varios productos, cada uno con su nivel y sus unidades; se calculan los totales y se genera un **texto editable para pegar en la respuesta al correo** (botón «Copiar el texto», con `navigator.clipboard` y selección como respaldo). No hay formulario ni envío a ningún servidor: el catálogo se manda por correo y el cliente responde a ese correo.
- Botones «Añadir a mi pedido» de cada ficha: llevan al bloque de pedido con ese producto ya añadido, con el nivel y las unidades elegidos en la ficha.
- Botón «Copiar» del correo de contacto.

**Los precios viven en dos sitios** (son los mismos datos): en la constante `PRODUCTS` al principio de `js/navidad-2026.js` (la usa la calculadora) y en las tablas HTML de cada ficha. Si cambian tarifas, mínimos o nombres hay que actualizar ambos, además de `data/productos.json`.

---

## 4. Datos de negocio que debe conservar la página

| Dato | Valor |
|---|---|
| Productos (orden en la página) | Árboles de Navidad · Estrellas de Navidad (pack 2) · Bola de Navidad (pack 2) · Portamóviles · Posavasos (pack 4) |
| Edición Navidad (cinta coral) | Árbol, estrellas y bolas |
| Acabado | Marsella (toda la colección). Material: Gravitec®, redes de pesca recuperadas del Mediterráneo |
| Niveles de personalización | 1 Estándar · 2 Packaging personalizado (tinta negra en kraft) · 3 Packaging + producto personalizado (además, logo en UVI blanco sobre la pieza) |
| Tamaño máximo del logo en la pieza | Posavasos 40 × 40 mm · Portamóvil, estrella, árbol y bola 30 × 30 mm |
| Pedido mínimo | Posavasos 80 packs · Portamóvil 150 uds · Estrellas 80 packs · Árbol 80 uds · Bolas 80 packs |
| Precios | Por tramo (80-200 / 201-500 / 501-1000; portamóvil 150-200 / 201-500 / 501-1000), **sin IVA ni gastos de envío**. Tabla completa en `data/productos.json` |
| Fecha límite de pedidos de Navidad | **6 de noviembre de 2026** |
| Contacto | info@thegravitywave.com · Gravity Wave, Calpe (Alicante) · thegravitywave.com |
| Flujo de pedido | Sin formulario: el cliente responde al correo con el que recibió el catálogo, pegando el texto que genera la calculadora y adjuntando su logo en vectorial |
| Requisitos del logo para UVI | Vectorizado (svg/ai o png sin fondo, mín. 300 px / 80 mm), monocolor (negro packaging, blanco pieza), sin textos ni piezas < 1 mm, elementos separados (la impresión añade 0,05 mm de contorno), diseños simples (colocación manual) |

---

## 5. Tipografías (importante para la versión en inglés)

- **Poppins** (texto, botones, tablas) y **Sacramento** (rótulos manuscritos «Recolectamos / Reciclamos / Transformamos») se cargan desde Google Fonts.
- **Cera Pro Black** (titulares, cifras) y **Cera Pro Regular** (subtítulos) son la tipografía de marca de Gravity Wave. Los archivos de `fonts/` son **subconjuntos extraídos del catálogo PDF**: solo contienen los glifos que aparecían en él (la lista exacta está en `fonts/CeraPro-Black.chars.txt` y `fonts/CeraPro-Regular.chars.txt`). Los titulares en español de esta página están escritos con esos glifos.
- **Consecuencia para el inglés:** a Cera Black le faltan, entre otras, las letras J K M R S W X Y f j w x y. Cualquier titular nuevo con esas letras mostrará huecos rellenados con Poppins (se ve feo). Opciones, de mejor a peor:
  1. Pedir al equipo de marca los archivos completos de Cera Pro Black y Regular (licencia TypeMates) y sustituir los de `fonts/`.
  2. Para la versión en inglés, usar Poppins 800 en los titulares: añadir en el CSS de la página EN `#gw-navidad-2026 .cera,#gw-navidad-2026 .cera-r{font-family:var(--font-body)}` (y `font-weight:800` para `.cera`).
  3. Elegir titulares en inglés que solo usen los glifos disponibles (poco práctico).

---

## 6. SEO

### Estructura ya presente en el HTML
- Un único `<h1>` (hero): «Esta Navidad, regala un pedacito de mar.»
- `<h2>` por sección y `<h3>` por producto. Los nombres de producto están en los `<h3>` y en las tarjetas del selector.
- Todas las imágenes de producto llevan `alt` descriptivo en español (los `alt` en inglés están en `data/productos.json`, campo `alt_en`). Las imágenes decorativas (fila de piezas, miniaturas de nivel, cinta) llevan `alt=""` o `aria-hidden`.
- Imágenes en WebP (productos) y JPG (fondos), con `loading="lazy"`; la pieza del hero lleva `fetchpriority="high"`.
- La sección lleva `lang="es"`. En la versión en inglés cambiar a `lang="en"`.

### Propuesta para la página en español
- URL: `/regalos-corporativos-navidad/` (o `/navidad-2026/`)
- Title: `Regalos corporativos de Navidad 2026 con redes de pesca recicladas | Gravitec by Gravity Wave`
- Meta description: `Árbol, estrellas, bolas, portamóvil y posavasos fabricados con redes de pesca recuperadas del Mediterráneo, en el nuevo acabado Marsella y con el logo de tu empresa. Precios por volumen y tres niveles de personalización.`
- Palabras clave: regalos corporativos navidad, regalos de empresa navidad sostenibles, regalos corporativos personalizados, merchandising sostenible, regalos de empresa reciclados, plástico reciclado del mar, redes de pesca recicladas, regalos corporativos con logo, Gravitec, Gravity Wave.

### Propuesta para la página en inglés
- URL: `/en/corporate-christmas-gifts/`
- Title: `Corporate Christmas Gifts 2026 Made from Recycled Fishing Nets | Gravitec by Gravity Wave`
- Meta description: `Christmas tree, stars, baubles, phone stand and coasters made from fishing nets recovered from the Mediterranean, in the new Marsella finish and with your company logo. Volume pricing and three levels of customisation.`
- Keywords: corporate Christmas gifts, sustainable corporate gifts, branded Christmas gifts, eco-friendly company gifts, recycled ocean plastic gifts, recycled fishing nets, custom logo gifts, Gravitec, Gravity Wave.
- H1 sugerido: «This Christmas, give a piece of the sea.» (ver §5 sobre la tipografía). Todos los textos traducidos están en `CONTENIDO-ES-EN.md`.

### Etiquetas comunes
```html
<link rel="canonical" href="https://thegravitywave.com/regalos-corporativos-navidad/">
<link rel="alternate" hreflang="es" href="https://thegravitywave.com/regalos-corporativos-navidad/">
<link rel="alternate" hreflang="en" href="https://thegravitywave.com/en/corporate-christmas-gifts/">
<link rel="alternate" hreflang="x-default" href="https://thegravitywave.com/regalos-corporativos-navidad/">
<meta property="og:type" content="website">
<meta property="og:title" content="…título…">
<meta property="og:description" content="…descripción…">
<meta property="og:image" content="https://thegravitywave.com/navidad-2026/img/seo/og-navidad-2026.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

### Datos estructurados (opcional)
Un `ItemList` con los cinco productos como `Product` (nombre, imagen principal, descripción, marca «Gravitec by Gravity Wave», material «Gravitec®, redes de pesca recicladas»). Si se añaden `Offer`, indicar `priceCurrency: EUR`, el precio «desde» del tramo más alto, `valueAddedTaxIncluded: false` y `eligibleQuantity` con el pedido mínimo, para no anunciar precios unitarios de consumo. Todos los valores están en `data/productos.json`.

---

## 7. Textos y traducción

`CONTENIDO-ES-EN.md` contiene todos los textos de la página en español con su traducción al inglés, sección por sección, incluidos los textos que genera el JavaScript (etiquetas, mensajes y el texto de la respuesta al correo). Para la versión en inglés hay que traducir el HTML con esa referencia **y también** las cadenas del JS (constantes `LEVELS`, `LNAME`, los textos de `renderAll`, los botones «Añadir/Quitar», los mensajes de `say()` y las plantillas del correo).

Nombres propios que no se traducen: Gravity Wave, Gravitec®, Marsella (nombre del acabado), Plastic Free Oceans.

---

## 8. QA después de instalar

- [ ] La sección se ve sobre fondo arena, con el hero (estrellas con «Tu logo aquí») y el selector de cinco productos.
- [ ] En cada ficha, al pulsar un nivel cambia la imagen grande y el precio. En Portamóviles la ficha abre con el 3D sin logos.
- [ ] «Ver toda la tabla de precios» abre y cierra la tabla.
- [ ] «Añadir a mi pedido» salta al bloque de pedido con el producto añadido.
- [ ] En «Calcula tu pedido»: añadir dos productos, cambiar unidades y nivel, ver el total y que el texto del correo se actualiza. «Copiar el texto» copia (en HTTPS) o selecciona el texto.
- [ ] «Copiar» junto al correo copia `info@thegravitywave.com`.
- [ ] Móvil (≈400 px): sin desplazamiento horizontal; las cintas «Edición Navidad» quedan recortadas en la esquina; las tablas se desplazan dentro de su caja.
- [ ] No hay errores en la consola. Las fuentes Cera Pro y Poppins cargan (comprobar en la pestaña Network).
- [ ] Las imágenes cargan desde `img/` (ninguna ruta rota) y la OG image responde en su URL pública.

---

## 9. Origen

Fuentes, generadores y fotos originales en el repositorio de GitHub `GravityWaveai/navidad`, carpeta `landing-marsella-2026` (rama `claude/sweet-ritchie-qenrh3`). Las fotos originales de producto (PNG a alta resolución, 2000 px) están en `landing-marsella-2026/src/fotos-producto/` por si hacen falta recortes nuevos.
