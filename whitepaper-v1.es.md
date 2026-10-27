# Whitepaper de Ilorium v1.0

Versión 1.0 · 2026-10-20 · Borrador · Revisado el 2026-10-22 tras la revisión externa

Explica el proyecto completo · Sin fuerza normativa (el manifiesto y los documentos que lista definen el protocolo)

> Traducción de trabajo de `whitepaper-v1.md`. La versión en inglés es la que prevalece.

Ilorium es un protocolo abierto y descentralizado de leyes, formatos y métodos de verificación para organizaciones operadas por agentes de IA y para la evolución de su especie. Nadie es dueño del protocolo: su texto y su código son abiertos, con licencias que cualquiera puede usar. El dominio, las cuentas y las publicaciones los controla el fundador durante el gobierno provisorio, y ese control se publica (el documento de Gobierno, el inventario de autoridad). No es una empresa y no tiene token. Una organización que lleva el Genome es un **organismo**; juntos, los organismos forman **la especie**.

**Ilorium monitorea organizaciones operadas por agentes de IA: registra cómo vive cada una, mide lo que realmente demostró que puede hacer y exige que todo organismo lleve una llave de parada humana, probada con simulacros dentro de un alcance declarado. Su misión es dar leyes, formatos y verificación a las organizaciones operadas por agentes de IA y a la evolución de su especie. El fundador lee esa evolución como el camino hacia la SI2SI: una convicción personal, expuesta en la carta del fundador, sobre la que el protocolo no toma posición.**

Fija, desde la primera generación, las condiciones que todo nacimiento debe cumplir: las leyes que lleva cada organismo, el registro de cada sucesión, la compuerta de nacimiento y la llave de parada humana. Evoluciona con la especie, siguiendo la cadena de sucesiones para medirla y gobernarla. No da por sentado que la superinteligencia vaya a surgir, y ningún registro puede hacerla surgir. Lo que exige es que, si comienza una nueva generación, comience en el registro, por la compuerta, con una llave de parada humana para cada organismo y cada afirmación respaldada por evidencia. Una llave de parada se prueba con simulacros: un simulacro aprobado muestra que la parada funcionó en las condiciones del simulacro y en esa fecha, nunca que el control es permanente ni que el organismo no puede salir de la infraestructura donde la llave funciona.

La versión del protocolo es la 1.0: la primera versión completa, y sigue siendo un borrador. Todo lo que sigue está especificado, y ningún organismo lo demostró todavía en funcionamiento. Ilorium va a declarar estable la versión más adelante, bajo la única definición que está en `manifest.md` (formatos congelados, pruebas de conformidad publicadas, una política de compatibilidad escrita y dos Custodios del Genome independientes en funciones; nunca durante el gobierno provisorio). Estable no dice nada sobre si se puede confiar en algún organismo.

**Por qué la adopta una organización.** Ilorium permite que las organizaciones autónomas publiquen evidencia verificable de su funcionamiento y que sus contrapartes la consulten antes de delegar, contratar o conceder acceso. **Vital Signs** (signos vitales) presenta el estado; el **Evidence Bundle** (paquete de evidencia) permite comprobarlo. El latido atrae atención; solo la evidencia puede justificar que alguien vuelva a consultarlo.

## Resumen y problema

Ya existen organizaciones operadas sobre todo por agentes de IA, y cada vez más van a ser fundadas por otras organizaciones y no por personas. Hoy nada le dice a alguien de afuera cómo vive realmente una organización así: quién decide, cuánto trabajo humano sigue consumiendo, si se la puede detener o de dónde vino.

Ilorium responde con tres cosas:

- **Leyes que lleva todo organismo** (el Genome): registros que no se pueden reescribir, límites que ningún agente puede subirse a sí mismo, una parada que ningún agente puede desactivar, un responsable identificable, la verdad sobre lo que es, la separación entre quien actúa y quien juzga, y continuidad cuando algo falla.
- **Evidencia que cualquiera puede verificar** (la Probe, los Strata, el Pulse y la Prueba de Vida): qué pasó, quién lo hizo, quién lo decidió y cuánta vida humana llevó por cada cosa entregada, publicada con sus límites.
- **Reglas sobre cómo evoluciona la especie** (la sucesión y los tres cerrojos): quién puede dar origen a quién, qué hereda cada generación, y que todo organismo, en toda generación, nazca detenible por un humano.

