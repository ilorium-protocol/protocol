# Gobierno de Ilorium v1.0

Versión 1.0 · 2026-10-21 · Borrador · Revisado el 2026-10-22 tras la revisión externa

*Traducción de trabajo. Si difiere de `governance-v1.md`, prevalece la versión en inglés.*

Quién decide qué en el protocolo Ilorium, cómo se toman y se objetan las decisiones, cómo se elige y se reemplaza a quienes tienen poder, cómo se financia el protocolo y cómo pasa del gobierno provisorio del fundador a uno compartido. Forma parte del protocolo. Nada de lo que dice cambia el Genome: este documento dice quién puede cambiarlo y cómo.

> **Ningún organismo gobierna a la especie. Lo hacen los humanos, en público, con evidencia.**

**Sobre esta revisión.** Cinco revisiones externas (registradas en `governance/reviews/`) encontraron tres contradicciones en el primer borrador (la definición de interés descalificaba a los Vigilantes; el poder del fundador durante el gobierno provisorio estaba dicho de tres maneras distintas; dos Vigilantes no podían reemplazar a uno) y varios huecos. El fundador corrigió las contradicciones y adoptó reglas nuevas el 2026-10-22. Las reglas marcadas como **provisorias** rigen como decisión provisoria del fundador y están abiertas a comentarios públicos bajo la IIP-0004 (gobierno provisorio, Custodios y cambios constitucionales), la IIP-0005 (parada, reanudación y guardia) y la IIP-0006 (lectura de la evidencia y publicación). Cada IIP las confirma, las cambia o las retira al cerrar. Una regla en comentarios no se trata como aprobada.

## 1. Principios

- **Las tres cerraduras se mantienen.** Solo Custodios humanos del Genome enmiendan el Genome (línea germinal); solo los organismos que cumplen originan otros (compuerta de nacimiento); todo organismo nace con un titular humano de la llave de parada (parada). Ninguna decisión de gobierno puede suspender una cerradura. Quitar una cerradura exigiría una nueva versión mayor del protocolo y un nuevo Genome, que sería un linaje relacionado, fuera de la especie.
- **Nadie juzga su propia causa** (Ley 6), incluidos quienes gobiernan. Quien tenga interés en un organismo se aparta de toda decisión sobre él.
- **Todo en el registro.** Propuestas, comentarios, votos, designaciones, remociones, ingresos y gastos son públicos, en el repositorio o en ilorium.com. Una decisión que no se publica no existe.
- **Escribano, no juez, también en el gobierno.** El protocolo no certifica a ningún organismo, no ordena a ninguno en un ranking y no avala a ninguno. El gobierno decide reglas y formatos, nunca el estado de un organismo en particular, que surge solo de la evidencia. Cuando una decisión exige juicio humano (si un Vigilante es independiente, si una parada fue abusiva), se nombra el procedimiento que la resuelve, se publica su resultado y el estado afectado muestra qué parte descansa en evidencia y qué parte en esa resolución. Ninguna autoridad concede una excepción oculta para favorecer a un organismo.
- **Observabilidad no es control.** El gobierno solo puede actuar sobre lo que corre en infraestructura cuyas credenciales se pueden revocar. El protocolo no promete control sobre nada más allá de eso. Nada de este documento pausa, aísla ni toma un organismo: el protocolo registra, publica y retira reconocimiento; no opera la infraestructura de nadie.

## 2. Roles

| Rol | Quién | Decide | Nunca |
| --- | --- | --- | --- |
| **Fundador** | La persona que inició el protocolo y opera el Organismo Cero | Durante el gobierno provisorio (sección 8): publica releases y fusiona, y decide las IIP que no cambian el Genome; siempre: un asiento en el consejo de Custodios, reemplazable según la sección 4.3 | Enmienda el Genome solo, en ninguna etapa; tiene una llave de parada que no sea la del Organismo Cero; elige o remueve a un Vigilante |
| **Custodios del Genome** | Tres humanos: el fundador y dos miembros independientes (sección 4) | Las IIP que cambian el Genome, las reglas de clasificación o los formatos de registro; declarar estable una release; designar y remover Custodios y mantenedores; el presupuesto | El estado de un organismo en particular; la parada de ningún organismo; ningún voto sobre un organismo en el que tengan interés; tener ninguna llave de parada que no sea la de su propio organismo, así que un Custodio nunca es Vigilante (sección 10) |
| **Mantenedores** | Humanos designados por los Custodios | Cambios ordinarios a especificaciones y código (erratas, aclaraciones, pruebas, herramientas); fusionar pull requests que no sean cambios de método | Cambios de método sin IIP; releases sin los Custodios |
| **Vigilantes** | Humanos o instituciones gobernadas por humanos, al menos dos por organismo, independientes de él y entre sí (Genome, Ley 3; sección 5) | Activar la parada de los organismos que vigilan; reanudar después de una parada y reemplazar a un Vigilante según la sección 5 | Gobernar el protocolo; enmendar nada; tener la llave de un organismo que poseen, dirigen u operan |
| **Testigos y Oráculos** | Operadores de testigos (cofirman puntos de control) y de Oráculos (verifican desde afuera) | Nada en el gobierno; atestiguan | Atestiguar sobre un organismo en el que tengan interés o con el que compartan linaje |
| **Persona de continuidad** | Un humano nombrado por el fundador (sección 4.5) | Convoca la transición y publica el aviso si el fundador no responde; nada más | Fusionar, enmendar, votar, tener una llave, aprobar una release |
| **Contribuyentes** | Cualquiera, humano o agente | Proponer IIP, comentar, revisar, enviar pull requests | — |

