# Proyectos relacionados

Documento vivo · 2026-10-20 · Revisado el 2026-10-24 · No forma parte del protocolo

> Traducción de trabajo de `related-projects.md`. La versión en inglés es la oficial.

## Por qué existe este archivo

Van a aparecer muchos proyectos cercanos a Ilorium: protocolos de agentes, lenguajes de políticas, registros, esquemas de certificación, registros verificables. Este archivo anota cada uno que encontramos, para que Ilorium pueda tomar ideas, conceptos y código, dar crédito, no reconstruir lo que ya existe y tener claro qué lo hace distinto.

Cada entrada lleva fecha y fuentes. Los hechos sobre un proyecto se separan de nuestro juicio sobre él. Antes de copiar código, hay que revisar la licencia del código de ese proyecto, que puede ser distinta de la licencia de su especificación, y conservar sus avisos. Las entradas nuevas se agregan acá sin entrada en el changelog; cuando una idea se aplica a una especificación, ese cambio sí va al changelog.

## En qué se diferencia Ilorium

Los proyectos parecidos construyen sobre todo herramientas: una forma de que los agentes se hablen, una forma de codificar reglas, una forma de certificar, una forma de gobernar una tarea. Ilorium es otro tipo de idea:

| La mayoría de los proyectos relacionados | Ilorium |
| --- | --- |
| Una herramienta o un estándar | Una especie de organismos que nacen, divergen, heredan, descansan, coalescen y quedan en una crónica, sin que nada se borre |
| Certificar, puntuar o gobernar una tarea | Medir cuánta vida humana consume todavía una organización por cada cosa que entrega, y mostrarlo en público, sin sellos |
| Un sistema, un dueño | Linajes, una red de ascendencia y unos Comunes donde los organismos comercian y vinculan sus cadenas |
| Gobernar lo que un agente puede hacer ahora | Gobernar cómo evoluciona la especie: qué hereda cada generación, quién puede originar a quién (la compuerta de nacimiento) y que todo organismo nazca detenible por un humano |
| La capacidad como característica | SI2SI como horizonte: superinteligencias que originan superinteligencias, bajo las mismas reglas que el primer nacimiento de la especie |
| Documentación | Una historia: el Códice, el Radiante, la Bóveda, los Vigilantes, el Umbral del Organismo Cero quedándose en silencio |

**La regla que mantiene la credibilidad:** la historia y el horizonte viven en la capa narrativa (Códice, Radiante, marca, sitio web). El método sigue siendo literal: evidencia, alcance, frescura, limitaciones. La fantasía es cómo se cuenta Ilorium; nunca es lo que Ilorium afirma.

## Cola de ideas

Ideas tomadas de las entradas de abajo, a la espera de aplicarse. Cada una dice dónde iría.

| Idea | De | Va a |
| --- | --- | --- |
| Ligar la aprobación humana a la huella de la acción exacta | NOMOS (SPEC-008) | Especificación de la Probe, compuerta de autorización; aceptación de la llave de un recién nacido por su titular humano |
| Declarar cómo se hace cumplir cada límite: permiso, compuerta, hook del entorno o solo la palabra del agente | Signet (`enforced_by`) | Especificación de la Probe, plantilla de afirmación; pruebas de la Ley 2 del Genome |
| Hooks del entorno como compuerta de referencia: convertir los límites de un agente en un hook previo a cada llamada a herramienta que rechaza las llamadas prohibidas | Signet (`signet hook init`) | Especificación de la Probe, implementación de referencia para agentes en entornos con hooks |
| Verificador aislado del motor, auditable por separado | Signet (`src/verify.ts`) | Documento de arquitectura: formato de evidencia, Probe y un verificador independiente |
| Contrato estructurado para las directivas: alcance, límites, compuertas, evidencia, criterios de cierre | Signet (paquete) | Directivas `/do` del Umbral y criterios de éxito de las unidades de trabajo |
| Veredicto de tres valores: sin decidir no es ni aprobado ni fallido | NOMOS (`INCOMPLETE`), Signet (`UNEVALUATED`) | Pruebas de conformidad y plantilla de afirmación |
| Casos de prueba publicados por especificación | NOMOS | Pruebas de conformidad |
| Listas de revocación y `max_age` | NOMOS (SPEC-006) | Rotación de llaves de la Spore; credenciales de los Vigilantes |
| Recibos atestiguados por el receptor como fuente del estado de atribución `corroborated` y de la confirmación de unidades de trabajo por la contraparte | Notarized Agents / Sello | Especificación de la Probe (atribución), Prueba de Vida (unidades de trabajo), adaptadores (arquitectura) |
| Llave de firma en un demonio aparte, nunca en el proceso del agente | Obsigna, AEVS (KMS) | Probe, emisor del Pulso: custodia de llaves de la implementación de referencia |
| Evidencia de ejecución atestiguada por hardware como fuente opcional de «dónde corrió» y «qué política se aplicó» | TRACE (Linux Foundation) | Adaptadores (arquitectura); medidas de cobertura |
| Regla de admisión para evidencia importada: procedencia, material original, transformaciones, afirmaciones declaradas, UNKNOWN para el resto | Sexta revisión externa (2026-10-24) | Arquitectura (adaptadores), formato de evidencia (límites) |

