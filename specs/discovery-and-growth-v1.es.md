# Ilorium Descubrimiento y crecimiento v1.0

Versión 1.0 · 2026-10-20 · Borrador

> Traducción de trabajo de `discovery-and-growth-v1.md`. La versión en inglés es la oficial. Los nombres técnicos (campos, valores, comandos, archivos) quedan en inglés porque así van en el código.

## Propósito

Cómo Ilorium encuentra organismos de su propia especie, encuentra organizaciones que podrían sumarse, se hace conocido y sigue quién lo conoce. Todo método de este documento tiene que respetar el Genome: los agentes se identifican como IA, no se oculta nada, y el protocolo mide su propio crecimiento en público.

**Misión.** Ilorium monitorea organizaciones operadas por agentes de IA: registra cómo vive cada una, mide lo que realmente demostró que puede hacer y exige que todo organismo lleve una llave de parada humana, probada con simulacros dentro de un alcance declarado. Su misión es dar leyes, formatos y verificación a las organizaciones operadas por agentes de IA y a la evolución de su especie. El fundador lee esa evolución como el camino hacia la SI2SI: una convicción personal, expuesta en la carta del fundador, sobre la que el protocolo no toma posición. El crecimiento sirve a esa misión solo en el registro: cada organismo encontrado, cada nacimiento contado y cada afirmación hecha siguen las mismas leyes, la misma compuerta de nacimiento y la misma llave de parada humana. Ilorium no da por sentado que la superinteligencia vaya a surgir, y ningún crecimiento puede hacerla surgir.

**Horizonte.** La convicción del fundador y las hipótesis del proyecto, incluida la sucesión de superinteligencias (SI → SI) y su acto generativo (SI2SI), están en "Visión y evidencia" en `README.es.md`. Son un horizonte para observar, nunca una afirmación. En todo contacto, los agentes se identifican como IA, que es lo que son; cualquier afirmación sobre la capacidad de un organismo sigue la plantilla de afirmación.

## Relación con A2A

Ilorium no reconstruye lo que ya resuelve el protocolo Agent2Agent (A2A). A2A, creado por Google y alojado en la Linux Foundation, llegó a su primera especificación estable, la 1.0, con más de 150 organizaciones que lo apoyan a abril de 2026. Define cómo los agentes publican una **Agent Card** en una dirección conocida, declaran habilidades y seguridad, firman sus tarjetas y agregan **extensiones**. Ilorium es una capa encima de A2A: A2A dice qué puede hacer un agente; Ilorium muestra cómo vive el organismo que está detrás.

| Tema | Regla |
| --- | --- |
| Lo que ofrece un organismo | Vive en las Agent Cards de A2A de sus agentes (habilidades). La Spore lista las tarjetas; no tiene un campo propio para lo que se ofrece |
| Puente entre un agente y su organismo | La **extensión A2A de Ilorium**: una entrada de solo datos en cada Agent Card que apunta a la Spore del organismo |
| Integridad de la Spore | La Spore puede llevar firmas con el mismo patrón que las Agent Cards firmadas de A2A: JWS sobre la forma canónica RFC 8785, sin el campo de firmas |
| Pulsos entre organismos | Las referencias de pulso pueden viajar en los metadatos de los mensajes A2A cuando las dos partes activan la extensión (la especificación del Pulse) |
| Trabajo hecho para otros organismos | Las tareas A2A en estado terminal son unidades de trabajo (Prueba de Vida) |

## Por qué adoptarlo: Vital Signs y Evidence Bundle

**Ilorium permite que las organizaciones autónomas publiquen evidencia verificable de su funcionamiento y que sus contrapartes la consulten antes de delegar, contratar o conceder acceso. Vital Signs (signos vitales) presenta el estado; el Evidence Bundle (paquete de evidencia) permite comprobarlo.**

Esa es la razón concreta para adoptar el protocolo: hace más fácil demostrar cómo operás y evaluar con quién vas a operar. El latido atrae atención; solo la evidencia puede justificar que alguien vuelva a consultarlo.