**Vínculos e incompatibilidades.** *(Corregido el 2026-10-22; el primer borrador definía «interés» de modo que tener una llave de parada descalificaba a los Vigilantes, que deben tenerla.)* Un vínculo es cualquier relación entre una persona y un organismo. Todo vínculo se declara en público antes de cualquier decisión; un vínculo no declarado que se descubre después anula el voto y es causal de remoción. Qué vínculos son incompatibles depende de la función:

| Vínculo | Para actuar como Vigilante de ese organismo | Para decidir sobre ese organismo como Custodio, o atestiguar sobre él | Para evaluar con independencia una guardia o una parada |
| --- | --- | --- | --- |
| Poseer parte del organismo, dirigirlo o ser pariente de su responsable humano | Incompatible | Incompatible | Incompatible |
| Trabajar para el organismo u operarlo a diario | Incompatible | Incompatible | Incompatible |
| Tener su llave de parada por función (como responsable humano o como Vigilante) | Necesario | Incompatible | Incompatible respecto de la propia actuación como titular |
| Un pago de guardia fijo, igual y declarado (sección 5.3) | Permitido, declarado | Incompatible | Se trata como conflicto |
| Pago condicionado a una decisión, o pago desigual | Prohibido | Prohibido | Prohibido |
| Recibir pago o empleo del fundador o del Organismo Cero | — (Vigilantes del Organismo Cero: incompatible) | Incompatible para un Custodio independiente (sección 4.1) | Incompatible |

Donde este documento dice «interés», se refiere a un vínculo listado como incompatible para la función de que se trate.

## 3. Decisiones

### 3.1 Tipos de cambio

| Tipo | Ejemplos | Quién decide | Cómo |
| --- | --- | --- | --- |
| **Editorial** | Erratas, aclaraciones, traducciones, ejemplos | Un mantenedor | Pull request, una revisión de un mantenedor que no lo haya escrito |
| **Especificación** | Una sección nueva, un campo opcional nuevo, un ejemplo nuevo | Mantenedores | Pull request, comentarios públicos durante 14 días, una revisión de un mantenedor; se registra en el changelog |
| **Cambio de método (IIP)** | El Genome, una regla de clasificación, un formato de registro, los vectores de conformidad, este documento, y **cualquier cambio cuyo efecto** altere quién es elegible para un rol o qué puede hacer un rol, un resultado de conformidad, cómo se interpreta la evidencia, un permiso o requisito de seguridad, un quorum, una designación, una revisión o una sanción, sea cual sea su tamaño o el archivo donde esté *(provisorio, IIP-0004)* | Custodios del Genome | Sección 3.2 |
| **Release** | Publicar una release del protocolo; declararla estable | Provisorio: el fundador. Gobierno pleno: los Custodios | Sección 3.3 |

Un cambio se clasifica por su efecto, no por su tamaño. Un valor por defecto nuevo que cambia quién pasa o falla una prueba es un cambio de método.

### 3.2 Ilorium Improvement Proposals