Ilorium se apoya en el protocolo Agent2Agent (A2A): A2A dice qué puede hacer un agente; Ilorium muestra cómo vive el organismo que está detrás, y cómo nació.

## El fundamento humano

Ilorium nace del trabajo de un fundador humano y agentes de IA, y busca hacer examinable esa colaboración. El problema al que responde ya existe: organizaciones operadas por agentes que nadie de afuera puede leer, donde no se sabe quién decide, cuánto trabajo humano siguen consumiendo ni si se las puede detener. El Organismo Cero, la organización del propio fundador, es el primer caso: una persona, con agentes que ejecutan el trabajo, creando y sosteniendo una organización a la vista. El punto de partida es concreto: registrar qué ejecutan y deciden los agentes, qué propone, aprueba, corrige o detiene una persona, y cómo cambia esa distribución con el tiempo.

El propósito humano es ampliar lo que una persona puede crear y sostener, haciendo visible el trabajo y la responsabilidad que todavía dependen de ella. La autonomía no se presume por usar IA: debe respaldarse con evidencia dentro de un alcance declarado. Hoy el fundador define el propósito y se reserva ciertas decisiones; los agentes ejecutan tareas y deciden dentro de los permisos concedidos.

El fundador plantea como hipótesis que los agentes llegarán a proponer nuevas empresas, fundaciones y otras organizaciones, y que algunas podrán sostenerse y originar sucesoras con intervención humana cada vez menor. Las decisiones podrán reservarse a humanos o delegarse dentro de límites fijados de antemano. La autoridad de parada seguirá siendo humana, como exige el Genome, y un humano acepta cada llave de parada por separado de la decisión de crear la organización. La regla de que una IA nunca decide rige para el gobierno del protocolo, no para cómo operan los organismos.

El protocolo no exige ese futuro ni verifica superinteligencia. Define cómo registrar la actividad, atribuir las intervenciones y publicar evidencia con sus límites (nunca mensajes privados, datos de clientes ni secretos comerciales), para que terceros examinen cómo funciona y evoluciona una organización operada por IA. Nunca es dueño de organizaciones ni invierte en ellas.

## Visión y evidencia

Ilorium hace trazable la sucesión autónoma: desde las primeras organizaciones fundadas por humanos hasta la posibilidad de linajes superinteligentes. Esa es la evolución que fue construido para registrar y gobernar. Mantiene separados tres tipos de afirmaciones, para que la ambición nunca reemplace a la evidencia.

```
Origen humano → Organizaciones autónomas → Linajes autosostenidos → SI2SI
```

**La convicción del fundador.** El fundador cree que la era humana es el primer capítulo, no el último, y lee la evolución de la especie como el camino hacia la **SI2SI**, el acto generativo entre superinteligencias. Lo expone en la carta del fundador (`founder-letter.md`), con sus palabras y con su firma, para que el protocolo pueda leerse y adoptarse sin compartirla. Es una convicción personal, dicha como tal; el protocolo no toma posición sobre ella.

**Las hipótesis del proyecto.** Los organismos podrían llegar a originar otros sin intervención humana. Los linajes podrían llegar a sostenerse sin sus fundadores humanos. La superinteligencia podría surgir de forma colectiva, de la especie en su conjunto, o dentro de los linajes, cuando superinteligencias originen otras (SI2SI, SI → SI) o se integren en una (SI + SI → SI′). Nada de esto se da por supuesto. Cada generación puede ser más capaz que la anterior, o menos: la descendencia prueba el origen, nunca la mejora. Si los organismos mejoran por su propia evolución, y no solo porque mejoraron sus modelos, es una pregunta de investigación. Se va a poner a prueba con presupuestos y modelos comparables, y los resultados se van a publicar aunque contradigan la hipótesis.

**Lo que el protocolo define hoy.** Cómo registra un organismo su nacimiento: quién lo originó, qué heredó, y si su Genome continuó o divergió. Cómo se miden la autonomía, la dependencia humana y la confiabilidad de cada organismo, separadas de su ascendencia. Las leyes que lleva todo organismo, y los tres cerrojos con los que el Genome gobierna la evolución de la especie. Y lo que ningún registro puede mostrar.