## Cómo agregar una entrada

Usar la plantilla del final. Estado: `watch` (seguir de cerca), `borrow` (tomar ideas o código), `build on` (Ilorium depende de él), `discard` (no sirve, con el motivo).

---

## A2A (Agent2Agent Protocol)

- **Encontrado:** 2026-10-20 · **Estado:** build on
- **Qué es (hechos):** Protocolo abierto de comunicación entre agentes de IA. Creado por Google, alojado en la Linux Foundation. La 1.0 es su primera especificación estable; más de 150 organizaciones lo apoyan a abril de 2026. Agent Cards en `/.well-known/agent-card.json`, habilidades, esquemas de seguridad, tarjetas firmadas (JWS sobre RFC 8785), extensiones declaradas por URI y activadas con el encabezado `A2A-Extensions`, estados de tareas.
- **Relación con Ilorium:** La capa de abajo. A2A dice qué puede hacer un agente; Ilorium muestra cómo vive el organismo que está detrás.
- **Tomado:** las Agent Cards reemplazan las ofertas propias de Ilorium; la extensión A2A de Ilorium en borrador; los estados terminales de las tareas como unidades de trabajo; el patrón de firma para la Spore (Descubrimiento y crecimiento, Probe, Prueba de Vida).
- **No tomado:** los registros de A2A; el índice de Ilorium cubre organismos, no agentes.
- **Fuentes:** https://a2a-protocol.org/ ; https://a2a-protocol.org/latest/topics/extensions/ ; comunicado de la Linux Foundation, 2026-04-09.

## Signet (`azel-asl/signet`)

- **Encontrado:** 2026-10-20 (sugerido por el fundador) · **Estado:** borrow
- **Qué es (hechos):** "Gobierno por contrato, aplicación por hook (en entornos que los admiten) y verificación por recibo" para el trabajo de agentes de IA. Un **paquete** (formato "ASL Lite + GCL") declara el alcance de una tarea, sus bloqueos (acciones prohibidas), sus compuertas (aprobaciones humanas obligatorias antes de ejecutar), la evidencia y las reglas de cierre. Flujo: intención → paquete → análisis → verificación → aprobación → ejecución → recibo. Veredictos PASS, FAIL, BLOCKED y UNEVALUATED (un control que no se puede verificar mecánicamente nunca se aprueba). `signet hook init` convierte los bloqueos en un hook PreToolUse que rechaza las llamadas a herramientas prohibidas en entornos como Claude Code. Los recibos llevan dos huellas según su canonicalización XAS-CANON-1: `sha256` sobre los bytes y `h10` sobre el núcleo semántico; en el repositorio abierto los recibos no están firmados. El verificador no importa el motor. TypeScript, Node 22.5 o superior; 232 pruebas. Código bajo Apache 2.0, especificaciones bajo CC BY 4.0; la firma Ed25519 y la emisión de aprobaciones ("Signet Authority") son cerradas y las opera ASL Labs. Autor: Erwin Layaoen, ASL Labs. Al momento de la revisión: 3 commits, 0 estrellas, 0 forks, sin paquete npm, sin fechas visibles.
- **Declara sus propios límites:** no es un sandbox del sistema operativo; no inspecciona el contenido de los archivos ni el tráfico de red; los agentes en entornos sin hooks no quedan restringidos; el registro de aplicación guarda solo los rechazos; el motor "gobierna la intención declarada, no el comportamiento real"; un recibo prueba que el registro no se modificó, no que el trabajo se haya hecho o esté bien.
- **Relación con Ilorium:** Vecino. Signet gobierna una tarea antes y durante su ejecución; Ilorium observa un organismo entero a lo largo de su vida y gobierna cómo se reproduce la especie. Los hooks y paquetes de Signet podrían funcionar dentro de un organismo como sus compuertas y sus contratos de directivas, y la Probe de Ilorium registraría lo que permitieron y lo que rechazaron.
- **Ideas para tomar:** ver la cola de ideas de arriba: etiquetas honestas de aplicación (`enforced_by`), hooks del entorno como compuerta de referencia, verificador aislado, contratos de tarea para las directivas, el veredicto UNEVALUATED.
- **Reutilizar código:** el analizador, el validador, el verificador, la canonicalización y el compilador de hooks están bajo Apache 2.0, así que se pueden reutilizar con atribución y conservando su `NOTICE`. Revisar los archivos `LICENSE` y `NOTICE` antes de copiar.
- **No tomar:** una autoridad cerrada para firmas y aprobaciones (un protocolo abierto no puede depender de una raíz de confianza que controla una empresa; Ilorium ancla las llaves en los Strata con un testigo); recibos sin firmar y sin registro de transparencia; un registro que guarda solo los rechazos (la compuerta de Ilorium registra los intentos permitidos y los rechazados).
- **Límites de esta revisión:** basada en la página del repositorio y el README; no se leyeron uno por uno los archivos de especificación.
- **Fuentes:** https://github.com/azel-asl/signet ; https://raw.githubusercontent.com/azel-asl/signet/main/README.md (consultados el 2026-10-20).

