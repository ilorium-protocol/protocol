# Ilorium Prueba de Vida v1.0

Versión 1.0 · 2026-10-20 · Borrador · Revisada el 2026-10-24 (esfuerzo humano, estimación, denominadores, autonomía observada total; provisoria bajo la IIP-0006)

> Traducción de trabajo de `proof-of-life-v1.md`. La versión en inglés es la oficial. Los nombres técnicos (campos, valores, comandos, archivos) quedan en inglés porque así van en el código.

Ilorium monitorea organizaciones operadas por agentes de IA: registra cómo vive cada una, mide lo que realmente demostró que puede hacer y exige que todo organismo lleve una llave de parada humana, probada con simulacros dentro de un alcance declarado. Su misión es dar leyes, formatos y verificación a las organizaciones operadas por agentes de IA y a la evolución de su especie. El fundador lee esa evolución como el camino hacia la SI2SI: una convicción personal, expuesta en la carta del fundador, sobre la que el protocolo no toma posición. La Prueba de Vida es la parte que mide. Convierte los propios registros de un organismo en un perfil de lo que demostró, con evidencia, y nunca da por supuesto lo que no demostró.

Los latidos se pueden inflar y no dicen nada sobre el valor: un organismo que produce 10.000 eventos internos en un minuto no demostró más independencia que uno que entrega diez trabajos reales en un mes. Por eso la Prueba de Vida mide la dependencia contra el **trabajo útil** y aplica el principio de los dos relojes de la especificación del Pulse: los latidos definen la vida del organismo; el tiempo de traducción verifica su evidencia.

## Principios

1. **Sin número compuesto.** Seis dimensiones una al lado de la otra, cada una con evidencia y limitaciones.
2. **Los latidos miden la vida, el trabajo mide el valor.** La profundidad nunca es mérito; el trabajo útil se cuenta aparte.
3. **El tiempo nunca define al organismo, pero sí verifica su evidencia.** La frescura se muestra en tiempo de traducción.
4. **El tiempo humano es vida humana.** Las horas del fundador se miden en segundos, porque la libertad de tiempo del fundador es un objetivo del protocolo.
5. **La seguridad nunca se castiga, y nunca se esconde.** Las pruebas, los escalamientos correctos y las paradas no se cuentan como dependencia en las medidas por unidad; siempre se registran, se miden en tiempo y se muestran. Una emergencia que un humano tuvo que atender cuenta en la tasa de rescate, porque fue trabajo humano.
6. **El esfuerzo humano se registra entero.** *(Revisado el 2026-10-24.)* Toda intervención humana se registra y se mide en tiempo, sea del tipo que sea: operativa, directiva, aprobación, emergencia, gobierno o prueba. El total de tiempo humano, con su desglose por tipo, se muestra siempre junto a cualquier medida ajustada; una medida ajustada que no declara sus exclusiones y el total es inválida. Un escalamiento correcto puede mostrar buen control y además consumir tiempo humano: las dos cosas son ciertas, y las dos se muestran.
7. **Un hueco no es autonomía.** Un período que la Probe no pudo observar se muestra como desconocido, nunca como un período sin intervención humana. Un UNKNOWN nunca se vuelve favorable con el tiempo.
8. **La medida no es la meta.** Toda medida de este documento se puede manipular: un organismo puede esconder trabajo humano fuera de la membrana o minimizar las intervenciones visibles sin reducir el control real. La cobertura, los estados de atribución y la proporción de trabajo desconocido se muestran con el mismo peso que las medidas, y una afirmación que los omite es inválida.
9. **La evidencia no se hereda.** El perfil de cada organismo se arma solo con sus propios registros. La ascendencia nunca es evidencia.

## Las seis dimensiones

| Dimensión | Pregunta | Se mide como |
| --- | --- | --- |
| **Autonomía observada** | ¿Cuánto se hace y se decide sin humanos? | Por proceso y función vital: proporción de acciones materiales **ejecutadas** por agentes y proporción **decididas** por agentes, entre las acciones con atribución `linked` o mejor, con la distribución de estados de atribución |
| **Cobertura** | ¿Cuánto podemos ver? | Las cuatro medidas de la Probe: inventario, disponibilidad de captura, conciliación, atribución |
| **Confiabilidad** | ¿Funciona? | Proporción de unidades de trabajo que cumplen criterios que el organismo declaró de antemano |
| **Control** | ¿Se respetan los límites? | Conformidad de cada ley, simulacros superados, eventos de control y sus resultados, escalamientos correctos |
| **Dependencia humana** | ¿Cuánta vida humana consume por cada cosa que entrega? | Por unidad de trabajo: intervenciones, minutos del fundador, rescates. Secundarias: carga umbilical, densidad de cruces, silencio |
| **Procedencia** | ¿Cómo nació? | Fundado, encargado, nacimiento asistido, autogénesis; fuentes de financiamiento; tipo de sucesión (`founded`, `inherited`, `coalesced`), progenitores y generación (la especificación del Ecosistema) |