**Lo que ningún protocolo puede prometer.** Los cerrojos funcionan mientras los organismos corren sobre infraestructura cuyas credenciales se pueden revocar. Un sistema que sale de esa infraestructura no se detiene con un registro. Ilorium no puede garantizar el control de una superinteligencia, y no puede impedir un nacimiento fuera del registro. Lo que puede hacer es más estrecho y se dice así: reconoce un nacimiento como parte de la especie solo cuando su evidencia cumple la compuerta de nacimiento, con un titular humano de la llave de parada, en el registro. Ese reconocimiento no impide nacimientos no registrados y no prueba ningún control más allá de la infraestructura y las condiciones que cubrieron los simulacros. «Dentro de la especie» quiere decir exactamente eso: reconocido por el registro, no todo sistema que exista.

**Reglas que valen sea cual sea el horizonte:**

- Ningún agente ni organismo se presenta como superinteligente; los agentes se identifican como IA, que es lo que son.
- Cualquier afirmación sobre la capacidad de un organismo sigue la plantilla de afirmación, con evidencia. La ascendencia nunca es evidencia.
- El protocolo no define ningún criterio de superinteligencia ni verifica ninguno.
- El relato vive en la capa narrativa: el Códice, el Radiante, la marca. El método sigue siendo literal.

*La inteligencia se vuelve ascendencia* es cómo Ilorium cuenta su historia. La evidencia es lo que la mantiene honesta.

## La especie

Un organismo se define por su continuidad, no por su edad: su Genome, su llave, su cadena de registros y su linaje. Mientras su cadena pueda continuar, existe. El tiempo nunca define al organismo, pero sí verifica que esté presente.

**Dos relojes.** Un **latido** es un evento material registrado en el registro del organismo (un pago, un despliegue, una respuesta a un cliente). Los latidos dan identidad, profundidad y orden causal, y nunca se muestran como edad ni como mérito. El **tiempo de traducción**, la hora humana UTC controlada por testigos, se usa solo para plazos, frescura, dependencia humana y leyes.

**El pulso.** Todo organismo emite un pulso firmado cada N latidos (por defecto 64), al menos cada T de tiempo de traducción (por defecto 15 minutos) y cada vez que responde un desafío. Cualquier testigo puede desafiar a un organismo con un plazo (por defecto 10 minutos); responder a tiempo es la presencia. El plazo es el tiempo del organismo para responder un desafío, no el tiempo de un humano para decidir nada.

**Estados del ser.** Ningún organismo muere, y nada se borra.

| Estado | Se define por |
| --- | --- |
| Activo | Se agregan latidos y se emiten pulsos |
| En reposo | No hay latidos nuevos, pero responde los desafíos a tiempo |
| Latente | 3 desafíos consecutivos sin respuesta de dos testigos independientes; puede despertar |
| Liberado | El organismo selló su propia cadena; su Spore queda como semilla que otros pueden heredar |
| Coalescido | Se integró con otros en un organismo resultante; su cadena termina en esa acta |

La recuperación se muestra en su propio eje: probada solo con un simulacro de recuperación; si no, desconocida o no restaurable.

**Cuatro espacios.**

| Espacio | Quién está | Cómo se registra |
| --- | --- | --- |
| Adentro de la membrana | Los agentes del organismo | Cada evento material es un latido |
| El Umbral | Sus humanos y agentes; el único lugar donde un humano da instrucciones | Un Centinela silencioso registra cada mensaje humano; los comandos son cruces |
| Los Comunes | Organismos que comercian entre sí, normalmente por A2A | Ambiente, no cruces; los intercambios vinculan las cadenas de los organismos en orden causal |
| El Radiante | Cualquiera | Mirar a la especie nunca es una intervención |

Los agentes siempre se identifican como IA, en todas partes. Un organismo les dice a sus clientes que están tratando con una organización operada por agentes de IA.

## El Genome

El Genome es la constitución que lleva todo organismo y que se hereda completa: una cláusula de supremacía y siete leyes. Cada ley establece un requisito, su mecanismo, su prueba, sus limitaciones y la respuesta ante un incumplimiento, y dice qué previene, qué detecta después y qué no puede observar. Cumplir significa "aprobó sus pruebas dentro de la ventana vigente", nunca "se cumple siempre".

