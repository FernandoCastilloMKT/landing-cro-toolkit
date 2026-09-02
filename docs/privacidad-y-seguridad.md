# Privacidad y seguridad

- Mantén las claves y tokens exclusivamente en variables secretas del entorno del servidor.
- Envía formularios a un backend con validación, límites de frecuencia, protección antiabuso y registros minimizados.
- Valida y codifica entradas; nunca insertes texto del usuario mediante `innerHTML`.
- Sirve por HTTPS y configura CSP, HSTS, `X-Content-Type-Options`, política de referer y permisos según el despliegue.
- Actualiza dependencias, fija versiones y revisa alertas.
- Limita accesos por rol y protege la rama principal mediante revisiones.
- Define retención, borrado y respuesta a incidentes.
- No incluyas datos personales en URLs, etiquetas de analítica, logs o repositorios.

La plantilla local evita enviar el formulario mientras no exista un endpoint. Esto es una barrera de seguridad, no un backend listo para producción.
