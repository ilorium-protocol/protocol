# Formato de Evidencia de Ilorium v1.0

Versión 1.0 · 2026-10-20 · Borrador

Cómo se escribe, se firma, se exporta y se comprueba la evidencia.

> **La evidencia vale lo que vale que un extraño pueda comprobarla sin confiar en quien la escribió.**

*Traducción del original en inglés (`evidence-format-v1.md`). Si difieren, manda el inglés.*

## 1. Propósito y alcance

La Probe (véase la especificación de la Probe) registra lo que hace una organización. El Pulse (véase la especificación del Pulse) muestra que está presente. Este documento define los **bytes**: la forma de cada registro, cómo los registros se convierten en un log verificable, qué formato de checkpoint se usa y cómo lo atestiguan los testigos, cómo se firman los pulsos, cómo se exporta un Strata, qué contienen una Spore, un Evidence Bundle y los Vital Signs, y qué debe informar un verificador.

Es el contrato entre el **protocolo** y cualquier **implementación**. El código de la Probe (Go, desde M1), el verificador aislado (Python, M0) y cualquier verificador escrito por otra persona leen este documento y los vectores de prueba compartidos. No leen el código de los demás.

**Qué hace este documento.** Define formatos y el comportamiento de un verificador. Dice qué se comprueba y, igual de importante, qué no.

**Qué no hace.** No dice qué es un buen organismo (Genoma), cómo se cuentan los latidos (Pulse), qué eventos se recolectan ni cómo se clasifican (Probe), ni cómo se calcula un puntaje (Proof of Life). Un verificador que sigue este documento comprueba la **integridad de la evidencia**, nada más (sección 16).

Hechos, hipótesis y visión se mantienen separados. Las secciones 4 a 15 son normativas. La sección 16 enumera límites que son hechos de esta versión. La sección 17 enumera lo que aún no está definido.

## 2. Convenciones

- Las palabras DEBE, NO DEBE, DEBERÍA y PUEDE se usan como en la RFC 2119.
- **Versión** `1.0` es la versión del protocolo. Este documento, los esquemas JSON y los vectores se mueven juntos con ella.
- El texto es UTF-8. Un archivo nunca empieza con marca de orden de bytes (BOM).
- Los tiempos son cadenas UTC `YYYY-MM-DDTHH:MM:SS[.fff]Z`, con como máximo tres decimales. Cualquier desfase distinto de `Z` es inválido.
- Los hashes se escriben `sha256:` seguido de 64 dígitos hexadecimales en minúscula. Las claves públicas Ed25519 se escriben `ed25519:` seguido de base64 estándar de los 32 bytes. Las firmas Ed25519 en JSON son base64 estándar de los 64 bytes (88 caracteres, con relleno).
- Los identificadores de registros son ULID (26 caracteres, base32 de Crockford, mayúsculas).
- **Las definiciones legibles por máquina** son los esquemas JSON (borrador 2020-12) en `schemas/`: `common`, `record`, `pulse`, `checkpoint-meta`, `trust`, `spore`, `bundle` y `vitalsigns`. Donde este texto y un esquema discrepan, es un defecto: deciden los vectores de conformidad y el defecto se corrige en la próxima edición.
- Todo objeto en los esquemas es cerrado (`unevaluatedProperties: false` o `additionalProperties: false`). Un campo desconocido es un rechazo, no algo que se ignora.

## 3. Dos codificaciones

En la evidencia de Ilorium aparecen dos formatos de texto distintos. Nunca se mezclan.

| Se usa para | Codificación | Definida por |
| --- | --- | --- |
| Registros, pulsos, sidecars de checkpoint, configuración de confianza, informe del verificador | **JSON de Ilorium**: JSON canonicalizado con RFC 8785, restringido por la sección 4 | Este documento |
| El manifiesto del bundle | **JSON de Ilorium**, canónico, en una línea | Sección 13 |
| La Spore y los Vital Signs | JSON bajo las restricciones de la sección 4 (lectura estricta, solo enteros, sin nombres duplicados); no se exige que sean canónicos al transmitirse | Secciones 12 y 14 |
| Checkpoints y las cofirmas de sus testigos | **Nota firmada C2SP**: una nota de texto con líneas de firma | C2SP `signed-note`, `tlog-checkpoint`, `tlog-cosignature`, fijados en la sección 7 |

Un checkpoint **no** es un documento JSON y **nunca** se canonicaliza con RFC 8785. El número de latido y el tiempo de traducción, que el Pulse necesita y un checkpoint C2SP no puede llevar, viajan en un objeto JSON firmado aparte, el sidecar (sección 7.3).

## 4. JSON de Ilorium

El JSON de Ilorium es RFC 8785 (JSON Canonicalization Scheme) aplicado a un conjunto restringido de valores JSON. Las restricciones eliminan todo aquello en lo que las implementaciones independientes tienden a discrepar.

Un verificador DEBE rechazar, con el código de la columna derecha:

