# Manifiesto del Protocolo Ilorium

Release 1.0 · 2026-10-20 · Borrador

*Traducción de trabajo. Si difiere de `manifest.md`, prevalece la versión en inglés.*

## Qué es este archivo

Este archivo nombra los documentos que, juntos, forman Ilorium en una release dada, y cuáles de ellos son el protocolo propiamente dicho. Quien implemente debe poder decir "implemento Ilorium 1.0" y señalar este archivo. Si otro documento contradice este manifiesto, prevalece el manifiesto hasta que se corrija.

**Una versión de cada documento.** Se conserva solo la versión vigente de cada documento. Lo que cambia entre releases queda en `CHANGELOG.md`. Cuando el protocolo pase a su repositorio público, el control de versiones guardará la historia completa.

**Propósito.** Ilorium monitorea organizaciones operadas por agentes de IA: registra cómo vive cada una, mide lo que realmente demostró que puede hacer y exige que todo organismo lleve una llave de parada humana, probada con simulacros dentro de un alcance declarado. Su misión es dar leyes, formatos y verificación a las organizaciones operadas por agentes de IA y a la evolución de su especie, fijando desde la primera generación las condiciones que todo nacimiento debe cumplir. La convicción del fundador (la carta del fundador, `founder-letter.md`), las hipótesis del proyecto y lo que el protocolo verifica hoy se exponen por separado en "Visión y evidencia" de `README.md` y en el whitepaper. Esos textos no tienen fuerza normativa; este manifiesto y los documentos que lista, sí.

## Release 1.0

La release 1.0 es la **primera versión completa** del protocolo. Sigue siendo un **borrador**: no se implementó de punta a punta, sus formatos pueden cambiar y ningún organismo lo demostró todavía en funcionamiento. Más adelante se declarará **estable** una release (ver Compatibilidad).

| Componente | Documento | Versión | Capa |
| --- | --- | --- | --- |
| Genome | `genome/genome-v1.md` | 1.0 | Protocolo |
| Gobierno | `governance-v1.md` | 1.0 | Protocolo (quién decide qué, cómo, y cómo se comparte y se transfiere el poder) |
| Pulse | `specs/pulse-v1.md` | 1.0 | Protocolo, con valores por defecto de referencia (N, T, D, K) |
| Formato de Evidencia | `specs/evidence-format-v1.md` | 1.0 | Protocolo (formatos, perfil de puntos de control, borradores de la Spore, el Evidence Bundle y Vital Signs, comportamiento del verificador); formas legibles por máquina en `schemas/` y `vectors/` |
| Probe | `specs/probe-v1.md` | 1.0 | Mixta; cada sección marcada [Protocolo] o [Referencia] |
| Proof of Life | `specs/proof-of-life-v1.md` | 1.0 | Protocolo |
| Ecosistema | `specs/ecosystem-v1.md` | 1.0 | Protocolo (estados, sucesión, coalescencia y linajes); la web es Observatorio |
| Descubrimiento y crecimiento | `specs/discovery-and-growth-v1.md` | 1.0 | Los campos de la Spore y la extensión A2A son protocolo; el resto es Observatorio y Organismo Cero |
| Glosario | `glossary.md` | 1.0 | Protocolo (lenguaje común) |

**Licencias.** El texto normativo (estos documentos): CC BY 4.0. Código, esquemas JSON, casos de conformidad y ejemplos: Apache-2.0, para poder incorporarlos a cualquier implementación. Quienes contribuyen conservan su copyright y licencian cada aporte bajo la licencia del archivo que cambian.

El whitepaper (`whitepaper-v1.md`) explica el proyecto completo y no tiene fuerza normativa. El documento de arquitectura (`engineering/architecture-v1.md`), el registro de proyectos relacionados y la identidad de marca (`brand/brand-identity-v1.md`) no forman parte del protocolo. Los archivos en español (`.es.md`) son traducciones de trabajo de las mismas versiones; si difieren, prevalece la versión en inglés.

## Tres capas

| Capa | Qué es | A quién obliga |
| --- | --- | --- |
| **Protocolo** | Formatos, significados, requisitos y pruebas de conformidad | A todo organismo y a toda implementación |
| **Implementación de referencia** | La Probe, el emisor del Pulse y sus valores por defecto | A nadie. Reemplazable por cualquier implementación que produzca evidencia conforme |
| **Organismo Cero** | El organismo del fundador: arquitectura, roles, herramientas y decisiones | Solo al Organismo Cero. Un piloto declarado, nunca una validación independiente de Ilorium |

### Dónde va cada elemento