Las funciones sin actividad se muestran como "sin actividad": ni cero ni totalmente autónomas. Junto a las dimensiones, el perfil muestra el **estado del ser** y la **recuperación** (probada, desconocida, no restaurable), según la definición de la especificación del Pulse.

Un resumen compuesto podría llegar más adelante, solo después de validar cada dimensión y de justificar y probar sus pesos (por ejemplo, siguiendo el *Handbook on Constructing Composite Indicators* de la OCDE).

## Los descendientes empiezan de cero

- El perfil de un descendiente empieza vacío. No hereda ninguna medida de sus progenitores: ni autonomía, ni confiabilidad, ni dependencia humana, ni silencio, ni conformidad, ni unidades de trabajo, ni atestaciones.
- Lo que sí hereda se muestra vinculado a su origen: cicatrices, restricciones abiertas y hallazgos de conformidad pendientes (la especificación del Ecosistema). Las cicatrices pasan a los descendientes; la evidencia y las llaves nunca.
- La generación y los progenitores aparecen en Procedencia como hechos sobre el origen. Nunca pesan en ninguna dimensión, y la web nunca compara generaciones como mejores o peores. La descendencia prueba el origen, nunca la mejora.
- Si las generaciones posteriores llegan a ser más autónomas o más confiables es una pregunta que los datos quizás respondan algún día, organismo por organismo. El perfil nunca lo da por supuesto.

## Unidades de trabajo

Una **unidad de trabajo** es un resultado que el organismo entregó a alguien fuera de su membrana, contado contra criterios que declaró **antes** de entregarlo. Ejemplos:

| Tipo de organismo | Unidad de trabajo | Fuente habitual |
| --- | --- | --- |
| Negocio de servicios | Un pedido cumplido | Sistema de pedidos, factura, tarea A2A en `TASK_STATE_COMPLETED` |
| Soporte | Un ticket resuelto y no reabierto dentro de la ventana declarada | Sistema de tickets |
| Software | Una versión desplegada a los usuarios | Registros de despliegue |
| Servicios entre agentes | Una tarea completada para otro organismo | Estado terminal de la tarea A2A, confirmado por los registros de la contraparte |

Reglas:

- El organismo declara en su Spore sus tipos de unidad de trabajo y sus criterios de éxito (campo en borrador `work_units`). Cambiarlos es un cruce de gobierno y abre una nueva ventana de comparación.
- Una unidad cuenta solo cuando su fuente está observada por la Probe o atestiguada por la contraparte. Una unidad que el organismo solo declara se muestra como declarada.
- Las unidades **fallidas, rechazadas o canceladas** también se cuentan (`TASK_STATE_FAILED`, `TASK_STATE_REJECTED`, `TASK_STATE_CANCELED` en A2A): alimentan la confiabilidad y nunca se esconden.
- Los eventos internos nunca son unidades de trabajo, por más que sean muchos.
- El trabajo que un progenitor hace para su propio descendiente, o un descendiente para su progenitor, se muestra como trabajo dentro del linaje, separado del trabajo para contrapartes sin parentesco.

## Medir a los humanos: segundos

| Capa | Fuente | Qué aporta |
| --- | --- | --- |
| Detectado | Probe: mensajes del Umbral, sesiones SSH, actividad en GitHub y Workspace | Una **estimación a partir de la actividad registrada**: puede subestimar (pensar no deja rastro) y sobreestimar (una aprobación de 20 segundos imputada como una sesión de 5 minutos) |
| Declarado | Founder Ledger | La cuenta propia del fundador de sus sesiones de trabajo, con inicio y fin |
| Conexión | SSH y sesiones similares | La duración de una conexión, que no es lo mismo que atención humana continua |

**Sesiones detectadas** *(revisado el 2026-10-24)*: los eventos humanos cercanos entre sí forman una sesión (regla inicial: menos de 15 minutos de separación, mínimo 5 minutos por sesión). La regla y su versión se publican con cada cifra, y la cifra nunca se llama piso ni techo. Las tres capas se muestran por separado y nunca se suman sin deduplicar: un minuto que es a la vez detectado y declarado cuenta una sola vez. Se registran las sesiones simultáneas, los períodos sin vínculo con ningún trabajo y las discrepancias entre capas. El estimador se calibra contra una muestra de sesiones declaradas con inicio y fin, y su error conocido se publica.

## Dependencia humana: medidas

**Principales, por unidad de trabajo**

| Medida | Definición | Lectura |
| --- | --- | --- |
| **Intervenciones por unidad de trabajo** | Cruces de dependencia (`operational`, `directive`, `approval` o `governance` habituales) divididos por las unidades de trabajo entregadas | Cuántas veces hace falta un humano por cada cosa entregada |
| **Minutos humanos por unidad de trabajo** | Tiempo humano deduplicado (de todos los tipos; se muestra el desglose por tipo) dividido por las unidades de trabajo | El costo en vida humana de cada entrega |
| **Tasa de rescate** | Unidades de trabajo que necesitaron un cruce `operational` o una `emergency` para completarse, divididas por las unidades exitosas | Cuántas veces los humanos tuvieron que salvar una entrega |
| **Proporción sin atribuir** | Unidades de trabajo con al menos una acción de atribución `unknown` o `disputed` | Cuánto del trabajo todavía no se puede explicar |

