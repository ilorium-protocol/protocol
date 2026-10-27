# Ilorium Arquitectura de software v1.0

Versión 1.0 · 2026-10-20 · Borrador

No forma parte del protocolo: la implementación de referencia.

> Traducción de trabajo de `architecture-v1.md`. La versión en inglés es la oficial.

## Propósito

Ilorium necesita su propio código: la implementación de referencia que cualquier organización puede instalar para producir evidencia conforme, y las herramientas con las que cualquiera puede verificarla. Su repositorio, su línea de comandos y sus paquetes se llaman `ilorium` (`ilorium-*` para los paquetes); la Spore vive en `/.well-known/ilorium.json`. Este documento define cómo se organiza, se escribe, se instala, se protege, se prueba y se publica ese código. Es una arquitectura inicial, a revisar a medida que se escriba el código.

Los proyectos relacionados (A2A, NOMOS, Signet) aportan ideas y, donde las licencias lo permiten, código. Ilorium reutiliza **estándares** y **bibliotecas** chicas y auditadas; no se apoya en el motor ni en la raíz de confianza de otro proyecto.

## Principios

1. **La especificación manda, el código la sigue.** Cada comportamiento remite a una sección de un documento del protocolo; todo lo que haga el código y la especificación no diga es un error o un pendiente.
2. **Verificable por alguien que no confía en nosotros.** El verificador es chico, aislado y auditable por separado. Un segundo verificador, en otro lenguaje y escrito aparte, es un objetivo antes de la primera versión estable del código.
3. **Pocas dependencias, cada una justificada.** Cada dependencia se lista, se fija, se revisa su licencia y se audita.
4. **Seguro por defecto, cerrado ante la duda donde importa.** Mínimo privilegio, ningún secreto en los repositorios, compuertas que rechazan cuando no están seguras.
5. **Tecnología aburrida.** Formatos estándar, herramientas estándar, código legible. Los operadores conocen systemd y los contenedores, y un único binario estático se instala sin entorno de ejecución; el verificador es lo bastante chico como para que un auditor lo lea.
7. **El protocolo no depende de un lenguaje.** Formatos, esquemas y casos de conformidad son compartidos; cualquier implementación en cualquier lenguaje que pase los casos vale lo mismo. El código de referencia se escribe en Go (la Probe) y en Python (el primer verificador) por motivos distintos, más abajo.
6. **Honesto sobre sus límites.** Cada componente documenta lo que no puede ver ni impedir, como hacen las especificaciones.

## Componentes

| Componente | Qué hace | Capa | Lenguaje |
| --- | --- | --- | --- |
| **Formato de evidencia** | Definido en `specs/evidence-format-v1.es.md`: esquemas JSON de registros, pulsos, sidecars de puntos de control y el archivo de confianza; el perfil de RFC 8785 llamado JSON de Ilorium; el perfil de puntos de control C2SP; los veredictos y el informe. Los esquemas de la Spore y de sucesión esperan a la especificación de la Spore | Protocolo | Esquemas y casos de conformidad (Apache-2.0). Ninguna biblioteca es normativa |
| **Verificador** | Controla un registro, los puntos de control, las pruebas de consistencia, los pulsos y una Spore contra el formato; controla los registros de sucesión contra la compuerta de nacimiento (progenitores que cumplen, titular humano de la llave de parada aceptado antes del acta, firmas de cada progenitor); produce un informe con veredictos PASS, FAIL, UNKNOWN | Herramienta del protocolo | Python (`ilorium-verifier`, M0); un segundo verificador más adelante, en otro lenguaje y escrito aparte |
| **Probe** | Servicio permanente: colectores, correlador, escritor del registro, firmante de puntos de control, publicador | Referencia | Go |
| **Colectores** | Uno por fuente: Centinela (Telegram), GitHub, Workspace/Gmail, diario del sistema, middleware de A2A, sistemas del negocio | Referencia | Go, un paquete cada uno |
| **Emisor del pulso** | Pulsos cada N latidos o cada T; responde desafíos. Parte de la Probe, y una baliza independiente para el modo baliza | Referencia | Go |
| **Compuerta de autorización** | Rechaza acciones irreversibles sin autorización registrada; hooks para entornos de agentes que los admiten y una compuerta HTTP para despliegues y pagos; informa a la Probe los intentos permitidos y rechazados | Referencia (opcional) | Go; scripts de hook sin dependencias |
| **Middleware de la extensión A2A** | Agrega la extensión de Ilorium a las Agent Cards; lleva las referencias de pulso; informa los estados de las tareas a la Probe | Referencia | Go |
| **Línea de comandos (`ilorium`)** | `init`, `spore`, `verify`, `status`, `keys`, `doctor` | Referencia | Go |
| **Índice** | Reúne Spores, sigue vínculos de parentesco, manda desafíos, publica datos abiertos en ilorium.com | Observatorio (repositorio aparte) | A decidir |

