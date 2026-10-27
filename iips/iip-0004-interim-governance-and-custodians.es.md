# IIP-0004 · Gobierno provisorio, Custodios y cambios constitucionales

*Traducción de trabajo. Si difiere de `iip-0004-interim-governance-and-custodians.md`, prevalece la versión en inglés.*

| Campo | Valor |
| --- | --- |
| Número | IIP-0004 |
| Título | Gobierno provisorio, Custodios y cambios constitucionales |
| Autor | El fundador (Seldon), con Claude (IA, identificada como tal) |
| Estado | Borrador; se abre a comentarios públicos cuando se publique el repositorio |
| Tipo | Cambio de método a `governance-v1.md`; toca la sección 10, así que lleva el período de comentarios reforzado: **90 días** *(corregido el 2026-10-24; el primer borrador decía 30)* |
| Afecta | Gobierno, secciones 2, 3.1, 3.2, 3.4, 4.2–4.6, 7, 8, 10 |
| Decide | El fundador, como único Custodio durante el gobierno provisorio, en público, después del período de comentarios, y solo para confirmar, acotar o retirar; las reglas constitucionales (punto 10) las ratifica después el consejo pleno |

## Motivación

Cinco revisiones externas del primer borrador de gobierno (`governance/reviews/`) coincidieron en cuatro problemas, y el texto los confirma:

1. La transición al gobierno pleno dependía de un solo evento (un organismo externo que llegara a Observado) que juzga el propio fundador, sin plazo. El gobierno provisorio podía durar para siempre.
2. El fundador invitaba a los dos Custodios independientes, y una objeción a una designación no tenía efecto declarado. Dos de tres podían ser el fundador con otro nombre.
3. Nada decía qué pasa si el fundador desaparece, se incapacita o abusa del gobierno provisorio.
4. El documento de gobierno se podía cambiar con dos votos de tres, incluidas las reglas que definen la independencia y la transición.

Las revisiones encontraron además que el poder del fundador estaba dicho de tres maneras incompatibles (la tabla de roles, la sección 3.2 y la sección 8). Esa contradicción se corrigió el 2026-10-22 como arreglo editorial; esta IIP registra la corrección y pide comentarios sobre las reglas construidas sobre ella.

## Especificación

Las reglas de abajo ya están en `governance-v1.md`, marcadas como *provisorias (IIP-0004)*. Esta IIP pregunta si se confirman, se cambian o se retiran.

