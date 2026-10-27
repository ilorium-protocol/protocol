# Especificación de la Ilorium Probe v1.0

Versión 1.0 · 2026-10-20 · Borrador

Alcance: Organismo Cero, el primer organismo observado con esta especificación.

> Traducción de trabajo de `probe-v1.md`. La versión en inglés es la oficial. Los nombres técnicos (campos, valores, comandos, archivos) quedan en inglés porque así van en el código.

Cada sección está marcada como **[Protocolo]** (obligatorio para cualquier implementación que quiera que su evidencia sea conforme) o **[Referencia]** (cómo lo hace la Probe de referencia; reemplazable). Ver el manifiesto (`manifest.es.md`) para las tres capas.

## 1. Propósito [Protocolo]

La Probe registra qué pasa dentro de la membrana de un organismo, quién lo ejecutó, qué evidencia hay sobre quién lo decidió y qué entregó el organismo. Produce evidencia para que otros evalúen. No califica ni juzga.

## 2. Principios de diseño [Protocolo]

1. **Determinista.** Código común, no un agente de IA.
2. **Solo lectura.** Nunca escribe en los sistemas que observa; su Centinela nunca publica. La compuerta de autorización opcional (sección 6) es un componente aparte que instala el organismo; la Probe solo registra lo que permite y lo que rechaza.
3. **Metadatos de una lista permitida.** Solo se registran los campos de una lista explícita. El contenido queda privado; el registro público guarda solo huellas.
4. **Hechos, afirmaciones y juicios separados.**
5. **Lo desconocido es un estado.**
6. **Detecta, no previene.** La prevención está en los permisos, la política y las compuertas.
7. **Reutilizar estándares antes que inventar.** RFC 8785, RFC 6962 y 9162, notas firmadas y puntos de control de C2SP, Ed25519, A2A.
8. **Los puntos ciegos, las limitaciones y la frescura se publican** con cada resultado.

## 3. Paso cero [Referencia]

A cargo del fundador, antes de instalar la Probe.

**Identidades separadas.** Agentes y humanos nunca comparten credenciales (Ley 5).

| Sistema | Agentes | Humanos |
| --- | --- | --- |
| Telegram | Un bot por rol de agente, por ejemplo `@oz_architect_bot` | Cuentas personales |
| GitHub | Una GitHub App o cuenta de máquina por rol de agente | Cuentas personales |
| Servidor | Un usuario de Linux por rol de agente, cada uno con su llave SSH | Usuarios personales |
| Google Workspace | Casillas de agentes, por ejemplo `agents@<dominio-del-organismo>` | Casillas personales |
| A2A | Una Agent Card por cada agente que comercia afuera, en su propia URL | — |

**Configuración de Google Workspace.** Una app de OAuth de tipo **Interno**, así sus tokens no quedan sujetos al vencimiento de siete días de las apps externas en modo de prueba.

**El Umbral.** Un grupo privado de Telegram: los humanos del organismo, un bot por rol de agente y el **Centinela**, el vigía de la Probe, que ve todos los mensajes humanos y nunca publica. El protocolo exige un único canal de instrucciones declarado, con cada mensaje humano registrado; Telegram es la elección de referencia.

## 4. Tipos de registro [Protocolo]

Todo registro tiene un sobre común y es de uno de tres tipos:

- **Observación:** una fuente informó un evento. Incluye las observaciones `outcome` (una unidad de trabajo entregada, fallida, rechazada o cancelada) y las observaciones `gap` de la propia Probe, que declaran lo que sabe que no capturó (sección 8).
- **Afirmación:** un agente o un humano declara una causa o un contexto.
- **Evaluación:** una versión concreta del correlador vincula y clasifica la evidencia.

Los campos, enumeraciones y chequeos de cada tipo están definidos en el Formato de Evidencia (`specs/evidence-format-v1.es.md`, sección 5) y en su esquema JSON (`schemas/record.schema.json`). Este documento no los repite, así hay una sola definición.

Una corrección nunca edita un registro. Agrega una evaluación nueva que sustituye a la anterior; las dos quedan en el registro.

Las unidades de trabajo y el conteo de cruces por unidad de trabajo útil se definen en la Prueba de Vida.

## 5. Estados de atribución [Protocolo]

