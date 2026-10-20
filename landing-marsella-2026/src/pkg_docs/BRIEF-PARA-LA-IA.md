BRIEF · Instalar la landing «Regalos corporativos Navidad 2026 · Acabado Marsella» en thegravitywave.com, con SEO en español e inglés

CONTEXTO
Gravity Wave (Calpe, Alicante) retira redes de pesca del Mediterráneo y las convierte en Gravitec®, su material reciclado. Para la Navidad 2026 vende regalos corporativos personalizados con el logo del cliente, todos en el nuevo acabado Marsella (base blanca arena con motas verdes). Te adjunto el zip navidad-2026-web.zip con la landing ya diseñada y probada. Tu trabajo es instalarla en nuestra web, thegravitywave.com, en español y en inglés, con el SEO bien hecho. No hay que rediseñar nada: hay que integrar lo que viene en el paquete y traducirlo.

LO QUE HAY EN EL ZIP
- navidad-2026.html: la página completa, autónoma, para previsualizar o publicar tal cual.
- fragmento-navidad-2026.html: SOLO la sección de contenido (<section id="gw-navidad-2026">), para pegar dentro de la plantilla de la web.
- css/navidad-2026.css: estilos, todos acotados bajo #gw-navidad-2026 para no interferir con la web.
- js/navidad-2026.js: interacciones en JavaScript puro, sin dependencias. Los ids llevan prefijo gw- o navidad-.
- fonts/: Cera Pro Black y Regular (woff2, subconjunto; ver el punto FUENTES).
- img/: todas las imágenes con nombres descriptivos, agrupadas por uso (marca, acabado, fondos, proceso, productos/{arbol, estrellas, bolas, portamovil, posavasos}, seo). Índice en img/INDICE-IMAGENES.md.
- data/productos.json: los cinco productos en ES y EN (nombres, textos, fichas, precios por tramo, mínimos, tamaño de logo, imágenes y textos alt).
- CONTENIDO-ES-EN.md: todos los textos de la página en español con su traducción al inglés, incluidos los mensajes y plantillas del JavaScript.
- README.md: instrucciones de integración, datos de negocio, propuesta SEO y lista de QA. Léelo entero antes de empezar.

REGLAS QUE NO SE PUEDEN SALTAR
1. La web ya tiene menú y footer. NO añadas barra de navegación ni footer propios: el paquete no los trae a propósito. Usa fragmento-navidad-2026.html dentro de la plantilla del sitio.
2. No cambies precios, mínimos, fechas ni textos de producto. Si crees que algo está mal, dilo, no lo corrijas por tu cuenta.
3. No hay formulario de pedido ni envío a ningún servidor, y así debe seguir. El cliente recibe el catálogo por correo, prepara su pedido en la calculadora de la página y pega el texto generado en su respuesta a ese correo. El único contacto es info@thegravitywave.com.
4. Usa las imágenes del paquete tal cual (ya están recortadas, sin fondo y optimizadas). No las recomprimas, no les pongas fondo, no las sustituyas.
5. Respeta la identidad visual: fondo arena #D9D0C6, azul marino #0D2656, turquesa #00ACB4, cinta coral #FF5757 solo para «Edición Navidad». Nada de otros colores.
6. Nombres propios que no se traducen: Gravity Wave, Gravitec®, Marsella (nombre del acabado), Plastic Free Oceans.

TAREAS
A) Subir los archivos
- Sube css/, js/, img/ y fonts/ al servidor manteniendo la estructura interna (por ejemplo bajo /navidad-2026/). El HTML referencia img/..., y el CSS referencia ../img/... y ../fonts/...; si cambias la estructura, ajusta esas rutas.
- Si la web es WordPress: página a ancho completo, el fragmento en un bloque «HTML personalizado», CSS y JS encolados (el JS con defer). Comprueba que el editor conserva los atributos data-view, data-level, data-calc, hidden y aria-* del HTML, porque el JS depende de ellos. Si es otro CMS o HTML estático, aplica el equivalente.

