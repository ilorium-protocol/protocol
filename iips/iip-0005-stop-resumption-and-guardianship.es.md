# IIP-0005 · Parada, reanudación y guardia

*Traducción de trabajo. Si difiere de `iip-0005-stop-resumption-and-guardianship.md`, prevalece la versión en inglés.*

| Campo | Valor |
| --- | --- |
| Número | IIP-0005 |
| Título | Parada, reanudación y guardia |
| Autor | El fundador (Seldon), con Claude (IA, identificada como tal) |
| Estado | Borrador; se abre a comentarios públicos cuando se publique el repositorio |
| Tipo | Cambio de método a `governance-v1.md`, sección 5, y una nota de especificación a la Spore (`stop_key_holders`) en `specs/evidence-format-v1.md` (30 días) |
| Afecta | Gobierno, secciones 2 (vínculos), 5.1–5.5; la Spore; Vital Signs (estado de guardia) |
| Decide | El fundador, como único Custodio durante el gobierno provisorio, en público, después del período de comentarios |
| No toca | La Ley 3 del Genome, la IIP-0002 ni ninguna cerradura. La llave de parada humana, «cualquier Vigilante puede parar» y «ningún organismo tiene una llave» quedan como están |

## Motivación

El primer borrador de la sección 5 contenía una contradicción y dos huecos, confirmados por las revisiones externas y por el texto:

- La definición de «interés» (sección 2) hacía de tener una llave de parada un interés, mientras la sección 5.1 exigía que los Vigilantes declararan no tener interés: un Vigilante no podía ser Vigilante. Corregido el 2026-10-22 con una tabla de incompatibilidades por función.
- Con exactamente dos Vigilantes, si uno desaparecía el otro no era mayoría y no podía reemplazarlo; los Custodios solo intervenían cuando no quedaba ningún Vigilante.
- Cualquier Vigilante podía parar, y nada decía quién podía reanudar, qué pasa con una parada abusiva ni cómo se comportan los pagos mientras un organismo está parado. Un revisor nombró el riesgo real: un Vigilante que amenaza con parar para extorsionar.

## Especificación

Las reglas de abajo están en `governance-v1.md`, marcadas como *provisorias (IIP-0005)*.

1. **Estados de guardia (sección 5.4).** Completa (al menos dos Vigilantes activos con simulacro aprobado), degradada (uno: la parada funciona; ningún nacimiento bajo el organismo es válido; se designa un Vigilante interino dentro de los 14 días), ausente (ninguno: «sin vigilar»; compuerta de nacimiento cerrada; Vigilantes interinos dentro de los 14 días). El denominador de toda votación de Vigilantes son los Vigilantes activos para esa decisión, excluido quien esté recusado; ningún Vigilante vota su propia remoción.
2. **Parada, reanudación, sanción (sección 5.5).** Tres decisiones. Una parada se registra de inmediato con motivo categorizado y justificación para revisores autorizados, con explicación pública después. Haber parado no es un conflicto y no excluye a ese Vigilante de la decisión de reanudar. Reanudar exige la causa evaluada, las credenciales comprometidas revocadas, el alcance declarado, una decisión de los Vigilantes elegibles y un simulacro aprobado; un simulacro aprobado no muestra por sí solo que el incidente se resolvió. Una falsa alarma prudente no es mala fe. Perder la llave exige una causa definida, derecho de respuesta, un revisor independiente y un reemplazo efectivo; retirar el reconocimiento y revocar el acceso son dos actos registrados. Los Vigilantes interinos desempatan y completan cuando las recusaciones dejan menos de dos elegibles.
3. **Pagos durante una parada o una disputa (sección 5.3).** Sin cambios mientras el organismo está parado o en revisión; un organismo que deja de pagar se muestra así, y eso nunca es causal para remover a un Vigilante.
4. **Concentración y atención, publicadas (sección 5.2).** Cada Vigilante publica cuántos organismos vigila y la proporción de ingreso de guardia de cada uno; sin tope fijo; la verificación de independencia lo lee como riesgo. Dos Vigilantes que comparten cuenta, dispositivo o vía de recuperación no son independientes.
5. **Recomendación para la Spore.** La especificación de la Spore recomienda, para los organismos fundados por humanos, al menos dos `stop_key_holders` independientes entre sí por acceso y recuperación; los Vital Signs muestran cuando hay uno solo. Es una recomendación, no una exigencia: exigirlo cambiaría la Ley 3 y queda fuera de esta IIP.
6. **Lo que el protocolo nunca hace acá.** No pausa, no aísla ni opera un organismo. Registra el estado de guardia, lo publica y retira el reconocimiento de nacimientos.

## Qué rompe

Nada en funcionamiento. Reemplaza «mayoría de los Vigilantes» como única regla de reemplazo.

## Qué no establece

- La lista pública de Vigilantes voluntarios calificados: cómo se mantiene, quién la verifica.
- La responsabilidad legal que asume un Vigilante por tener una llave, que necesita asesoramiento legal antes de reclutar un Vigilante real.
- La regla de escala («nunca dos organismos del mismo linaje»), que se mantiene y queda marcada en revisión; su costo se mide en el piloto.
- Un procedimiento de respuesta a incidentes a nivel del protocolo, a escribir antes de que empiece la guardia real.
- *(Agregado el 2026-10-24.)* Quién selecciona, acepta, aprovisiona, revoca y demuestra la revocación del acceso técnico de un Vigilante, separado de la decisión pública que lo designa o lo remueve; y qué pasa cuando no existe ningún Vigilante elegible en la lista.
- *(Agregado el 2026-10-24.)* Una reserva financiada para que «los pagos siguen durante una parada» sea un mecanismo, con la regla para fondos insuficientes; hoy es una obligación escrita.

## Preguntas para quien comente

1. ¿Un organismo degradado debería conservar algún derecho a originar (por ejemplo, con un Vigilante interino), o «ningún nacimiento» es lo correcto?
2. ¿14 días es un plazo viable para los Vigilantes interinos antes de que exista una lista de voluntarios?
3. ¿Qué categorías de motivo de parada debería admitir el registro?
4. ¿Mantener los pagos sin cambios durante una parada crea su propio incentivo (parar y seguir cobrando)? ¿Qué agregarías?
5. ¿Quién debería tener y revocar las credenciales técnicas de un Vigilante, para que la decisión pública y el control de accesos sean dos actos y ninguno sea del organismo?

## Vectores de prueba

El estado de guardia va a necesitar vectores en el esquema de Vital Signs (`complete`, `degraded`, `absent`) cuando la IIP-0006 defina cómo se lee la evidencia; ninguno en esta IIP.