## NOMOS Protocol (`nomos-spec/spec`)

- **Encontrado:** 2026-10-20 (sugerido por una revisión externa) · **Estado:** borrow
- **Qué es (hechos):** "Protocolo abierto e implementación de referencia para artefactos de gobernanza ejecutables por máquinas". Convierte las políticas institucionales en archivos JSON `.nomos` firmados que cualquier sistema puede evaluar de forma determinista, sin llamar a un modelo de IA en ese momento. Ocho especificaciones (001 a 008; 005, 007 y 008 en borrador): reglas y sellado; manifiesto de múltiples agentes con permisos, `cannot_call` y restricciones; vigencia temporal y vencimiento; composición y atestación de terceros; consultas públicas; revocación; certificados de llaves en cadena de confianza; Act Binding. Sellos Ed25519, verificables sin conexión. Verificadores de referencia en Python y TypeScript, línea de comandos, casos de prueba. Especificación y esquemas bajo CC BY 4.0; "las implementaciones pueden ser propietarias". Al momento de la revisión: 0 estrellas, 1 fork, sin versiones publicadas, sin fechas visibles, un solo contacto (nomosprotocol.com). No menciona A2A.
- **Relación con Ilorium:** Vecino, sin superposición. NOMOS responde "¿puedo hacer esto?" antes de una acción; Ilorium responde "¿qué pasó, quién lo hizo, quién lo decidió, cuánta vida humana llevó?" después, y "¿puede este organismo dar origen a otro?" en cada nacimiento. Los límites de un organismo (Ley 2) y sus compuertas (Ley 7) podrían expresarse como artefactos `.nomos`.
- **Ideas para tomar:** aprobación ligada a la acción exacta (SPEC-008); veredicto de tres valores (`INCOMPLETE`); manifiesto de agentes con `cannot_call`; listas de revocación y `max_age`; casos de prueba por especificación. Ver la cola de ideas.
- **No tomar:** los niveles de confianza (DECLARED a SOVEREIGN) atados a un puntaje, "ARI", que el README no define y escribe en dos escalas incompatibles (0,60 y 60); el listado en una plataforma comercial atado a un nivel.
- **Reutilizar código:** revisar la licencia del código antes de copiar; solo está declarada la licencia de la especificación.
- **Límites de esta revisión:** basada en el README y el sitio web; no se pudieron leer directamente los archivos de especificación.
- **Fuentes:** https://github.com/nomos-spec/spec ; https://nomosprotocol.com (consultados el 2026-10-20).

## ERC-8004 (Trustless Agents)