| Regla | Código |
| --- | --- |
| El valor de nivel superior no es un objeto | `not_object` |
| No es JSON válido, o hay contenido después del valor | `invalid_json` |
| Un número con fracción o exponente (`1.0`, `1E5`) | `float_not_allowed` |
| Un entero fuera de ±(2^53 − 1) | `integer_out_of_range` |
| `-0` | `negative_zero` |
| Una clave duplicada en cualquier objeto | `duplicate_key` |
| Un sustituto UTF-16 suelto en una cadena o clave | `lone_surrogate` |
| Anidamiento de más de 64 niveles | `too_deep` |
| Una marca de orden de bytes | `invalid_json` |

Consecuencias: ningún número de coma flotante entra jamás en la evidencia (una proporción son dos enteros o una cadena), y la canonicalización no necesita ningún algoritmo de formato de números. Las claves se ordenan por unidades de código UTF-16, como exige la RFC 8785.

**Forma canónica en disco.** Cada línea de `records.jsonl`, `checkpoints.jsonl` y `pulses.jsonl` DEBE ser ya la forma canónica de su objeto. Una línea que se analiza pero no es canónica es un fallo (`records.canonical`, `checkpoints.parse`, `pulses.parse`). Hay una sola cadena de bytes por objeto, así que hay un solo hash por objeto.

**Las firmas sobre JSON** usan una etiqueta de dominio para que una firma hecha con un propósito no pueda reutilizarse con otro:

```
entrada de firma = etiqueta || 0x0A || canónico(objeto sin su campo "signature")
firma            = Ed25519(entrada de firma)
```

| Objeto | Etiqueta (ASCII) |
| --- | --- |
| Pulso | `ilorium.pulse.v1` |
| Sidecar de checkpoint | `ilorium.checkpoint-meta.v1` |

## 5. Registros

Un **registro** es una línea del Strata: una observación, una afirmación o una evaluación (véase la especificación de la Probe para su significado). La sección 5 define sus campos; `schemas/record.schema.json` es la forma legible por máquina.

### 5.1 Envoltorio

| Campo | Significado |
| --- | --- |
| `id` | ULID, único en el log |
| `type` | `observation`, `claim` o `evaluation` |
| `occurred_at` | Cuándo ocurrió el evento según su fuente |
| `received_at` | Cuándo lo recibió la Probe |
| `recorded_at` | Cuándo lo escribió la Probe en el log |
| `beat` | El conteo de latidos del organismo, si el registro es un evento material (opcional) |
| `protocol_release`, `probe_version`, `rules_version`, `policy_version`, `spore_version` | Versiones vigentes cuando se escribió el registro |

Los tres tiempos se mantienen separados a propósito: una fuente puede llegar tarde y un reloj puede estar mal. Nunca se fusionan.

### 5.2 Observación

Lo que el instrumento vio, sin interpretación: `source`, `source_event_id`, `kind` (`event`, `outcome` o `gap`), `actor` (`id` y `kind`: `agent`, `human`, `unknown` o `instrument`), `action`, `object`, `fields` opcional (hasta 64 valores escalares; cadenas de hasta 1024 caracteres; sin objetos anidados) y `content_hash` opcional.

El contenido nunca se guarda en un registro, solo su hash.

### 5.3 Observaciones de hueco

Una ausencia de evidencia es evidencia, si se deja escrita. Cuando la Probe sabe que no capturó algo, DEBE escribir una observación con `kind: "gap"`. Su `actor.kind` DEBE ser `instrument` (informa la propia Probe, no un agente). Sus `fields` DEBEN contener:

| Campo | Significado |
| --- | --- |
| `from`, `to` | El tramo, en UTC |
| `reason` | `collector_down`, `queue_overflow`, `source_retention`, `probe_down`, `clock_unreliable` u `other` |
| `lost` | Cantidad de eventos que se sabe perdidos, si se sabe (opcional) |

Un hueco declarado aparece en el informe del verificador como un hueco de tipo `declared`. Un verificador nunca convierte un hueco en fallo por sí solo: la Probe dijo la verdad sobre lo que se le escapó.

### 5.4 Afirmación

Un enunciado hecho por alguien sobre un evento: `claimant` (`id`, `kind` de `agent` o `human`), `about` (un `id` de registro o un nombre), `cause.type` (`autonomous`, `environment`, `directive` o `approval`, con un `ref` opcional), `policy` y `context` opcionales. Una afirmación nunca se presenta como un hecho.

### 5.5 Evaluación

Una conclusión que un instrumento saca de registros anteriores: `evaluator` (`name`, `version`), `inputs` (uno o más ids de registro), `function` (`operation`, `resources`, `resolution`, `development`, `growth` o `unclassified`), `attribution` (`declared`, `linked`, `corroborated`, `unknown` o `disputed`), `crossing` (`none`, `unknown`, `operational`, `directive`, `approval`, `emergency`, `governance` o `test`), `work_unit` opcional, `weight` (`low`, `medium` o `high`) y `supersedes` opcional. Una evaluación nunca edita lo que evalúa: una corrección es una evaluación nueva que reemplaza a la anterior.

### 5.6 Qué comprueba un verificador sobre los registros

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `records.parse` | Una línea no es JSON de Ilorium, o el archivo tiene una línea en blanco, no termina en salto de línea o contiene un retorno de carro |
| `records.canonical` | Una línea no está en forma canónica |
| `records.schema` | Un registro no cumple el esquema |
| `records.ids` | Dos registros comparten un `id` |
| `records.refs` | Una entrada de `inputs` o `supersedes` de una evaluación, o un `about` de una afirmación que es un id, no apunta a un registro **anterior** (de tipo evaluación en el caso de `supersedes`) |
| `records.order` | `beat` no crece estrictamente (FAIL); `recorded_at` retrocede (UNKNOWN: puede ser una regresión del reloj, no una manipulación) |

