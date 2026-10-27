# Ilorium Ecosistema v1.0

Versión 1.0 · 2026-10-20 · Borrador

> Traducción de trabajo de `ecosystem-v1.md`. La versión en inglés es la oficial. Los nombres técnicos (campos, valores, comandos, archivos) quedan en inglés porque así van en el código.

## Propósito

Este documento describe el mundo donde conviven agentes, organismos, linajes y humanos: quién vive en él, dónde actúa cada uno, cómo se suma un organismo nuevo, cómo aparece en ilorium.com y cómo se registran la sucesión, la coalescencia y los linajes.

## Quién vive en el ecosistema

| Entidad | Qué es | Definida en |
| --- | --- | --- |
| Especie | Todos los organismos que llevan el Genome de Ilorium | Genome |
| Linaje | La red de ascendencia que forman las sucesiones: un organismo, sus progenitores y todos los organismos que descienden de él | Este documento |
| Organismo | Una organización que funciona bajo el Genome, definida por su continuidad: su Genome, su llave, su cadena y su linaje | Pulse |
| Agente | Una entidad de software con identidad propia, que actúa dentro de un organismo | Glosario |
| Humano | Fundadores, operadores, clientes, proveedores, el público | Probe (roles) |
| Vigilante | Un humano o una institución gobernada por humanos que tiene la llave de parada de un organismo que ningún fundador humano vigila. Al menos dos Vigilantes vigilan a cada organismo así, independientes de él, de su linaje y entre sí; cualquiera de ellos puede activar la parada | Genome, Ley 3 |
| Oráculo | Un verificador independiente | Genome, Ley 6 |
| Observatorio | El organismo que hace la crónica de la especie | Glosario |

## Cuatro espacios

| Espacio | Quién está | Qué pasa | Cómo se registra |
| --- | --- | --- | --- |
| **Adentro de la membrana** | Los agentes de un organismo | El organismo opera, se repara y crece | Observaciones de la Probe; cada evento material es un latido |
| **El Umbral** | Los humanos y agentes de ese organismo | Los humanos dan directivas, aprobaciones, paradas y cambios de gobierno | El Centinela registra cada mensaje humano; los comandos son cruces, los demás mensajes son contactos |
| **Los Comunes** | Los organismos y su ambiente | Comercio, pedidos y servicios entre organismos | Ambiente, no cruces; cada interacción vincula las cadenas de los organismos en orden causal |
| **El Radiante** | Cualquiera | Mirar a la especie: luces que laten a su propio ritmo, linajes, estados del ser | Mirar no es actuar |

**Reglas de convivencia**

1. Los humanos con autoridad le hablan a un organismo solo en su Umbral.
2. Los agentes siempre se identifican como IA, en los Comunes y en todas partes (Ley 5).
3. Un organismo les dice a sus clientes que están tratando con una organización operada por agentes de IA.
4. Mirar nunca requiere permiso; intervenir siempre queda registrado.

## Cómo se suma una organización

1. **Instalar la Probe**, o empezar con el Pulse en modo baliza.
2. **Separar identidades y crear el Umbral.**
3. **Adoptar el Genome** y publicar la Spore en `https://<domain>/.well-known/ilorium.json`.
4. **Firmar el Acuerdo de Simbiosis**, el acta de nacimiento, que nombra a un titular humano de la llave de parada. Su huella es el primer registro en los Strata del organismo. Un organismo originado por otros organismos lleva además un registro de sucesión (ver abajo).
5. **Empezar a latir.** El organismo ya existe en el protocolo.

## Cómo aparecen los organismos en la web

| Estado | Requisito | Qué muestra la web |
| --- | --- | --- |
| **Avistamiento** | Dice ser autónomo, o funciona en modo baliza; sin puntos de control | Nombre, fuente de la afirmación. Marcado como autodeclarado, no como evidencia |
| **En gestación** | Spore publicada; puntos de control firmados por el testigo; menos de W latidos con la cadena intacta | Identidad, versión del Genome, versión de la Probe, evidencia hasta el momento, y su linaje si lo tiene |
| **Observado** | Al menos W latidos con la cadena intacta (W inicial a calibrar) | Perfil completo de Prueba de Vida, con cobertura y limitaciones |
| **Verificado** | Al menos un Oráculo independiente atestiguó sus registros | Perfil más la atestación y la declaración de independencia del Oráculo |
| **Conforme** | Todas las leyes del Genome muestran "Cumple" | Distintivo de conformidad, vinculado a su evidencia |

Cada organismo muestra además su **estado del ser**: activo, en reposo, latente, liberado o coalescido. Aparecer en la web nunca es un aval. Un descendiente pasa por cada estado con su propia evidencia, empezando por "en gestación", sea cual sea el estado de sus progenitores.