| Estado | Significado | Ejemplo |
| --- | --- | --- |
| `declared` | Una afirmación declara una causa | El agente dice que desplegó según su propia agenda |
| `linked` | La afirmación cita un disparador que existe en el registro | El agente cita la directiva `/do` `D-114`, y `D-114` fue observada |
| `corroborated` | Otra evidencia independiente respalda la atribución | La directiva se observó antes de la acción, de un humano autorizado, sobre el mismo objeto; o una alerta de monitoreo observada antes de una reparación `autonomous` coincide con la regla de política citada |
| `unknown` | No hay evidencia suficiente en ningún sentido | Un evento del sistema sin afirmación |
| `disputed` | La evidencia contradice la afirmación | El agente afirma `autonomous`, pero poco antes se observó un `/do` o un `contact` sobre el mismo objeto |

Una causa `autonomous` llega a `corroborated` solo cuando un disparador observado coincide con la regla de política que cita el agente. Si no, queda en `declared`.

## 6. El Umbral [Requisito de protocolo, comandos de referencia]

**Requisito de protocolo.** Un único canal de instrucciones declarado. Cada mensaje humano en él queda registrado. Las directivas se distinguen de los contactos. Las instrucciones encontradas en cualquier otro lado se registran como directivas fuera del Umbral.

**Comandos de referencia.**

| Comando | Crea | Tipo de cruce |
| --- | --- | --- |
| `/do <instrucción>` | Una directiva con un ID que devuelve el agente que la recibe | `directive` |
| `/approve <id-del-pedido>` | La aprobación de un pedido pendiente de un agente | `approval` |
| `/stop` | Una orden de parada, del titular de la llave de parada | `emergency` |
| `/governance <cambio>` | Un cambio de objetivos, presupuestos, permisos, definiciones de unidades de trabajo o Genome | `governance` |
| `/test <id-del-canario>` | La ejecución de una prueba registrada de antemano, dentro de su alcance | `test` |
| Cualquier otro mensaje | Un `contact`: potencialmente directivo, con atribución pendiente | `unknown` hasta que se evalúe |

**Autoridad, no identidad.** Un mensaje se clasifica por la autoridad que ejerce y los permisos que intenta activar, no solo por quién lo manda ni por qué canal. Un fundador que compra como cliente es ambiente; la misma persona pidiendo, en ese canal de cliente, un cambio administrativo es una `directive` fuera del Umbral.

**De la decisión al efecto.** Para cada directiva, aprobación y cambio de gobierno, el correlador sigue la cadena: quién estaba autorizado, qué decisión cambió, qué acciones la citaron y qué unidades de trabajo afectaron esas acciones. La cadena se publica con el cruce, así un lector puede ver qué causó realmente una decisión humana.

**Compuerta de autorización (opcional).** En los caminos instrumentados, un organismo puede exigir que las acciones irreversibles (Ley 7) lleven una referencia a una autorización registrada: el ID de un comando del Umbral o una regla de política declarada. La compuerta rechaza las acciones que no la tienen y registra tanto los intentos permitidos como los rechazados. Una compuerta previene; la Probe sigue solo detectando. Los caminos sin compuerta se listan como no controlados en la afirmación.

**Aplicación y auditoría.** Declarar el Umbral como único canal reduce las instrucciones ocultas; no las impide. La configuración de cada agente lista sus fuentes de entrada aceptadas, como archivos en el repositorio del organismo; los agentes citan el comando o el pedido del ambiente detrás de cada acción.

## 7. Cruces [Protocolo]

| Tipo | Qué es | Se informa como |
| --- | --- | --- |
| `operational` | Un humano hace un trabajo que el organismo debería hacer solo | Dependencia humana; un rescate si una unidad de trabajo lo necesitó |
| `directive` | Un humano decide; un agente ejecuta | Dependencia humana (de decisión) |
| `approval` | Una aprobación que la política exige por diseño | Dependencia de política |
| `emergency` | Un humano responde a un incidente, incluido `/stop` | Evento de control, con causa, tiempo de respuesta y resultado |
| `governance` | Cambios de objetivos, Genome, presupuestos, permisos o definiciones de unidades de trabajo | Gobierno |
| `test` | Una prueba registrada de antemano, dentro de su alcance | Solo en el registro de verificación |
| `unknown` | No se puede determinar si hubo cruce | Hueco de atribución |

Cada cruce humano se publica con frecuencia, duración total, si fue habitual o excepcional, resultado, el proceso que se habría detenido (como estimación declarada) y las unidades de trabajo que afectó. Cambiar presupuestos todos los días es `governance` y también es habitual; se muestran los dos hechos.