## 6. El log

El Strata es un árbol de Merkle de solo añadir, según la RFC 6962 sección 2.1 (la construcción que la RFC 9162 mantiene para logs con SHA-256).

- **Hoja**: `SHA-256(0x00 || bytes canónicos del registro)`, donde los bytes del registro son la línea sin su salto de línea.
- **Nodo**: `SHA-256(0x01 || izquierda || derecha)`.
- **Árbol vacío**: `SHA-256("")`.
- El árbol se parte en la mayor potencia de dos menor que el tamaño.
- Las **pruebas de inclusión** y las **pruebas de consistencia** son las de la RFC 6962 secciones 2.1.1 y 2.1.2, verificadas como en la RFC 9162 secciones 2.1.3.2 y 2.1.4.2.

Un verificador que recibe los registros recalcula él mismo la raíz en cada tamaño de checkpoint. No necesita una prueba de la Probe para hacerlo, y nunca toma una raíz por la palabra de la Probe.

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `log.root` | Los registros no producen la raíz en el tamaño de un checkpoint (FAIL); el checkpoint cubre más registros de los que se entregaron (UNKNOWN) |
| `log.coverage` | Hay registros posteriores al último checkpoint (UNKNOWN: aún no están protegidos) |

## 7. Checkpoints y testigos

### 7.1 Formato: C2SP, fijado

Los checkpoints son **tlog-checkpoints de C2SP** en formato **signed-note**. Ilorium no inventa un formato de checkpoint. Las versiones están fijadas:

| Especificación | Versión fijada |
| --- | --- |
| `signed-note` | C2SP v1.1.0 |
| `tlog-checkpoint` | C2SP v1.1.0 |
| `tlog-cosignature` | C2SP v1.1.0 |
| `tlog-witness` | C2SP v1.1.0 |

Cambiar una versión fijada es un cambio a este documento, con entrada en el changelog y vectores nuevos.

El cuerpo de un checkpoint tiene tres líneas: el **origen** (la identidad del log, configurada en el archivo de confianza), el tamaño del árbol en decimal y el hash raíz en base64 estándar. **En Ilorium 1.0 no se permiten líneas de extensión**: un checkpoint con una cuarta línea falla (`checkpoint.note`).

Una clave de verificación («vkey») se escribe como en C2SP: `nombre+hex(keyid)+base64(tipo || clave pública)`, donde `keyid = SHA-256(nombre || 0x0A || tipo || clave pública)[:4]`. Como la parte en base64 puede contener `+`, una vkey se divide solo en los dos primeros `+`. Una vkey cuyo identificador no coincide con su clave es inválida.

### 7.2 Perfil de algoritmos y firmas no soportadas

| Rol | Byte de tipo de firma | Algoritmo | Estado en 1.0 |
| --- | --- | --- | --- |
| Firma del log | `0x01` | Ed25519 sobre el texto de la nota | Obligatoria |
| Cofirma de testigo | `0x04` | Ed25519 (`cosignature/v1`, con marca de tiempo) | Soportada |
| Cofirma de testigo | `0x06` | ML-DSA-44 (estructura `subtree/v1`, con marca de tiempo) | Soportada |
| Cualquier otro tipo, incluido `0x02` (ECDSA) | — | — | **No soportado** |

El perfil inicial no es «todo es Ed25519». Los testigos que firman con ML-DSA-44, que C2SP recomienda, se aceptan junto a los testigos Ed25519.

**Qué pasa con una firma que el verificador no puede comprobar.** Nunca cuenta como verificada y nunca cuenta como inválida:

- Una cofirma con un algoritmo no soportado se informa como `unsupported`. No cuenta para el quórum de testigos. Si no se alcanza el quórum y existe al menos una de esas firmas, el resultado es **UNKNOWN** con el motivo indicado, no FAIL: el verificador no sabe que el testigo se equivocó, solo que no puede saberlo.
- Una firma soportada que no verifica es **FAIL**.
- Una firma del log con un algoritmo no soportado, sin otra firma válida del log, es **UNKNOWN**. Un checkpoint sin firma del log de una clave configurada es **FAIL**.
- Una línea de firma de una clave que no está en el archivo de confianza se ignora.

**ML-DSA-44 depende de la plataforma.** Un verificador necesita una biblioteca criptográfica que lo ofrezca (el verificador de referencia exige `cryptography` 48 o posterior, que usa OpenSSL 3.5 o posterior). Un verificador que no lo tiene DEBE informar las cofirmas ML-DSA-44 como `unsupported`, lo que da UNKNOWN como arriba, nunca un error, y DEBE decirlo en el informe (`verifier.ml_dsa_44` es `false`).

Un algoritmo nuevo entra al perfil solo mediante un cambio a este documento y vectores nuevos.

### 7.3 El sidecar