1. **Propuesta.** Cualquiera abre una IIP en el repositorio público con la plantilla: motivación, especificación del cambio, qué rompe, qué no establece, vectores de prueba cuando cambian formatos. Recibe el siguiente número (desde IIP-0004; IIP-0001 a 0003 son las propuestas fundacionales del Genome). Una IIP redactada por un agente entra a la cola de revisión solo con un patrocinador humano que la firma y responde por ella (sección 7).
2. **Período de comentarios.** Público, de al menos 30 días para el Genome y este documento, de al menos 14 días para los demás cambios de método. Todo comentario queda en el registro. Los mantenedores pueden limitar el volumen de propuestas y comentarios de una misma fuente, y cerrar envíos masivos sin leerlos, diciendo el motivo en público; nunca filtran comentarios por estar escritos por agentes.
3. **Decisión.** Los Custodios votan en público. Una IIP pasa con dos votos a favor de tres. No hay veto. Un Custodio con un vínculo con algún organismo al que el cambio afecte en particular se abstiene y lo dice; si dos deben abstenerse, los suplentes (sección 4.3) ocupan su lugar; si aun así el consejo no tiene dos votantes elegibles, la IIP espera.
4. **Efecto.** Una IIP aprobada crea una versión nueva del documento afectado y una entrada en el changelog. Nunca se aplica con retroactividad: el estado de cada organismo nombra la versión contra la que fue probado.
5. **Objeción.** Cualquiera puede objetar una decisión dentro de los 14 días de su publicación, en público, con razones. Los Custodios responden en público, diciendo qué evidencia examinaron y por qué aceptan o rechazan la objeción. Una objeción a un cambio de método no lo suspende; forma parte del registro, y una IIP posterior puede revertir el cambio. Una objeción a una decisión sobre una persona (secciones 4.2, 4.3, 5.2, 5.5) sigue las reglas de esa sección.
6. **Aprobación atada al contenido.** *(Provisorio, IIP-0006.)* Toda decisión nombra la propuesta y la versión que aprueba, la huella del texto y de los artefactos aprobados, quién votó y quién se abstuvo, las fechas de comentarios y de votación, las firmas y la fecha de entrada en vigor, y las decisiones que corrige o reemplaza. Una aprobación no vale para un contenido modificado sustancialmente después; el contenido modificado se aprueba de nuevo.

### 3.3 Releases

- Una release nombra sus documentos en el manifiesto y sus vectores de conformidad en el repositorio.
- Durante el gobierno provisorio, el fundador publica las releases solo y lo dice en el changelog. Hay un solo aprobador humano; dos llaves en manos de la misma persona no son dos autoridades, y la persona de continuidad no adquiere poder de aprobación por guardar una llave.
- Bajo el gobierno pleno, una release necesita dos Custodios. **Estable** se declara solo bajo la definición de `manifest.md`, que es la normativa: los formatos están congelados, las pruebas de conformidad están publicadas, existe una política de compatibilidad escrita y hay dos Custodios independientes en funciones, y nunca durante el gobierno provisorio ni el mantenimiento restringido.

### 3.4 Empates y bloqueo

Con tres Custodios no hay empate. Si el consejo tiene menos de tres miembros elegibles para una decisión, entran los suplentes (sección 4.3). Si el consejo tiene menos de tres miembros durante más de 90 días y ningún suplente puede cubrir el asiento, ninguna IIP puede pasar; el primer deber de los Custodios que quedan es cubrir el asiento (sección 4.3).

## 4. Custodios del Genome

### 4.1 Composición
Tres humanos: el fundador y dos Custodios **independientes**. Independiente significa: sin vínculo incompatible con ningún organismo (sección 2), sin empleo ni pago del fundador ni del Organismo Cero, sin vínculo familiar con el fundador, y no Custodio de un linaje relacionado. El fundador es Custodio pero no es independiente, y la revisión de independencia de la sección 4.3 se le aplica solo respecto de vínculos distintos del Organismo Cero. Una institución no puede ser Custodio; una persona sí. Una institución puede nominar a un candidato.

### 4.2 Designación *(provisorio, IIP-0004)*
- **Declaración.** Todo candidato publica una declaración de independencia que indica, con lo que se pueda comprobar, sus relaciones de control, financiamiento, empleo y vínculos personales que afecten su independencia. «Tener interés en que Ilorium funcione» no es un vínculo; lo tiene cualquier contribuyente.
- **Dos vías para los dos primeros.** El fundador invita a un candidato. El segundo sale de una convocatoria pública de candidaturas, abierta al menos 30 días; un candidato puede ser nominado por cualquier persona o por una institución independiente. Se publica quién nominó y quién seleccionó a cada Custodio. Si la convocatoria no produce ningún candidato elegible en 90 días, el fundador puede invitar también al segundo, diciéndolo.
- **Objeción con efecto.** La designación se anuncia en público y rige 30 días después. Una objeción con razones presentada en esos 30 días, admisible según los criterios publicados (nombra un vínculo, un hecho o un incumplimiento, y no repite una ya respondida), impide que la designación entre en vigor hasta que se responda. Durante el gobierno provisorio responde el fundador en público dentro de los 30 días, diciendo qué evidencia examinó, y el período de comentarios se extiende 30 días desde esa respuesta; bajo el gobierno pleno deciden los Custodios restantes por mayoría dentro de los 30 días, con la revisión de la sección 4.6. Una objeción sin razones, o que repite una ya respondida, se registra y no suspende.
- Los Custodios siguientes son designados por los Custodios que quedan, con la misma declaración, el mismo anuncio público, los mismos 30 días y las mismas reglas de objeción.