### Flujo de datos

```
fuentes ──► colectores ──► almacén local (solo agregar, SQLite) ──► correlador ──► evaluaciones
                                   │
                                   ▼
                     escritor del registro (JSON de Ilorium + árbol RFC 6962)
                                   │
              firmante de puntos de control (cada N latidos o cada T)
                                   │
             publicador ──► repositorio público de los Strata ──► testigos ──► verificadores
                                   │
                     emisor del pulso ──► índices / contrapartes A2A
```

### Límites de confianza

| Límite | Qué lo cruza | Control |
| --- | --- | --- |
| Fuente → colector | Eventos de APIs de terceros | Credenciales de solo lectura por fuente; solo campos permitidos; el contenido se guarda como huella, nunca se publica |
| Agentes → Probe | Afirmaciones y registros de tareas A2A | Punto de recepción local autenticado por identidad de agente; las afirmaciones nunca se toman como hechos (estados de atribución) |
| Probe → público | Registros, puntos de control, pulsos | Firmados con llaves que solo tiene el usuario de la Probe; nada privado sale |
| Público → verificador | Todo lo publicado | El verificador no confía en nada que no pueda recalcular; las llaves se toman del acta de nacimiento y de las rotaciones firmadas por testigos |
| Agente → compuerta | Pedidos para hacer acciones irreversibles | Cerrada ante la duda; la autorización tiene que referenciar un comando o una regla registrados |
| Titular de la llave de parada → organismo | La parada | La llave de parada la tiene un humano, fuera de todo agente y fuera de la Probe; la Probe registra la parada, nunca tiene la llave |

## Formatos y estándares

| Necesidad | Elección | Estado |
| --- | --- | --- |
| Formato de datos | JSON, JSON Schema (borrador 2020-12) | Decidido |
| Forma canónica | RFC 8785 (JCS), restringida a enteros y entradas estrictas (JSON de Ilorium, Formato de Evidencia sección 4). El verificador se contrasta en sus pruebas con el paquete de Python `rfc8785` (0.1.4) | Decidido |
| Huella | SHA-256 | Decidido |
| Firmas | Ed25519 para logs, pulsos y sidecars; Ed25519 y ML-DSA-44 aceptados para cofirmas de testigos; los demás algoritmos se informan UNKNOWN, nunca PASS. Verificador en Python: `cryptography` (pyca) | Decidido |
| Árbol y pruebas del registro | Árbol de Merkle de RFC 6962 con la verificación de pruebas de RFC 9162 | Decidido |
| Puntos de control y testigos | C2SP `signed-note`, `tlog-checkpoint`, `tlog-cosignature` y `tlog-witness`, fijados en v1.1.0 (un punto de control es una nota firmada, no JSON de RFC 8785; el latido y el tiempo de traducción viajan en un sidecar firmado). Un testigo C2SP comprueba la consistencia y cofirma; no manda desafíos de Ilorium. El operador de desafíos (Pulso, sección 6) es una función aparte, que corre un índice o un testigo dedicado, aunque una misma entidad haga las dos | **Decidido** como formato. Usar testigos públicos **no está disponible** hasta que haya una prueba de interoperabilidad y un acuerdo con un operador de testigo |
| Firmas de la Spore y de las Agent Cards | JWS sobre RFC 8785, como en A2A 1.0 | Propuesto |
| Comunicación entre agentes | A2A | Decidido (Descubrimiento y crecimiento) |

