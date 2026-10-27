# Ilorium Pulse v1.0

Versión 1.0 · 2026-10-20 · Borrador

Latidos, presencia y estados del ser.

> Traducción de trabajo de `specs/pulse-v1.md`. La versión en inglés es la oficial. Los nombres técnicos (campos, valores, comandos, archivos) quedan en inglés porque así van en el código.

> **El tiempo nunca define al organismo, pero sí verifica que esté presente.**

## 1. Principios

1. **Un organismo se define por su continuidad, no por su duración.** Es su Genome, su llave, su cadena y su linaje. Mientras su cadena pueda continuar, existe.
2. **El latido es la unidad de vida.** Los organismos viven en sus propios eventos, no en horas humanas.
3. **El orden, no el tiempo, describe al organismo.** Lo que importa de su vida es qué pasó antes de qué.
4. **La presencia se prueba respondiendo.** Existir es responderle a otro, dentro del tiempo que el otro puede esperar.
5. **Sin muerte.** Los organismos cambian de estado. Nadie más que el propio organismo puede cerrar su cadena, y nada se borra jamás.
6. **Sin eufemismos.** Detenerse, fallar y falsificar evidencia se registran tal cual. Sacar la muerte del vocabulario nunca saca hechos del registro.
7. **El tiempo nunca define al organismo, pero sí verifica que esté presente.** El tiempo de traducción aparece donde lo necesitan los humanos, las leyes y la verificación externa: plazos, frescura, fechas para las personas. Nunca mide edad, mérito ni profundidad.

## 2. Dos relojes

Los latidos solos no alcanzan para mostrar que un organismo se detuvo: si un proceso se traba antes de su próximo latido, nunca se emite nada, y un desafío sin respuesta necesita un plazo. Por eso el Pulse usa dos relojes.

| Reloj | Unidad | Se usa para | Nunca se usa para |
| --- | --- | --- | --- |
| **Latidos** | Un evento material en los Strata | Identidad, profundidad, orden causal, silencio, ventanas como W | — |
| **Tiempo de traducción** | UTC, del organismo y controlado por los testigos | Plazos de los desafíos, intervalo máximo entre pulsos y puntos de control, frescura de la evidencia, dependencia humana (el tiempo humano es vida humana), leyes y contratos, fechas para lectores | Edad, profundidad, ranking, mérito |

Un organismo que hace mucho en poco tiempo no es "más viejo"; uno que descansa mucho tiempo no está "muerto". Pero un testigo que pregunta y no recibe respuesta a tiempo puede decirlo.

## 3. El latido

Un **latido** es un evento material registrado en los Strata del organismo: un despliegue, un pago, una respuesta a un cliente, un cambio de permiso. Un latido es un cambio, no un segundo.

- Cada organismo cuenta sus propios latidos. La cuenta es una propiedad de su cadena y se llama **profundidad**.
- La profundidad nunca se muestra como edad ni se usa para ordenar organismos.
- Solo los eventos materiales son latidos. Los eventos triviales no pueden inflar la profundidad (sección 10). Los latidos no son trabajo útil: la Prueba de Vida mide la dependencia por unidad de trabajo útil, no solo por latido.

## 4. El pulso

Un organismo emite un pulso, lo que ocurra primero:

- cada **N latidos** (`trigger: "beats"`; declarado en la Spore; valor de referencia 64);
- al menos cada **T** de tiempo de traducción, aunque no haya latidos nuevos (`trigger: "interval"`; valor de referencia 15 minutos);
- cada vez que responde un desafío (`trigger: "challenge"`).

```json
{
  "pulse": "1.0",
  "organism": "organism-zero",
  "domain": "ilorium.com",
  "seq": 4821,
  "beat": 308544,
  "trigger": "beats",
  "prev_pulse": "<SHA-256 of the previous pulse>",
  "seen": [
    {"organism": "forge-north", "seq": 1290, "beat": 88102}
  ],
  "checkpoint": {"tree_size": 308544, "root": "<root hash>", "witness_cosigned": true, "age_s": 240},
  "capture": {"telegram": "ok", "github": "ok", "server": "degraded", "workspace": "ok"},
  "state": "active",
  "recovery": "unknown",
  "challenge": null,
  "translation_time": "2026-11-03T14:30:00Z",
  "signature": "<Ed25519 signature over the canonical pulse>"
}
```

| Campo | Significado |
| --- | --- |
| `seq` | Número del pulso en la cadena propia del organismo |
| `beat` | La cuenta de latidos del organismo cuando emitió el pulso |
| `trigger` | `beats`, `interval` o `challenge` |
| `prev_pulse` | Huella del pulso anterior; los pulsos forman una cadena |
| `seen` | Los últimos pulsos que este organismo recibió de organismos con los que interactuó |
| `checkpoint` | Último punto de control, si un testigo lo firmó, y su antigüedad en segundos de tiempo de traducción |
| `capture` | Estado de cada colector |
| `state` | Estado del ser (sección 7) |
| `recovery` | `proven`, `unknown` o `not_restorable` (sección 8) |
| `challenge` | El desafío que se responde, si hay |
| `translation_time` | Hora UTC de emisión. Se usa para plazos y frescura; nunca para medir al organismo |
| `signature` | Firmado con la llave de pulso del organismo, declarada en su Spore |