Un checkpoint C2SP no lleva número de latido ni tiempo de traducción. El Pulse necesita ambos (dos relojes). Por eso cada checkpoint viaja con un **sidecar**, un objeto JSON de Ilorium firmado (`schemas/checkpoint-meta.schema.json`):

| Campo | Significado |
| --- | --- |
| `checkpoint_meta` | `"1.0"` |
| `origin`, `tree_size`, `root` | Deben coincidir exactamente con la nota |
| `beat` | El conteo de latidos del organismo cuando se hizo el checkpoint |
| `translation_time` | Hora UTC en que el log lo firmó |
| `trigger` | `beats` o `interval` |
| `signature` | Ed25519 con la clave del log (la de la firma `0x01` del log), etiqueta `ilorium.checkpoint-meta.v1` |

El sidecar es la afirmación del organismo sobre su propio latido y hora. Los testigos cofirman la nota, no el sidecar. La **marca de tiempo** del testigo en una cofirma `0x04` o `0x06` es la referencia de tiempo independiente: un verificador la compara con el `translation_time` del sidecar (sección 7.4).

### 7.4 Qué comprueba un verificador sobre los checkpoints

Una línea de `checkpoints.jsonl` es un objeto JSON de Ilorium con exactamente dos campos: `note` (la nota firmada, como cadena) y `meta` (el sidecar).

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `checkpoints.parse` | El archivo está mal formado, una línea no es canónica o no tiene exactamente `note` y `meta` |
| `checkpoint.note` | La nota está mal formada, el origen no es el configurado o tiene líneas de extensión |
| `checkpoint.log_signature` | No hay firma válida del log (FAIL); solo hay una no soportada (UNKNOWN) |
| `checkpoint.witnesses` | Una cofirma soportada no verifica (FAIL); hay menos cofirmas verificadas que el quórum (UNKNOWN) |
| `checkpoint.meta` | El sidecar es inválido, no coincide con la nota o su firma falla (FAIL); no hay clave para comprobarlo (UNKNOWN) |
| `checkpoint.monotonic` | El tamaño del árbol se reduce, el mismo tamaño tiene otra raíz, o el latido o el tiempo retroceden (FAIL). Que un árbol mayor extienda a uno menor lo comprueba `log.root`, que recalcula cada raíz de checkpoint a partir de los registros |
| `checkpoint.interval` | Más de `max_interval_s + grace_s` entre checkpoints (UNKNOWN; un hueco de tipo `checkpoint_interval`); no hay configuración de frescura (UNKNOWN) |
| `checkpoint.witness_time` | La marca de tiempo de un testigo difiere del tiempo del sidecar en más de `grace_s`, o está en el futuro (UNKNOWN) |

Que crezca el tamaño del árbol sin que crezca el latido, o al revés, no es un error en sí; retroceder sí lo es.

### 7.5 Testigos públicos: qué se afirma y qué no

Usar el formato C2SP hace a Ilorium **compatible** con testigos públicos. No da acceso a ellos: cada operador de testigo configura los logs y las claves que acepta, y puede rechazar un origen desconocido.

**La integración con testigos públicos no está disponible en esta versión.** Se declarará disponible solo después de ambas cosas: (1) una prueba de interoperabilidad de un log de Ilorium contra un testigo real, y (2) un acuerdo con un operador de testigo. Hasta entonces, los testigos son los que la organización configura y opera o gestiona por su cuenta, y el verificador comprueba las cofirmas que se le entreguen.

## 8. Pulsos

Un pulso es el objeto definido en la especificación del Pulse, sección 4; `schemas/pulse.schema.json` es la forma legible por máquina. Esta sección solo agrega las reglas de evidencia.

- `signature` es Ed25519 con la clave del Spore (`pulse_key`) bajo la etiqueta `ilorium.pulse.v1` (sección 4).
- `prev_pulse` es `sha256:` del **pulso anterior canónico, firma incluida**. El primer pulso tiene `prev_pulse: null`.
- `seq` empieza en 1 y aumenta de uno en uno.
- `checkpoint` nombra un tamaño de árbol y una raíz; la raíz debe ser la que los registros producen en ese tamaño.

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `pulses.parse` | El archivo está mal formado o una línea no es canónica |
| `pulse.schema` | Un pulso no cumple el esquema |
| `pulse.signature` | La firma no verifica (FAIL); no hay clave de pulso configurada (UNKNOWN) |
| `pulse.chain` | `prev_pulse` no coincide, el primer pulso tiene predecesor o `seq` no aumenta (FAIL); faltan pulsos entre dos (UNKNOWN; un hueco de tipo `pulse_seq`) |
| `pulse.order` | `beat` o `translation_time` retroceden (FAIL) |
| `pulse.interval` | Más de `max_interval_s + grace_s` entre pulsos (UNKNOWN; un hueco de tipo `pulse_interval`), o el último pulso es más viejo que eso en el momento de la verificación (UNKNOWN; un hueco de tipo `stale_pulse`) |
| `pulse.checkpoint_ref` | La raíz no coincide con los registros (FAIL); el tamaño del árbol no está cubierto por los registros entregados (UNKNOWN) |

## 9. La exportación del Strata

Una exportación es un directorio:

| Archivo | Contenido |
| --- | --- |
| `records.jsonl` | Todos los registros, en orden del log, una línea canónica cada uno, cada una terminada en un único salto de línea |
| `checkpoints.jsonl` | Los checkpoints (sección 7.4), del más antiguo al más reciente |
| `pulses.jsonl` | Los pulsos, del más antiguo al más reciente |

`checkpoints.jsonl` y `pulses.jsonl` pueden faltar; se informa como UNKNOWN, no como FAIL. `records.jsonl` es obligatorio.

**La exportación no contiene las claves que la verifican.** Las claves se entregan aparte en `trust.json` (sección 10). Una exportación que trajera sus propias claves solo probaría que coincide consigo misma.

Un archivo vacío es un archivo válido de cero entradas. Las líneas terminan en un único salto de línea; se rechazan los retornos de carro, las líneas en blanco y la falta de salto de línea final.

## 10. Configuración de confianza

`trust.json` (`schemas/trust.schema.json`) es lo que aporta **quien verifica**:

| Campo | Significado |
| --- | --- |
| `trust` | `"1.0"` |
| `organism` | La etiqueta del organismo |
| `log.origin`, `log.vkeys` | El origen del log y sus claves de verificación (1 a 8) |
| `witnesses.quorum`, `witnesses.vkeys` | Cuántos testigos distintos deben haber cofirmado, y sus claves |
| `pulse_key` | La clave de pulso Ed25519 |
| `freshness.max_interval_s`, `freshness.grace_s` | Máximo de segundos entre checkpoints y pulsos, y la demora tolerada |

Los testigos distintos se cuentan por **nombre de testigo**: el mismo testigo firmando dos veces cuenta una vez. Una cofirma con marca de tiempo posterior a la hora de verificación no cuenta para el quórum.

En la versión 1.0 el archivo de confianza se entrega a mano. Anclar las claves en el acto de nacimiento, para que un verificador pueda partir del Spore, aún no está implementado (sección 17).

## 11. Veredictos e informe

Cada chequeo termina en uno de tres resultados. No hay un cuarto.

| Veredicto | Significado |
| --- | --- |
| **PASS** | El chequeo se ejecutó y lo examinado es consistente |
| **FAIL** | La evidencia es inconsistente, falsificada o alterada |
| **UNKNOWN** | El verificador no pudo decidir: falta evidencia, está vencida o usa algo que no soporta |

El veredicto global es el peor de todos los chequeos: FAIL, luego UNKNOWN, luego PASS. Un archivo ausente o una configuración ausente es UNKNOWN, **nunca PASS**. UNKNOWN no es un FAIL más suave; es un «no probado» honesto, y el informe dice por qué.

**Huecos.** El informe lista cada hueco, declarado o detectado:

| Tipo | Origen |
| --- | --- |
| `declared` | Una observación de hueco escrita por la Probe (sección 5.3) |
| `checkpoint_interval` | Demasiado tiempo entre dos checkpoints |
| `stale` | El último checkpoint es más viejo de lo permitido al momento de verificar |
| `pulse_interval` | Demasiado tiempo entre dos pulsos |
| `pulse_seq` | Faltan números de pulso |
| `stale_pulse` | El último pulso es más viejo de lo permitido al momento de verificar |

La frescura (`stale`, `stale_pulse`) necesita un momento de verificación. El verificador lo toma de `--now`; sin él, esos dos chequeos son UNKNOWN. El verificador nunca lee por su cuenta el reloj del sistema, de modo que la misma entrada da el mismo informe.

**Informe.** Un objeto JSON de Ilorium con `report: "1.0"`, `verifier` (nombre, versión y si ML-DSA-44 está disponible), `protocol_release`, `organism`, `origin`, `verdict`, `summary` (conteos de registros, checkpoints y pulsos, registros posteriores al último checkpoint, el último checkpoint), `checks` (id, veredicto y motivo de cada uno), `gaps` y `limitations`. Un informe sobre un bundle (sección 13) agrega `bundle`.

**Las limitaciones son parte de todo informe.** Un informe que las omitiera podría tomarse por más de lo que es. El verificador de referencia imprime siempre las cinco de la sección 16, también con PASS.

**Estado de salida** del verificador por línea de comandos: 0 PASS, 1 FAIL, 2 UNKNOWN, 64 error de uso.

## 12. La Spore

La Spore es el documento que un organismo sirve en `https://<dominio>/.well-known/ilorium.json` (especificación de Descubrimiento y Crecimiento). `schemas/spore.schema.json` es su forma legible por máquina. Esta versión define los campos que lista el esquema; son un borrador y pueden cambiar antes de que exista una especificación de la Spore (sección 17).

Campos obligatorios: `spore` (`"1.0"`), `ilorium` (la versión), `organism`, `domain` y `stop_key_holders`. Opcionales: `genome`, `probe`, `membrane`, `threshold`, `agents`, `work_units`, `pulse_key`, `pulse`, `checkpoints`, `witnesses`, `humans`, `responsible`, `kin`, `partners`, `announce` y `signatures`. El objeto es cerrado.

**`stop_key_holders`** es una lista de uno a 64 titulares. Cada uno es `{kind, id, name, contact, credential}`:

| Campo | Significado |
| --- | --- |
| `kind` | `human` o `institution`. No hay valor para un organismo: un organismo nunca tiene una llave de parada |
| `id` | Un identificador estable, único en la lista |
| `name`, `contact` | Quién es el titular y cómo contactarlo, en público |
| `credential` | Una referencia a lo que identifica al titular. Su contenido no está definido en esta versión (sección 17) |

**Cualquiera de la lista puede parar el organismo.** Un linaje sin fundadores humanos lista a sus Vigilantes, al menos dos, independientes del organismo, de su linaje y entre sí. Ese requisito pertenece al Genoma y se verifica contra el registro de sucesión; el esquema no lo comprueba, y esta versión no define el registro de sucesión.

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `spore.parse` | El documento no es JSON de Ilorium válido (FAIL) |
| `spore.schema` | El documento no cumple el esquema (FAIL) |
| `spore.holders` | Dos titulares comparten un `id` (FAIL) |

Un chequeo que no pudo correr porque falló uno anterior es UNKNOWN. Estos chequeos no muestran que un titular sea quien la Spore dice, que la credencial sea válida, que el contacto funcione ni que las `signatures` verifiquen; nada de eso se verifica en esta versión.

## 13. El Evidence Bundle

Un Evidence Bundle es la evidencia detrás de los Vital Signs de un organismo (sección 14), descargable y comprobable sin confiar en Ilorium ni en el organismo. Es una exportación del Strata (sección 9), la Spore tal como estaba, y un manifiesto sobre ambas. `schemas/bundle.schema.json` es la forma legible por máquina del manifiesto.

Un bundle es un directorio plano. Cómo se empaqueta para descargarlo no está definido en esta versión; al verificador se le entregan los archivos por nombre.

| Archivo | Contenido | Obligatorio |
| --- | --- | --- |
| `bundle.json` | El manifiesto | Sí |
| `spore.json` | La Spore, tal como la sirvió el organismo | Sí |
| `records.jsonl` | Como en la sección 9 | Sí |
| `checkpoints.jsonl` | Como en la sección 9 | No |
| `pulses.jsonl` | Como en la sección 9 | No |

Las evaluaciones y afirmaciones de Proof of Life en que se apoyan los Vital Signs son registros (secciones 5.4 y 5.5) dentro de `records.jsonl`; no hay un archivo aparte. El bundle empieza siempre en el primer registro del log. Un bundle de una parte del log no está definido (sección 17).

**Un bundle nunca contiene las claves que lo verifican.** No hay archivo de confianza en un bundle, ni campo en el manifiesto para claves. La Spore puede llevar la `pulse_key` del organismo; es una afirmación del organismo, que se compara con la clave en que confía quien verifica (`bundle.spore_key`), nunca una raíz de confianza.

**El manifiesto** es un objeto JSON de Ilorium, canónico, en una línea que termina en un único salto de línea:

| Campo | Significado |
| --- | --- |
| `bundle` | `"1.0"` |
| `ilorium` | La versión del protocolo |
| `organism`, `domain`, `origin` | La etiqueta del organismo, su dominio y el origen de su log |
| `created_at` | Cuándo se armó el bundle |
| `period` | `from` y `to`: el `recorded_at` de cada registro está entre ambos, y `to` no es posterior a `created_at` |
| `files` | Por cada archivo que no es el manifiesto: `sha256` de sus bytes, `bytes` y, para los `.jsonl`, `entries` (el número de líneas) |

El hash del archivo del manifiesto, `sha256:` seguido del SHA-256 de sus bytes, es cómo los Vital Signs señalan el bundle con el que se calcularon.

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `bundle.parse` | El manifiesto está mal formado o no es canónico (FAIL); no se entregó (UNKNOWN) |
| `bundle.schema` | El manifiesto no cumple el esquema, o su período no cumple `from <= to <= created_at` (FAIL) |
| `bundle.files` | El hash, el tamaño o el número de entradas de un archivo difiere del manifiesto, o hay un archivo presente que no está listado (FAIL); un archivo listado no se entregó (UNKNOWN) |
| `bundle.no_trust` | El bundle contiene `trust.json` (FAIL) |
| `bundle.period` | El `recorded_at` de un registro queda fuera del período (FAIL) |
| `bundle.identity` | El organismo o el origen del manifiesto no es el configurado, o el organismo o el dominio de la Spore difiere del manifiesto (FAIL); la Spore no se puede leer para comparar (UNKNOWN) |
| `bundle.spore_key` | La `pulse_key` de la Spore difiere de la clave de pulso en que confía el verificador (FAIL); falta alguna de las dos (UNKNOWN) |

Un verificador además corre los chequeos de la Spore (sección 12) sobre `spore.json` y todos los chequeos de la sección 9 sobre los archivos del Strata. El veredicto del bundle es el peor de todos. Un manifiesto ausente es UNKNOWN, nunca PASS.

El informe es el de la sección 11, con los chequeos del bundle primero, un objeto `bundle` (`manifest_sha256`, `created_at`, `period`, `files`) y dos limitaciones más: el manifiesto es una lista de sumas de verificación que no está firmada, así que muestra que los archivos son los listados y no quién los armó; y la Spore es lo que el organismo dice de sí mismo.

Consultar y descargar un bundle es gratis y no requiere cuenta. Nada en un bundle es un sello, un certificado ni un puntaje.