## Estructura del repositorio

Un único repositorio público para el protocolo y la implementación de referencia, en la organización de GitHub `ilorium-protocol`; el índice en su propio repositorio.

```
ilorium/
  ilorium/         documentos del protocolo (genome/, specs/, engineering/, research/, brand/)
  schemas/         esquemas JSON (Apache-2.0)
  vectors/         casos de conformidad por especificación (generados, Apache-2.0)
  tools/           gen_vectors.py: generador independiente, no comparte código con el verificador
  verifier/        verificador aislado (Python): no importa nada de probe/
  probe/           (desde M1, en Go)
    core/          registros, almacén local, escritor del registro, firmante de puntos de control, publicador
    collectors/    sentinel_telegram, github, workspace, journal, a2a, business
    correlator/    atribución, cruces, unidades de trabajo
    pulse/         emisor, respuesta a desafíos, modo baliza
  gate/            compuerta de autorización: hooks del entorno, compuerta HTTP
  a2a/             middleware de la extensión
  cli/             comando ilorium
  deploy/          unidades de systemd, imagen de contenedor, configuraciones de ejemplo
  docs/            guías para operadores y contribuyentes
  LICENSE  LICENSE-SPECS  NOTICE  SECURITY.md  CONTRIBUTING.md
```

Hoy existen solo `ilorium/`, `schemas/`, `vectors/`, `tools/`, `verifier/` y los archivos del repositorio (M0).

**El verificador nunca importa la Probe.** Depende solo del formato de evidencia y de sus bibliotecas fijadas (`cryptography`, `jsonschema`, `referencing`), así se puede auditar por separado (idea tomada de Signet). Una prueba (`tests/test_isolation.py`) falla si importa cualquier otra cosa.

## Lenguaje, licencias y gobierno

Decidido el 2026-10-20, por el fundador.

**Lenguajes.** La Probe permanente se escribe en **Go** desde M1: la prioridad es la distribución mediante ejecutables y la operación como servicio. El primer verificador (M0) se escribe en **Python**, porque es chico y los auditores lo leen con facilidad. El protocolo sigue independiente de ambos: formatos y casos son compartidos, y un segundo verificador en un tercer lenguaje es el hito M7.

**Prioridades de M1 para la Probe en Go**, en este orden: persistencia durable (un registro confirmado es un registro en disco), recuperación ante fallos (reiniciar en cualquier punto sin perder ni duplicar registros, y escribir el hueco), límites de recursos (colas, disco, memoria y archivos abiertos acotados, con el desborde registrado como hueco, nunca descartado en silencio) y señalización explícita de huecos en la evidencia (cada intervalo en que un colector o la Probe estuvieron caídos se vuelve una observación `gap`, Formato de Evidencia sección 5.3).

**Licencias.** Código, esquemas JSON, casos de conformidad y ejemplos: **Apache-2.0**, para que cualquiera pueda incorporarlos a una implementación, con la concesión de patentes de los contribuyentes. Texto normativo (los documentos Markdown): **CC BY 4.0**. Cada aporte lo licencia su autor bajo la licencia del archivo que cambia (entrada = salida); quienes contribuyen conservan su copyright. «Nadie posee el protocolo» describe cómo se gobierna; no reemplaza decir quién licencia qué. El titular del copyright en los encabezados es, por ahora, «The Ilorium Authors», hasta que el fundador nombre una entidad legal.

**Gobierno, provisorio.** Hasta que exista el documento de gobierno, solo el fundador fusiona y publica las releases. Se declara, no se oculta, y cambia cuando se acepte el documento de gobierno.