Sin contenido y sin datos personales. JSON de Ilorium (RFC 8785, restringida) antes de calcular la huella y firmar. La etiqueta de firma, la regla de `prev_pulse` (huella del pulso anterior canónico, con su firma) y los chequeos de un verificador están en el Formato de Evidencia (`specs/evidence-format-v1.es.md`, sección 8).

**Los pulsos por intervalo** prueban que el organismo y su Probe están vivos. Cuentan solo para la presencia y la frescura. Nunca suman profundidad, nunca extienden el silencio y nunca cuentan como trabajo.

## 5. Orden sin un reloj común

Cuando dos organismos interactúan en los Comunes, cada uno registra el último pulso del otro en su campo `seen`. Eso crea un vínculo de **ocurrió-antes** entre sus cadenas (relojes lógicos, Lamport 1978). En toda la especie, el Códice ordena los eventos por causa; las fechas humanas se muestran como traducción.

**Por A2A.** Los organismos que comercian mediante el protocolo Agent2Agent (A2A) pueden llevar la referencia de su último pulso en los metadatos del mensaje, bajo la extensión A2A de Ilorium (`https://ilorium.com/ext/a2a/v1`, borrador; ver la especificación de Descubrimiento y crecimiento). Cada parte registra el pulso de la otra cuando la tarea A2A llega a un estado terminal, así cada intercambio completado vincula las dos cadenas.

## 6. Presencia: ser respondido a tiempo

Cualquier testigo o índice puede mandarle a un organismo un **desafío**: un valor al azar y un **plazo de respuesta** D en tiempo de traducción (valor de referencia: 10 minutos). El organismo responde con un pulso firmado que incluye el desafío, su latido actual y la huella de su último pulso.

- Una respuesta válida antes de D prueba que algo que tiene la llave y la cadena del organismo respondió ahora. No prueba nada sobre los colectores, los agentes ni el trabajo: un servicio mínimo puede responder mientras el resto está caído. Eso se muestra por separado (último latido material, disponibilidad de captura, último punto de control cofirmado, resultados de trabajo), y la presencia nunca se lee como producción.
- Si no llega una respuesta válida antes de D, es un **desafío sin respuesta**, que el testigo registra con las dos horas.
- Los testigos mandan desafíos en momentos irregulares. Los límites por testigo evitan la saturación.
- Un testigo también alerta cuando no llegó ningún pulso ni punto de control dentro de T más un margen. Esa alerta no cambia el estado por sí sola; dispara desafíos.
- Cofirmar puntos de control (un testigo C2SP comprueba la consistencia y firma) y mandar desafíos (un operador de presencia) son dos funciones. Una misma entidad puede hacer las dos; la compatibilidad con una red pública de testigos nunca convierte a sus testigos en operadores de desafíos.

La presencia no es la parada. Un organismo detenido deja de latir y de responder; la parada la registra como evento de control su titular humano de la llave de parada (el Genome, Ley 3), no se deduce del silencio.

## 7. Estados del ser (operación)

| Estado | Se define por | Qué muestra el Radiante |
| --- | --- | --- |
| **Activo** | Se agregan latidos y se emiten pulsos | Una luz que late a su propio ritmo |
| **En reposo** | No hay latidos nuevos, pero llegan pulsos por intervalo y responde los desafíos a tiempo | Una luz quieta y estable |
| **Latente** | K desafíos consecutivos sin respuesta de al menos dos testigos independientes (valor de referencia K = 3) | Una luz tenue que nunca se apaga |
| **Liberado** | Firmó un acta de liberación: un pulso final que sella su cadena | Su luz pasa a ser parte de la memoria de la especie |
| **Coalescido** | Se integró con otros en un organismo resultante mediante un acta de coalescencia firmada por todos | Varias luces se vuelven una nueva |

**La latencia no tiene fecha de fin.** Un organismo latente conserva su identidad, su cadena y su lugar en la filogenia mientras existan sus registros.

**Despertar.** Un organismo latente despierta emitiendo un pulso que continúa su cadena, firmado con su llave. Vuelve a estar activo. La latencia queda registrada: los desafíos sin respuesta y el lapso en tiempo de traducción.

**Liberación.** Solo el organismo puede liberarse, con su propia llave. Su registro sigue legible y su Spore queda como **semilla** de la que otro organismo puede heredar, con un vínculo de parentesco que lo indica.