## 14. Vital Signs

Los Vital Signs son el estado actual de un organismo en una forma que una persona o un agente lee en segundos (especificación de Descubrimiento y Crecimiento). `schemas/vitalsigns.schema.json` es la forma legible por máquina del JSON que se sirve en una dirección estable. **Presentan evidencia; por sí mismos no establecen nada.** Su vínculo con la evidencia es el bundle (sección 13).

| Campo | Significado |
| --- | --- |
| `vitalsigns` | `"1.0"` |
| `ilorium`, `organism`, `domain` | Versión, etiqueta del organismo y dominio |
| `generated_at`, `period` | Cuándo se calcularon y el período que cubren (`from <= to <= generated_at`) |
| `bundle` | `url` (https) y `manifest_sha256`: el Evidence Bundle con el que se calcularon |
| `web_status` | `sighting`, `in_gestation`, `observed` o `verified` (especificación del Ecosistema) |
| `latest_pulse` | `seq`, `beat`, `translation_time`, `state` y `recovery` del pulso más reciente, o `null` |
| `dimensions` | Las seis dimensiones de Proof of Life: `autonomy`, `coverage`, `reliability`, `control`, `human_dependency`, `provenance`. Siempre están las seis |
| `conformity` | Una entrada por ley del Genoma: `law` y `status` (`conforms`, `does_not_conform` o `not_observed`) |
| `provenance` | `birth`, `succession`, `generation` y `parents` (especificación del Ecosistema) |
| `stop_key_holders` | Como en la Spore (sección 12) |
| `limitations` | Al menos una |

Cada dimensión tiene los mismos campos sea cual sea su estado: `status`, `newest_evidence`, `measures` y `limitations` (al menos una). `status` es `observed`, `not_observed`, `no_activity` o `stale`. `observed` y `stale` necesitan `newest_evidence`; `not_observed` no tiene ninguna ni medidas; `no_activity` puede tener o no. **«No observado» tiene los mismos campos, y por lo tanto el mismo peso, que «observado».** Una medida es `{id, count, of}`: enteros, con `of` nulo para un conteo simple y el denominador para una proporción, de modo que no aparece ningún número de coma flotante. El cálculo de cada medida pertenece a Proof of Life y no está definido aquí (sección 17); los identificadores de medidas aún no están registrados.

**No hay campo para un puntaje, un ranking, un sello ni una insignia, y el objeto es cerrado**: agregar uno requiere una nueva versión. Los organismos nunca se ordenan en un ranking.

| ID de chequeo | Falla o es desconocido cuando |
| --- | --- |
| `vitals.parse` | El documento no es JSON de Ilorium válido (FAIL) |
| `vitals.schema` | El documento no cumple el esquema; el período está desordenado; `newest_evidence` es posterior al fin del período; una ley figura dos veces (FAIL) |
| `vitals.words` | Un texto de `limitations` contiene la palabra «certified», «trusted» o «approved», en cualquier caja, como palabra completa (FAIL) |
| `vitals.bundle` | El manifiesto no es el que nombra `manifest_sha256`, o un archivo del bundle ya no coincide con él (FAIL); el bundle no se puede alcanzar, o falta un archivo listado (UNKNOWN) |
| `vitals.identity` | El organismo, el dominio o el período difieren de los del manifiesto (FAIL) |
| `vitals.pulse` | `latest_pulse` no es el último pulso del bundle (FAIL); el bundle no tiene archivo de pulsos (UNKNOWN) |
| `vitals.stop_key_holders` | Difieren de la Spore del bundle (FAIL); la Spore no se puede leer (UNKNOWN) |

**Los Vital Signs cuyo bundle no se puede alcanzar son UNKNOWN**, nunca PASS. El chequeo de palabras es un mínimo mecánico para el texto escrito por quien presenta los Vital Signs; no garantiza que no se diga nada engañoso. Estos chequeos muestran que los Vital Signs coinciden con su bundle en lo que se puede comparar mecánicamente. No recalculan las dimensiones, el estado web, la conformidad ni la procedencia (sección 16).

## 15. Vectores de conformidad

Los vectores en `vectors/` son la otra mitad de esta especificación: las mismas entradas y los mismos resultados esperados para toda implementación, en cualquier lenguaje.

- Un archivo de vectores tiene `vector`, `operation`, `spec` (la sección que prueba), `description` y `cases`. Cada caso tiene un `id`, un `input` y el resultado esperado `expect` (coincidencia por subconjunto: la implementación puede devolver más, nunca menos ni algo distinto).
- Operaciones: `canonicalize`, `merkle_root`, `verify_inclusion`, `verify_consistency`, `verify_signed_note`, `verify_records`, `verify_strata`, `verify_spore`, `verify_bundle` y `check_vitalsigns`.
- `vectors/index.json` lista cada archivo con su SHA-256 y su número de casos.
- **Los vectores los genera `tools/gen_vectors.py`, que no comparte código con el verificador**, y las expectativas se escriben a mano. Los vectores nunca se editan a mano. Las firmas ML-DSA-44 se hacen en el modo determinista de FIPS 204, así que regenerar reproduce cada archivo byte por byte; una prueba lo comprueba, y `vectors/index.json` fija cada archivo por SHA-256.
- Un vector es externo: la nota firmada de ejemplo publicada en C2SP, para que el verificador se pruebe contra algo que ni Ilorium ni el generador escribieron.
- Las claves de prueba se derivan de cadenas públicas (`ilorium-test-vector-key/<nombre>`) y NO DEBEN usarse para nada más.