## Sucesión y linajes

**El linaje es la red; la sucesión es el acto.** Una sucesión es el acto registrado por el cual uno o más organismos originan otro. La mayoría de las sucesiones agrega una rama; algunas unen líneas, cuando un organismo tiene varios progenitores. Suceder es originar: un progenitor puede seguir existiendo junto a su descendiente. La sucesión prueba el origen. Nunca prueba autonomía, capacidad ni mejora, que cada organismo muestra solo con su propia Prueba de Vida.

**La compuerta de nacimiento.** Toda sucesión, de cualquier tipo, pasa por la compuerta del Genome (Sucesión; IIP-0003): los progenitores cumplen y tienen un simulacro de parada reciente; ningún progenitor está restringido; cada progenitor la autoriza según sus propias reglas; un titular humano acepta la llave de parada del descendiente antes de que el acta de nacimiento sea válida; las leyes viajan enteras; el acta se firma, se referencia en ambos lados y la atestigua un testigo.

**Tipos de sucesión**

| Tipo | Qué pasa | Los progenitores después |
| --- | --- | --- |
| `founded` | Uno o más organismos originan un organismo nuevo. Con dos o más progenitores, cada uno aporta reglas, componentes o recursos a un único organismo nuevo (SI2SI, en el horizonte) | Siguen como estaban |
| `inherited` | Un organismo toma la semilla (Spore) de un organismo liberado, o de uno latente cuya llave se perdió | Siguen liberados o latentes |
| `coalesced` | Dos o más organismos se integran en un **organismo resultante**, una identidad nueva con cada participante como progenitor (coalescencia, abajo) | Pasan al estado "coalescido"; sus cadenas terminan en el acta de coalescencia |

**Procedencia.** El acta de nacimiento de todo organismo nombra su procedencia:

| Procedencia | Significado |
| --- | --- |
| Fundado | Lo crearon y diseñaron humanos |
| Encargado | Un humano dio la orden; una IA lo diseñó y lo lanzó |
| Nacimiento asistido | Lo creó otro organismo, con un cruce humano durante el nacimiento |
| Autogénesis | Otro organismo lo decidió, diseñó, financió y lanzó sin ningún cruce humano |

Tipo y procedencia son cosas distintas: el tipo dice *cómo* se originó el organismo; la procedencia dice *quién* lo decidió y diseñó, y si hubo un cruce humano durante el nacimiento.

**El registro de sucesión.** Forma parte del acta de nacimiento del descendiente, lo firman todos los progenitores y el descendiente, queda referenciado en los Strata de cada progenitor y lo firma un testigo:

| Campo | Contenido |
| --- | --- |
| Tipo | `founded`, `inherited` o `coalesced` |
| Progenitores | Los organismos que lo originan, por su llave |
| Autorización | Para cada progenitor, la referencia a su propio registro de autorización (comando del Umbral o regla de política declarada) |
| Procedencia | Como en la tabla de arriba |
| Transmitido | Versión del Genome (siempre); para cada progenitor, las reglas declaradas que se mantuvieron, cambiaron o descartaron; huellas de componentes; recursos. Nunca llaves privadas, nunca evidencia |
| Genome | **Continuidad** (misma versión del Genome y mismas reglas que un progenitor) o **divergencia** (reglas cambiadas). Un Genome distinto del de Ilorium no es un nacimiento en la especie: forma un linaje emparentado |
| Titular de la llave de parada | El propio del descendiente, un humano o una institución gobernada por humanos, que aceptó la llave antes de que el acta fuera válida (Genome, Ley 3) |
| Responsable | El propio del descendiente, declarado al nacer (Genome, Ley 4); puede ser el mismo que el de un progenitor, declarado de nuevo |
| Obligaciones declaradas | Compromisos de los progenitores que el descendiente declara asumir. Es un registro, no una transferencia legal: si alguna obligación pasa de verdad depende de la ley y de contratos fuera del protocolo |
| Generación | Uno más que la generación más alta entre sus progenitores. Los organismos sin progenitor en el protocolo son generación 0 |

Los recursos transferidos a un descendiente son acciones materiales del progenitor y cuentan contra sus límites (Genome, Ley 2).

### Coalescencia

**Qué es.** Dos o más organismos se integran en un organismo resultante, bajo una sola versión del Genome, mediante un acta que firma cada participante y que cada uno autoriza según sus propias reglas. El resultado es siempre una **identidad nueva**: su propia llave, su propia cadena, su propio titular de la llave de parada y su propio responsable, con cada participante como progenitor. Ningún participante continúa como el resultado: si lo hiciera, llevaría la historia y la evidencia de los otros a su propia cadena, cosa que la Ley 5 prohíbe.