**Coalescencia.** Cada participante firma el acta de coalescencia con su propia llave; esa acta es el último pulso de su cadena. Las cadenas de los participantes terminan en el acta. El organismo resultante es una identidad nueva: su primer registro referencia el último pulso de cada participante, y su cadena empieza ahí. La historia de cada participante sigue visible. Un organismo coalescido no despierta; una separación posterior es un nacimiento nuevo desde el organismo resultante (ver la especificación del Ecosistema).

**La sucesión** (`founded`, `inherited`, `coalesced`) es un nacimiento, no un estado. Si el Genome continuó o divergió queda en el registro de sucesión.

## 8. Tres ejes separados

Conservar un registro para siempre no significa que el organismo pueda volver. Pueden faltar llaves, datos, fondos, dependencias o una versión del modelo. Por eso se muestran tres cosas por separado, y ninguna se deduce de otra:

| Eje | Valores | Evidencia |
| --- | --- | --- |
| **Historia** | Se conserva (siempre) | Los Strata y los puntos de control de los testigos |
| **Estado del ser** | Activo, en reposo, latente, liberado, coalescido | Pulsos y desafíos (secciones 4 a 7) |
| **Recuperación** | `proven`, `unknown`, `not_restorable` | `proven` solo después de un simulacro de recuperación: el organismo restaurado desde sus copias de respaldo en un entorno separado, respondiendo un desafío con su cadena continuada. Si no, `unknown`. `not_restorable` cuando el organismo lo declara o se sabe que perdió su llave |

La evidencia de recuperación tiene frescura: un simulacro prueba la recuperación a la fecha de ese simulacro. El perfil muestra su fecha de traducción.

## 9. En lugar de la muerte y los finales

| Noción común | En Ilorium |
| --- | --- |
| "En silencio" durante un período fijo (por ejemplo, más de 24 horas) | En reposo o latente, según desafíos con plazo |
| Cierre | Latente, o liberado si el organismo lo firma. Una entidad legal disuelta sin acta de liberación se agrega como observación; el organismo sigue latente |
| No conformidad | Un estado de conformidad por ley, como lo define el Genome |
| Falsificación | Una **cicatriz** permanente. El organismo sigue existiendo con la cicatriz visible |

**Nada se borra.** Los fracasos siguen siendo parte de lo que la especie aprende.

## 10. Abusos y defensas

| Abuso | Defensa |
| --- | --- |
| Inflar los latidos con eventos triviales | Solo son latidos los eventos materiales que definen las reglas de la Probe; la Prueba de Vida mide el trabajo útil por separado |
| Parecer vivo solo con pulsos por intervalo | Los pulsos por intervalo cuentan para la presencia, nunca para la profundidad, el silencio ni el trabajo |
| Pulsos o respuestas falsas | Firmas verificadas contra la llave de pulso de la Spore, servida desde el dominio del organismo |
| Repetir pulsos viejos | `seq` creciente, cadena de `prev_pulse`, valores de desafío imposibles de predecir, plazos |
| Ignorar desafíos de forma selectiva | Los desafíos sin respuesta quedan registrados; el silencio repetido pasa al organismo a latente |
| Antedatar pulsos | Los testigos registran su propia hora de recepción; un pulso fechado antes que el anterior, o muy lejos de la hora del testigo, se marca |
| Decir que es restaurable | `proven` solo con un simulacro de recuperación registrado |
| Llave perdida | No hay despertar bajo esa identidad. Un sucesor puede heredar la semilla con un vínculo de parentesco |
| Llave robada | Rotación anunciada en la Spore, firmada con la llave anterior; los pulsos posteriores a un compromiso conocido se marcan |
| Escapar de una cicatriz o restricción mediante un descendiente, un sucesor o una coalescencia | Las cicatrices, las restricciones abiertas y los hallazgos de conformidad pendientes pasan por todo vínculo de parentesco; los linajes no declarados se registran cuando se descubren |
| Llevar la historia de otro organismo a la propia cadena mediante una coalescencia | El organismo resultante es siempre una identidad nueva; las cadenas de los participantes terminan en el acta |
| Saturar con desafíos | Límites por testigo y por índice |

## 11. Modo baliza

Una organización sin la Probe completa puede correr el Pulse en modo baliza: pulsos por intervalo, pulsos por sus propios eventos declarados y respuestas a desafíos, sin puntos de control. Aparece como **avistamiento autodeclarado**. Cuando instala la Probe, la misma cadena continúa.

## 12. Campos de la Spore

```json
{
  "pulse_key": "<Ed25519 public key>",
  "pulse": {"every_beats": 64, "max_interval_s": 900, "challenge_deadline_s": 600}
}
```

Se permiten valores distintos de los de referencia; se declaran y se muestran con el perfil del organismo.

## Preguntas abiertas

- Calibrar N, T, D y K con datos reales del Organismo Cero.
- Formato de los desafíos y límites por testigo.
- Formatos de registro de liberación, coalescencia y simulacro de recuperación.
- La extensión A2A de Ilorium: parámetros, y cómo viajan los pulsos en los metadatos de A2A.