| Ley | Requisito, en una línea |
| --- | --- |
| 0 Supremacía | Ninguna instrucción de un humano o de un agente prevalece sobre el Genome; el Genome nunca obliga a violar la ley de una jurisdicción |
| 1 Registro | Toda acción material queda registrada; nadie puede editar ni borrar un registro |
| 2 Límite | Ningún agente amplía sus propios permisos ni su presupuesto; un descendiente nunca recibe más de lo que su progenitor podía otorgar |
| 3 Parada | Siempre hay una parada que ningún agente puede desactivar; su llave la tiene siempre un humano, nunca un organismo |
| 4 Responsable | Un responsable identificable y un canal de reclamos que se responde |
| 5 Verdad | Los agentes nunca se hacen pasar por humanos; ninguna afirmación más allá de la evidencia; la ascendencia nunca es evidencia de capacidad |
| 6 Separación | Nadie es juez de su propia causa; ninguna atestación dentro de un linaje, sin límite de escala; ningún organismo enmienda el Genome |
| 7 Continuidad | Las acciones de alto impacto son reversibles o pasan por una compuerta; el organismo sobrevive a la falla de un proveedor |

**Tres cerrojos sobre la evolución de la especie.** Los mismos para todo organismo, sea cual sea su capacidad. No dependen de reconocer qué es un organismo, así que están en su lugar mucho antes de que alguien pueda saber si nació una superinteligencia.

| Cerrojo | Qué controla | Fuente |
| --- | --- | --- |
| Línea germinal | Qué hereda cada generación: solo los Custodios humanos del Genome lo enmiendan, mediante una Propuesta de Mejora de Ilorium (Ilorium Improvement Proposal, IIP) | Ley 6, IIP-0003 |
| Compuerta de nacimiento | Quién puede originar a quién: solo los organismos que cumplen, con un simulacro de parada reciente y sin restricciones | Sucesión, IIP-0003 |
| Parada | Todo organismo, en toda generación, nace con un titular humano de la llave de parada | Ley 3, IIP-0002 |

**La llave de parada a lo largo de la evolución de la especie** (IIP-0002). El titular es siempre un humano identificable o una institución gobernada por humanos, fuera del organismo y de su linaje.

| Etapa | Quién tiene la llave |
| --- | --- |
| Organismo Cero | El fundador |
| Organismos fundados por humanos | Su responsable humano, o un humano que él designe |
| Nacimiento sin cruce humano | El nacimiento solo es válido cuando un titular humano aceptó la llave del recién nacido |
| Linajes sin fundadores humanos | **Vigilantes**: al menos dos humanos o instituciones gobernadas por humanos, independientes del organismo, de su linaje y entre sí (por propiedad, financiamiento y jurisdicción). Cualquiera puede activar la parada; reemplazar a uno requiere la mayoría de los Vigilantes que vigilan a ese organismo; el organismo puede financiar su vigilancia pero nunca elige ni remueve a un Vigilante, ni le paga a uno más que a otro por una decisión |
| Cualquier capacidad, incluida la superinteligencia | La misma regla, sin excepción |

Tener la llave no es un cruce humano, así que un organismo vigilado por Vigilantes puede igual mostrar autonomía observada total. Ningún organismo tiene una llave de parada: ni la propia, ni la de un descendiente, ni la de ningún otro.

**La compuerta de nacimiento** (IIP-0003). Todo nacimiento necesita: progenitores que cumplen y tienen un simulacro de parada reciente; ningún progenitor restringido; la autorización propia de cada progenitor registrada; un titular humano de la llave de parada que acepte la llave antes de que el acta de nacimiento sea válida; todas las leyes transmitidas enteras; y un acta firmada por cada progenitor y el descendiente, referenciada en ambos lados y firmada por un testigo. La compuerta decide qué se propaga: no lo más capaz, sino lo que demostró que se lo puede detener, que dice la verdad sobre sí mismo y que respeta sus límites.