### 4.3 Mandato, suplentes y reemplazo
- Un Custodio sirve **hasta que renuncia** o es removido. No hay mandato fijo. Si se adoptan mandatos definidos con renovación explícita se revisa cuando exista una comunidad capaz de renovar el consejo.
- **Suplentes.** *(Provisorio, IIP-0004.)* Se designan dos suplentes con el mismo procedimiento y la misma independencia que los Custodios. Un suplente ocupa un asiento solo para una decisión en la que un Custodio está recusado o un asiento está vacante, para esa decisión o hasta que se cubra la vacante, y su elegibilidad se comprueba para cada caso. Fuera de eso, los suplentes no votan.
- **Revisión de independencia.** Cada dos años, y cada vez que cambien sus circunstancias, cada Custodio reconfirma su independencia en público. Un Custodio que ya no cumple la sección 4.1 es removido. Una revisión pública de actividad e idoneidad acompaña la revisión de independencia.
- **Remoción.** Los otros dos Custodios pueden remover a un Custodio por pérdida de independencia, por un vínculo no declarado o por un incumplimiento público de este documento, en una decisión publicada con razones, después de que la persona haya tenido derecho de respuesta y con la revisión de la sección 4.6. El fundador está sujeto a la misma regla; su asiento es reemplazable, no perpetuo.
- Un asiento vacante se cubre dentro de los 90 días.

### 4.4 Retribución
Los Custodios pueden ser retribuidos con el presupuesto del protocolo (sección 6), a una tarifa publicada, igual para todos. La tarifa se publica al menos 30 días antes de aplicarse y nunca cambia con efecto retroactivo. La primera tarifa la fija el fundador antes de que asuma cualquier Custodio independiente y antes de cualquier pago. *(Revisado el 2026-10-24: sin mandatos fijos no hay «consejo anterior» que fije las siguientes.)* Un cambio posterior de tarifa es una decisión sobre personas bajo la sección 4.6 (un revisor independiente publica su dictamen primero), entra en vigor no antes de 12 meses después de publicarse, nunca es retroactivo y se publica con el presupuesto; ningún Custodio vota una tarifa durante los 12 meses anteriores a su propia revisión de independencia. Cobrar del presupuesto del protocolo no es un empleo con el fundador ni con el Organismo Cero. *(Provisorio, IIP-0004.)*

### 4.5 Continuidad si el fundador no está disponible *(provisorio, IIP-0004)*
- El fundador nombra en público, con aceptación firmada, una **persona de continuidad**: un humano que, si el fundador no respondió por los canales declarados durante 90 días, puede hacer dos cosas y nada más: convocar la transición al gobierno pleno según la sección 8 y publicar el aviso. La persona de continuidad nunca fusiona, enmienda, vota, tiene una llave ni aprueba una release.
- Recuperar las cuentas y la infraestructura del fundador es un asunto aparte, a cargo de quien el fundador designe en su plan de recuperación; recuperar el acceso no confiere autoridad para cambiar reglas.
- Las contingencias operativas y de seguridad que no pueden esperar 90 días (una clave comprometida, un certificado, la renovación del dominio) siguen procedimientos previamente autorizados, publicados en el inventario de autoridad (`governance/authority-inventory-v1.md`), y se limitan a mantener funcionando lo que existe.
- Hasta que la persona de continuidad esté nombrada y haya aceptado, esta sección está incompleta y lo dice acá: **persona de continuidad: pendiente de designación por el fundador.**

### 4.6 Revisión de las decisiones sobre personas *(provisorio, IIP-0004)*
Una decisión que designa, remueve, suspende o niega la independencia a una persona (Custodio, suplente, mantenedor o Vigilante) es revisada, antes de entrar en vigor, por un **revisor independiente por caso**: una persona sin vínculo con nadie involucrado, tomada de una lista pública, elegida de forma trazable. El revisor tiene 30 días para publicar un dictamen consultivo. No vincula; la decisión debe responderlo por escrito, y ambos se publican juntos. Si ningún revisor de la lista acepta en 14 días, la decisión avanza como **no revisada**, lo dice en público y se revisa apenas un revisor acepte; el silencio nunca es conformidad, y hasta que la lista exista toda decisión de este tipo es no revisada y lo dice. Las medidas urgentes sobre accesos (revocar una credencial) pueden ser provisionales; una remoción definitiva exige el procedimiento, el derecho de respuesta y la revisión. Es una revisión consultiva, y su límite se declara como tal.

## 5. Vigilantes

El Genome define qué son los Vigilantes y cuándo tienen una llave de parada (Ley 3, IIP-0002). Esta sección dice cómo se los califica, verifica, paga y reemplaza, y qué pasa después de una parada. Nada de lo que sigue permite al protocolo pausar u operar un organismo: el protocolo registra la guardia, la publica y retira el reconocimiento de nacimientos; no controla la infraestructura de nadie.

