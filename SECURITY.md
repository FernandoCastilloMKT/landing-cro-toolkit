# Seguridad

## Comunicar una vulnerabilidad

No publiques vulnerabilidades explotables, credenciales ni datos personales en un Issue. Utiliza la opción **Report a vulnerability** de la pestaña Security del repositorio para informar de forma privada.

Indica el componente afectado, el impacto, pasos mínimos para reproducirlo y una posible mitigación. Se confirmará la recepción y se coordinará la divulgación cuando exista una solución.

## Alcance

Este repositorio contiene una plantilla educativa. Quien la despliegue debe configurar HTTPS, cabeceras de seguridad, consentimiento, retención de datos, protección antiabuso y un proveedor de formularios adecuado a su jurisdicción.

## Auditoría antes de publicar

Ejecuta `python scripts/audit_public_repo.py . --history=--all` desde un clon
independiente con historial completo. Incluye ramas y etiquetas locales,
identidades de commits, texto eliminado y rutas históricas prohibidas.
Los nombres confidenciales pueden pasarse mediante `--deny-term`, también para
el historial; nunca guardes la lista de términos ni los hallazgos privados aquí.

Los detectores cubren formatos comunes de credenciales y archivos de sesión,
pero no garantizan detectar todos los secretos ni datos personales. Las imágenes,
documentos, logs de Actions, Issues, PR y metadatos requieren revisión adicional.
Un cambio de nombre o borrar un archivo en un commit nuevo no limpia su historial.
Si se filtra una credencial, revócala y coordina la limpieza sin publicar su valor.
