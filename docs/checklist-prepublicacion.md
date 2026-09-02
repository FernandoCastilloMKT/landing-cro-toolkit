# Checklist de prepublicación

## Contenido y CRO

- [ ] La promesa coincide con anuncio, palabra clave y oferta.
- [ ] La CTA principal es clara y consistente.
- [ ] Cada cifra, plazo, premio, garantía y testimonio tiene una fuente vigente.
- [ ] No hay texto de relleno ni afirmaciones absolutas sin respaldo.
- [ ] Precio, impuestos, condiciones y limitaciones son comprensibles.

## Formulario y llamadas

- [ ] Solo se solicitan los datos imprescindibles.
- [ ] Etiquetas, errores, foco y confirmación funcionan con teclado y lector de pantalla.
- [ ] El formulario no duplica envíos y comunica fallos sin perder datos.
- [ ] Teléfono, horario y enlaces `tel:` han sido comprobados.
- [ ] Consentimiento y enlaces legales corresponden al responsable real.

## Técnico

- [ ] No hay errores de consola, enlaces rotos ni contenido mixto.
- [ ] Funciona en anchos móviles y de escritorio.
- [ ] Imágenes tienen dimensiones, formato eficiente y texto alternativo correcto.
- [ ] Se han revisado Core Web Vitals, SEO básico y metadatos sociales.
- [ ] HTTPS, cabeceras y dependencias están actualizados.

## Medición y privacidad

- [ ] Los eventos se disparan una sola vez y solo cuando corresponde.
- [ ] Los parámetros de campaña se conservan sin almacenar más datos de los necesarios.
- [ ] La medición respeta el consentimiento aplicable.
- [ ] No se envían datos personales a analítica o publicidad por accidente.

## Repositorio

- [ ] `python scripts/audit_public_repo.py .` termina sin hallazgos.
- [ ] El diff y los archivos versionados se han revisado manualmente.
- [ ] No hay secretos, datos personales, rutas locales ni materiales sin licencia.
