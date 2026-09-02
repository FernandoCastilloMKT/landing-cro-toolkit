# Landing CRO Toolkit

Kit abierto y neutral para crear landings orientadas a conversión, campañas de pago, formularios y llamadas. Incluye una plantilla sin dependencias, un método de trabajo, listas de control, un prompt de revisión y una auditoría automática antes de publicar.

> Todo el contenido de demostración es ficticio. Sustituye los marcadores, aporta fuentes y valida legalmente cada afirmación antes de usarlo en producción.

## Qué incluye

- `template/`: landing estática, responsive y accesible.
- `docs/`: método CRO, medición, verificación factual, privacidad y checklist de publicación.
- `prompts/agente-revisor.md`: prompt reutilizable para una revisión independiente.
- `scripts/audit_public_repo.py`: detector preventivo de secretos, rutas locales y archivos no publicables.
- `.github/workflows/quality.yml`: auditoría automática en cada cambio.

## Inicio rápido

1. Duplica `template/` para tu proyecto.
2. Edita `template/config.js` y sustituye todos los valores entre corchetes.
3. Abre `template/index.html` en el navegador.
4. Ejecuta `python scripts/audit_public_repo.py .` antes de subir cambios.
5. Revisa `docs/checklist-prepublicacion.md`.

La plantilla no envía datos mientras `formEndpoint` esté vacío. No guardes claves privadas, credenciales ni datos reales de leads en el repositorio.

## Principios

- Una intención de búsqueda y una acción principal por landing.
- Mensajes verificables, específicos y coherentes con el anuncio.
- Medición con consentimiento y minimización de datos.
- Accesibilidad, rendimiento y móvil desde el inicio.
- Nunca inventar cifras, clientes, certificaciones, testimonios ni condiciones.

## Colaborar

Las mejoras se proponen mediante Issues y Pull Requests. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y [SECURITY.md](SECURITY.md).

## Licencia

MIT. Consulta [LICENSE](LICENSE).