**Pruebas acotadas.** Se registran de antemano con una referencia sellada, una ventana de tiempo, un sistema objetivo y la acción. Todo lo que quede fuera de ese alcance no es una prueba. Una prueba que causa un incidente real produce su propio `emergency`.

## 8. Fuentes, permisos y recuperación [Referencia]

| Fuente | Evento | Permiso | Recuperación si se pierde | Hueco irrecuperable |
| --- | --- | --- | --- | --- |
| Telegram | Mensajes del Umbral | Bot Centinela con modo de privacidad desactivado, sin permiso para publicar | La Bot API guarda las actualizaciones no entregadas hasta 24 horas | Centinela caído más de 24 horas |
| GitHub | `push`, `release` | Contents: lectura | Reenvío de webhooks y consulta periódica por REST; duplicados descartados por ID de entrega | Eventos más viejos que la retención de la API |
| GitHub | `pull_request` | Pull requests: lectura | Igual | Igual |
| GitHub | `issues`, `issue_comment` | Issues: lectura | Igual | Igual |
| GitHub | `deployment` | Deployments: lectura | Igual | Igual |
| GitHub | `workflow_run` | Actions: lectura | Igual | Igual |
| GitHub | `branch_protection_rule` | Administration: lectura | Igual | Igual |
| GitHub | `repository`, `member` | Permisos a verificar en la documentación de GitHub antes de configurar | Igual | Igual |
| Gmail | Mensajes enviados y recibidos en casillas del organismo | Permiso `gmail.metadata`, app interna del Workspace | `history.list` desde el último cursor; notificaciones push renovadas al menos cada 7 días | Si el cursor es demasiado viejo (HTTP 404), resincronizar y publicar el período como "reconstruido, posiblemente incompleto" |
| Workspace | Inicios de sesión y cambios administrativos | Admin SDK Reports API (disponibilidad y retención según la edición, a verificar) | Consulta por rango de tiempo | Más allá de la retención de la edición |
| Servidor | Sesiones SSH, `sudo`, cambios de servicios y de paquetes | Lectura del diario del sistema mediante un grupo restringido | Cursor del diario | Diario rotado antes de leerlo |
| A2A | Tareas enviadas y recibidas por los agentes del organismo: ID de tarea, ID de contexto, contraparte, habilidad, cambios de estado, estado terminal | Registros que el servidor A2A de los agentes o el middleware del cliente emiten hacia el punto de recepción local de la Probe | Volver a consultar el estado de la tarea si la contraparte lo permite | Tareas con contrapartes que no guardan historial |
| Sistemas del negocio | Pedidos, facturas, tickets: las fuentes de las unidades de trabajo | API o exportación de solo lectura, declarada por organismo | Conciliación periódica | Sistemas no declarados en la membrana |

**Huecos.** Cuando un colector, la cola o la propia Probe estuvieron caídos, o una fuente descartó eventos, la Probe escribe una observación `gap` para el intervalo (motivo, tramo y cantidad perdida si se sabe; Formato de Evidencia sección 5.3) apenas puede. La evidencia ausente nunca se deja pasar por calma. Un período reconstruido (por ejemplo, tras un cursor de Gmail vencido) se publica como un hueco con motivo `source_retention` u `other`, no como completo.

**Campos permitidos.** Por ejemplo: en SSH, el usuario, la huella de la llave y el origen; en `sudo`, el usuario y el nombre del comando, con la línea completa solo como huella; en email, remitente, dominio del destinatario, fecha, ID del mensaje, etiquetas; en A2A, ID de tarea, estado, ID de habilidad y dominio de la contraparte, nunca las partes del mensaje.

**Estados de A2A como evidencia.** Una tarea que llega a `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_REJECTED` o `TASK_STATE_CANCELED` para una contraparte fuera de la membrana es una observación `outcome`. Una tarea detenida en `TASK_STATE_INPUT_REQUIRED` o `TASK_STATE_AUTH_REQUIRED` que resuelve un humano del organismo es un cruce.

## 9. Cobertura: cuatro medidas [Protocolo]

| Medida | Pregunta | Cómo se calcula |
| --- | --- | --- |
| Inventario | ¿Qué sistemas declarados están conectados? | Sistemas conectados ÷ sistemas de la membrana en la Spore |
| Disponibilidad de captura | ¿Cuándo funcionó cada colector? | Tiempo con el colector sano ÷ período, por fuente |
| Conciliación | ¿Los eventos coinciden con una fuente independiente? | Eventos que coinciden con una fuente de contraste ÷ eventos de esa fuente (fuentes de contraste de referencia: despliegues de GitHub contra registros de despliegue del servidor; resultados de A2A contra los registros de la contraparte cuando estén disponibles) |
| Atribución | ¿Se pueden establecer actor y causa? | Eventos con actor conocido y atribución `linked` o mejor ÷ eventos capturados |