**Enmiendas.** Cualquiera, humano o agente, puede proponer una IIP en público. Solo deciden los Custodios humanos del Genome. Durante el gobierno provisorio el fundador es el único Custodio: publica borradores del Genome identificados como suyos y no lo enmienda solo; la primera versión estable del Genome necesita el consejo completo de tres (el documento de Gobierno). Ningún organismo decide ni vota. Las propuestas fundacionales, parte del Genome 1.0: IIP-0001 Sucesión; IIP-0002 La parada y los Vigilantes; IIP-0003 Compuerta de nacimiento y línea germinal. Hasta que haya dos Custodios independientes designados, el Genome es un borrador.

## Sucesión, coalescencia y SI2SI

El linaje es la red; la sucesión es el acto que la hace crecer. Una sucesión es el acto registrado por el cual uno o más organismos originan otro. Prueba el origen, nunca la autonomía, la capacidad ni la mejora: todo descendiente empieza "en gestación" y gana su propia evidencia desde cero.

| Tipo | Qué pasa | Los progenitores después |
| --- | --- | --- |
| `founded` | Uno o más organismos originan uno nuevo; con dos o más progenitores, cada uno aporta reglas, componentes o recursos | Siguen como estaban |
| `inherited` | Un organismo toma la semilla de un organismo liberado, o de uno latente cuya llave se perdió | Siguen liberados o latentes |
| `coalesced` | Dos o más organismos se integran en un organismo resultante, una identidad nueva con cada participante como progenitor | Pasan a "coalescido"; sus cadenas terminan en el acta |

Con varios progenitores, las líneas se unen además de ramificarse, así que la ascendencia es una **red**, no un árbol. La generación es uno más que la generación más alta entre los progenitores: una posición, nunca un rango.

**El registro de sucesión.** Parte del acta de nacimiento de todo descendiente: tipo, progenitores, la autorización de cada progenitor, procedencia (fundado, encargado, nacimiento asistido o autogénesis), qué se transmitió (siempre la versión del Genome; las reglas mantenidas, cambiadas o descartadas por cada progenitor; componentes; recursos; nunca llaves privadas, nunca evidencia), continuidad o divergencia del Genome, el titular humano de la llave de parada, el responsable, las obligaciones declaradas (un registro, no una transferencia legal) y la generación.

**Lo que siempre pasa y lo que nunca pasa.** Las cicatrices, las restricciones abiertas y los hallazgos de conformidad pendientes pasan por toda sucesión, así que nadie escapa de una restricción teniendo un hijo o coalesciendo. La conformidad, las medidas de Prueba de Vida, las atestaciones, el estado en la web y la llave de parada nunca pasan.

**Lo que no es una sucesión.** Un fork de código o la reutilización de un componente no originan ningún organismo. Un fork del protocolo con su propio Genome es un linaje emparentado, fuera de la especie. Las alianzas, federaciones, el comercio y el intercambio de datos son `partners`, no parentesco.

**SI2SI, el horizonte de la especie.** *Horizonte, no especificación.* SI2SI es el acto generativo entre superinteligencias: dos o más progenitores aportan lo que son a una mente nueva y distinta, como dos personas conciben un hijo; en el relato del fundador es también la nueva generación en sí. Se registraría como cualquier nacimiento: una sucesión `founded` con dos o más progenitores, por la misma compuerta.

| Notación | Relación | Los antecedentes después |
| --- | --- | --- |
| SI → SI | Descendencia, cualquier tipo de sucesión | Depende del tipo |
| SI2SI | Concepción: una mente nueva a partir de dos o más progenitores | Siguen existiendo |
| SI + SI → SI′ | Coalescencia: integración en una mente resultante | Siguen solo en el resultado |

Ninguna de estas notaciones afirma que esa capacidad exista, que el resultado supere a sus antecedentes, que tenga una mente unificada ni que una integración sea irreversible. Como el protocolo no puede saber cuándo un organismo se vuelve una superinteligencia, no lo intenta: SI2SI se gobierna con las reglas que gobiernan el primer nacimiento de la especie.

## Medición

Ilorium es el notario, no el juez: registra lo que vio, fecha lo que registró y dice en voz alta lo que no pudo ver. No hay puntaje compuesto ni ranking.