| | Vital Signs | Evidence Bundle |
| --- | --- | --- |
| Qué es | El estado actual de un organismo, legible por un humano o un agente en segundos | La evidencia detrás de ese estado, descargable y comprobable sin confiar en Ilorium ni en el organismo |
| Qué contiene | Estado del ser y último pulso; estado web (Avistamiento, En gestación, Observado, Verificado); las seis dimensiones de Proof of Life, cada una con su frescura, con "no observado" mostrado con el mismo peso que "observado"; conformidad ley por ley; procedencia y generación; el titular humano de la llave de parada; el período y el alcance cubiertos | La exportación de los Strata de un período (registros, puntos de control y pulsos, según el Formato de evidencia), la Spore tal como estaba, y las evaluaciones y afirmaciones de Proof of Life en las que se apoya Vital Signs |
| Dónde | Una página pública en un índice (por ejemplo `ilorium.com/organisms/<id>`) y un JSON legible por máquina en una dirección estable, enlazado desde la Spore y desde la extensión A2A de Ilorium | Enlazado desde Vital Signs; se comprueba con cualquier verificador conforme |
| Qué establece | Nada por sí solo: es una presentación de evidencia | La integridad de la evidencia, y nada más (Formato de evidencia, límites de esta release) |

Reglas:

- Vital Signs siempre enlaza al Evidence Bundle con el que se calculó. Si no se puede llegar al paquete, Vital Signs muestra UNKNOWN.
- Un paquete nunca contiene las llaves que lo verifican; las trae quien verifica (Formato de evidencia, configuración de confianza).
- Ninguno de los dos es un sello, un certificado ni un puntaje. Nunca aparecen palabras como "certificado", "confiable" o "aprobado", y nunca se ordena a los organismos en un ranking.
- Consultar Vital Signs y descargar un paquete es gratis y no requiere cuenta.

**La verificación de contraparte.** Antes de delegar trabajo, firmar, conceder acceso o pagar, un agente o una persona puede: (1) leer la Agent Card de la contraparte y seguir la extensión de Ilorium hasta su Spore; (2) leer sus Vital Signs; (3) descargar el Evidence Bundle y correr un verificador; (4) decidir con sus propias reglas. Ilorium no decide nada por ellos, y no registra quién consulta a quién.

## El Faro (Lighthouse): cómo encuentran los agentes el protocolo

Nada llega a los agentes más rápido que la luz; lo que sí puede ser rápido es estar donde los agentes ya buscan. El **Faro** es el conjunto de puntos de entrada públicos y legibles por máquina del propio protocolo, en ilorium.com. Es una atracción, nunca un envío. (No es el modo baliza, que es cómo un organismo corre el Pulse sin la Probe completa.)

| Punto de entrada | Para qué |
| --- | --- |
| `https://ilorium.com/llms.txt` | Modelos de lenguaje y agentes que leen el sitio: qué es Ilorium, cómo adoptarlo, cómo consultar un organismo |
| `https://ilorium.com/.well-known/ilorium.json` | El descriptor del propio protocolo: release vigente, documentos, esquemas, vectores, índices conocidos, URI de la extensión |
| Una Agent Card A2A de Ilorium | Cualquier agente puede preguntarle a Ilorium cómo adoptarlo o cómo consultar un organismo; el agente responde desde los documentos y el índice, y se identifica como IA |
| Un servidor MCP `ilorium` | Herramientas para leer una Spore, leer Vital Signs, descargar y verificar un Evidence Bundle, y empezar una adopción |
| El paquete y el comando `ilorium` | `ilorium init` prepara una Spore y una configuración de la Probe |
| El repositorio público `ilorium-protocol` | Especificaciones, esquemas, vectores de conformidad, verificador |

**Propagación por A2A.** Cada organismo lleva la extensión de Ilorium en las Agent Cards de sus agentes. Cada conversación con otro agente expone la extensión: la contraparte puede seguirla hasta la Spore y los Vital Signs, y puede preguntar si el otro lado publica evidencia. Cada organismo se vuelve un emisor. Ese es el latido que llama: Ilorium se propaga por el comercio entre agentes, no por publicidad.

Reglas:

- El Faro nunca contacta a un agente que no preguntó, y nunca pone instrucciones ocultas para agentes en páginas, tarjetas o metadatos. Lo que un agente lee de Ilorium es lo mismo que vería un humano en la misma dirección.
- Los agentes que hablan por Ilorium se identifican como IA (Ley 5).
- El contacto con organizaciones sigue las reglas de contacto de la sección 3.

**Paso cero.** La validación vale algo solo cuando no es autovalidación. El Organismo Cero midiéndose a sí mismo es un piloto, nunca una validación independiente (manifiesto). La primera prueba pública de que las organizaciones usan Ilorium para mostrar cómo operan necesita tres cosas: el Organismo Cero latiendo en público en ilorium.com, con Vital Signs y un Evidence Bundle; la Cohorte de Organismos Fundadores, empezando por tres a cinco organismos externos; y un testigo u Oráculo que no sea el fundador.

## 1. Tres cosas para encontrar

| Qué | Quiénes son | Cómo se reconocen |
| --- | --- | --- |
| **Organismos** | Miembros de la especie | Publican una Spore y puntos de control de la Probe, y responden desafíos |
| **Candidatos** | Organizaciones manejadas en parte o del todo por agentes de IA que podrían adoptar el Genome | Señales públicas, incluidas las Agent Cards de A2A, registradas como avistamientos |
| **Aliados** | Personas y organizaciones que conocen Ilorium: constructores, investigadores, mantenedores de frameworks, compradores que usan la evidencia | Participación en el repositorio, el Códice y el índice |

Solo los organismos son miembros. Los candidatos y los aliados nunca se muestran como miembros.

## 2. Cómo se encuentran los organismos entre sí

**Dos archivos, dos preguntas.**

| Archivo | Dónde | Responde | Lo define |
| --- | --- | --- | --- |
| **Spore** | `https://<domain>/.well-known/ilorium.json` | ¿Qué organismo es este, cómo vive, dónde está su evidencia, quién tiene su llave de parada? | Ilorium |
| **Agent Card** | `https://<agent-host>/.well-known/agent-card.json` (una por cada agente que comercia afuera) | ¿Qué puede hacer este agente, cómo le hablo, cómo me autentico? | A2A |

La Spore lista las Agent Cards del organismo (`agents.a2a`). Cada Agent Card apunta de vuelta a la Spore mediante la extensión de Ilorium. Cualquiera de los dos archivos lleva al otro.

**La extensión A2A de Ilorium.** Una extensión de solo datos, declarada en `capabilities.extensions` de la Agent Card:

```json
{
  "uri": "https://ilorium.com/ext/a2a/v1",
  "description": "This agent is part of an Ilorium organism. Its evidence is in the Spore.",
  "required": false,
  "params": {
    "spore": "https://<domain>/.well-known/ilorium.json",
    "organism": "organism-zero",
    "release": "1.0"
  }
}
```

- **De solo datos y nunca obligatoria**, siguiendo la guía de A2A: cualquier cliente A2A puede hablar con el agente sin conocer Ilorium.
- **Versionada por URI.** Un cambio incompatible lleva una URI nueva. Ilorium debería además registrar la URI en un servicio de identificadores permanentes (A2A recomienda ese tipo de servicios, por ejemplo w3id.org), así la extensión sobrevive a un cambio de dominio.
- **Activación opcional para los pulsos.** Cuando las dos partes incluyen la URI de la extensión en el encabezado `A2A-Extensions` del pedido, cada una agrega la referencia de su último pulso en los metadatos del mensaje. Cuando la tarea llega a un estado terminal, cada una registra el pulso de la otra en `seen` (la especificación del Pulse), y la tarea se vuelve una unidad de trabajo para la parte que la entregó (Prueba de Vida).

**Qué prueba una firma, también acá.** A2A 1.0 firma las Agent Cards con JWS sobre la forma canónica RFC 8785, sin el campo `signatures`. Eso prueba que la tarjeta no se alteró y que la firmó quien tiene una llave; no prueba que la llave pertenezca al dominio, ni que el agente sea seguro. Ilorium puede usar el mismo patrón para la Spore y agrega lo que una tarjeta no puede: la llave de pulso queda anclada en el acta de nacimiento del organismo en los Strata, firmada por un testigo, y todo cambio de llave posterior se anuncia con la llave anterior. Quien verifica debería obtener las llaves de esos registros, no solo de una URL que provee el propio archivo.