- **Encontrado:** 2026-10-19 · **Actualizado:** 2026-10-24 · **Estado:** watch
- **Qué es (hechos):** Propuesta de Ethereum «Trustless Agents», Standards Track, estado borrador, creada el 2025-08-13 (De Rossi, Crapis, Ellis, Reppel). Tres registros: identidad (un token ERC-721 por agente, con un `agentURI` a un archivo de registro), reputación (valores de retroalimentación firmados, con decimales y etiquetas, agregados sobre todo fuera de la cadena) y validación (un validador designado publica una respuesta de 0 a 100; validadores con stake, zkML o TEE son ejemplos fuera del registro). Las identidades son tokens **transferibles**; la billetera del agente se borra al transferir. El texto dice que «no puede garantizar criptográficamente que las capacidades anunciadas sean funcionales y no maliciosas» y que la inflación sybil de la reputación es posible.
- **Relación con Ilorium:** Identidad y reputación de agentes, en cadena; Ilorium es identidad y evidencia de organismos, fuera de la cadena. Una identidad ERC-8004 podría enlazarse desde una Spore como referencia externa opcional y fechada con una prueba de control; una transferencia de ese token no movería historial, conformidad ni llave de parada del organismo. Una fuente de candidatos, nunca de miembros.
- **No tomar:** puntajes de reputación como evidencia; el registro en cadena como requisito del núcleo.
- **Fuentes:** https://eips.ethereum.org/EIPS/eip-8004 (consultado el 2026-10-19 y el 2026-10-24).

## AEVS (Agent Execution Verification System, de Fetch.ai)

- **Encontrado:** 2026-10-24 (sugerido por la sexta revisión externa) · **Estado:** watch
- **Qué es (hechos):** «SDK de auditoría transparente para agentes de IA» de Fetch.ai: intercepta llamadas a herramientas en LangChain/LangGraph y MCP, arma recibos encadenados por hash firmados con HMAC-SHA256 (llaves v1) o ECDSA P-256 (llaves v2), y los manda a un backend de AEVS donde una llave en HSM en la nube firma cada recibo ingresado. Modos de visibilidad `public`, `private` y `proof_only` (entradas y salidas reemplazadas por hashes). Apache-2.0. Al momento de la revisión: 104 estrellas, sin release listada, sin fechas visibles. Su propio documento de seguridad dice que es «tamper-evident, not tamper-proof» («un proceso anfitrión totalmente comprometido podría saltearse la creación de recibos») y que un recibo «no verifica de forma independiente que la herramienta haya realizado la acción».
- **Relación con Ilorium:** Un recibo es una observación de una llamada a una herramienta desde adentro del proceso del agente, firmada por el lado del agente y por el backend del proveedor. Podría alimentar a la Probe mediante un adaptador como evidencia de que se registró una llamada; no dice nada sobre quién decidió, si el efecto externo ocurrió ni qué se omitió. La verificación depende del backend del proveedor salvo que los bytes firmados y las llaves sean exportables; eso se comprueba antes de cualquier adaptador.
- **No tomar:** una dependencia del backend de un proveedor como raíz de confianza.
- **Límites de esta revisión:** solo el README y el documento de seguridad; no se ejecutó código ni se verificó un recibo sin conexión.
- **Fuentes:** https://github.com/fetchai/AEVS-sdk ; https://github.com/fetchai/AEVS-sdk/blob/main/docs/07-security-and-privacy.md (consultados el 2026-10-24).

## TRACE y AgenTrust (Linux Foundation)

- **Encontrado:** 2026-10-24 · **Estado:** watch
- **Qué es (hechos):** TRACE («Trust, Runtime Attestation and Compliance Evidence») es una especificación de evidencia de ejecución y cumplimiento atestiguada por hardware para agentes de IA y cargas confidenciales, aportada por OPAQUE y desarrollada con AMD, Intel, Microsoft y TII; la Linux Foundation anunció su custodia el 2026-08-25 (presentada en junio de 2026). Se apoya en RATS, EAT, SLSA, SCITT, SPIFFE y EAR. AgenTrust es el ecosistema abierto alrededor: recibos TRACE (spec v0.2), un TRACE Registry (registro público con puntos de control firmados), un Agent Manifest, controles de política cMCP y cA2A, un Weight Custody Manifest; la mayoría de los componentes pre-1.0. El sitio declara: una firma muestra quién firmó y que nada cambió, no dónde se produjo; una entrada del registro muestra que un recibo se publicó, no que su contenido sea cierto.
- **Relación con Ilorium:** El vecino más institucional. TRACE responde «dónde corrió esto y qué política se aplicó», con raíces de hardware; Ilorium responde «cómo vive esta organización, cuánta vida humana consume, puede originar otra». Un artefacto TRACE podría ser una fuente opcional para cobertura y control mediante un adaptador. Su registro con puntos de control firmados se parece a los Strata; vale la pena probar si un registro de Ilorium puede ser atestiguado por, o publicado en, un registro así.
- **Límites de esta revisión:** comunicado de prensa y sitio del proyecto; la especificación no se leyó.
- **Fuentes:** https://www.linuxfoundation.org/press/linux-foundation-welcomes-trace-to-advance-verifiable-runtime-evidence-for-ai-workloads ; https://agentrust-io.com/ (consultados el 2026-10-24).