1. **Fundador y Genome (secciones 2 y 8).** Durante el gobierno provisorio el fundador decide las IIP que no cambian el Genome; los cambios al Genome se publican solo como borradores identificados como suyos y los ratifica el consejo completo. Nunca enmienda el Genome solo, en ninguna etapa. Su asiento es reemplazable, no perpetuo.
2. **Plazo (sección 8).** El gobierno provisorio termina cuando se constituye el consejo (tres Custodios, dos suplentes), y a más tardar 18 meses después de publicar el repositorio público; la fecha de inicio se registra en el changelog y nunca se reinicia. La adopción externa (el primer organismo externo Observado) es un hito, no la condición. Si vencen los 18 meses con el consejo incompleto, el protocolo entra en **mantenimiento restringido**: correcciones de seguridad, continuidad de la infraestructura y el procedimiento para constituir el consejo; ninguna IIP pasa; el fundador sigue convocando candidatos y no tiene autoridad unilateral sobre las reglas. La falta de candidatos nunca prorroga el gobierno provisorio.
3. **Designación (sección 4.2).** Declaraciones de independencia comprobables; dos vías para los dos primeros Custodios independientes (uno invitado por el fundador, otro de una convocatoria pública, con nominadores y seleccionadores publicados); una objeción admisible impide que una designación entre en vigor hasta que se responda en público con la evidencia examinada, dentro de los 30 días, con una extensión de 30 días del período de comentarios.
4. **Suplentes, revisión y remoción (secciones 4.3 y 4.6).** Dos suplentes con la misma independencia, que votan solo por recusaciones y vacantes; una revisión periódica de actividad e idoneidad; remoción solo después del derecho de respuesta y de un revisor independiente por caso, cuyo dictamen consultivo se responde por escrito.
5. **Retribución (sección 4.4).** Tarifas publicadas 30 días antes de aplicarse, nunca retroactivas; la primera la fija el fundador antes de que asuma cualquier Custodio independiente.
6. **Continuidad (sección 4.5).** Una persona de continuidad, nombrada por el fundador con aceptación firmada, que tras 90 días sin respuesta solo puede convocar la transición y publicar el aviso. La recuperación de cuentas es aparte y no confiere autoridad. Los procedimientos previamente autorizados para las contingencias que no pueden esperar están en el inventario de autoridad.
7. **Clasificación por efecto (sección 3.1).** Todo cambio cuyo efecto altere elegibilidad, poderes, resultados de conformidad, interpretación de la evidencia, requisitos de seguridad, quorum, designaciones, revisiones o sanciones es un cambio de método, sea cual sea su tamaño.
8. **Patrocinio humano de las propuestas de agentes (secciones 3.2 y 7).** Una IIP redactada por un agente entra a revisión solo con un patrocinador humano que la firma y responde por ella; los mantenedores pueden limitar el volumen y cerrar envíos masivos con motivo público; los comentarios nunca se filtran por estar escritos por agentes.
9. **Cambios constitucionales (sección 10).** Los criterios de independencia, el umbral de dos de tres, las reglas sobre personas, la transición y su plazo, las prohibiciones centrales y la propia sección 10 cambian solo con 90 días de comentarios, una justificación escrita, un revisor independiente, dos de tres sin suplentes y, cuando exista un cuerpo capaz de ratificar, su ratificación. Sin unanimidad.
10. **Constitución inicial (sección 10; agregado el 2026-10-24).** Una sexta revisión encontró que esta IIP dejaba que el fundador confirmara, a los 30 días, reglas que la sección 10 protege con 90 días y dos de tres Custodios. La respuesta es explícita: estas reglas las adoptó la decisión provisoria del fundador porque no existía ningún consejo; son provisorias hasta que el consejo pleno las ratifique como su primera decisión constitucional; esta IIP lleva el período de 90 días; durante el gobierno provisorio el fundador puede acotar su autoridad, nunca ampliarla, nunca reiniciar el reloj, nunca agregar a la lista; y la excepción se aplica una sola vez. El texto exacto adoptado, su SHA-256 y su fecha se registran en `governance/decisions/0004` cuando se publique el repositorio.
11. **Retribución y revisión sin consejo (secciones 4.4, 4.6; revisado el 2026-10-24).** Las tarifas posteriores se deciden con un revisor independiente, entran en vigor no antes de 12 meses después de publicarse y nunca son retroactivas. Una decisión sobre personas que no encuentra revisor en 14 días avanza como no revisada y lo dice.
12. **Los Custodios nunca tienen la llave de parada de otro organismo (secciones 2, 10).** La pregunta abierta sobre si un Custodio puede ser Vigilante se cierra en negativo, en línea con la sección 10.

## Qué rompe

Nada que esté en funcionamiento: ningún organismo adoptó el protocolo. Cambia las expectativas de quien haya leído el primer borrador de la sección 8.

## Qué no establece

- Quiénes son los Custodios, los suplentes o la persona de continuidad. La persona de continuidad está pendiente de la designación y aceptación del fundador; la IIP puede cerrar sin ella, y la sección 4.5 lo dice hasta que se complete.
- El cuerpo capaz de ratificar cambios constitucionales: su composición y sus reglas son una pregunta abierta.
- Si los 18 meses son el número correcto. Es una elección institucional para esta etapa, no una cifra validada con datos; los comentarios que propongan otro límite deben decir qué se gana con él.

## Preguntas para quien comente

1. ¿El plazo más el mantenimiento restringido crean un compromiso creíble, o un callejón sin salida? ¿Qué debería permitir el mantenimiento restringido que hoy no permite?
2. ¿La convocatoria pública para el segundo Custodio es viable antes de que exista una comunidad? ¿Por qué la reemplazarías?
3. ¿La cuenta de recuperación del fundador debería contar como segundo owner para algo más que la recuperación?
4. ¿Qué reglas faltan en la lista constitucional, o cuáles no deberían estar?
5. ¿La regla de constitución inicial (punto 10) es lo bastante estrecha? ¿Qué más debería tener prohibido el fundador con reglas provisorias?

## Vectores de prueba

Ninguno: esta IIP no cambia ningún formato.