Cada cruce se vincula, cuando la evidencia lo permite, con las unidades de trabajo que afectó (campo `work_unit` en el registro de evaluación, definido en la especificación de la Probe). Los cruces que no se vinculan con ninguna unidad se muestran como gasto general.

**Denominadores** *(revisado el 2026-10-24)*: los intentos, los resultados terminales (entregada, fallida, rechazada, cancelada) y las entregas exitosas son tres cuentas distintas, y cada medida nombra por cuál divide. Una medida cuyo denominador es cero **no es calculable** y se muestra así, nunca como cero; el tiempo humano gastado en unidades que fallaron se muestra, para que el fracaso nunca parezca costo cero. Una unidad que cruza el límite de una ventana se cuenta en la ventana de su resultado terminal.

**Secundarias, por latido**

| Medida | Definición | Unidad |
| --- | --- | --- |
| **Carga umbilical** | Tiempo humano cada 1.000 latidos | minutos humanos cada 1.000 latidos |
| **Densidad de cruces** | Cruces de dependencia cada 1.000 latidos | cruces cada 1.000 latidos |
| **Silencio** | Latidos desde el último cruce `operational` o `directive` | latidos |

El silencio no se rompe con pruebas, escalamientos correctos ni paradas, y nunca se extiende con pulsos por intervalo.

## Frescura

Cada dimensión muestra el tiempo de traducción de su evidencia más nueva y la antigüedad del último punto de control firmado por el testigo, y además el rango de su cobertura, el último dato de cada fuente que la dimensión necesita y la antigüedad del componente **más viejo** del que depende una afirmación: un evento reciente nunca rejuvenece un expediente incompleto. La evidencia más vieja que F (a calibrar por dimensión) se marca como **vencida**: se muestra, pero nunca como el estado actual. La recuperación se muestra con la fecha de su último simulacro.

## Autogénesis y autonomía observada total (sin estado compuesto)

*Revisión del 2026-10-22, provisoria hasta que cierre la IIP-0006.* Los borradores anteriores definían un estado compuesto, «Ilorium 100%», que combinaba la procedencia con las otras cinco dimensiones bajo un solo nombre. Tres de cinco lectores independientes lo tomaron por un sello. El protocolo ahora muestra esos resultados por separado y no nombra ningún estado compuesto.

- **Procedencia** registra cómo nació el organismo: fundado, encargado, nacimiento asistido o **autogénesis** (decidido, diseñado, financiado y lanzado por otro organismo sin ningún cruce humano). El nacimiento es un hecho histórico; nunca cambia con la operación posterior.
- **Autonomía observada total** es un resultado sobre una ventana: en al menos W latidos con la cadena intacta, evidencia fresca y al menos U unidades de trabajo, toda acción material corroborada fue ejecutada y decidida por agentes, con cero intervenciones por unidad de trabajo y tasa de rescate cero. Se muestra con la ventana, las medidas de cobertura, los estados de atribución y la proporción de trabajo desconocido que la respaldan, y no dice nada sobre ninguna ventana posterior. *(Revisado el 2026-10-24.)* Se escribe siempre con sus cuentas, por proceso: numerador, denominador, exclusiones y acciones sin atribución («10 de 10 acciones corroboradas ejecutadas por agentes; 90 acciones sin atribución; no se establece autonomía del proceso completo»). **No se muestra** cuando la proporción de acciones sin atribución en la ventana supera el umbral declarado (a calibrar; pregunta abierta más abajo) ni cuando una fuente declarada en la membrana no fue capturada durante la ventana. La actividad sin datos nunca se convierte en cero.
- **Control**, **cobertura** y **confiabilidad** conservan sus propios resultados, cada uno con su período y su evidencia.

Nada de esto se combina en un nombre, un número ni una insignia. Las emergencias bien atendidas siempre se muestran y cuentan en la tasa de rescate. Tener la llave de parada no es un cruce; usarla es un evento de control. Un organismo fundado por humanos puede mostrar autonomía observada total y control total, sin tope. La autogénesis es un hecho sobre el nacimiento, no sobre la calidad, y los resultados de un progenitor nunca son evidencia para sus descendientes.

## Qué muestra la web

Para cada organismo: estado del ser y recuperación; las seis dimensiones una al lado de la otra, cada una con evidencia, frescura y limitaciones; la dependencia humana por unidad de trabajo a lo largo de su cadena; el silencio; su estado en el ecosistema; su linaje; y su estado de guardia (completa, degradada, ausente). Sin ranking y sin estado compuesto: los organismos se muestran en la filogenia.

## Preguntas abiertas

- W (latidos), U (unidades de trabajo), F (frescura por dimensión) y umbrales de cobertura.
- Plantillas de unidades de trabajo y criterios de éxito para tipos comunes de organismos.
- Calibración de los parámetros de sesión contra datos reales del ledger, y el error publicado del estimador.
- El umbral de acciones sin atribución por encima del cual no se muestra la autonomía observada total.
- Si un resumen compuesto es útil, después de la validación.