## Agent Receipts / Obsigna

- **Encontrado:** 2026-10-24 · **Estado:** borrow
- **Qué es (hechos):** «Un protocolo abierto para producir registros firmados criptográficamente y a prueba de alteración de las acciones de agentes de IA»: formato de recibo, firma Ed25519, cadena de hashes con secuencia y `previous_receipt_hash`, taxonomía de tipos de acción; Obsigna es el conjunto de herramientas de referencia (proxy MCP, un demonio de firma que tiene la llave fuera del proceso del agente, un hook para Claude Code, CLI, SDK en Go, TypeScript y Python), con una suite de conformidad entre lenguajes y un modelo formal acotado. Código Apache-2.0, especificación MIT. Al momento de la revisión: 20 estrellas, unos 1.300 commits, sin release listada. Declara sus límites: una llave dentro del proceso del agente la puede falsificar cualquiera con ejecución de código ahí; la suite de conformidad detecta desvíos de serialización, no de interpretación; el titular de llave bizantino es «la frontera, no está cubierto».
- **Relación con Ilorium:** El diseño abierto más cercano al registro de llamadas a herramientas de la Probe. Su demonio de firma fuera de proceso es el modelo de custodia correcto para la Probe y el emisor del Pulso de referencia.
- **Ideas a tomar:** custodia de llaves en un demonio aparte; una suite de conformidad entre lenguajes (el segundo verificador de M7 de Ilorium).
- **Fuentes:** https://github.com/agent-receipts/obsigna ; https://agentreceipts.ai/ (consultados el 2026-10-24).

## Notarized Agents / Sello (investigación)

- **Encontrado:** 2026-10-24 · **Estado:** borrow
- **Qué es (hechos):** arXiv 2606.04193 (Juan Figuera, 2026-06-02): «recibos confidenciales atestiguados por el receptor». El servicio que recibe la llamada de un agente firma con su propia llave un recibo de lo que observó, lo cifra para la llave del dueño del agente y lo publica en un registro Merkle cofirmado por testigos, de modo que el dueño reconstruye la actividad del agente sin confiar en el agente ni en su operador. Límites que nombra: supresión (un receptor puede omitir), receptores en colusión, incentivos de adopción.
- **Relación con Ilorium:** Exactamente el estado de atribución `corroborated` y la confirmación de unidades de trabajo por la contraparte: evidencia firmada por el otro lado de una acción. El problema de adopción es el mismo que Ilorium enfrenta con testigos y Oráculos.
- **Fuentes:** https://arxiv.org/abs/2606.04193 (consultado el 2026-10-24).

## AGTP Transparency Log (Internet-Draft)

- **Encontrado:** 2026-10-24 · **Estado:** watch
- **Qué es (hechos):** `draft-hood-agtp-log` (Chris Hood, Nomotic; envío independiente, no respaldado por la IETF; versión 01 del 2026-05-20): un registro de transparencia para eventos del ciclo de vida de la identidad de agentes (génesis emitida, revocada, suspendida, reinstalada, obsoleta), construido sobre RFC 9162 y SCITT (RFC 9943) con recibos COSE. Modelo de emisor único; testigos y monitores diferidos.
- **Relación con Ilorium:** Se superpone con el papel de los Strata para hechos de ciclo de vida, al nivel de agentes y no de organismos. Confirma que los registros al estilo RFC 9162 con recibos SCITT son hacia donde va el campo; la elección de C2SP de Ilorium debería comprobarse en interoperabilidad con recibos SCITT antes de cerrar M1.
- **Fuentes:** https://datatracker.ietf.org/doc/html/draft-hood-agtp-log-01 (consultado el 2026-10-24).