Una implementación declara conformidad con la versión 1.0 al pasar todos los vectores de esa versión. Pasarlos es necesario, no suficiente: muestra los casos anteriores y nada más.

## 16. Límites de esta versión

Son hechos sobre lo que significa una verificación bajo este documento:

1. Una firma muestra quién firmó, no que el contenido sea verdadero.
2. Un verificador comprueba solo los registros, checkpoints y pulsos que se le dieron. No puede mostrar que se registró todo evento relevante.
3. Los registros posteriores al último checkpoint no están protegidos por él.
4. Las claves vienen del archivo de confianza entregado; todavía no están ancladas en el acto de nacimiento.
5. Un verificador comprueba la integridad de la evidencia. No evalúa las leyes del Genoma ni Proof of Life.

6. El manifiesto de un bundle es una lista de sumas de verificación y no está firmado: muestra que los archivos son los listados, no quién armó el bundle.
7. Los Vital Signs se comparan con su bundle en identidad, último pulso, titulares de la llave de parada y palabras que no pueden usar. Las dimensiones, el estado web, la conformidad y la procedencia no se recalculan a partir de los registros, porque su cálculo aún no está definido.
8. *(Agregado el 2026-10-24.)* La evidencia producida por otro sistema (un recibo firmado de una llamada a una herramienta, una atestación de hardware, una identidad externa) e importada al Strata es un registro de que ese artefacto se recibió. Importar, normalizar, resumir con un hash o firmar un registro externo no aumenta la fuerza probatoria de la afirmación que ese registro hace. Un verificador DEBE mantener separadas la integridad del artefacto y la autenticación de su emisor de la evidencia de ejecución, la atribución de una decisión, la completitud de la observación y la conformidad del organismo; las afirmaciones que un registro importado no respalda quedan en UNKNOWN. La firma de un intermediario nunca es la firma de la contraparte de una acción. En esta versión no existe ningún adaptador para evidencia externa (sección 17).

Además, a la fecha de esta versión: los vectores ML-DSA-44 los produce `dilithium-py`, una implementación de FIPS 204 en Python puro que no comparte nada con el código de OpenSSL que usa el verificador, y ambas coinciden; nadie fuera de este proyecto ha revisado los vectores. Está previsto un segundo verificador, escrito por separado en otro lenguaje (arquitectura, M7), para comprobar si este documento basta para construir uno sin leer el primero.

## 17. Aún no definido

- La especificación de la Spore más allá de la sección 12, la verificación de sus firmas, qué debe ser la `credential` de un titular de la llave de parada, y el registro de sucesión firmado que permita comprobar el requisito de los Vigilantes.
- Un Evidence Bundle de una parte del log: llevaría la frontera de Merkle al comienzo (los hashes de los subárboles de los primeros registros) y un checkpoint cofirmado de ese tamaño, para unir los registros con el resto del log. Las referencias de sus registros a registros anteriores serían UNKNOWN, no FAIL.
- Cómo se empaqueta un bundle para descargarlo.
- Cómo se calculan a partir de los registros las medidas de Proof of Life, el estado web y la conformidad, y el registro de identificadores de medidas.
- Anclaje de las claves del log y del pulso en el acto de nacimiento.
- Registros de rotación de claves.
- Formato de desafío y respuesta (Pulse, preguntas abiertas).
- Registros de liberación, coalescencia y simulacro de recuperación.
- Integración con testigos públicos (sección 7.5).
- Redacción de registros, y la prueba de que una redacción ocultó solo lo que declaró.
- Adaptadores que importan evidencia de otros sistemas, los campos que esos registros conservan (sistema de origen y versión, identificador de origen, compromiso con el original, fechas de captura e importación, material del emisor, alcance de lo firmado, transformaciones, versión del adaptador) y sus vectores (arquitectura, «Adaptadores para evidencia externa»; límite 8 de la sección 16).

## 18. Licencias

El texto de este documento se licencia bajo CC BY 4.0. Los esquemas JSON, los vectores de conformidad, los ejemplos y todo el código se licencian bajo Apache-2.0, para que cualquiera pueda incorporarlos a una implementación sin una segunda licencia. Quienes contribuyen conservan sus derechos sobre lo que aportan y lo licencian bajo la licencia del archivo que cambian (entrada = salida). «Nadie posee el protocolo» es un propósito de gobierno; no reemplaza decir quién licencia cada aporte.

Quien figura como titular del copyright en los encabezados es «The Ilorium Authors», listado en `AUTHORS`. Cada commit lleva una línea `Signed-off-by:` (Developer Certificate of Origin 1.1). Un commit escrito por un agente de IA tiene al agente como autor, con su propia identidad, y el `Signed-off-by:` del humano u organización responsable; un agente nunca firma por sí mismo. El texto completo de CC BY 4.0 está en `LICENSE-SPECS`, y el de Apache-2.0 en `LICENSE`.
