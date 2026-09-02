# Instrucciones para agentes

## Clasificación del repositorio: PÚBLICO

Este proyecto corresponde al repositorio público `FernandoCastilloMKT/landing-cro-toolkit`. Todo archivo, commit, rama, Issue, Pull Request, acción automática y parte de su historial puede quedar visible y ser descargado por cualquier persona.

Puede existir un repositorio privado independiente con proyectos reales. Este repositorio público no es su copia, espejo ni copia de seguridad. No intentes descubrirlo, recorrer sus carpetas, importar su historial ni sincronizar contenido desde él.

Antes de modificar o publicar:

- Comprueba con `git remote -v` que estás en `FernandoCastilloMKT/landing-cro-toolkit`.
- Trabaja en una rama y entrega los cambios mediante Pull Request; `main` está protegida y requiere revisión.
- Crea ejemplos originales, ficticios, genéricos y reutilizables. No basta con cambiar el nombre de un cliente real.
- No copies archivos, commits, capturas, diseños, textos, fotografías, logotipos, documentos ni configuraciones desde proyectos privados.
- Excluye nombres de agencias y clientes, personas, dominios, teléfonos, correos, ubicaciones precisas, campañas, métricas, testimonios, identificadores de analítica, publicidad, alojamiento o formularios, y cualquier dato que permita inferir su identidad.
- No introduzcas rutas locales, nombres de usuario del ordenador, secretos, tokens, claves, cookies, archivos `.env`, datos de leads ni materiales cuya licencia no permita publicarlos.
- Si el usuario proporciona términos confidenciales para auditar, pásalos localmente mediante `--deny-term`; nunca guardes esa lista dentro del repositorio público.
- Ante una duda de privacidad, omite el material y pide confirmación. La utilidad pública nunca prevalece sobre la confidencialidad.

## Obligatorio

- Usa Product Design para decisiones relevantes de interfaz o revisión visual.
- Usa Playwright para validar la landing en navegador, móvil y escritorio.
- No introduzcas nombres, dominios, teléfonos, correos, imágenes, testimonios ni métricas reales de clientes.
- No inventes afirmaciones comerciales. Marca los ejemplos como ficticios y pide fuentes para producción.
- No añadas secretos, tokens, identificadores de cuentas, rutas locales ni archivos `.env`.
- Ejecuta `python scripts/audit_public_repo.py .` antes de proponer un commit.
- Revisa también nombres de archivos, historial del commit y `git diff --cached`; superar el script no sustituye la revisión humana.
- Mantén una CTA principal clara, accesibilidad WCAG, buen rendimiento y consentimiento válido.

## Entrega

Resume qué cambió, qué pruebas se ejecutaron, qué afirmaciones necesitan fuente y cualquier riesgo pendiente.