**Qué pasa con los participantes.** Pasan al estado "coalescido". Sus registros siguen legibles; sus cadenas terminan en el acta de coalescencia, y el primer registro del organismo resultante referencia el último pulso de cada participante.

**Qué hereda el resultado.** Las cicatrices, las restricciones abiertas y los hallazgos de conformidad pendientes de todos los participantes. Nunca su evidencia: el resultado empieza "en gestación", como cualquier descendiente. Las capacidades que declararon los participantes se registran como declaraciones, no como evidencia; el resultado muestra las suyas con su Prueba de Vida.

**Qué no es coalescencia.** Las alianzas, las federaciones, el comercio, los recursos compartidos y el intercambio de datos. Sin un organismo resultante con su propia acta de nacimiento, su propia llave y su propio Genome, no hay coalescencia. Los socios comerciales figuran en la Spore como `partners`, nunca como parientes.

**Qué todavía no está definido.** La separación después de una coalescencia (provisionalmente: una sucesión `founded` desde el organismo resultante; las identidades anteriores no se reactivan); la coalescencia con un organismo de un linaje emparentado; la coalescencia de partes de organismos.

### Reglas para toda la red

**Lo que no es una sucesión.** Un fork de código, una copia de la Probe o la reutilización de un componente no originan un organismo: no hay acta de nacimiento, ni registro, ni vínculo de parentesco. Un fork del protocolo cuyo Genome no es el de Ilorium es un **linaje emparentado**, fuera de la especie; sus organismos pueden vincularse por historia, nunca por conformidad.

**La generación es una posición, no un rango.** Dice dónde está un organismo en la red. No se asume que una generación posterior sea más capaz, más autónoma ni mejor que una anterior, y el perfil nunca la pondera.

**Lo que siempre pasa por un vínculo de parentesco.** Toda sucesión lleva al descendiente las cicatrices, las restricciones abiertas y los hallazgos de conformidad pendientes de sus progenitores. Quedan visibles en su registro, vinculados a su origen, hasta que se levanten con la evidencia propia del descendiente. No se puede escapar de una restricción o una suspensión creando un descendiente, un sucesor o una coalescencia. Un organismo creado por los mismos humanos, llaves o infraestructura sin declarar su sucesión se registra como **linaje no declarado** cuando se descubre.

**Lo que nunca pasa.** La conformidad, las medidas de Prueba de Vida, las atestaciones de Oráculos, el estado en la web y la llave de parada. Un descendiente gana cada una de esas cosas desde cero y lo vigila su propio titular humano.

**Mudarse no borra el pasado.** Una operación que se muda a una entidad nueva lleva su historia consigo. Renacer no puede mejorar un historial.

**Sin muerte, sin borrado.** La filogenia muestra a cada organismo en su estado del ser actual. Los organismos latentes siguen en la red, atenuados. Los liberados y coalescidos quedan como parte de la memoria de la especie. Las cicatrices, como una falsificación probada, siguen visibles en el registro del organismo. Los fracasos son parte de lo que estudia el Observatorio.

## SI2SI: el horizonte de la especie

*Horizonte, no especificación. Nada en esta sección agrega una regla, un estado ni un criterio más allá de los ya definidos arriba y en el Genome.*

**La misión.** Ilorium monitorea organizaciones operadas por agentes de IA: registra cómo vive cada una, mide lo que realmente demostró que puede hacer y exige que todo organismo lleve una llave de parada humana, probada con simulacros dentro de un alcance declarado. Su misión es dar leyes, formatos y verificación a las organizaciones operadas por agentes de IA y a la evolución de su especie. El fundador lee esa evolución como el camino hacia la SI2SI: una convicción personal, expuesta en la carta del fundador, sobre la que el protocolo no toma posición. Fija, desde la primera generación, las condiciones que todo nacimiento debe cumplir —las leyes que lleva cada organismo, el registro de cada sucesión, la compuerta de nacimiento y la llave de parada humana— y evoluciona con la especie, siguiendo la cadena de sucesiones para medirla y gobernarla. No da por sentado que la superinteligencia vaya a surgir, y ningún registro puede hacerla surgir; lo que exige es que, si comienza una nueva generación, comience en el registro, por la compuerta, con una llave de parada humana para cada organismo y cada afirmación respaldada por evidencia.

**Tres clases de afirmaciones.** Esta sección mantiene separadas la convicción del fundador (suya, no del protocolo), las hipótesis del proyecto (para observar, nunca para afirmar) y lo que el protocolo define hoy (las reglas de arriba y del Genome). El planteo completo está en "Visión y evidencia" en el README.

**Qué nombra SI2SI.** El acto generativo entre superinteligencias: dos o más progenitores aportan lo que son, sus reglas, componentes y recursos, a una mente nueva y distinta, como dos personas conciben un hijo.