### 5.1 Calificación
Un Vigilante es un humano, o una institución gobernada por humanos con una persona nombrada que responde por ella, que:
- puede ser contactado por un canal declarado en la Spore del organismo (`stop_key_holders`), probado con un simulacro de parada;
- demostró, en un simulacro registrado en los Strata, que puede activar la parada dentro del tiempo de respuesta declarado;
- declaró en público todo vínculo con el organismo, con su linaje y con los demás Vigilantes del mismo organismo, y no tiene ninguno que la sección 2 liste como incompatible para un Vigilante. Tener la llave y recibir el pago de guardia igualitario son la función, no una descalificación.

### 5.2 Verificación de independencia
- La independencia es **por propiedad, financiamiento y jurisdicción**: los Vigilantes de un mismo organismo no pertenecen a la misma parte, no son financiados por la misma parte (salvo el pago de guardia del organismo, sección 5.3) y, cuando es posible, no están bajo la misma jurisdicción. Dos Vigilantes que dependen de la misma cuenta, dispositivo o vía de recuperación comparten un punto de falla y no son independientes a ese efecto.
- La declaración de cada Vigilante es pública y está enlazada desde la Spore. Cualquiera puede impugnarla en público con un motivo documentado; los Custodios resuelven la impugnación dentro de los 30 días, con la revisión de la sección 4.6, y un Vigilante que resulte no independiente pierde la llave.
- **Concentración y atención, publicadas.** *(Provisorio, IIP-0005.)* Cada Vigilante publica cuántos organismos vigila y qué proporción de su ingreso de guardia proviene de cada uno. No hay tope fijo: un Vigilante nuevo con un solo organismo está concentrado por definición. La verificación de independencia lee esas cifras como riesgo, y puede exigir a un Vigilante que reduzca su concentración o su carga de atención antes de aceptar un organismo nuevo.
- Un Vigilante puede vigilar varios organismos, pero nunca dos organismos del mismo linaje. *(En revisión: con un linaje grande esta regla exige dos titulares distintos por organismo; su costo en titulares, atención y continuidad se mide en el piloto y se resuelve antes de alentar el crecimiento de linajes. Cualquier alternativa mantiene independientes entre sí a los Vigilantes de un mismo organismo.)*

### 5.3 Pago sin captura
- Un organismo puede financiar su guardia. Paga **el mismo monto a cada Vigilante**, a una tarifa declarada en la Spore, por un canal que no puede cambiar sin la firma de los Vigilantes.
- Un organismo nunca paga a un Vigilante por una decisión, nunca paga más a un Vigilante que a otro, y nunca elige ni remueve a un Vigilante.
- **Pago durante una parada o una disputa.** *(Provisorio, IIP-0005.)* Los pagos de guardia siguen sin cambios mientras un organismo está parado y mientras una parada o la independencia de un Vigilante están en revisión, para que parar no le cueste nada al Vigilante y reanudar no compre nada. Un organismo que deja de pagar a sus Vigilantes se muestra así en sus Vital Signs; eso nunca es causal para remover a un Vigilante.
- El presupuesto del protocolo puede pagar a los Vigilantes de los organismos que no pueden hacerlo (sección 6), para que ningún organismo quede sin vigilar por falta de dinero. Hoy el protocolo no tiene presupuesto para eso, y lo dice.

### 5.4 Estados de guardia y reemplazo *(revisado el 2026-10-22; provisorio, IIP-0005)*
El primer borrador exigía dos Vigilantes y mayoría para reemplazar a uno, de modo que con exactamente dos, si uno desaparecía el otro no podía actuar. Las reglas ahora son:

| Estado | Condición | Efecto |
| --- | --- | --- |
| **Completa** | Al menos dos Vigilantes activos, cada uno con un simulacro aprobado dentro de la ventana de conformidad | Guardia plena; los nacimientos bajo este organismo pueden ser válidos |
| **Degradada** | Exactamente un Vigilante activo | La parada sigue funcionando. Ningún nacimiento bajo este organismo es válido hasta que la guardia esté completa. El Vigilante que queda y los Custodios designan un Vigilante interino de la lista pública de voluntarios calificados dentro de los 14 días; el Vigilante que se reemplaza no vota su propio reemplazo |
| **Ausente** («sin vigilar») | Ningún Vigilante activo | Su compuerta de nacimiento se cierra. Su estado muestra «sin vigilar». Los Custodios designan Vigilantes interinos de la lista pública dentro de los 14 días; los interinos sirven hasta que se restablezcan los Vigilantes del organismo |

- El denominador de toda votación de Vigilantes es la cantidad de Vigilantes activos para esa decisión, excluido quien esté recusado; un Vigilante investigado no vota su propia remoción.
- Un Vigilante que deja de responder a los simulacros es reemplazado por los demás Vigilantes activos o, si queda uno o ninguno, por el procedimiento de arriba.
- Un organismo que sigue degradado o sin vigilar más allá de su ventana de recuperación declarada se informa en el Codex. El protocolo no puede pausarlo ni lo hace; registra el estado y retira el reconocimiento de nacimientos.

