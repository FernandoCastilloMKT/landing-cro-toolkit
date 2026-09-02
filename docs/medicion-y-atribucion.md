# Medición y atribución

## Eventos mínimos

Usa nombres estables y documenta cuándo se producen:

- `cta_click`: interacción con la CTA principal.
- `form_start`: primera interacción válida con el formulario.
- `form_submit_success`: respuesta confirmada por el servidor.
- `form_submit_error`: error real de envío.
- `phone_click`: clic en un enlace telefónico.

No confundas un clic en enviar con un lead confirmado. Deduplica eventos y evita incluir nombre, email, teléfono o texto libre en las cargas de analítica.

## Campañas

Conserva únicamente los parámetros necesarios, valida su longitud y no los interpretes como HTML. Documenta la ventana de atribución y contrasta leads con resultados de negocio, no solo con interacciones.

## Plan de prueba

Antes de publicar, revisa modo consentimiento denegado y concedido, navegación directa y con parámetros, éxito y error de formulario, doble clic y regreso mediante historial del navegador.