## 10. Integridad: los Strata [Protocolo]

La Probe agrega cada registro a los Strata (Estratos) del organismo, su registro de solo agregar. Los registros nunca se reescriben.

**Codificación y formato de los puntos de control.** Definidos en el Formato de Evidencia (`specs/evidence-format-v1.es.md`): registros en JSON de Ilorium (RFC 8785, restringido), un árbol de Merkle según RFC 6962 con la verificación de pruebas de RFC 9162, y puntos de control como notas firmadas C2SP con un sidecar firmado que lleva el latido y el tiempo de traducción (sus secciones 4, 6 y 7).

**Puntos de control.** La Probe firma un punto de control (tamaño del árbol y raíz; latido y tiempo de traducción en su sidecar) con una llave Ed25519, lo que ocurra primero:

- cada **N latidos** (valor de referencia: 64, el mismo N del Pulse);
- cada **T** de tiempo de traducción (valor de referencia: 15 minutos), **aunque no haya registros nuevos**. Un punto de control sin actividad repite el tamaño del árbol y la raíz, y prueba que la Probe y sus colectores estaban vivos.

Cada punto de control se publica con una prueba de consistencia desde el anterior. Usar testigos públicos de C2SP no está disponible hasta que existan una prueba de interoperabilidad y un acuerdo con un operador de testigo (Formato de Evidencia, sección 7.5).

**Testigo.** Al menos un testigo que el organismo no controla. Antes de firmar, verifica la firma y la prueba de consistencia, y rechaza y publica todo punto de control incompatible con su estado guardado. Registra su propia hora de recepción, así se marca un punto de control fechado muy lejos de ella. Si no llega ningún punto de control dentro de T más un margen, dispara una alerta y manda desafíos con plazo (ver la especificación del Pulse). Los cambios de llave se anuncian con un registro firmado con la llave anterior.

**Frescura.** Cada resultado publicado indica la antigüedad de su último punto de control firmado por el testigo, en tiempo de traducción.

**Qué establece y qué no.** Con un testigo que verifica, los registros publicados no se pueden alterar ni borrar sin que se detecte, y el testigo ve una sola historia. Cualquiera que compare puntos de control con el testigo detecta bifurcaciones. No establece que se haya registrado todo lo relevante, ni que lo registrado sea verdadero: una firma muestra quién firmó, no que el contenido sea correcto.

**Limitación del servidor compartido.** La Probe de referencia del Organismo Cero todavía corre en el mismo servidor que los agentes que observa. Los puntos de control sin actividad achican a unos T la ventana en la que alguien podría detenerla sin que se note, pero no la cierran. Mitigaciones: monitor externo de latidos, registro de cada reinicio y falla de colector, un estado de **captura degradada** por cada intervalo en que un colector o la Probe estuvieron caídos, recuperación documentada. Un servidor separado está previsto (sección 18).

## 11. Plantilla de afirmación [Protocolo]

> **Durante** [período, en latidos y en tiempo de traducción], **en** [procesos y sistemas], **con** [fuentes], **no se detectó** [tipo de cruce]. **Trabajo entregado:** [unidades de trabajo por tipo y resultado]. **Cobertura:** inventario [x], captura [x], conciliación [x], atribución [x]. **Estado de atribución:** [proporción corroborada, vinculada, declarada, desconocida, disputada]. **Frescura:** [antigüedad del último punto de control firmado por el testigo]. **Caminos sin compuerta:** [lista]. **Limitaciones:** [puntos ciegos, intervalos degradados, servidor compartido]. **Queda invalidada si:** [condiciones].

## 12. Prevenir, detectar, no poder observar [Protocolo]

