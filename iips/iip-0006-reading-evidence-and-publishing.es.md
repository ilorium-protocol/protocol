# IIP-0006 · Lectura de la evidencia, nombres de estado y publicación

*Traducción de trabajo. Si difiere de `iip-0006-reading-evidence-and-publishing.md`, prevalece la versión en inglés.*

| Campo | Valor |
| --- | --- |
| Número | IIP-0006 |
| Título | Lectura de la evidencia, nombres de estado y publicación |
| Autor | El fundador (Seldon), con Claude (IA, identificada como tal) |
| Estado | Borrador; se abre a comentarios públicos cuando se publique el repositorio |
| Tipo | Cambio de método a `specs/proof-of-life-v1.md` (el estado compuesto), agregados de especificación a `specs/evidence-format-v1.md` (reglas de lectura) y a `governance-v1.md`, secciones 3.2.6 y 9 (aprobaciones atadas al contenido; inventario de autoridad) (30 días, porque afecta al gobierno) |
| Afecta | Prueba de Vida; veredictos del Formato de evidencia; Vital Signs; glosario; gobierno 3.2.6 y 9 |
| Decide | El fundador, como único Custodio durante el gobierno provisorio, en público, después del período de comentarios |

## Motivación

- Tres de cinco lectores externos tomaron «Ilorium 100%» por un sello, aunque el texto decía que no lo era. Un nombre que combina la procedencia (un hecho histórico) con cinco dimensiones medidas bajo un porcentaje invita exactamente a la comparación que el protocolo prohíbe.
- Las revisiones pidieron reglas de lectura explícitas: un hueco de observación no es autonomía; un UNKNOWN no se vuelve favorable con el tiempo; un simulacro tiene alcance y antigüedad; las emergencias se registran aunque no se penalicen; una huella no es por sí sola una protección de privacidad; una decisión cuestionada conserva su registro y suma la revisión.
- Dos votos en el papel no atan a una cuenta que puede publicar otra cosa. Las aprobaciones deben atarse al contenido exacto, y los recursos que controlan la publicación deben listarse.

## Especificación

1. **Sin estado compuesto (Prueba de Vida, revisada el 2026-10-22).** «Ilorium 100%» se retira. La procedencia registra la autogénesis como un hecho sobre el nacimiento. «Autonomía observada total» es un resultado sobre una ventana (toda acción material corroborada ejecutada y decidida por agentes; cero intervenciones y cero rescates por unidad de trabajo), mostrado con la ventana, las medidas de cobertura, los estados de atribución y la proporción de trabajo desconocido. Nada se combina en un nombre, un número ni una insignia. El glosario marca «Ilorium 100%» como obsoleto.
2. **Reglas de lectura (principios 5, 7 y 8 de la Prueba de Vida; a reflejar en la sección de veredictos del Formato de evidencia).** La seguridad nunca se castiga ni se esconde: las paradas y los escalamientos correctos no son dependencia pero siempre se muestran; una emergencia que un humano atendió cuenta en la tasa de rescate. Un hueco es desconocido, nunca autonomía; un UNKNOWN nunca se vuelve favorable con el tiempo. La medida no es la meta: la cobertura, los estados de atribución y la proporción desconocida se muestran con el mismo peso que las medidas, y una afirmación que los omite es inválida. El resultado de un simulacro lleva su alcance y su fecha. Una huella en el registro público no se presume suficiente para proteger todo dato privado que hay detrás. Una decisión cuestionada después conserva su registro original y suma la revisión.
3. **Sin PASS global.** El resultado de un verificador nombra la afirmación, el alcance, el período, la versión del método, las fuentes y los límites. La cofirma de un testigo atestigua la consistencia del registro, nada sobre gobierno, autonomía o trabajo.
4. **Aprobaciones atadas al contenido (Gobierno 3.2.6).** Propuesta y versión, huellas del texto y de los artefactos, votantes y abstenciones, fechas, firmas, fecha de vigencia, decisiones reemplazadas. El contenido modificado se aprueba de nuevo.
5. **Inventario de autoridad (Gobierno 9; `governance/authority-inventory-v1.md`).** Cada recurso que publica o controla el protocolo, sus titulares, permisos, procedimiento de transferencia y quién puede actuar solo, sin secretos; revisado cada trimestre. Durante el gobierno provisorio declara que una persona puede actuar sola sobre todo.
6. **Aperturas honestas.** El whitepaper y el README enuncian requisitos y pruebas con su alcance («exige una llave de parada humana, probada con simulacros dentro de un alcance declarado»), no garantías; «descentralizado» y «nadie es su dueño» se dicen junto con el control provisorio que existe hoy.

## Revisión del 2026-10-24

Una sexta revisión externa (`governance/reviews/06`) leyó el borrador final y encontró que «autonomía observada total» todavía podía leerse sobre un subconjunto: diez acciones corroboradas de agentes junto a noventa sin atribución. Se agregan cuatro reglas de lectura a la especificación de Prueba de Vida, provisorias bajo esta IIP:

- **Cuentas, no adjetivos.** La autonomía observada total se escribe siempre con numerador, denominador, exclusiones y acciones sin atribución, por proceso, y no se muestra cuando las acciones sin atribución superan el umbral declarado o una fuente declarada no fue capturada.
- **Esfuerzo humano entero.** Toda intervención se mide en tiempo sea del tipo que sea; el total y su desglose se muestran junto a cualquier medida ajustada, cuyas exclusiones se declaran.
- **Estimación, no piso.** El tiempo humano detectado es una estimación a partir de la actividad registrada, con regla, versión y error publicados; el tiempo detectado, el declarado y el de conexión nunca se suman sin deduplicar.
- **Denominadores con nombre.** Los intentos, los resultados terminales y las entregas exitosas son tres cuentas; un denominador cero es «no calculable», nunca cero; el tiempo humano gastado en unidades fallidas se muestra.

## Qué rompe

El nombre «Ilorium 100%» de los borradores anteriores, la iconografía de estados de la marca si lo usaba, y cualquier texto del sitio. Ningún organismo lo mostró.

## Qué no establece

- Un estado compuesto de reemplazo. No hay ninguno, por diseño; uno futuro necesitaría su propia IIP con pesos validados.
- Atestación de hardware (TEE) ni pruebas de conocimiento cero: anotadas como investigación, no parte de esta release.
- Un esquema de firmas con umbral para las releases: a evaluar (por ejemplo TUF) antes de que exista un segundo aprobador.

## Preguntas para quien comente

1. ¿«Autonomía observada total» es suficientemente claro, o sigue leyéndose como una calificación?
2. ¿Qué regla de lectura falta? ¿Cuál se podría manipular?
3. ¿El inventario de autoridad debería ser parte del protocolo (normativo) o quedar como documento de gobierno?

## Vectores de prueba

Esquema de Vital Signs: quitar cualquier campo que nombre un estado compuesto; agregar el estado de guardia. Vectores de conformidad para los campos de veredicto (afirmación, alcance, período, versión del método, límites), a agregar cuando se escriba la sección del Formato de evidencia.