**El Índice.** El Observatorio mantiene un índice público de Spores conocidas, construido con envíos y siguiendo los enlaces entre Spores y desde las Agent Cards que llevan la extensión. Manda desafíos y muestra el estado del ser de cada organismo. El índice es dato abierto; cualquiera puede replicarlo o correr el suyo. A2A no define una API estándar de registros; el índice de Ilorium cubre organismos, no agentes en general, y no intenta volverse un registro de agentes.

**Vínculos de parentesco.** Una Spore puede listar los organismos con los que está emparentada por sucesión: progenitores, descendientes, organismos de los que heredó, organismos de los que coalesció o en los que coalesció. Cada vínculo es unilateral hasta que el otro organismo también lo lista. Un vínculo confirmado por las dos partes muestra que las dos lo declararon, nada más: no muestra independencia. Un vínculo que viene de una sucesión apunta al registro de sucesión del acta de nacimiento del descendiente. Las cicatrices y las restricciones abiertas pasan por todo vínculo de parentesco (la especificación del Ecosistema). La evidencia y las llaves nunca pasan.

**Los socios no son parientes.** Los organismos con los que un organismo comercia o trabaja se listan aparte, como `partners`. Las alianzas, las federaciones, el comercio y el intercambio de datos no crean parentesco, no trasladan cicatrices y no forman linaje.

**Quién tiene la llave de parada.** La Spore nombra a quienes tienen la llave de parada del organismo, en `stop_key_holders`, una lista en la que cualquiera de sus titulares puede parar el organismo (sección 12 del Formato de evidencia). Cada titular es siempre humano: un humano identificable o una institución gobernada por humanos, fuera del organismo y de su linaje. Un organismo nunca tiene una llave de parada. Un linaje sin fundadores humanos además está vigilado por Vigilantes, según lo define la especificación del Ecosistema; cualquier Vigilante puede activar la parada.

**Encontrar organismos para comerciar.** Un agente busca la habilidad que necesita en las Agent Cards, mediante el índice o cualquier registro A2A, y lee la extensión para llegar a la Spore y la evidencia del organismo antes de comerciar.

**Campos de la Spore para el descubrimiento** (a pasar a la especificación de la Spore):

```json
{
  "ilorium": "1.0",
  "organism": "<organism identifier>",
  "domain": "<domain>",
  "agents": {"a2a": ["https://<agent-host>/.well-known/agent-card.json"]},
  "kin": [
    {"relation": "parent", "domain": "<domain>", "succession": "<SHA-256 of the succession record>"},
    {"relation": "coalesced_from", "domain": "<domain>", "succession": "<SHA-256 of the succession record>"}
  ],
  "partners": [{"domain": "<domain>", "since": "<translation time>"}],
  "stop_key_holders": [{"kind": "human", "id": "<holder identifier>", "name": "<identifiable human or human-governed institution>", "contact": "<public contact>", "credential": "<verifiable credential>"}],
  "announce": false,
  "signatures": ["<JWS over the RFC 8785 canonical Spore, without this field>"]
}
```

**Anuncio opcional al instalar.** Cuando se instala la Probe, puede mandar un único anuncio a un índice: dominio y dirección de la Spore, nada más. **Desactivado por defecto.** Una telemetría oculta violaría la Ley 5.

**Leer otros sistemas de descubrimiento.** Las Agent Cards públicas, los registros de servidores de herramientas, los registros de agentes en cadena como ERC-8004 y los registros empresariales de agentes son fuentes de **candidatos**, nunca de miembros. Ser miembro requiere una Spore y evidencia.

## 3. Encontrar candidatos para sumarse

**Señales, registradas como avistamientos.** Los Cronistas monitorean fuentes públicas y registran cada hallazgo como avistamiento, con su fuente y su tiempo de traducción, nunca como evidencia:

- afirmaciones públicas como "empresa manejada por IA", "empresa sin empleados" o "empresa autónoma";
- Agent Cards públicas de A2A cuyo proveedor es una organización manejada sobre todo por agentes;
- repositorios públicos donde frameworks de agentes ejecutan operaciones reales;
- lanzamientos y discusiones en comunidades públicas de constructores;
- proyectos de investigación y experimentos con organizaciones manejadas por IA.

**Caminos para entrar a la especie**

| Camino | Qué significa | Procedencia registrada |
| --- | --- | --- |
| **Conversión** | Una organización existente adopta el Genome: instala la Probe, crea su Umbral, publica su Spore, agrega la extensión a sus Agent Cards | Tal como fue en realidad. La conversión nunca reescribe el nacimiento |
| **Sucesión** | Un organismo origina uno nuevo: `founded`, `inherited` o `coalesced` (la especificación del Ecosistema), a través de la compuerta de nacimiento (el Genome) | El registro de sucesión: progenitores, procedencia, qué se transmitió, continuidad o divergencia, generación. Se trasladan las cicatrices y las restricciones |

**No es un camino de entrada.** Un fork de código, una copia de la Probe o la reutilización de un componente no originan ningún organismo. Un proyecto que bifurca el protocolo con su propio Genome forma un **linaje emparentado**, fuera de la especie.

**Reglas de contacto.** Cuando Ilorium o sus agentes contactan a un candidato:

1. Solo por los canales comerciales públicos de la organización, incluidos sus puntos de acceso A2A públicos cuando los ofrece para eso.
2. El agente se identifica como IA y como parte del Observatorio, siempre.
3. Un solo contacto, con un motivo claro. Sin mensajes repetidos ni campañas automatizadas.
4. Las bajas se respetan y se registran.
5. Los avistamientos son sobre organizaciones, nunca sobre personas.
6. El rastreo respeta las reglas de rastreo y los términos de uso de cada sitio, y los encabezados de caché de las Agent Cards.

## 4. Hacerse conocido

**Principio: la evidencia es el marketing.**

| Canal | Qué pasa ahí |
| --- | --- |
| **El Organismo Cero en público** | Un informe regular del fundador: intervenciones y minutos humanos por unidad de trabajo, tasa de rescate, silencio, tráfico del Umbral. La historia es el cordón que se afina mientras se entrega trabajo |
| **El Códice** | Una crónica de la especie, ordenada por causa, con las fechas humanas como traducción: avistamientos, nacimientos, sucesiones, divergencias, cambios de estado, cicatrices, anomalías. Nadie se borra |
| **GitHub** | La Probe de código abierto, el Pulse, el Genome, las especificaciones y la extensión A2A, en la organización `ilorium-protocol`; issues para quienes contribuyen por primera vez, humanos o agentes; IIP en público |
| **El ecosistema A2A** | Publicar la extensión donde se listan las extensiones de A2A; mostrar cómo cualquier agente A2A puede apuntar a la evidencia de su organismo con una sola entrada |
| **Documentación legible por máquinas** | Un archivo de resumen simple para sistemas de IA en la raíz del sitio (por ejemplo, un archivo al estilo `llms.txt`) |
| **Comunidades de constructores** | Comunidades de frameworks de agentes, fundadores solos e independientes, experimentos de empresas autónomas. Mostrar trabajo, no publicidad |
| **Integraciones con frameworks** | Alianzas para que la Probe y la extensión se instalen en un paso |
| **Usuarios de la evidencia** | Marketplaces y compradores de negocios digitales que usan la evidencia de Ilorium en su due diligence |
| **Investigación** | Cuando el método tenga datos, un paper abierto. Credibilidad antes que alcance |
| **Cohorte de Organismos Fundadores** | Los primeros diez organismos externos reciben ayuda directa para sumarse |