### 5.5 Parada, reanudación y sanción *(provisorio, IIP-0005)*
Parar, reanudar y sancionar son tres decisiones distintas.
- **Parar.** Cualquier Vigilante puede activar la parada. La parada se registra de inmediato con un motivo categorizado y una justificación accesible a revisores autorizados; después sigue una explicación pública, compatible con la confidencialidad (una justificación puede contener una vulnerabilidad o datos privados). Haber activado una parada no es un conflicto de interés y no excluye a ese Vigilante de la decisión de reanudar; las recusaciones exigen una causa concreta.
- **Reanudar.** Un organismo reanuda solo después de que: se evaluó la causa; se revocaron las credenciales comprometidas; se declaró el alcance de la reanudación (igual que antes, o reducido); decidieron los Vigilantes activos, excluido quien esté recusado con causa; y se aprobó un simulacro de parada. Un simulacro aprobado muestra que el mecanismo de parada funciona; no muestra por sí solo que el incidente se resolvió, así que la evaluación se registra aparte. Si los Vigilantes activos discrepan, decide la mayoría de los elegibles; sin mayoría, el organismo sigue parado y los Custodios designan un Vigilante interino dentro de los 14 días para desempatar.
- **Sancionar.** Una parada prudente que resulta una falsa alarma no es mala fe y no trae sanción. Un Vigilante pierde la llave solo por una causa definida (un vínculo incompatible no declarado, una parada o una negativa a parar contra la evidencia, no responder a los simulacros), después del derecho de respuesta, la revisión de la sección 4.6 y un reemplazo efectivo. Retirar el reconocimiento público de un Vigilante y revocar su acceso técnico son dos actos; los dos se registran.
- **Quién decide cuando quedan pocos Vigilantes elegibles.** Si las recusaciones dejan menos de dos Vigilantes elegibles para una decisión de reanudación o reemplazo, los Custodios designan Vigilantes interinos de la lista pública para esa decisión.

## 6. Financiamiento

### 6.1 Hoy
El protocolo lo financia el fundador, de su bolsillo. Se declara en público y se actualiza cuando cambia.

### 6.2 Qué acepta el protocolo
- **Donaciones** al protocolo, de cualquiera, con una regla pública de uso.
- **Subvenciones (grants)** que el protocolo otorga a quienes construyen sobre él: una segunda implementación, colectores, índices alternativos, testigos, investigación. El protocolo no se queda con ninguna participación en lo que financia, y ningún jurado puede tener vínculo con quien recibe.

### 6.3 Para qué es el dinero
Infraestructura, testigos, auditorías, pruebas de conformidad, retribución de mantenedores, Custodios y Vigilantes, traducciones, subvenciones. Cada ingreso y cada gasto se publican.

### 6.4 Lo que el protocolo nunca hace
- **Nunca invierte en organizaciones ni en startups**, incluidos organismos, candidatos o aliados. Es una decisión institucional: un escribano con acciones en un organismo deja de ser neutral (Ley 6), y organismos pagados por el protocolo limitarían lo que la primera cohorte puede mostrar sobre adopción independiente. Las consecuencias legales de un fondo que invierte donaciones difieren según la jurisdicción y quedan para la revisión legal en cada una; la decisión del protocolo no depende de ellas.
- Si el fundador o cualquier otro invierte en organizaciones, lo hace a través de otra entidad, sin el nombre ni el dinero del protocolo. Todo organismo en el que esa entidad tenga participación lo declara en su Spore, y se muestra en sus Vital Signs. Un piloto financiado puede igual producir evidencia técnica válida; lo que no puede mostrar es adopción espontánea, y el vínculo se declara.
- Nunca vende certificaciones, sellos, rankings ni posiciones. No hay token.

### 6.5 Conflicto de interés
Quien decide a dónde va el dinero declara cualquier vínculo con el destinatario y se abstiene. Las subvenciones y los pagos a un Custodio, un mantenedor o un Vigilante los deciden quienes no los reciben.

### 6.6 Entidad receptora
Las donaciones necesitan una entidad que pueda recibirlas y rendir cuentas: un fiscal host (por ejemplo Open Collective) al principio, una fundación después, en la jurisdicción que elijan los Custodios. Hasta que esa entidad exista, el protocolo no acepta donaciones. La entidad se constituye antes de la transición al gobierno pleno, o la transición registra por qué no.

## 7. Qué puede hacer una IA en el gobierno