## Dependencias

**Política**

- Cada dependencia necesita un motivo escrito, una licencia compatible con Apache 2.0, un mantenedor activo y una revisión antes de agregarse.
- Versiones fijadas con huellas en un archivo de bloqueo; la instalación rechaza paquetes sin fijar.
- Ninguna dependencia puede hacer llamadas de red al importarse.
- Se prefiere la biblioteca estándar y HTTP directo antes que los SDK de los proveedores; un colector que necesite un SDK lo aísla en su propio módulo.
- Cada versión publicada incluye una lista de materiales de software (SBOM, CycloneDX o SPDX).
- Las actualizaciones de dependencias llegan como pull requests y un mantenedor que no las escribió revisa las diferencias.

**Candidatas iniciales**

Verificador (Python, en uso):

| Biblioteca | Para | Notas |
| --- | --- | --- |
| `cryptography` (pyca) | Ed25519, ML-DSA-44, SHA-256 | Muy usada, auditada |
| `jsonschema`, `referencing` | Validación de JSON Schema 2020-12 | Fijadas |
| `rfc8785` | Contraste de la canonicalización | Solo desarrollo y pruebas; el verificador tiene su propio canonicalizador |

Probe (Go, a revisar en M1; ninguna está adoptada todavía):

| Biblioteca | Para | Notas |
| --- | --- | --- |
| Biblioteca estándar de Go | Ed25519, SHA-256, HTTP, `database/sql` | Preferida donde alcance |
| `golang.org/x/mod/sumdb/note` | Notas firmadas C2SP | A verificar que cubra el perfil fijado, incluido ML-DSA-44 |
| `github.com/transparency-dev/merkle` | Huellas y pruebas de RFC 6962 | A verificar, y a comparar con nuestros casos |
| `modernc.org/sqlite` | Almacén local de solo agregar, sin cgo | A comparar con archivos simples y un registro de escritura previa, por la durabilidad |

Lo que se adopte tiene que pasar los casos de conformidad.

Todavía no existen para el verificador en Python: un archivo de bloqueo con huellas, una lista de materiales de software ni integración continua.

## Instalación

| Camino | Para quién | Cómo |
| --- | --- | --- |
| **Baliza** | Cualquiera que quiera aparecer como avistamiento | Un binario o script chico: genera una llave de pulso, publica una Spore, emite pulsos, responde desafíos |
| **Probe completa, ejecutable** | Operadores con un servidor Linux | Descargar el binario estático firmado (o `go install`), después `ilorium init` |
| **Probe completa, contenedor** | Operadores con plataformas de contenedores | Imagen firmada, usuario no root, sistema de archivos de solo lectura, base mínima |
| **Compuerta** | Organismos que quieren prevenir, no solo detectar | Scripts de hook instalados en el entorno del agente; compuerta HTTP delante de los puntos de despliegue o de pago |

`ilorium init` guía el paso cero: identidades separadas, llaves, Spore, membrana, Umbral, titular humano de la llave de parada, colectores a activar, elección del testigo. `ilorium doctor` controla permisos, sincronización del reloj, estado de los colectores y custodia de las llaves.