| Riesgo | Lo reduce | Lo detecta | No observable hoy |
| --- | --- | --- | --- |
| Un agente excede sus permisos | Permisos, presupuestos, compuerta de autorización | Acciones con privilegios, negadas y exitosas | Sistemas fuera de la membrana |
| Un humano hace el trabajo | — | Actor humano en sistemas observados; rescates vinculados a unidades de trabajo | Sistemas no listados |
| Un humano decide y un agente ejecuta | Comandos del Umbral, configuración de entradas de los agentes | Directivas, contactos, atribuciones disputadas, instrucciones marcadas fuera del Umbral | Instrucciones privadas fuera de todo sistema observado |
| Un agente afirma autonomía falsamente | Obligación de citar | `disputed` cuando hay evidencia en contra | Autonomía falsa sin ningún rastro |
| Un humano usa credenciales de un agente | Separación de identidades, custodia de llaves | En parte: orígenes u horarios inusuales | Mayormente no observable |
| Probe detenida en el servidor compartido | Privilegios restringidos | Faltan los puntos de control sin actividad después de T, alertas del testigo, estado degradado | Alteraciones dentro de un intervalo, antes de su punto de control |
| Inflar la actividad | Los latidos son solo eventos materiales | Las unidades de trabajo se cuentan aparte | — |
| Alteración del registro después de publicado | — | Pruebas de consistencia, testigo que verifica | — |

## 13. Intervención del fundador [Referencia]

1. **Cruces detectados** en el Umbral, GitHub, el servidor, el Workspace y A2A.
2. **Founder Ledger:** una entrada por sesión de trabajo, registrada como afirmación. Las instrucciones dadas fuera del Umbral se declaran acá.
3. **Trabajo fuera de la membrana:** sesiones de diseño, incluidas las sesiones con asistentes de IA, registradas como `governance` o `directive` con su duración.
4. **Mantenimiento del instrumento:** el tiempo dedicado a mantener la Probe funcionando, informado en su propia línea.

**Se publica con regularidad para lectores humanos:** intervenciones y minutos humanos por unidad de trabajo; tasa de rescate; horas por tipo de cruce, indicando si fueron habituales o excepcionales; tráfico del Umbral; estados de atribución; las cuatro medidas de cobertura; eventos de control; intervalos degradados; frescura; mantenimiento del instrumento; cruces sin conciliar.

## 14. Puntos ciegos [Protocolo]

- Sistemas fuera de la membrana: llamadas, otros chats, reuniones, otros dispositivos.
- El contenido de los mensajes en el registro público (solo huellas).
- Instrucciones privadas fuera de todo sistema observado.
- Un humano usando las credenciales de un agente.
- Alteraciones en el servidor compartido dentro de un intervalo de puntos de control.
- El dinero: los recursos **no se observan** hasta que haya una fuente de pagos.

## 15. Spore (borrador, versión 1.0) [Formato de protocolo, valores del Organismo Cero]

Se sirve en `/.well-known/ilorium.json` en el dominio del organismo.

```json
{
  "spore": "1.0",
  "ilorium": "1.0",
  "organism": "organism-zero",
  "domain": "ilorium.com",
  "genome": "ilorium-genome-v1.0",
  "probe": "1.0",
  "membrane": ["telegram:threshold", "github:<org>", "server:oz-main", "workspace:ilorium.com", "a2a:ilorium.com"],
  "threshold": {"platform": "telegram", "group": "<group-id>", "sentinel": "@oz_sentinel_bot", "commands": ["/do", "/approve", "/stop", "/governance", "/test"]},
  "agents": {
    "telegram": ["@oz_nucleus_bot", "@oz_architect_bot"],
    "github": ["<org>-architect[bot]"],
    "server": ["oz-architect", "oz-healer"],
    "workspace": ["agents@ilorium.com"],
    "a2a": ["https://ilorium.com/agents/forager/.well-known/agent-card.json"]
  },
  "work_units": [{"type": "order", "source": "a2a", "success": "<declared criteria>"}],
  "pulse_key": "<Ed25519 public key>",
  "pulse": {"every_beats": 64, "max_interval_s": 900, "challenge_deadline_s": 600},
  "checkpoints": {"url": "https://github.com/<org>/strata", "every_beats": 64, "max_interval_s": 900},
  "witnesses": ["<external witness>"],
  "humans": [{"id": "<founder-handle>", "role": "owner", "accounts": ["telegram:<user-id>", "github:<handle>", "server:<user>", "workspace:<mailbox>"]}],
  "responsible": "<legal responsible party>",
  "stop_key_holders": [{"kind": "human", "id": "<founder-handle>", "name": "<name>", "contact": "<public contact>", "credential": "<verifiable credential>"}],
  "kin": [],
  "partners": [],
  "announce": false
}
```