B) Página en español
- URL propuesta: /regalos-corporativos-navidad/
- En el <head>: el enlace a Google Fonts (Poppins 400/500/600/700/800 y Sacramento) y css/navidad-2026.css. Si la web ya carga Poppins, asegúrate de que incluya esos pesos y añade Sacramento.
- Pega el contenido de fragmento-navidad-2026.html en la plantilla, entre el menú y el footer del sitio.
- Carga js/navidad-2026.js con defer después del HTML.
- Title: Regalos corporativos de Navidad 2026 con redes de pesca recicladas | Gravitec by Gravity Wave
- Meta description: Árbol, estrellas, bolas, portamóvil y posavasos fabricados con redes de pesca recuperadas del Mediterráneo, en el nuevo acabado Marsella y con el logo de tu empresa. Precios por volumen y tres niveles de personalización.
- Palabras clave a trabajar: regalos corporativos navidad, regalos de empresa navidad sostenibles, regalos corporativos personalizados, merchandising sostenible, regalos de empresa reciclados, redes de pesca recicladas, regalos corporativos con logo.

C) Página en inglés
- URL propuesta: /en/corporate-christmas-gifts/
- Traduce el HTML del fragmento usando CONTENIDO-ES-EN.md, que tiene cada texto en ES con su EN, sección por sección. Cambia lang="es" por lang="en" en la sección.
- Traduce también las cadenas del JS (constantes LEVELS y LNAME, textos de renderAll, botones Añadir/Quitar, mensajes de say() y las dos plantillas del correo). Las traducciones están en el punto 13 y en el bloque de «Texto generado» de CONTENIDO-ES-EN.md. Guárdalo como un segundo archivo (por ejemplo js/navidad-2026-en.js) para no mezclar idiomas.
- Textos alt en inglés: en data/productos.json, campo alt_en de cada vista, y en CONTENIDO-ES-EN.md.
- Formato de precios en inglés: €18.20 en lugar de 18,20 €, y separador de miles con coma (1,360.00). Los importes son los mismos.
- Title: Corporate Christmas Gifts 2026 Made from Recycled Fishing Nets | Gravitec by Gravity Wave
- Meta description: Christmas tree, stars, baubles, phone stand and coasters made from fishing nets recovered from the Mediterranean, in the new Marsella finish and with your company logo. Volume pricing and three levels of customisation.
- Keywords: corporate Christmas gifts, sustainable corporate gifts, branded Christmas gifts, eco-friendly company gifts, recycled ocean plastic gifts, recycled fishing nets, custom logo gifts.
- H1: This Christmas, give a piece of the sea.

D) SEO técnico en las dos páginas
- Un solo H1 (el del hero), H2 por sección, H3 por producto (ya viene así en el HTML).
- canonical en cada idioma y hreflang cruzado (es, en y x-default apuntando a la española). Ejemplo en el README, apartado 6.
- Open Graph y Twitter card con la imagen img/seo/og-navidad-2026.jpg (1200×630) y el title/description de cada idioma.
- Datos estructurados opcionales: un ItemList con los cinco productos como Product (nombre, imagen principal, descripción, marca «Gravitec by Gravity Wave», material). Si añades Offer: priceCurrency EUR, precio «desde» del tramo más alto, valueAddedTaxIncluded false y eligibleQuantity con el pedido mínimo. Todos los valores están en data/productos.json.
- Añade las dos URLs al sitemap y enlázalas desde donde corresponda en la web (menú, blog o página de regalos corporativos).

E) FUENTES (importante para el inglés)
Los archivos de fonts/ son subconjuntos de Cera Pro sacados del catálogo PDF: solo tienen las letras que aparecían en él (lista en fonts/CeraPro-Black.chars.txt y fonts/CeraPro-Regular.chars.txt). Los titulares en español están escritos con esas letras. A Cera Black le faltan, entre otras, J K M R S W X Y f j w x y, así que los titulares en inglés mostrarían huecos. Haz una de estas dos cosas, por este orden de preferencia:
1. Pídenos los archivos completos de Cera Pro Black y Regular y sustituye los de fonts/.
2. Si no los tienes, en la página en inglés añade al CSS: #gw-navidad-2026 .cera,#gw-navidad-2026 .cera-r{font-family:var(--font-body)} y #gw-navidad-2026 .cera{font-weight:800}, para que los titulares vayan en Poppins.