| Elemento | Capa | ¿Requerido para la conformidad? |
| --- | --- | --- |
| Las siete leyes, los estados de conformidad, la enmienda por IIP | Protocolo | Sí |
| Las tres cerraduras: línea germinal, compuerta de nacimiento, parada | Protocolo | Sí |
| Gobierno: roles, proceso de IIP, Custodios, calificación y pago de los Vigilantes, reglas de financiamiento, qué puede hacer una IA | Protocolo | Obliga a quienes gobiernan el protocolo; no decide la conformidad de ningún organismo |
| Tipos de registro (observación con `event` y `outcome`, afirmación, evaluación con `work_unit`), estados de atribución, tipos de cruce | Protocolo | Sí |
| Cuatro medidas de cobertura, frescura y la plantilla de afirmación | Protocolo | Sí |
| JSON de Ilorium (RFC 8785 restringida), árbol RFC 6962 con pruebas RFC 9162, puntos de control en nota firmada C2SP con sidecar firmado, firmados cada N latidos o cada T, un quórum de testigos que verifica, veredictos PASS, FAIL y UNKNOWN | Protocolo | Sí (Formato de Evidencia) |
| Esquemas JSON y casos de conformidad | Protocolo | Sí: una implementación declara conformidad al pasar los casos de la release |
| Verificador aislado de referencia (`ilorium-verifier`, Python) | Implementación de referencia | No; cualquier verificador que pase los casos vale lo mismo |
| Spore en `/.well-known/ilorium.json` y sus campos | Protocolo | Sí (campos todavía en borrador) |
| Formato del Pulse, pulsos por intervalo, desafíos con plazo, estados del ser, eje de recuperación, vínculos de parentesco y lo que pasa por ellos | Protocolo | Sí |
| Registro de sucesión, tipos de sucesión (`founded`, `inherited`, `coalesced`), generación, la compuerta de nacimiento, y lo que pasa y nunca pasa a un descendiente | Protocolo | Sí, para todo organismo originado por otro (formato del registro todavía en borrador) |
| Un titular humano de la llave de parada para cada organismo; Vigilantes para los linajes sin fundadores humanos | Protocolo | Sí |
| Dimensiones de Proof of Life, unidades de trabajo; la autogénesis y la autonomía observada total se muestran como resultados separados, nunca como un estado compuesto | Protocolo | Sí |
| Un único canal de directivas declarado, todo mensaje humano registrado, directivas distinguidas de contactos, directivas seguidas hasta su efecto | Protocolo | Sí |
| Los agentes nunca usan una identidad humana y siempre se identifican como IA (Ley 5) | Protocolo | Sí |
| La extensión A2A de Ilorium (`https://ilorium.com/ext/a2a/v1`) | Protocolo | Opcional |
| Compuerta de autorización | Protocolo (opcional) | No; los caminos sin compuerta se declaran en las afirmaciones |
| SI2SI, SI → SI y SI + SI → SI′ | Horizonte (glosario, Ecosistema, README, whitepaper) | No. No es requisito, estado ni criterio |
| Umbral en Telegram, el bot Centinela, los comandos `/do`, `/approve`, `/stop`, `/governance`, `/test` | Implementación de referencia | No |
| Recolectores para GitHub, Workspace, Gmail, un servidor Linux, middleware A2A; el comando `ilorium` | Implementación de referencia | No |
| Valores por defecto: N = 64 latidos, T = 15 minutos, D = 10 minutos, K = 3 | Implementación de referencia | No; se declaran en la Spore si cambian |
| Seis roles de agentes, nombres `OZ-…`, temperamentos | Organismo Cero | No |
| Google Workspace, los agentes y casillas del Organismo Cero en ilorium.com, un servidor compartido, el Observatorio como primer producto | Organismo Cero | No |
| ilorium.com como sitio del protocolo y primer índice | Observatorio | No |
| El índice, el Codex, el Radiant y los estados web tal como se muestran | Observatorio | No. Cualquiera puede operar un índice u otra vista sobre la misma evidencia |

**Deuda conocida.** El formato de evidencia ya es un documento aparte con casos de conformidad, y el documento de la Probe remite a él; el documento de la Probe todavía mezcla secciones de protocolo y de referencia, que siguen marcadas. La Spore tiene un esquema en borrador en el Formato de evidencia (con `stop_key_holders`), pero el registro de sucesión, los vínculos de parentesco y `partners` todavía necesitan un formato único en una especificación de la Spore; el Evidence Bundle y los Vital Signs están definidos como borrador, y un bundle de una parte del log no. La integración con testigos públicos no está disponible hasta que existan una prueba de interoperabilidad y un acuerdo con un operador de testigo.

## Compatibilidad

- **1.0 es completa, no estable.** Hasta que una release se declare estable, los formatos todavía pueden cambiar; cada cambio queda en el changelog y no se promete compatibilidad entre borradores.
- **Estable significará** (esta es la definición normativa; todos los demás documentos remiten acá): formatos congelados, pruebas de conformidad publicadas, una política de compatibilidad escrita y al menos dos Custodios del Genome independientes en funciones; y nunca se declara durante el gobierno provisorio ni el mantenimiento restringido (Gobierno, sección 8). Estable es una afirmación sobre formatos y gobierno, no sobre operación: el plan del fundador ordena otros hechos antes (el Organismo Cero latiendo, la adopción externa), y esos son su plan, no condiciones de esta definición. Ser estable no dice nada sobre si se puede confiar en algún organismo.
- **Después de declarar estable una release:** los cambios dentro de su versión mayor son aditivos; todo lo que rompa evidencia o validadores existentes es una nueva versión mayor.
- **Release declarada.** Cada Spore declara la release que implementa (`"ilorium": "1.0"`).
- **Prueba de apertura.** El protocolo es abierto en la práctica cuando alguien construye una segunda implementación sin ayuda del fundador y ambos validadores llegan a los mismos resultados sobre la misma evidencia.

## Quién publica este archivo

Lo dice el documento de gobierno (`governance-v1.md`). Durante el **gobierno provisorio**, el fundador solo publica las releases y lo declara en el changelog. Bajo el **gobierno pleno**, dos Custodios del Genome. El gobierno provisorio termina cuando se constituye el consejo de Custodios; la autoridad unilateral del fundador termina a más tardar 18 meses después de publicar el repositorio público, con o sin consejo completo (Gobierno, sección 8, revisada el 2026-10-22 y provisoria hasta que cierre la IIP-0004). Todavía no se designó ningún Custodio del Genome; el Genome y esta release siguen en borrador hasta que haya dos Custodios independientes en funciones, y no se puede declarar estable una release durante el gobierno provisorio.
