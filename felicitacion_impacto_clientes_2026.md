# Felicitación de Navidad 2026 con el impacto de cada cliente

Un correo de Navidad a las empresas cliente en el que lo primero que leen es su propia cifra: los kilos de residuos plásticos que han retirado del Mediterráneo junto a Gravity Wave. No vende nada. Felicita, devuelve el dato y deja la puerta abierta para 2027.

- **A quién:** clientes fríos, de este año y de años anteriores.
- **Para qué:** negocio nuevo. Todo lo que salga de estos correos cuenta como tal, así que tiene que poder medirse.
- **Quién queda fuera:** los clientes que tienen panel propio lo ven en una reunión, no por este correo. Los clientes más importantes reciben además producto de Navidad.

Este correo es distinto de los de `correos_navidad_2026.md`: aquellos ofrecían el catálogo de regalos; este no ofrece nada.

## Datos que hacen falta por cliente

| Variable | Qué es | De dónde sale |
|---|---|---|
| `[NOMBRE]` | Persona de contacto | CRM |
| `[EMPRESA]` | Nombre de la empresa | CRM |
| `[KG]` | Kilos retirados con Gravity Wave | Reparto de kilos por cliente (existe desde septiembre de 2025). Para lo anterior, el informe o certificado que se entregó en su día: **por confirmar con Operaciones** |
| `[DESDE]` | Año en que empezaron | CRM |
| `[PUERTOS]` | Puertos o zonas de recogida, dos o tres como mucho | Informe de impacto del cliente |
| `[ENLACE_INFORME]` | Su informe de impacto | Por decidir (ver «Por decidir») |

**Regla:** si no hay una cifra fiable para un cliente, se le manda la versión C. No se estima, no se redondea hacia arriba y no se reparte «a ojo» el total entre clientes.

## Los correos

### A. Cliente con cifra trazada (reparto desde septiembre de 2025)

**Asunto:** [EMPRESA]: [KG] kg menos de plástico en el Mediterráneo

> Hola [NOMBRE]:
>
> Antes de cerrar el año queríamos daros un dato que es vuestro: desde [DESDE], [EMPRESA] ha retirado junto a Gravity Wave **[KG] kg de residuos plásticos del Mediterráneo y sus puertos**.
>
> Salieron de [PUERTOS], con los pescadores que trabajan con nosotros, y cada recogida está registrada con su fecha, su pesaje y sus fotos.
>
> Os dejamos el informe por si os apetece contarlo estas fiestas, dentro o fuera de casa:
>
> **[ Ver el impacto de [EMPRESA] ]** → `[ENLACE_INFORME]`
>
> Gracias por formar parte de esto. Si en 2027 queréis volver al agua con nosotros, respondedme a este correo y lo vemos en enero.
>
> Feliz Navidad,
> [FIRMA]

### B. Cliente de años anteriores, con la cifra de su proyecto

**Asunto:** Lo que [EMPRESA] dejó hecho en el Mediterráneo

> Hola [NOMBRE]:
>
> Hace tiempo que no hablamos y la Navidad es buena excusa para escribiros.
>
> En [DESDE], [EMPRESA] retiró junto a Gravity Wave **[KG] kg de residuos plásticos del Mediterráneo y sus puertos**. Ese dato sigue siendo vuestro y aquí lo seguimos contando.
>
> Desde entonces hemos seguido sacando redes del mar con los pescadores, y hoy cada recogida se puede seguir con su puerto, su fecha y su pesaje.
>
> Si os apetece retomarlo en 2027, respondedme y os cuento en diez minutos en qué andamos.
>
> Feliz Navidad,
> [FIRMA]

### C. Cliente sin cifra fiable

**Asunto:** Feliz Navidad desde el Mediterráneo

> Hola [NOMBRE]:
>
> Antes de cerrar el año queríamos daros las gracias. [EMPRESA] es una de las empresas que han hecho posible que hoy haya **[KG_TOTALES_GW] kg menos de residuos plásticos en el Mediterráneo y sus puertos**.
>
> Seguimos en ello, con los pescadores y puerto a puerto. Si en 2027 os apetece volver a formar parte, respondedme a este correo y lo vemos en enero.
>
> Feliz Navidad,
> [FIRMA]

`[KG_TOTALES_GW]`: la guía de mensajes de 2025 da +998.172 kg. Hay que confirmar con Operaciones la cifra a cierre de 2026 antes de enviar.

## Cómo se escribe la cifra

Según la guía de mensajes antigreenwashing:

- Sí: «retirar / recuperar [KG] kg de residuos plásticos del Mediterráneo y sus puertos», «junto a Gravity Wave», «redes de pesca descartadas».
- No: «limpiamos los océanos», «habéis eliminado el plástico de…», «neutralizar», «100 % sostenible».
- Equivalencias (botellas, campos de fútbol…) solo si Operaciones da la oficial. No se inventan.

## Envío

1. Uno a uno, desde el buzón de la persona que lleva la cuenta, y firmado por ella. Nada de envío masivo desde `info@`: es la misma regla que en septiembre, para cuidar el dominio.
2. Máximo 10–15 correos al día por persona.
3. Sin recordatorio. Es una felicitación: si no contestan, no se insiste.
4. Propuesta de fechas: lista cerrada el 2 de diciembre, cifras el 5 y envíos del 9 al 17, antes de que la gente se vaya de vacaciones.

## Medición

- Etiqueta en el CRM a cada contacto que lo recibe: `felicitacion-navidad-2026`.
- El botón lleva `?utm_source=email&utm_medium=felicitacion&utm_campaign=navidad-2026-impacto`.
- Cuenta como negocio nuevo de esta acción toda respuesta u oportunidad que abra un contacto etiquetado. Propuesta: hasta el 31 de marzo de 2027.

## Por decidir

1. **Lista de destinatarios:** quién cuenta como cliente frío y qué clientes de años anteriores entran.
2. **Cifra de los clientes anteriores a septiembre de 2025:** de dónde sale y quién la valida (Operaciones).
3. **Adónde lleva el botón**, ahora que el panel completo se reserva para unos pocos clientes. Propuesta: al informe de impacto en PDF del cliente cuando exista; si no existe, se manda la versión B o C, que no llevan botón.
4. **Quién firma** cada correo.