F) Comprobación final (hazla en las dos páginas y dime el resultado)
- La sección se ve sobre fondo arena, con el hero (estrellas con «Tu logo aquí») y el selector de cinco productos en este orden: Árboles, Estrellas, Bolas, Portamóviles, Posavasos.
- En cada ficha, al pulsar un nivel cambia la imagen grande y el precio. En Portamóviles la ficha abre con el render 3D sin logos.
- «Ver toda la tabla de precios» abre y cierra la tabla.
- «Añadir a mi pedido» salta al bloque de pedido con el producto añadido.
- En «Calcula tu pedido»: añadir dos productos, cambiar unidades y nivel, ver el total y que el texto del correo se actualiza. «Copiar el texto» copia (en HTTPS) o selecciona el texto.
- «Copiar» junto al correo copia info@thegravitywave.com.
- Móvil (unos 400 px de ancho): sin desplazamiento horizontal; las cintas «Edición Navidad» recortadas en la esquina; las tablas se desplazan dentro de su caja.
- Sin errores en consola. Cargan Cera Pro, Poppins y Sacramento. Ninguna imagen rota. La OG image responde en su URL pública.

DATOS DE NEGOCIO QUE DEBE CONSERVAR LA PÁGINA
- Productos: Árboles de Navidad (1 árbol de 2 piezas encajables, 250×150×10 mm, 500 g) · Estrellas de Navidad pack 2 (110×105×10 mm, 150 g) · Bola de Navidad pack 2 (110×90×10 mm, 120 g) · Portamóviles (130×80×18 mm, 300 g) · Posavasos pack 4 (90×90×20 mm, 240 g). Edición Navidad: árbol, estrellas y bolas.
- Tres niveles de personalización: Estándar · Packaging personalizado (logo en tinta negra sobre el kraft) · Packaging + producto personalizado (además, logo en UVI blanco sobre la pieza).
- Pedido mínimo: 80 packs (estrellas, bolas, posavasos), 80 uds (árbol), 150 uds (portamóvil). Hasta 1.000 online; más, con presupuesto.
- Precios por tramo, sin IVA ni gastos de envío. Tabla completa en data/productos.json y en las tablas HTML de cada ficha.
- Tamaño máximo del logo en la pieza: posavasos 40×40 mm; el resto 30×30 mm.
- Requisitos del logo para UVI: vectorizado (svg/ai o png sin fondo, mínimo 300 px / 80 mm), monocolor (negro packaging, blanco pieza), sin textos ni piezas menores de 1 mm, elementos separados, diseños simples porque la colocación es manual.
- Fecha límite de pedidos de Navidad: 6 de noviembre de 2026.
- Contacto: info@thegravitywave.com · Gravity Wave, Calpe (Alicante) · thegravitywave.com.
- Los precios están en dos sitios que deben coincidir: la constante PRODUCTS al principio del JS (la usa la calculadora) y las tablas HTML de cada ficha. Si alguna vez cambian, hay que actualizar ambos y data/productos.json.

QUÉ ME TIENES QUE ENTREGAR
1. Las dos URLs publicadas (ES y EN) o, si no puedes publicar, los archivos listos para subir con la misma estructura del paquete.
2. Lista de lo que has cambiado respecto al paquete (rutas, ids, CSS añadido, fuentes) y cualquier duda o dato que creas incorrecto.
3. El resultado de la comprobación final del punto F en cada idioma, con capturas de escritorio y móvil.
4. Las etiquetas SEO finales de cada página (title, description, canonical, hreflang, OG) y el JSON-LD si lo has puesto.