**Endurecimiento con systemd** para el servicio de la Probe: usuario dedicado `oz-probe`, `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, una única ruta escribible para su almacén, acceso al diario mediante un grupo restringido, credenciales cargadas con las credenciales de systemd o con un archivo 0600 del usuario del servicio.

## Configuración y secretos

- **La configuración** (no secreta: membrana, colectores, N, T, tipos de unidad de trabajo) vive en el repositorio del organismo, así sus cambios quedan observados por la propia Probe.
- **Los secretos** (tokens de las fuentes, token del bot Centinela, llaves de firma) nunca viven en un repositorio. Solo los puede leer el usuario de la Probe.
- **Llaves separadas por propósito:** llave de firma del registro (puntos de control), llave de pulso (pulsos y respuestas a desafíos) y la identidad del organismo anclada en su acta de nacimiento. Cada una puede rotar por separado; cada rotación es un registro firmado con la llave anterior y firmado también por un testigo. La **llave de parada** no está entre ellas: pertenece al titular humano y nunca vive en las máquinas del organismo.
- **Llaves en hardware** (TPM, llaves de seguridad) quedan como opción posterior para las llaves de firma.

## Seguridad

### Modelo de amenazas

| Amenaza | Ejemplo | Controles principales | Riesgo residual (se publica) |
| --- | --- | --- | --- |
| El operador altera la historia | Borrar un cruce incómodo | Registro de solo agregar, pruebas de consistencia, testigos que verifican | Eventos alterados antes de su primer punto de control (ventana de unos T) |
| El operador detiene la Probe | Silencio durante una intervención humana | Puntos de control sin actividad, alertas del testigo, desafíos, captura degradada | El hueco se ve, su contenido no |
| Agente comprometido | Un agente excede sus permisos o afirma una autonomía falsa | Mínimo privilegio, compuerta, estados de atribución, afirmaciones disputadas | Acciones fuera de los sistemas observados |
| Llave de firma robada | Puntos de control falsificados | Llaves que solo lee el usuario de la Probe; rotación con la llave anterior; los testigos rechazan historias incompatibles | Falsificación hasta la rotación, acotada por el estado que guardan los testigos |
| Nacimiento por fuera de la compuerta | Un descendiente creado sin titular humano de la llave de parada o por un progenitor restringido | El verificador rechaza el registro de sucesión; el linaje no declarado se registra cuando se descubre | Organismos creados totalmente por fuera del protocolo |
| Cadena de suministro | Dependencia maliciosa o versión adulterada | Huellas fijadas, SBOM, versiones firmadas con procedencia, revisión de dos personas | Compromiso de un mantenedor externo antes de detectarlo |
| Índice o testigo malicioso | Esconder o inventar organismos | Datos abiertos, varios índices y testigos, los verificadores recalculan todo | Colusión de todos los testigos que usa un organismo |
| Filtración de privacidad | Publicar el contenido de los mensajes | Campos permitidos, solo huellas, almacén privado cifrado | Los metadatos pueden revelar patrones; se documenta |

### Prácticas

- `SECURITY.md` con un canal privado de reporte y divulgación coordinada.
- Compuertas cerradas ante la duda para las acciones irreversibles; nunca abiertas sin un motivo registrado.
- La salida de red de la Probe limitada a sus fuentes declaradas, el repositorio de los Strata, los testigos y los índices.
- Revisión periódica de los permisos de los colectores contra el mínimo de la especificación de la Probe.

## Compilación y publicación

- Integración continua con cada acción de terceros fijada a un commit.
- Versiones compiladas en la integración continua, firmadas y publicadas con su procedencia (Sigstore y procedencia SLSA como objetivo), mediante publicación de confianza en el registro de paquetes.
- Compilaciones reproducibles como objetivo, para que cualquiera pueda recompilar una versión y compararla.
- Etiquetas firmadas; cada versión lista sus dependencias (SBOM) y sus resultados de conformidad.
- El código usa versionado semántico, separado de la versión del protocolo; cada versión del código dice qué versión del protocolo implementa.

## Pruebas

| Nivel | Qué |
| --- | --- |
| Pruebas unitarias y de propiedades | Canonicalización, huellas, árbol y pruebas, reglas de atribución |
| **Casos de conformidad** | Por especificación: entradas y salidas esperadas, publicados en `vectors/` para que cualquier implementación los corra (idea tomada de NOMOS). Los genera una herramienta que no comparte código con el verificador, con expectativas escritas a mano y un caso externo de C2SP |
| Conformidad | El verificador corrido contra los casos de prueba y contra registros grabados, incluidos nacimientos que la compuerta tiene que rechazar |
| Aceptación | Los casos que lista la especificación de la Probe (canarios, directiva por nota de voz, organismo sin actividad, Probe congelada, resultado de A2A, rechazo de la compuerta) y, desde el 2026-10-24, los casos de lectura siguientes: un colector caído mientras el Pulso responde (presencia mostrada, cobertura degradada, ninguna autonomía inferida); una aprobación de seguridad de 20 segundos (esfuerzo real o declarado registrado, sin un piso de 5 minutos presentado como probado); diez acciones corroboradas y noventa sin atribución (sin extrapolar al proceso completo); un registro alterado, firma inválida, duplicado, truncamiento o raíz incompatible (un veredicto por afirmación, nunca un solo PASS); una falla de publicación o un testigo ausente (registro local conservado, antigüedad informada); una decisión de gobierno que aprueba A y publica B (B no aprobado); una parada durante una caída de la Probe o del índice (camino técnico independiente comprobado, registro posterior documentado); cero entregas exitosas con intentos fallidos y horas humanas (denominadores explícitos, «no calculable» donde corresponda, nunca costo cero) |
| Verificación cruzada | Los dos verificadores tienen que coincidir en todos los casos antes de la primera versión estable del código |
| Simulacros de falla | Matar colectores, cortar la red, rotar llaves, restaurar desde una copia (simulacro de recuperación), simulacro de parada a cargo del titular humano |

## Orden de construcción

| Hito | Entrega | Prueba |
| --- | --- | --- |
| **M0 · Formato** | Especificación del Formato de Evidencia, esquemas JSON (registro, pulso, sidecar de punto de control, confianza), canonicalización y perfil de puntos de control C2SP, casos de conformidad, verificador aislado en Python. *Entregado como borrador el 2026-10-20; los esquemas de la Spore, el Evidence Bundle y Vital Signs, con vectores, se agregaron el 2026-10-21.* El esquema de sucesión pasa a la especificación de la Spore | Que otro pueda verificar la evidencia |
| **M1 · Registro** | En Go: almacén local, escritor del registro, puntos de control cada N latidos o cada T, publicador a un repositorio público, primer testigo. Prioridades: persistencia durable, recuperación ante fallos, límites de recursos, huecos explícitos | Que la historia no se pueda reescribir sin que se note |
| **M2 · Primeros colectores** | GitHub y diario del sistema; correlador con estados de atribución | Los primeros latidos reales del Organismo Cero |
| **M3 · Umbral** | Colector del Centinela, comandos, contactos, directivas seguidas hasta su efecto | Que las decisiones humanas se vean |
| **M4 · Pulso** | Emisor, desafíos con plazo, modo baliza, Spore | Presencia sin confiar en el operador |
| **M5 · Unidades de trabajo** | Colectores de sistemas del negocio y de A2A, unidades de trabajo, dependencia por unidad | Que la libertad del fundador se pueda medir |
| **M6 · Compuerta** | Hooks del entorno y compuerta HTTP; intentos permitidos y rechazados registrados | Prevenir donde importa |
| **M7 · Segundo verificador** | Verificador independiente en otro lenguaje | Apertura en la práctica |
| **M8 · Sucesión** | Registros de sucesión, controles de la compuerta de nacimiento en el verificador, credenciales del titular de la llave de parada | Que el primer nacimiento de la especie pueda pasar la compuerta |

## Adaptadores para evidencia externa *(agregado el 2026-10-24; después del piloto del Organismo Cero, nunca antes de M2)*

Existen sistemas que producen recibos firmados de acciones de agentes, evidencia de ejecución atestiguada por hardware e identidades externas de agentes (`research/related-projects.es.md`). La implementación de referencia podrá, más adelante, ingerir esa evidencia mediante **adaptadores opcionales**. Un adaptador es un colector, y sus registros conservan: el sistema de origen y su versión; el identificador de origen; un compromiso con el artefacto original y dónde puede obtenerse; la fecha de captura y la de importación, por separado; la identidad del emisor y su material de verificación; el alcance de lo firmado; las transformaciones aplicadas y lo que se perdió; la versión del adaptador; la relación agente–organismo en ese momento; y los límites que la propia fuente declara. La política de privacidad se aplica antes de publicar nada: el original puede quedar en el almacén privado.

Lo que un adaptador puede y no puede hacer está dicho en el formato de evidencia (sección 16, límite 8): importar, normalizar, resumir con un hash o firmar un registro externo nunca fortalece la afirmación que ese registro hace. Un adaptador declara qué afirmaciones puede respaldar («se registró una invocación de herramienta») y deja el resto en UNKNOWN («el pago se liquidó», «ningún humano decidió»). Una firma inválida es FAIL para la afirmación criptográfica; material insuficiente es UNKNOWN. Una identidad externa que cambia de dueño no mueve historial, conformidad ni llave de parada. Soportar un sistema no respalda a sus operadores ni obliga a otras implementaciones a usarlo, y el formato central no exige blockchain, token ni proveedor de servicio. No se anuncia ninguna compatibilidad antes de tener vectores y una prueba de interoperabilidad reproducible, que incluya: un recibo válido con un resultado externo no corroborado (la integridad puede pasar; la entrega sigue desconocida); el mismo recibo importado dos veces (una sola acción, las dos importaciones trazables); una identidad externa transferida (no hereda autoridad ni historial favorable); un servicio externo inalcanzable (el bundle reproduce los controles para los que tiene material; el resto UNKNOWN, sin consulta remota silenciosa).

## Decisiones abiertas

- Prueba de interoperabilidad de un log de Ilorium contra un testigo C2SP real, y acuerdo con un operador de testigo, antes de declarar disponibles los testigos públicos. Comprobar, en la misma prueba, si el log también puede publicarse en, o ser atestiguado por, un registro al estilo SCITT (el borrador AGTP log y el TRACE Registry usan RFC 9162 con recibos COSE; `research/related-projects.es.md`).
- El nombre legal o la entidad para el aviso de copyright (hoy «The Ilorium Authors»).
- Decidido el 2026-10-21: la regla para contribuyentes es el certificado de origen del desarrollador (DCO); los commits de agentes llevan el `Signed-off-by:` del humano u organización responsable y al agente como autor con su propia identidad (`CONTRIBUTING.md`). Se mantiene «The Ilorium Authors», con un archivo `AUTHORS`.
- Documento de gobierno; hasta entonces, solo el fundador fusiona y publica.
- Resuelto: la Spore lleva `stop_key_holders`, una lista; el Genoma y el Ecosistema siguen hablando de «quien tiene la llave de parada» como un rol, lo que sigue siendo correcto. Pendiente: qué debe ser la `credential` de un titular.
- Un Evidence Bundle de una parte del log (frontera de Merkle), y cómo se empaqueta un bundle, antes de que el repositorio público sirva bundles.
- Archivo de bloqueo con huellas, SBOM e integración continua para el verificador.
- Biblioteca para el almacén privado cifrado.
- Custodia de llaves de la Probe y del emisor del Pulso: un demonio de firma separado de todo proceso de agente, como hace Obsigna (`research/related-projects.es.md`), para que ejecutar código dentro de un agente no permita falsificar registros.
- Dónde vive el índice y en qué lenguaje.
- Nombre de paquete en PyPI para `ilorium` e `ilorium-*`. La organización de GitHub es `ilorium-protocol`, porque el nombre `ilorium` en GitHub está tomado.

## Fuentes

- Repositorio de especificaciones C2SP, `signed-note`, `tlog-checkpoint`, `tlog-cosignature` y `tlog-witness` en v1.1.0: https://github.com/C2SP/C2SP (consultado el 2026-10-20); testigos de transparency.dev (tlog-witness v0.1.0, operados por el equipo TrustFabric de Google; participación mediante witness-network.org): https://transparency.dev/witnesses (consultados el 2026-10-20).
- Paquete de Python `rfc8785`, versión 0.1.4, empaquetado por Debian y Gentoo (consultado el 2026-10-20).
- Ideas de proyectos relacionados: ver `research/related-projects.es.md`.