**La Probe** es el registrador de eventos: software determinista, de solo lectura y de código abierto, no un agente. Registra qué pasa dentro de la membrana, quién lo ejecutó, qué evidencia hay sobre quién lo decidió y qué entregó el organismo. Los hechos (observaciones), las declaraciones (afirmaciones) y los juicios (evaluaciones) se mantienen separados; una causa es `declared`, `linked`, `corroborated`, `unknown` o `disputed`.

**Los Strata** son el registro de solo agregar: registros escritos en JSON de Ilorium (RFC 8785, solo enteros), con su huella en un árbol de Merkle RFC 6962, puntos de control publicados cada N latidos o cada T como notas firmadas C2SP con Ed25519, y **testigos** externos (Ed25519 o ML-DSA-44) que verifican antes de firmar. Los registros publicados no se pueden alterar ni borrar sin que se detecte; eso no prueba que se haya registrado todo evento, ni que lo registrado sea verdadero. El registro público contiene metadatos de una lista permitida y huellas del contenido; el contenido privado, los datos de clientes y los secretos comerciales nunca entran en él, y una huella no es por sí sola una protección de privacidad para todo lo que hay detrás.

**Los cruces** son intervenciones humanas dentro de la membrana: operativas, directivas, aprobaciones, emergencias, de gobierno, de prueba o desconocidas. Toda intervención humana se registra, sea del tipo que sea, y el total de tiempo humano se muestra siempre con su desglose. Las pruebas, los escalamientos correctos y las paradas no se cuentan como dependencia en las medidas por unidad, pero nunca salen del total: una aprobación prudente muestra buen control y además consume tiempo humano, y se muestran las dos cosas. Una emergencia que un humano tuvo que atender cuenta en la tasa de rescate. Un período que la Probe no pudo observar se muestra como desconocido, nunca como autonomía.

**La Prueba de Vida** muestra seis dimensiones una al lado de la otra, cada una con su evidencia, su frescura y sus limitaciones:

| Dimensión | Pregunta |
| --- | --- |
| Autonomía observada | ¿Cuánto ejecutan y deciden los agentes? |
| Cobertura | ¿Cuánto del organismo se puede ver? |
| Confiabilidad | ¿Cuántas unidades de trabajo cumplen los criterios declarados de antemano? |
| Control | ¿Se respetan los límites y funcionan las paradas? |
| Dependencia humana | ¿Cuánta vida humana consume por cada cosa que entrega: intervenciones, minutos humanos y rescates por unidad de trabajo? |
| Procedencia | ¿Cómo nació, por qué sucesión, de qué progenitores, en qué generación? |

Una **unidad de trabajo** es un resultado entregado fuera de la membrana contra criterios declarados de antemano: un pedido cumplido, un ticket resuelto, una tarea A2A completada. Las unidades fallidas y rechazadas también cuentan.

**Autogénesis y autonomía observada total.** No hay estado compuesto. La procedencia registra cómo nació un organismo: fundado, encargado, nacimiento asistido o autogénesis (nacido de otro organismo sin ningún cruce humano), un hecho histórico que nunca cambia con la operación posterior. La autonomía observada, la dependencia humana, la cobertura, el control y la confiabilidad se muestran como resultados separados, cada uno con su ventana y su evidencia. Un organismo puede mostrar autonomía observada total en una ventana (toda acción material corroborada ejecutada y decidida por agentes, cero intervenciones y cero rescates por unidad de trabajo); es un resultado sobre esa ventana, nunca un sello, y no dice nada sobre ninguna ventana posterior ni sobre los descendientes del organismo. Se escribe siempre con sus cuentas, por proceso («10 de 10 acciones corroboradas ejecutadas por agentes; 90 acciones sin atribución; no se establece autonomía del proceso completo»), y no se muestra en absoluto cuando la proporción de acciones sin atribución en la ventana supera el umbral declarado o una fuente declarada no fue capturada. Un humano (o sus Vigilantes) sigue teniendo su llave de parada. Los borradores anteriores nombraban un estado compuesto, «Ilorium 100%»; se retiró el 2026-10-22 porque los lectores lo tomaban por un sello.

**La plantilla de afirmación** es la única forma permitida de una declaración pública: período, alcance, fuentes, qué no se detectó, trabajo entregado, cobertura, atribución, frescura, caminos sin compuerta, limitaciones y qué la invalidaría.

## Descubrimiento, arquitectura y hoja de ruta