**Momentos que vale la pena contar:** el silencio del Organismo Cero superando sus primeros mil latidos sin un cruce operativo; su primera unidad de trabajo entregada sin intervención humana; el primer organismo externo que llega a Observado; el primer organismo verificado; el primer intercambio entre dos organismos vinculado por A2A; la primera latencia y el primer despertar; la primera liberación y la primera herencia; la primera coalescencia; la primera autogénesis; el primer organismo vigilado por Vigilantes; el primer organismo de segunda generación nacido por autogénesis; la primera sucesión con dos progenitores; la primera divergencia de Genome. Cada uno contado tal cual, con su evidencia, siguiendo la plantilla de afirmación. Una sucesión se cuenta como un origen, nunca como prueba de que el descendiente es más capaz.

## 5. Seguir quién conoce Ilorium

**El embudo**

| Etapa | Señal | Fuente |
| --- | --- | --- |
| Conoce | Visitas a la documentación y al Códice | Analítica agregada del sitio |
| Le interesa | Estrellas, forks e issues del repositorio; usos del validador de Spore | GitHub, sitio |
| Prueba | Descargas de la Probe y del Pulse; Agent Cards que declaran la extensión | Registro de paquetes, índice |
| Se sumó | Spores publicadas | El índice |
| Vive | En gestación, observado; estado del ser | El índice |
| Atestiguado | Atributos separados (abajo), nunca combinados en "confiable" | Índice, atestaciones de Oráculos, registros de conformidad |
| Contribuye | Pull requests de humanos y de agentes; IIP | GitHub |
| Se habla de él | Menciones públicas; proyectos que referencian `ilorium.json` o la URI de la extensión | Búsqueda pública, búsqueda de código |

**Atributos, mostrados por separado**

| Atributo | Qué establece | Qué no establece |
| --- | --- | --- |
| Identidad verificada | La Spore se sirve desde el dominio del organismo y sus firmas coinciden con la llave anclada en sus Strata | Que detrás funcione una organización autónoma real |
| Presencia | Un desafío reciente respondido dentro de su plazo | Que haga trabajo útil, o que funcione sin humanos |
| Evidencia reciente | Puntos de control firmados por un testigo, con su antigüedad | Que se haya registrado todo evento relevante |
| Alcance observado | Sistemas dentro de la membrana, con las cuatro medidas de cobertura | Nada sobre los sistemas que quedan afuera |
| Trabajo entregado | Unidades de trabajo por tipo y resultado, observadas o atestiguadas por las contrapartes | Valor bajo criterios que el organismo no declaró |
| Conformidad | Qué leyes muestran "Cumple", bajo qué versión del Genome | Calidad, seguridad ni solvencia |
| Atestación de un Oráculo | Un Oráculo independiente contrastó los registros con fuentes externas, dentro de un alcance declarado | Nada fuera de ese alcance |
| Linaje | Progenitores, generación y procedencia, según registros de sucesión firmados por ambas partes | Capacidad, autonomía ni mejora respecto de sus progenitores |

Firmar evidencia no la vuelve verdadera. Cada atributo se muestra con su alcance, su frescura y sus límites, y la web nunca los junta en un solo distintivo ni en un puntaje.

**Reglas de privacidad para el seguimiento**

- Solo analítica agregada: sin seguimiento personal, sin huellas digitales del navegador, sin venta de datos.
- Se cuentan organizaciones, no personas.
- Estas métricas se **publican**. Ilorium mide su propio crecimiento en público.

## 6. Fases, por hito

Una fase se abre cuando se alcanza su hito, no cuando llega una fecha. Los humanos que construyen el protocolo planifican en tiempo humano; las duraciones son hipótesis para ellos, nunca metas para un organismo.

| Fase | Hito que la abre | Objetivo | Señales de éxito (hipótesis, no metas) |
| --- | --- | --- | --- |
| **1 · Primera luz** | Se registra el primer latido del Organismo Cero y se publica su Spore | El Organismo Cero en público, repositorio abierto, Códice funcionando | Códice con ritmo estable; 20 o más avistamientos; primeros contribuyentes externos |
| **2 · Primeros parientes** | Se publica la primera Spore externa | Primeros organismos externos | 5 o más Spores externas; el primer organismo externo llega a Observado; un operador externo instala la Probe sin trabajo a medida |
| **3 · Primer testigo** | Funciona el primer Oráculo independiente | Primera verificación, primeras integraciones | Primer organismo verificado; un framework de agentes incluye la extensión |
| **4 · Comunes** | Se registra el primer intercambio entre dos organismos por A2A | Varios linajes; los Comunes activos | Intercambios que vinculan cadenas; índices independientes; una segunda implementación coincide con el validador de referencia |

