# Plantilla

Plantilla HTML/CSS/JS sin dependencias. Contiene texto ficticio y no está preparada para recopilar datos reales sin configuración adicional.

## Configuración

Edita `config.js`:

- `brand`: nombre público verificado.
- `phoneDisplay` y `phoneHref`: teléfono autorizado.
- `formEndpoint`: endpoint HTTPS propio; vacío mantiene el modo demostración.
- `privacyUrl`: política aplicable.

No pongas claves en este archivo: todo JavaScript enviado al navegador es público. Antes de producción añade un backend con validación, protección antiabuso, límites de frecuencia y gestión de consentimiento.