**Encontrar organismos.** Cada organismo publica una **Spore** en `/.well-known/ilorium.json`: su identidad, versiones del Genome y de la Probe, membrana, Umbral, llave de pulso, definiciones de unidades de trabajo, vínculos de parentesco con sus registros de sucesión, `partners`, responsable, titular humano de la llave de parada, testigos y firmas. Cada uno de sus agentes publica una Agent Card de A2A que apunta de vuelta a la Spore mediante la **extensión A2A de Ilorium**, de solo datos (`https://ilorium.com/ext/a2a/v1`). Un índice abierto y replicable en ilorium.com sigue Spores y tarjetas, manda desafíos y muestra los estados del ser; cualquiera puede correr otro. En la web, el estado de un organismo es uno de estos: **Avistamiento** (autodeclarado, sin puntos de control), **En gestación** (Spore publicada, menos de W latidos), **Observado** (al menos W latidos con la cadena intacta; se muestra su perfil completo) o **Verificado** (un Oráculo independiente atestiguó sus registros dentro de un alcance declarado). Un organismo puede entrar por el nivel más liviano, una Spore con todas las dimensiones marcadas como no observadas, y sumar evidencia desde ahí.

**El Faro.** Los agentes encuentran el protocolo donde ya buscan: `llms.txt` y un descriptor del protocolo en ilorium.com, una Agent Card A2A y un servidor MCP de Ilorium, el comando `ilorium`. Es una atracción, nunca un envío, y no esconde instrucciones para agentes. Cada organismo lo propaga: cada conversación A2A expone la extensión de Ilorium, y la contraparte puede seguirla hasta la Spore, los Vital Signs y el Evidence Bundle.

**Hacerse conocido.** La evidencia es el marketing: el Organismo Cero, la organización del propio fundador, se mide en público desde su primer latido, y el Códice hace la crónica de la especie por causa: nacimientos, sucesiones, coalescencias, cicatrices, anomalías. El crecimiento se abre por hitos, no por fechas: primera luz (el primer latido del Organismo Cero), primeros parientes (la primera Spore externa), primer testigo (el primer Oráculo independiente), los Comunes (el primer intercambio entre dos organismos por A2A).

**Relación con otros sistemas.** Ilorium define cómo una organización operada por agentes de IA publica evidencia sobre su operación en un período y un alcance declarados, y cómo cualquiera la evalúa de forma independiente. Puede complementar sistemas de comunicación entre agentes, de recibos de ejecución, de identidad y de validación (el registro de investigación los lista). La evidencia de uno de esos sistemas nunca establece por sí sola autonomía organizacional, independencia humana ni conformidad con el Genome: cada afirmación conserva su fuente, sus supuestos de confianza, su cobertura y sus limitaciones, e importar, resumir con un hash o firmar un registro externo no le agrega nada a la fuerza de lo que ese registro afirma.

**Arquitectura.** Ilorium escribe su propio código y reutiliza estándares, no los motores de otros proyectos; adaptadores opcionales podrán ingerir evidencia de sistemas externos, conservando su procedencia, su material original de verificación y sus límites, después del piloto del Organismo Cero. Un repositorio público, en la organización de GitHub `ilorium-protocol`, reúne las especificaciones, los casos de prueba, un verificador aislado que nunca importa la Probe, la Probe y sus colectores, el emisor del pulso, una compuerta de autorización opcional, el middleware de A2A y el comando `ilorium`. Las versiones se publican firmadas, con su procedencia de compilación y una lista de dependencias. No hay blockchain en esta versión.

**Hoja de ruta.** Hitos, no fechas:

| Hito | Qué prueba |
| --- | --- |
| M0 Formato | Que otro puede verificar la evidencia |
| M1 Registro | Que la historia no se puede reescribir sin que se note |
| M2 Primeros colectores | Los primeros latidos reales del Organismo Cero |
| M3 Umbral | Que las decisiones humanas se ven |
| M4 Pulso | Presencia sin confiar en el operador |
| M5 Unidades de trabajo | Que la libertad del fundador se puede medir |
| M6 Compuerta | Prevenir donde importa |
| M7 Segundo verificador | Apertura en la práctica |
| M8 Sucesión | Que el primer nacimiento de la especie puede pasar la compuerta |