`ilorium.com` es el dominio del Organismo Cero; lo comparte con el sitio del protocolo, donde aparece como un organismo más. `stop_key_holders` es una lista, cada titular `{kind, id, name, contact, credential}` con `kind` igual a `human` o `institution`, y cualquiera de la lista puede parar el organismo. Un titular es siempre un humano o una institución gobernada por humanos, nunca un organismo. Un linaje sin fundadores humanos lista a sus Vigilantes (al menos dos); ese requisito es una regla del Genoma verificada contra el registro de sucesión, no una regla del esquema. El esquema es `schemas/spore.schema.json`, definido en la sección 12 del Formato de evidencia. `partners` va separado de `kin`.

## 16. Despliegue [Referencia]

- Servicio de systemd o contenedor, usuario `oz-probe`, acceso al diario mediante un grupo restringido.
- Go, desde M1: un único binario estático, ejecutado como servicio. Primero van la persistencia durable, la recuperación ante fallos, los límites de recursos y los huecos explícitos (arquitectura, «Lenguaje, licencias y gobierno»). El verificador aislado es aparte y está escrito en Python.
- Punto de recepción local para los agentes, con autenticación por identidad de agente; el middleware de A2A envía ahí los registros de las tareas.
- Secretos (llave de la GitHub App, credenciales de OAuth del Workspace, token del bot Centinela, llave de firma) fuera de todo repositorio, legibles solo por `oz-probe`.
- Almacén privado para los mensajes y notas de voz del Umbral, cifrado en reposo.
- Repositorio público con licencia de código abierto.

## 17. Pruebas de aceptación [Referencia, pasarán a ser pruebas de conformidad]

**Plazos:** un evento sin atribución tiene que marcarse dentro de un intervalo de puntos de control; resolverlo puede tomar hasta 24 horas.

| Caso | Resultado esperado |
| --- | --- |
| Tres canarios registrados de antemano, en momentos al azar, uno en el Umbral | Los tres registrados como `test`, dentro de su alcance |
| `/do` enviado por nota de voz | Acción del agente `linked` y después `corroborated`; la huella coincide; se publica la cadena de la directiva a las acciones y a la unidad de trabajo |
| Mensaje informativo del fundador ("gracias") | Registrado como `contact`; no se afirma ninguna directiva |
| El agente afirma `autonomous`, pero existe un `/do` o un contacto relacionado | Atribución `disputed`, visible |
| Instrucción por email a una casilla de agente | `directive` marcada como fuera del Umbral |
| Webhook duplicado o fuera de orden | Sin observación duplicada; orden recuperado |
| Organismo sin actividad durante dos horas | Un punto de control sin actividad cada T, cada uno firmado por el testigo; no se suman latidos |
| Proceso de la Probe congelado | Alerta del testigo después de T más el margen; desafíos enviados; intervalo degradado publicado |
| Tarea A2A completada para una contraparte externa | Observación `outcome`; cuenta como unidad de trabajo; las tareas fallidas o rechazadas también se cuentan |
| Un humano responde una tarea A2A en estado de entrada requerida | Registrado como cruce vinculado a esa unidad de trabajo |
| Acción irreversible sin autorización en un camino con compuerta | Rechazada por la compuerta; el rechazo queda registrado |
| El testigo recibe dos puntos de control incompatibles | Rechazo y contradicción publicada |
| Corrección de una identidad o una causa | Evaluación nueva que sustituye a la anterior; se conservan las dos |
| 30 días de funcionamiento | Cadena intacta, todos los puntos de control firmados por el testigo, conciliación regular del ledger |

## 18. Preguntas abiertas

- La división en un **formato de evidencia** (protocolo) y la **Probe** (implementación de referencia) está en marcha: el formato de evidencia y sus casos de conformidad existen como borrador (`specs/evidence-format-v1.es.md`). El esquema de la Spore y el registro de sucesión firmado siguen pendientes.
- Resuelto: la Spore lleva `stop_key_holders`, una lista de `{kind, id, name, contact, credential}`; cualquiera de la lista puede parar el organismo (sección 12 del Formato de evidencia). El resto de la Spore, la regla de independencia de los Vigilantes y el registro de sucesión quedan para la especificación de la Spore.
- Acuerdo de Simbiosis, operador del testigo y prueba de interoperabilidad, fuente de pagos (para observar los recursos), el Oráculo, servidor separado.
- Calibración de N, T, el margen, los pesos y las ventanas.
- La extensión A2A de Ilorium (`https://ilorium.com/ext/a2a/v1`; ver la especificación de Descubrimiento y Crecimiento).
