# Inventario de autoridad v1.0

Versión 1.0 · 2026-10-22 · Borrador · Provisorio bajo la IIP-0006

Actualizado el 2026-10-27: clave de firma provisoria por software (decisión 0005); segundos factores y repositorios corregidos.

*Traducción de trabajo. Si difiere de `authority-inventory-v1.md`, prevalece la versión en inglés.*

Cada recurso por el que el protocolo Ilorium se publica o se controla: quién lo tiene, con qué permisos, cómo se transfiere y quién puede actuar solo. Lo exige Gobierno, sección 9. **Sin secretos:** acá y en ningún lugar del repositorio aparecen contraseñas, códigos de recuperación, claves privadas, tokens ni frases semilla. Se actualiza cada vez que cambia un titular o un permiso; se revisa cada trimestre.

**Resumen honesto.** Durante el gobierno provisorio, una sola persona, el fundador, puede actuar solo sobre cada recurso de abajo. Dos votos en el papel no atan a una sola cuenta que puede reemplazar un binario, cambiar el dominio o publicar una release. Este inventario existe para que ese hecho sea público, para que cada aprobación se pueda comparar con lo que efectivamente se publicó, y para que la transición al gobierno pleno tenga una lista de lo que debe cambiar de manos.

| Recurso | Qué controla | Titular(es) hoy | Permisos | ¿Puede actuar solo? | Procedimiento de transferencia |
| --- | --- | --- | --- | --- | --- |
| Organización de GitHub `ilorium-protocol` | Repositorios `.github`, `protocol`, `site`, `probe`, `agent-kit`; rulesets; secretos; Actions | El fundador (`fseldon`) y una segunda cuenta privada del fundador, guardada solo para recuperación; ambas owners con verificación en dos pasos (una passkey en `fseldon`, una app autenticadora en la cuenta de recuperación); llaves físicas previstas | Owner | Sí, el fundador | Agregar a un Custodio como owner; quitar la cuenta de recuperación del fundador cuando haya dos owners independientes (Gobierno, sección 8) |
| Rulesets de repositorio (`main-protection`, `tags-protocol`) | Commits firmados, revisión de PR por CODEOWNERS, quién puede etiquetar una release | El fundador | Bypass de administrador por pull request, registrado | Sí | El bypass se quita cuando haya dos Custodios en funciones |
| Dominio `ilorium.com` | El sitio, el Faro, el correo | El fundador, en el registrador (GoDaddy); renovación automática y privacidad de WHOIS a confirmar en la revisión trimestral | Registrante | Sí | Transferencia del registrante a la entidad receptora cuando exista |
| DNS y alojamiento (Cloudflare: zona, DNSSEC, Pages) | Dónde resuelven `ilorium.com`, `llms.txt` y `/.well-known/ilorium.json` | El fundador (`root@ilorium.com`), verificación en dos pasos con app autenticadora; llaves físicas previstas | Dueño de la cuenta | Sí | Agregar un segundo administrador; regla del registro DS: quitar el DS en el registrador antes de cualquier mudanza de DNS |
| Correo (`@ilorium.com`, Google Workspace) | El correo de verificación de todos los demás recursos; los grupos `hello@`, `security@`, `press@`, `agents@` | El fundador (`root@`, superadmin, verificación en dos pasos; llaves físicas previstas) | Superadmin | Sí | Segundo superadmin por agregar (abierto) |
| Clave de firma, **provisoria** (decisión 0005): Ed25519 por software con frase de contraseña, `SHA256:rd2Y71cS6Vz956Qmql8w66RfAZpU6d7IqTp0RJ29E/Q`, desde el 2026-10-27; el único respaldo es una copia cifrada de la misma clave. Prevista: `ed25519-sk` en llave física, con llave de respaldo | La identidad seudónima «Seldon»; cada commit, etiqueta y release | El fundador | — | Sí | Rotación prevista: decisión 0005, punto 4 (una declaración firmada con la clave vieja y con la nueva). Compromiso: decisión 0005, punto 3 (todavía no hay una llave de respaldo independiente). Después de la rotación: regla de recuperación de Gobierno (un mensaje firmado con la llave de respaldo nombra la clave nueva); pérdida de ambas: lo anuncian los Custodios, clave nueva, registrado como decisión de gobierno |
| Firma de releases (Sigstore, procedencia de compilación) | Lo que la gente instala | El fundador, a través de CI | — | Sí (un solo aprobador humano) | Segundo aprobador cuando haya dos Custodios en funciones; evaluar un esquema de umbral (por ejemplo TUF) antes de inventar uno |
| Registro de paquetes (PyPI, planificado) | El verificador que la gente instala | El fundador (por crear) | — | Sí | Publicación confiable desde CI; segundo dueño con los Custodios |
| Agente de seguridad (`ilorium-security-agent`, una GitHub App) | Lee repositorios, abre issues; cero escritura (decisión 0002) | Instalado por el fundador | `Contents: Read` | No: no puede escribir | Se revoca desinstalando la App |
| Fondos | Ninguno. El fundador paga de su bolsillo; el protocolo no acepta donaciones hasta que exista una entidad receptora | El fundador | — | — | Entidad receptora (Gobierno, sección 6.6) |
| Recuperación de cuentas | Códigos de recuperación, llaves de respaldo, el plan sellado | El fundador, en un plan sellado con una persona designada que recupera solo el acceso | — | — | Recuperar el acceso no confiere autoridad sobre las reglas (Gobierno, sección 4.5) |
| Los documentos del Proyecto (Claude Project, borradores de trabajo) | Los borradores antes de llegar al repositorio | El fundador | — | Sí | El repositorio es la fuente de verdad una vez publicado |

## Procedimientos previamente autorizados (Gobierno, sección 4.5)

Mantienen funcionando lo que existe y no cambian ninguna regla. Durante el gobierno provisorio los ejecuta el fundador; si no está disponible, la persona nombrada en su plan de recuperación ejecuta solo estos, e informa en público.

1. **Credencial o token comprometido:** revocar, rotar, publicar un aviso firmado, registrar el incidente bajo `governance/incidents/`.
2. **Rotación de certificado o de clave DNSSEC:** rotar en Cloudflare, actualizar el registro DS en el registrador, confirmar la resolución.
3. **Renovación del dominio:** renovar; nunca dejar vencer el dominio.
4. **Despliegue:** `DEPLOY_ENABLED` queda en `false` por defecto; un despliegue es una release y sigue las reglas de release.
5. **Corrección de seguridad:** una release de seguridad puede publicarla el fundador solo y se declara como tal en el changelog; bajo mantenimiento restringido (Gobierno, sección 8) es el único tipo de release permitido.

## Aprobaciones atadas al contenido (Gobierno, sección 3.2.6)

Toda decisión de gobierno bajo `governance/decisions/` registra: la propuesta y la versión aprobadas; el SHA-256 del texto aprobado y de cada artefacto; quién votó y quién se abstuvo; las fechas del período de comentarios y del voto; las firmas; la fecha de entrada en vigor; y las decisiones que corrige o reemplaza. Un artefacto publicado que no coincide con una huella aprobada no está aprobado, lo haya publicado quien lo haya publicado.

## Revisión trimestral

- Cada titular y cada permiso de arriba siguen siendo correctos.
- Segundos owners, administradores y superadmins: quién existe, quién falta.
- Vencimiento del dominio, renovación automática, privacidad de WHOIS.
- Lectura de los registros de auditoría de GitHub, Cloudflare y Workspace: actores, miembros, roles, Apps instaladas y solicitudes de licencias.
- Llaves y recuperación probadas.