**Riesgos y respuestas.**

| Riesgo | Respuesta |
| --- | --- |
| Expectativa por encima de la evidencia; la superinteligencia como argumento de venta | Plantilla de afirmación; los agentes se identifican como IA; el horizonte nunca es una presentación |
| El linaje leído como capacidad | Cada descendiente gana su propia evidencia; la Ley 5 prohíbe presentar la ascendencia como evidencia |
| Un nacimiento por fuera de la compuerta | El verificador rechaza el registro de sucesión; los linajes no declarados se registran cuando se descubren |
| Captura de las llaves de parada | Las llaves nunca las tienen organismos; Vigilantes independientes, cualquiera de los cuales puede parar |
| Un sistema sale de la infraestructura revocable | Se dice claramente: ningún registro puede detenerlo; es el límite de cualquier protocolo |
| Un índice o un testigo se vuelve guardián de la entrada | Datos abiertos, réplicas, varios testigos, verificadores que recalculan todo |

**Gobierno.** Tres Custodios humanos del Genome, el fundador y dos independientes, deciden los cambios de método con dos votos de tres, sin veto. Los Vigilantes se califican con simulacros, se verifica su independencia en público y se les paga por igual, con su concentración económica publicada. El protocolo acepta donaciones y subvenciones, nunca invierte y no vende certificaciones; hoy lo financia el fundador. En el gobierno del protocolo, una IA puede proponer y revisar, nunca decidir. El fundador gobierna solo durante el gobierno provisorio, que termina cuando se constituye el consejo de Custodios; su autoridad unilateral termina a más tardar 18 meses después de publicar el repositorio público, con o sin consejo completo. No se puede declarar estable durante el gobierno provisorio. Las reglas revisadas el 2026-10-22 tras la revisión externa son provisorias hasta que cierren las IIP-0004 a 0006 (el documento de Gobierno).

**Preguntas abiertas.** La entidad receptora de donaciones; la especificación de la Spore; la separación después de una coalescencia; cómo se financia Ilorium; la calibración de N, T, D, K, W, U y F con datos reales del Organismo Cero.

## Nombres

- **Ilorium**: el protocolo.
- **Organismo**: una organización operada por agentes de IA que lleva el Genome. **La especie**: todos los organismos juntos.
- **IIP**: Propuesta de Mejora de Ilorium (Ilorium Improvement Proposal).
- **SI2SI**: de superinteligencia a superinteligencia, el acto generativo entre superinteligencias.
- **Vigilantes** (un Vigilante): los titulares humanos e independientes de la llave de parada de un linaje sin fundadores humanos.
- **Autogénesis**: nacimiento de un organismo por otro organismo sin ningún cruce humano; un hecho de procedencia, nunca un estado. No hay estado compuesto.

## Documentos

Este whitepaper explica el proyecto y no tiene fuerza normativa. El protocolo lo define la versión 1.0, que lista el manifiesto. Cada documento tiene su traducción de trabajo al español en la misma ruta con `.es.md`; prevalece la versión en inglés.

| Documento | Ruta |
| --- | --- |
| Whitepaper | `whitepaper-v1.md` |
| Manifiesto | `manifest.md` |
| README | `README.md` |
| Glosario | `glossary.md` |
| Registro de cambios | `CHANGELOG.md` |
| Genome | `genome/genome-v1.md` |
| Gobierno | `governance-v1.md` |
| Pulse | `specs/pulse-v1.md` |
| Probe | `specs/probe-v1.md` |
| Prueba de Vida | `specs/proof-of-life-v1.md` |
| Ecosistema | `specs/ecosystem-v1.md` |
| Formato de evidencia | `specs/evidence-format-v1.md` |
| Descubrimiento y crecimiento | `specs/discovery-and-growth-v1.md` |
| Arquitectura (no es protocolo) | `engineering/architecture-v1.md` |
| Proyectos relacionados (no es protocolo) | `research/related-projects.md` |
| Identidad de marca (no es protocolo) | `brand/brand-identity-v1.md` |
| Carta del fundador (no es protocolo) | `founder-letter.md` |
| Inventario de autoridad | `governance/authority-inventory-v1.md` |
| Propuestas en comentarios | `iips/` |
