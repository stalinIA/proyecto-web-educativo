# slvera.com · v10 "Cúpulas de Cuenca"

Sitio de SLVERA Education Advisor. HTML, CSS y JavaScript planos: sin dependencias
ni compilación. Se sube tal cual a GitHub Pages y funciona.

Modelo actual: **guía gratis por país** para captar leads (nombre, correo y WhatsApp)
+ **lista de espera** de la comunidad ($39 al mes cuando abra). Revisión de contratos
disponible hoy; sesiones en vivo, instituciones recomendadas y asesoría VIP, próximamente.

```
index.html                 Inicio. Se edita a mano.
styles.css / app.js        Diseño e interacción  ← CONFIG arriba de app.js
destinos/*.html            Una página por país      ┐
legal/*.html               Términos, privacidad…    │ los genera
guias/*.pdf                Las 5 guías gratuitas    │ _herramientas/construir.py
llms.txt, llms-full.txt    Resumen para IA          │
robots.txt, sitemap.xml    Para buscadores          ┘
datos/destinos-2026.json   Cifras públicas con su fuente (sin fondos)
_herramientas/             Constructor, fuentes y datos privados (no se publica)
automatizacion/            Script de Google para los formularios (no se publica)
assets/                    Fotos + og.jpg
```

---

## Pendientes

- [ ] **Conectar los formularios.** `automatizacion/LEEME.md`. Sin esto no se captura nada.
- [ ] **Grupo de WhatsApp de la lista de espera.** Cuando tengas la línea, el enlace va en dos lugares (está explicado en `automatizacion/LEEME.md`).
- [ ] **Apuntar el dominio** (abajo).
- [ ] **Redes sociales.** Los enlaces `href="#"` del footer; agrégalos también como `"sameAs"` en el schema de `index.html`.
- [ ] **Testimonios reales.** Hay una sección comentada en `index.html`. Se llena con las respuestas al correo de la guía, con permiso.
- [ ] **Cuando abra la comunidad:** en `app.js`, `COMUNIDAD_ABIERTA: true` y la URL en `COMUNIDAD_URL`. Todos los botones de "lista de espera" pasan a llevar ahí.

## Actualizar datos, páginas y PDF

Las cifras viven en dos archivos:

- `datos/destinos-2026.json` → lo que se publica en la web (trabajo, salario, arriendo, transporte…).
- `_herramientas/datos-privados.json` → **fondos y tasa de visa**. Solo van en los PDF, a cambio del lead; nunca en la web.

Después de cambiar un dato, cambia `HOY` en `_herramientas/construir.py` y corre:

```bash
python _herramientas/construir.py
```

Eso rehace las páginas de destino, las legales, los archivos para IA y los 5 PDF. Necesita Python y Google Chrome instalados. Con `--sin-pdf` salta los PDF.

Calendario: los salarios mínimos cambian en **enero** (Europa) y en **julio** (Australia), y el Abono Joven de Madrid está garantizado hasta diciembre de 2026.

## Conectar slvera.com

En tu proveedor de dominio:

| Tipo | Nombre | Valor |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `stalinia.github.io` |

En GitHub: *Settings → Pages → Custom domain* → `slvera.com` → guardar, y cuando aparezca, marca **Enforce HTTPS**.

## AEO: que los buscadores de IA te encuentren

Lo técnico está hecho: `robots.txt` abierto a los rastreadores de IA de 2026, `llms.txt`, datos estructurados que conectan persona, organización y servicios, respuestas cortas al inicio de cada sección, tablas citables y fuentes oficiales con fecha.

Lo que depende de tu cuenta, **cuando slvera.com funcione**:

1. **Bing Webmaster Tools**: es lo más importante para IA, porque ChatGPT y Copilot buscan sobre el índice de Bing. Envía `https://slvera.com/sitemap.xml`.
2. **Google Search Console**: el mismo sitemap.
3. **Perfil de Google Business** en Cuenca, con el mismo nombre y descripción que la web.
4. **Mismo nombre en todas las redes** ("SLVERA Education Advisor" y "Abog. Stalin Vera"), con enlace a slvera.com.
5. **Menciones externas**: una entrevista o un artículo invitado pesan más que cualquier ajuste técnico.

## Ver el sitio mientras editas

```bash
npx serve . -p 4321
```

Si cambias `styles.css` o `app.js`, sube la versión en los enlaces (`?v=10` → `?v=11`), en `index.html` y en `_herramientas/construir.py`.

## Decisiones que conviene no deshacer

- **La analítica solo carga si aceptan las cookies** (`cargarAnalitica()` en `app.js`). Nunca en el `<head>`.
- **La casilla de lista de espera va desmarcada.** Consentimiento activo, como pide la LOPDP.
- **Nada de contadores falsos ni actividad inventada.** Tampoco testimonios que no existan.
- **Los fondos no se publican en la web.** Son el gancho de la guía.