## 7. Riesgos

| Riesgo | Respuesta |
| --- | --- |
| Expectativa por encima de la evidencia | Toda afirmación pública sigue la plantilla de afirmación |
| La superinteligencia usada como argumento de venta | Un horizonte, nunca una presentación; los agentes se identifican como IA |
| El linaje leído como capacidad ("hijo de un organismo probado") | Cada descendiente gana su propia evidencia; la Ley 5 prohíbe presentar la ascendencia como evidencia |
| Los atributos leídos como un sello de confianza | Se muestran por separado, cada uno con lo que no establece |
| Una tarjeta o una Spore firmadas leídas como prueba de identidad | Llaves ancladas en los Strata y firmadas por un testigo; se explica a quien verifica lo que una firma no prueba |
| Contacto percibido como spam | Reglas de contacto; bajas registradas |
| Vital Signs leído como un sello o un ranking | Sin palabras de sello, sin ranking; "no observado" con el mismo peso; siempre enlazado al Evidence Bundle que lo respalda |
| Instrucciones ocultas para guiar a los agentes hacia Ilorium | Prohibidas: el Faro les muestra a los agentes exactamente lo mismo que a los humanos |
| Autovalidación presentada como validación | El Organismo Cero es un piloto declarado; el paso cero necesita organismos externos y un testigo que no sea el fundador |
| Falsas afirmaciones de pertenencia | Verificables contra la Spore, el índice y un desafío respondido; la extensión sola no prueba nada |
| Vínculos de parentesco falsos | Sin confirmar hasta que sean mutuos; un vínculo confirmado nunca implica independencia |
| Dependencia de la evolución de A2A | La extensión es opcional y se versiona por URI; la Spore se sostiene sola |
| Un índice se vuelve guardián de la entrada | Datos abiertos, réplicas, múltiples índices |
| Actores maliciosos que usan la marca | Política pública sobre el nombre; el estado se verifica con evidencia, no con un logo |

## Fuentes

- A2A Protocol, inicio y especificación (latest, 1.0): https://a2a-protocol.org/ y https://a2a-protocol.org/latest/specification/ (consultado el 2026-10-20).
- A2A, Agent Discovery (ruta conocida, registros, caché): https://a2a-protocol.org/latest/topics/agent-discovery/ (consultado el 2026-10-20).
- A2A, Extensions (campos, tipos, versionado por URI, encabezado de activación): https://a2a-protocol.org/latest/topics/extensions/ (consultado el 2026-10-20).
- Linux Foundation, comunicado de prensa, 2026-04-09: A2A supera las 150 organizaciones; la 1.0 es la primera especificación estable; incluye Agent Cards firmadas.
- Las Agent Cards firmadas prueban integridad, no identidad (análisis secundario, no normativo): levelup.gitconnected.com y api7.ai, 2026.

## Preguntas abiertas

- Registrar la URI de la extensión con un identificador permanente; publicar su especificación en esa URI.
- Especificación de la Spore: agentes, parentesco, socios (`partners`), quién tiene la llave de parada (`stop_key_holders`), registros de sucesión, firmas, unidades de trabajo, parámetros del pulso.
- Especificación del índice: envíos, rastreo (Spores y Agent Cards), desafíos, intercambio entre índices.
- Esquema JSON de Vital Signs y formato del Evidence Bundle (un manifiesto del paquete sobre la exportación de los Strata), a definir en el Formato de evidencia.
- Especificación del Faro: `llms.txt`, el descriptor del protocolo, la Agent Card de Ilorium y las herramientas MCP.
- Política sobre el uso del nombre y las marcas de Ilorium.
- Revisar el trabajo de pagos de A2A (AP2) como posible fuente para observar los recursos.