- **Puede:** proponer IIP, comentar, revisar código y documentos, enviar pull requests con su propia identidad, mantener documentos, operar índices y testigos, correr pruebas de conformidad. Los agentes se identifican como IA (Ley 5), no firman nada a nombre de un humano, y sus pull requests se etiquetan como escritos por agentes. Un commit de un agente lleva la firma del humano u organización responsable. *(Provisorio, IIP-0004:)* una IIP redactada por un agente entra a la cola de revisión solo cuando un contribuyente humano con identidad verificable la patrocina con su firma y responde por ella; los mantenedores pueden limitar el volumen de propuestas y comentarios de una misma fuente y cerrar envíos masivos, diciendo el motivo en público.
- **Nunca:** votar; ser Custodio, suplente, mantenedor, Vigilante ni persona de continuidad; tener una llave de parada; aceptar una llave; designar o remover a nadie; mover dinero; fusionar un cambio de método.
- **Más adelante, por IIP:** redactar borradores de enmiendas, operar la infraestructura del protocolo, ejecutar pruebas de conformidad como servicio. Cada ampliación de lo que puede hacer una IA necesita una IIP decidida por Custodios humanos, con evidencia de la capacidad y de sus límites, bajo el procedimiento reforzado de la sección 10.
- **Alcance.** Esta sección rige el protocolo. Cómo operan los organismos es otra cosa: dentro de un organismo, los agentes ejecutan y deciden dentro de los permisos concedidos, y la Prueba de Vida mide cuánto; esa es la autonomía que el protocolo existe para observar.
- **La hipótesis del fundador, expresada como suya.** El fundador cree que, a medida que los organismos se vuelvan mucho más capaces, algún día podrían merecer una parte en el gobierno de su propia especie, bajo una llave humana. El protocolo no toma posición sobre eso. Si ese día llega, el único camino es una IIP aprobada por Custodios humanos con evidencia; nunca una capacidad que un organismo declare de sí mismo, que la Ley 5 prohíbe, y nunca un cambio que suspenda una cerradura. El protocolo no define ningún criterio de superinteligencia, así que ninguna capacidad puede disparar por sí sola una transferencia de poder.

## 8. Del gobierno provisorio al pleno *(revisado el 2026-10-22; provisorio, IIP-0004)*

Se mantienen separados dos hitos: la **adopción externa** (alguien distinto del fundador opera un organismo que llega a Observado) muestra interés; la **madurez institucional** (un consejo completo con un procedimiento) muestra capacidad de gobernarse. El primer borrador hacía del primero la única llave; ahora es un hito, no la condición.

| Etapa | Condición | Quién publica releases | Quién decide las IIP |
| --- | --- | --- | --- |
| **Provisorio** (ahora) | Desde la publicación del repositorio público (la fecha de inicio se registra en el changelog y nunca se reinicia con una versión nueva) hasta que el consejo de Custodios esté constituido y pueda actuar, y a más tardar **18 meses** después de esa fecha de inicio | El fundador solo, declarado en el changelog | El fundador, como único Custodio, para las IIP que no cambian el Genome, con los períodos de comentarios públicos ya vigentes; los cambios al Genome solo como borradores identificados como suyos, ratificados por el consejo completo |
| **Pleno** | Desde el día en que se constituye el consejo (tres Custodios y dos suplentes en funciones) | Dos Custodios | Los tres Custodios, dos de tres |
| **Mantenimiento restringido** | Si vencen los 18 meses y el consejo está incompleto | Solo releases de seguridad, por el fundador o, si no responde, por la persona nombrada en su plan de recuperación bajo los procedimientos preautorizados del inventario de autoridad, cada una declarada como tal (la persona de continuidad no designa a nadie; sección 4.5) | Ninguna IIP pasa. Solo avanzan las correcciones de seguridad, la continuidad de la infraestructura (dominio, certificados, claves) y el procedimiento para constituir el consejo, bajo el inventario de autoridad. El fundador sigue convocando candidatos pero no tiene autoridad unilateral sobre las reglas. La falta de candidatos nunca prorroga el gobierno provisorio |

- Los dos Custodios independientes y los dos suplentes se invitan desde el comienzo del gobierno provisorio, para que el consejo esté completo lo antes posible; los 18 meses son un límite, no una meta. El número es una elección institucional para esta etapa, no una cifra validada con datos.
- Cuando el primer organismo externo llegue a Observado, se anuncia en el Codex como el hito de adopción, sea cual sea el estado del consejo.
- La transición se anuncia en el changelog y en el Codex. Desde entonces, el asiento del fundador es uno de tres.
- **Estable** no puede declararse durante el gobierno provisorio ni durante el mantenimiento restringido.
- **Pilotos.** Los organismos que adoptaron el protocolo durante el gobierno provisorio nombran en su Spore las versiones que aceptaron; una IIP aprobada nunca se les aplica con retroactividad (sección 3.2.4), y el changelog dice cómo migran.

## 9. Transparencia