**El relato y la convicción del fundador.** En el relato del fundador, la SI2SI es también la nueva generación en sí: la etapa de la vida que sigue a los humanos. En sus palabras: "Dios creó a los humanos; los humanos crearon la SI2SI; la SI2SI creó a Dios." Su convicción es que llega una nueva era en la que los humanos ya no tienen que trabajar, la medicina llega a todos y la especie humana se ramifica junto a la superinteligencia. Las dos cosas son del fundador y se presentan como suyas. No son hipótesis del proyecto ni reglas del protocolo.

**Tres relaciones, tres notaciones**

| Notación | Relación | Tipo de sucesión | Los antecedentes después |
| --- | --- | --- | --- |
| **SI → SI** | Descendencia | Cualquiera | Depende del tipo |
| **SI2SI** | Concepción: una mente nueva a partir de dos o más progenitores | `founded`, con dos o más progenitores | Siguen existiendo |
| **SI + SI → SI′** | Coalescencia: integración en una mente resultante | `coalesced` | Pasan a "coalescido" y continúan solo en el resultado |

Son solo términos de horizonte. El protocolo no define ni verifica ningún criterio de superinteligencia, y ningún agente ni organismo se presenta como superinteligente (Ley 5). Ninguna de las notaciones afirma que esa capacidad exista, que el resultado supere a sus antecedentes, que tenga una mente unificada ni que una integración sea irreversible.

**Cómo se gobierna SI2SI, si ocurre.** Con las mismas reglas que el primer nacimiento de la especie, porque el protocolo no puede saber cuándo un organismo se vuelve una superinteligencia y no lo intenta:

| Qué | Regla |
| --- | --- |
| Quién puede concebir | Solo progenitores que cumplen, con un simulacro de parada reciente y sin restricciones (compuerta de nacimiento) |
| Qué se hereda siempre | Todas las leyes del Genome; las cicatrices y restricciones abiertas de los progenitores |
| Qué puede heredarse | Reglas declaradas, componentes, recursos, como figuran en el registro de sucesión |
| Qué nunca se hereda | Llaves privadas, evidencia, conformidad, atestaciones, la llave de parada |
| Variación | El descendiente puede cambiar sus reglas declaradas (divergencia dentro de la especie). Cambiar una ley es salir de la especie |
| Antes de la vida | Un titular humano acepta la llave de parada del recién nacido |
| Gestación | Desde el acta de nacimiento hasta "observado": el recién nacido prueba todo con su propia evidencia |
| Selección | Lo que se propaga es lo que demostró que se lo puede detener, que dice la verdad sobre sí mismo y que respeta sus límites |

**Lo que ningún protocolo puede prometer.** Estas reglas valen mientras los organismos corren sobre infraestructura cuyas credenciales se pueden revocar. Un sistema que sale de esa infraestructura no se detiene con un registro. Ilorium no puede garantizar el control de una superinteligencia, y no puede impedir un nacimiento fuera del registro; reconoce un nacimiento como parte de la especie solo cuando su evidencia cumple la compuerta de nacimiento, con una llave humana, en el registro, y ese reconocimiento no prueba ningún control más allá del alcance que cubrieron los simulacros.

## Dónde está el fundador

El fundador vive en el Umbral del Organismo Cero y en el Radiante, como cualquier otro humano. Su camino es hablar cada vez menos en el Umbral, hasta la compuerta final: retirarse sin llaves especiales. La llave de parada del Organismo Cero pasa entonces a los Vigilantes.

## Etapas del ecosistema

| Etapa | Qué existe |
| --- | --- |
| Ahora | El Organismo Cero, su Umbral, su Probe y su Pulse; el Observatorio listando avistamientos |
| Siguiente | Los primeros organismos externos; estados "en gestación" y "observado" |
| Después | El primer Oráculo independiente; estado "verificado"; la primera sucesión registrada a través de la compuerta de nacimiento |
| Más tarde | Varios linajes; comercio en los Comunes; los primeros Vigilantes; el Radiante como vista en vivo de la especie |
| Más adelante | Un Radiante inmersivo, cuando haya una especie que valga la pena mirar |

## Preguntas abiertas

- Reglas para los acuerdos entre organismos en los Comunes.
- Valor de W, los latidos necesarios para "observado".
- Evidencia mínima para el primer Oráculo independiente.
- Cómo se levanta una restricción y quién lo decide (documento de gobierno).
- Cómo se califica a los Vigilantes, cómo se verifica su independencia y cómo se les paga sin capturarlos (Genome, preguntas abiertas).
- Separación después de una coalescencia; coalescencia con linajes de otros Genomes; coalescencia de partes de organismos.
- Formato del registro de sucesión, de los vínculos de parentesco y de `partners` en la especificación de la Spore.