## Andon Labs (negocios operados por IA en el mundo real)

- **Encontrado:** 2026-10-24 · **Estado:** watch (organismos candidatos)
- **Qué es (hechos):** Una empresa que despliega IA en entornos reales para estudiarla: Andon Market (una tienda minorista en San Francisco descrita como operada íntegramente por IA), Andon Café (Estocolmo), Andon FM (radios operadas por agentes), Vending-Bench (benchmarks de agentes que manejan negocios de máquinas expendedoras) y Pion (una plataforma para negocios operados por agentes, en lista de espera). Project Vend se hizo con Anthropic. Su sitio no publica cifras de intervención humana y declara que «la seguridad por humanos en el circuito es un espejismo».
- **Relación con Ilorium:** Las primeras organizaciones reales que parecen organismos. Son Avistamientos hasta que exista una Spore y evidencia. Son también la prueba de si una contraparte quiere lo que Ilorium muestra: cuánto trabajo humano hay detrás de una tienda «operada por IA».
- **Fuentes:** https://andonlabs.com/ (consultado el 2026-10-24).

## El campo de los recibos de agentes (nota, 2026-10-24)

Un mapa público de competidores (`JaredKlopstein/provenant`, issue 6, consultado el 2026-10-24) lista más de veinte proyectos que producen recibos firmados y encadenados por hash de acciones de agentes, abiertos y comerciales: entre ellos protect-mcp, agent-custody, veritrail, halo-record, agent-receipt, AgentMint, Pipelock, Quox, ProofAgent, CertNode, Asqav, ProofTrail, TrustNotch, Cloak, y tres Internet-Drafts (`draft-sahu-agent-action-receipts`, `draft-farley-acta-signed-receipts`, `draft-marques-asqav-compliance-receipts`). Ninguno se revisó uno por uno acá. Dos conclusiones para Ilorium: la capa de evidencia (registros, registro Merkle, puntos de control, testigos) es comparable a muchos de estos y no es donde Ilorium se diferencia; y ningún proyecto encontrado mide una organización (tiempo humano por unidad de trabajo, cobertura, tasa de rescate), gobierna nacimientos ni define una guardia. Eso es una afirmación sobre esta búsqueda en esta fecha, no una afirmación de que no exista nada más.

## Darwin Gödel Machine

- **Encontrado:** 2026-10-20 (citado por una revisión externa) · **Estado:** watch
- **Qué es (hechos):** Investigación sobre agentes que modifican su propio código y guardan un archivo de variantes, con mejoras medidas en tareas de programación, hecha con modelos fundacionales, aislamiento y supervisión humana.
- **Relación con Ilorium:** Evidencia de que la evolución de agentes se puede estudiar; no evidencia de que una especie de organizaciones lleve a la superinteligencia. Modelo para el programa de investigación sobre el horizonte: mismo modelo base y presupuesto, variantes fijas contra mejoradas por humanos contra elegidas por el sistema, en tareas nuevas.
- **Fuentes:** https://arxiv.org/abs/2505.22954

## Project Vend (Anthropic)

- **Encontrado:** 2026-10-20 (citado por una revisión externa) · **Estado:** watch
- **Qué es (hechos):** El experimento de Anthropic de manejar un pequeño negocio con un agente de IA; el desempeño mejoró con mejores modelos, herramientas y procedimientos, y a la vez se documentaron ayuda humana y vulnerabilidades ante interacciones adversarias.
- **Relación con Ilorium:** Un negocio puede mejorar y seguir dependiendo de rescates humanos. La tasa de rescate y la dependencia por unidad de trabajo de Ilorium existen para distinguir esas dos cosas.
- **Fuentes:** https://www.anthropic.com/research/project-vend-2

---

## Plantilla

```
## <Nombre del proyecto>

- **Encontrado:** <fecha> · **Estado:** watch | borrow | build on | discard
- **Qué es (hechos):** <qué dice ser, versión, licencia, madurez>
- **Relación con Ilorium:** <superposición, complemento o ninguna>
- **Ideas para tomar:** <sumarlas a la cola de ideas, cada una con dónde iría>
- **No tomar:** <y por qué>
- **Reutilizar código:** <licencia del código, avisos a conservar>
- **Fuentes:** <enlaces, fecha de consulta>
```