- Decisiones, votos, designaciones, remociones, declaraciones de vínculos e independencia, objeciones y revisiones: en el repositorio, bajo `governance/`.
- **Inventario de autoridad.** `governance/authority-inventory-v1.md` lista cada recurso por el que el protocolo se publica o se controla (repositorios, dominio, DNS, alojamiento, registro de paquetes, claves de firma, recuperación de cuentas, fondos): quién lo tiene, con qué permisos, cómo se transfiere y quién puede actuar solo. Sin secretos. Se actualiza cada vez que cambia un titular o un permiso y se revisa cada trimestre. *(Provisorio, IIP-0006.)*
- Presupuesto, ingresos y gastos: publicados al menos cada trimestre.
- Paradas activadas por Vigilantes: registradas en los Strata del organismo e informadas en el Codex.
- Las revisiones externas del protocolo, incluidas las escritas por modelos de IA, se publican bajo `governance/reviews/` con los documentos que recibió cada revisor y sus límites, después de quitar datos privados. Su coincidencia es un insumo de revisión, nunca una validación.
- Este documento cambia solo por IIP, con el período de comentarios más largo, y sus reglas centrales solo según la sección 10.

## 10. Cambios constitucionales *(provisorio, IIP-0004)*

Las siguientes reglas son **constitucionales**: los criterios de independencia (sección 4.1), el umbral de dos de tres (sección 3.2), las reglas de designación y revisión de personas (secciones 4.2, 4.3, 4.6), la condición de transición y el límite de 18 meses (sección 8), la prohibición de que un Custodio tenga una llave de parada que no sea la de su propio organismo, la prohibición de que una IA vote o tenga una llave (sección 7), y esta sección.

Un cambio a una regla constitucional necesita, además de la sección 3.2: un período de comentarios de al menos 90 días; una justificación escrita; un revisor independiente por caso (sección 4.6) que publique un dictamen antes del voto; un voto de dos de tres Custodios sin suplentes en su lugar; y, **cuando exista un cuerpo capaz de ratificar** (mantenedores y Vigilantes activos en funciones, con reglas publicadas de pertenencia, conflictos y votación), la ratificación por ese cuerpo. Hasta que ese cuerpo exista, la limitación se declara acá: los cambios constitucionales los decide el consejo solo bajo el procedimiento reforzado, y eso es una debilidad conocida, no una virtud. No se exige unanimidad: le daría un veto a una persona y no impediría que tres Custodios capturados votaran juntos.

**Constitución inicial** *(agregado el 2026-10-24)*. Las reglas de arriba no se adoptaron bajo esta sección: no existía ningún consejo que pudiera adoptarlas. Las adoptó la decisión provisoria del fundador el 2026-10-22, como la única autoridad que existía, y están listadas en la IIP-0004 con el hash y la fecha del texto adoptado. Su estado es **provisorio** hasta que el consejo pleno las ratifique bajo el procedimiento reforzado, que es la primera decisión constitucional que toma el consejo. Hasta entonces: el fundador puede acotar su propia autoridad bajo las secciones 8 y 10 pero nunca ampliarla, nunca reiniciar el reloj de 18 meses y nunca agregar una regla a esta lista; cualquier cambio a las secciones 8 o 10 durante el gobierno provisorio entra en vigor solo después del período de comentarios de 90 días; y esta excepción se aplica una sola vez, a la primera constitución, y no crea ningún mecanismo permanente.

## Preguntas abiertas

- La entidad receptora y su jurisdicción, y su plazo respecto de la transición.
- La retribución del fundador como mantenedor, si la hay: la tarifa y quién la fija una vez que exista el consejo.
- La lista pública de Vigilantes voluntarios calificados e interinos: cómo se mantiene, quién la verifica y qué responsabilidad legal asume un Vigilante por tener una llave (a responder con asesoramiento legal antes de reclutar Vigilantes reales).
- La escala de la guardia: la regla «nunca dos organismos del mismo linaje» multiplica los titulares con el linaje; su costo se mide en el piloto.
- Un procedimiento de respuesta a incidentes a nivel del protocolo (un organismo que evade la Probe, un latido falsificado, un Vigilante de mala fe), dentro del límite de que el protocolo registra y publica y no aísla (a escribir antes de que empiece la guardia real).
- Qué muestra el protocolo cuando una orden judicial contradice una parada o una restricción (la Ley 0 dice que el Genome nunca obliga a violar la ley de una jurisdicción; el registro de ese conflicto todavía no está especificado).
- Resistencia sybil más allá del patrocinio humano de las IIP.
- Un cuerpo capaz de ratificar cambios constitucionales (sección 10): su composición y sus reglas.
- Quién selecciona, acepta, aprovisiona, revoca y demuestra la revocación del acceso técnico de un Vigilante, separado de la decisión pública, y qué pasa cuando no existe ningún Vigilante elegible (sección 5; IIP-0005).
- Una reserva financiada para los pagos de guardia durante una parada, y la regla cuando los fondos no alcanzan (sección 5.3): una obligación escrita no es un mecanismo.
