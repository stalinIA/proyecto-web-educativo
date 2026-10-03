#!/usr/bin/env python3
"""
SLVERA · construir.py
Regenera todo lo que sale de los datos:
  · destinos/*.html   (páginas por país)
  · legal/*.html      (términos, privacidad, cookies, aviso legal)
  · robots.txt, sitemap.xml, llms.txt, llms-full.txt
  · guias/*.pdf       (las 5 guías gratuitas, con Chrome sin interfaz)

Uso, desde la carpeta del proyecto:
    python _herramientas/construir.py            → todo
    python _herramientas/construir.py --sin-pdf  → todo menos los PDF

Cuando cambie un dato: edita datos/destinos-2026.json (lo público) o
_herramientas/datos-privados.json (fondos y visa, solo para los PDF),
cambia HOY aquí abajo y vuelve a correr este script.
index.html NO se genera: se edita a mano.
"""
import html, json, os, pathlib, subprocess, sys

# ── CONFIGURACIÓN ────────────────────────────────────────────────────
HOY, HOY_TXT = "2026-09-25", "25 de septiembre de 2026"
CURSO = "2026-27"
SITE = "https://slvera.com"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

AQUI = pathlib.Path(__file__).resolve().parent
ROOT = AQUI.parent
E = html.escape
PUB = json.load(open(ROOT / "datos" / "destinos-2026.json", encoding="utf-8"))["destinos"]
PRIV = json.load(open(AQUI / "datos-privados.json", encoding="utf-8"))["destinos"]
ORDEN = ["australia", "malta", "alemania", "dubai", "espana"]
PDF = {s: f"slvera-guia-{s}-{CURSO}.pdf" for s in ORDEN}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500'
         '&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='16' fill='%231F4E9C'/%3E"
        "%3Ctext x='16' y='21' font-family='Georgia,serif' font-size='13' font-weight='600' fill='%23FCFBF8' text-anchor='middle'%3ESV%3C/text%3E%3C/svg%3E")

# ── CONTENIDO EDITORIAL POR DESTINO ──────────────────────────────────
EDIT = {
 "australia": dict(img="dest-australia.webp", alt="Estudiante latinoamericana caminando por un campus universitario en Australia",
   titulo=f"Estudiar en Australia sin agencia {CURSO}: trabajo, sueldo por hora, arriendo y transporte",
   desc=f"Cuánto puedes trabajar y ganar estudiando en Australia en {CURSO}, cuánto cuesta una habitación y el transporte en Brisbane, Melbourne y Sídney. Guía sin agencia, con fuentes oficiales.",
   corta="Sí. Puedes aplicar directo a universidades y colleges australianos. Como estudiante puedes trabajar 48 horas por quincena durante el curso y sin límite en vacaciones, y el salario mínimo es A$26,44 la hora desde julio de 2026. Una habitación compartida cuesta entre A$200 y 350 por semana, y en Brisbane cada viaje en transporte público cuesta A$0,50.",
   kpis=[("Trabajo","48 h / quincena","Sin límite en vacaciones"),("Hora mínima","A$26,44","A$33,05 como casual"),("Habitación","A$200–350","por semana, compartida")],
   ojo=[("El agente que te 'ayuda gratis'","Si no te cobra a ti, le cobra a la institución. Esa comisión condiciona qué opciones te muestra."),
        ("Colleges sin historial","Hay colleges excelentes y hay fábricas de matrículas. La diferencia está en el registro oficial y el historial, no en la web."),
        ("El reembolso si te niegan la visa","Cada institución lo redacta distinto. Algunas devuelven casi todo; otras se quedan con el depósito completo."),
        ("El 'intake' que se mueve","Tu fecha de inicio se puede correr. Revisa qué pasa con tu dinero si eso ocurre.")],
   paso="Confirma que tu título y tu nivel de inglés (IELTS, PTE o TOEFL) cumplen lo que pide la institución."),
 "malta": dict(img="dest-malta.webp", alt="Dos estudiantes latinoamericanos conversando en una calle de piedra en Malta",
   titulo=f"Estudiar inglés en Malta sin agencia {CURSO}: trabajo, sueldo, arriendo y transporte",
   desc=f"Cuántas horas puedes trabajar estudiando en Malta en {CURSO}, cuánto se gana, cuánto cuesta una habitación en Sliema, Gżira o Msida y cómo moverte gratis en transporte público.",
   corta="Sí. Las escuelas de inglés y los centros superiores de Malta aceptan postulaciones directas. Con visa de estudiante puedes trabajar hasta 20 horas por semana; en cursos de inglés, a partir del tercer mes. El salario mínimo en 2026 es de €229,44 por semana, una habitación compartida cuesta entre €400 y €900 al mes, y el transporte público es gratis con la tarjeta Tallinja.",
   kpis=[("Trabajo","20 h / semana","Desde el mes 3 en inglés"),("Salario mínimo","€229,44","por semana (≈ €5,74/h)"),("Habitación","€400–900","por mes, según zona")],
   ojo=[("El paquete 'todo incluido'","Curso, alojamiento y traslado en un solo precio suelen esconder el margen del intermediario. Pide el desglose."),
        ("La acreditación de la escuela","No todas las escuelas de inglés tienen la misma licencia. Es lo primero que hay que verificar."),
        ("El alojamiento obligatorio","Algunos contratos te amarran al alojamiento de la escuela, que casi siempre sale más caro."),
        ("Semanas mínimas y penalidades","Revisa qué pasa si te quieres retirar antes o extender el curso.")],
   paso="Confirma que la escuela tenga licencia vigente y que tu curso dure más de 90 días si piensas trabajar."),
 "alemania": dict(img="dest-germany.webp", alt="Estudiante latinoamericano estudiando en una biblioteca universitaria de Alemania",
   titulo=f"Estudiar en Alemania sin agencia {CURSO}: matrícula, sueldo por hora, arriendo y transporte",
   desc=f"Universidades públicas casi sin matrícula, €13,90 la hora mínima y pase de estudiante por €37,80 al mes para todo el país. Cuánto cuesta vivir en Múnich, Berlín o Hamburgo en {CURSO}.",
   corta="Sí, y es de los destinos donde menos sentido tiene pagar una agencia: la mayoría de universidades públicas alemanas no cobran matrícula. Puedes trabajar 140 días completos al año con un salario mínimo de €13,90 la hora, y el pase de estudiante para moverte por todo el país cuesta €37,80 al mes.",
   kpis=[("Trabajo","140 días / año","o 280 medios días"),("Hora mínima","€13,90","€14,60 en 2027"),("Habitación","€510–850","por mes (WG)")],
   ojo=[("La homologación de tu título","Tu título tiene que ser reconocido para entrar. Es el paso que más gente subestima."),
        ("La cuenta bloqueada a última hora","Abrirla y depositar toma semanas. Prepárala antes de pedir cita en la embajada."),
        ("Los plazos de postulación","Son estrictos y no se negocian: un día tarde es un semestre perdido."),
        ("Los programas privados en inglés","Existen y son legítimos, pero cobran como privados. Compara siempre con la opción pública.")],
   paso="Averigua si tu título te da acceso directo a la universidad o si necesitas un año preparatorio."),
 "dubai": dict(img="dest-dubai.webp", alt="Estudiante caminando por un campus universitario moderno en Dubái",
   titulo=f"Estudiar en Dubái sin agencia {CURSO}: trabajo, pago por hora, arriendo y transporte",
   desc="Cómo funciona la visa de estudiante patrocinada por la universidad en Dubái, cuántas horas puedes trabajar, cuánto pagan por hora, cuánto cuesta una residencia y el descuento de transporte para estudiantes.",
   corta="Sí. En Dubái la universidad patrocina tu visa de estudiante, así que aplicas directo a ella. Con permiso del MOHRE puedes trabajar medio tiempo, lo habitual es hasta 15 horas por semana, y los trabajos de estudiante pagan entre AED 20 y 60 la hora. Una habitación compartida cuesta entre AED 1.500 y 3.000 al mes.",
   kpis=[("Trabajo","≈ 15 h / semana","con permiso del MOHRE"),("Pago por hora","AED 20–60","no hay mínimo para extranjeros"),("Habitación","AED 1.500–3.000","por mes, compartida")],
   ojo=[("El título de la sede satélite","Pregunta por escrito si el diploma es idéntico al de la casa matriz. La respuesta no siempre es sí."),
        ("La acreditación local","La institución debe estar reconocida por la autoridad educativa de Emiratos. No te quedes con la web."),
        ("Quién patrocina tu permiso","Entiende qué pasa con tu visa si dejas el programa o cambias de universidad."),
        ("El costo de vida","La matrícula es solo una parte. Vivienda y transporte pesan mucho en el presupuesto real.")],
   paso="Confirma que la universidad esté acreditada en Emiratos y que el título sea el mismo de la casa matriz."),
 "espana": dict(img="dest-spain.webp", alt="Grupo de estudiantes latinoamericanos en un patio universitario de España",
   titulo=f"Estudiar en España sin agencia {CURSO}: 30 horas de trabajo, sueldo mínimo, arriendo y transporte",
   desc=f"Con el nuevo reglamento puedes trabajar 30 horas por semana estudiando en España. Salario mínimo 2026, precio de una habitación en Madrid o Barcelona y Abono Joven de transporte, para el curso {CURSO}.",
   corta="Sí. Aplicas directo a la universidad y luego pides la estancia por estudios. Desde mayo de 2025 puedes trabajar hasta 30 horas por semana sin otra autorización, con un salario mínimo de €1.221 al mes en 14 pagas. Una habitación cuesta en promedio €425 al mes y, en Madrid, el Abono Joven de transporte cuesta €10.",
   kpis=[("Trabajo","30 h / semana","sin otra autorización"),("Hora mínima","€9,55","€1.221 al mes × 14 pagas"),("Habitación","€425–600","por mes; Barcelona, la más cara")],
   ojo=[("La homologación de tu título","Es el trámite que más demora y el que más gente deja para el final."),
        ("Pública contra privada","Un mismo programa puede costar varias veces más en una privada. Compara antes de enamorarte de una marca."),
        ("Título oficial o título propio","No valen lo mismo. Pregunta siempre qué tipo de título te entregan."),
        ("Las tasas que no aparecen","Matrícula, tasas administrativas y seguro se cotizan por separado. Pide el total.")],
   paso="Empieza la homologación de tu título: es el trámite que más tarda."),
}
for s in ORDEN:                                   # la 4.ª cifra clave es el transporte
    EDIT[s]["kpis"].append(tuple(PUB[s]["transporte"]["kpi"]))

CODIGOS = [("593","Ecuador","EC"),("57","Colombia","CO"),("51","Perú","PE"),("52","México","MX"),("54","Argentina","AR"),
           ("56","Chile","CL"),("58","Venezuela","VE"),("591","Bolivia","BO"),("595","Paraguay","PY"),("598","Uruguay","UY"),
           ("55","Brasil","BR"),("507","Panamá","PA"),("506","Costa Rica","CR"),("503","El Salvador","SV"),("502","Guatemala","GT"),
           ("504","Honduras","HN"),("505","Nicaragua","NI"),("53","Cuba","CU"),("1809","Rep. Dominicana","DO"),
           ("1","EE. UU. / Canadá","US"),("34","España","ES"),("39","Italia","IT"),("49","Alemania","DE")]


# ── PLANTILLA COMÚN ──────────────────────────────────────────────────
def head(title, desc, slug, og_title, jsonld, robots="index, follow, max-image-preview:large, max-snippet:-1", og_type="article"):
    return f"""<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.className='js'</script>
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="Abog. Stalin Leonardo Vera Ortega">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE}/{slug}">
<link rel="alternate" type="text/markdown" title="Resumen para modelos de lenguaje" href="{SITE}/llms.txt">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="es_419">
<meta property="og:site_name" content="SLVERA Education Advisor">
<meta property="og:url" content="{SITE}/{slug}">
<meta property="og:title" content="{E(og_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og.jpg">
<meta name="theme-color" content="#F6F4EF">
<link rel="icon" href="{ICON}">
{FONTS}
<link rel="stylesheet" href="../styles.css?v=10">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<div id="progreso" aria-hidden="true"></div>
<header id="nav">
  <div class="wrap nav-in">
    <a href="../index.html" class="brand" aria-label="SLVERA Education Advisor, inicio">
      <span class="brand-mark" aria-hidden="true">SV</span>
      <span class="brand-txt"><b>SLVERA</b><span>Education Advisor</span></span>
    </a>
    <nav class="nav-links" aria-label="Principal">
      <a href="../index.html#test">Test</a>
      <a href="../index.html#datos">Datos {CURSO}</a>
      <a href="../index.html#destinos">Destinos</a>
      <a href="../index.html#comunidad">Comunidad</a>
      <a href="../index.html#faq">Preguntas</a>
    </nav>
    <a href="../index.html#guia" class="btn btn-primary btn-sm nav-cta">Guía gratis <span class="ar">→</span></a>
    <button class="burger" id="burger" type="button" onclick="toggleNav()" aria-label="Abrir menú" aria-expanded="false" aria-controls="mnav"><span></span><span></span></button>
  </div>
</header>
<div id="mnav">
  <a href="../index.html#test">¿Cuál es tu destino?</a>
  <a href="../index.html#datos">Datos {CURSO}</a>
  <a href="../index.html#destinos">Destinos</a>
  <a href="../index.html#comunidad">Comunidad</a>
  <a href="../index.html#faq">Preguntas</a>
  <div class="mn-foot">
    <a href="../index.html#guia" class="btn btn-primary btn-block">Descargar mi guía gratis <span class="ar">→</span></a>
    <button type="button" class="btn btn-ghost btn-block" data-espera>Unirme a la lista de espera</button>
    <a href="mailto:sac@slvera.com">sac@slvera.com</a>
  </div>
</div>
<main>
"""


def modal_espera(up):
    return f"""
<dialog id="espera" aria-labelledby="esperaT">
  <div class="dlg">
    <button type="button" class="dlg-x" data-cerrar aria-label="Cerrar">×</button>
    <div class="dlg-cuerpo" id="esperaCuerpo">
      <span class="label">Comunidad SLVERA · abre pronto</span>
      <h3 id="esperaT">Entra primero a la comunidad.</h3>
      <p class="muted">Déjanos tus datos y te avisamos antes que a nadie cuando abramos. Anotarte no cuesta nada ni te compromete a nada.</p>
      <form id="esperaForm" novalidate>
        <div class="f" id="e-nombre"><label for="eNombre">Tu nombre <span class="req">*</span></label><input id="eNombre" name="nombre" autocomplete="given-name" placeholder="Como te dicen tus amigos" required><span class="f-err">Escribe tu nombre.</span></div>
        <div class="f" id="e-email"><label for="eEmail">Tu correo <span class="req">*</span></label><input id="eEmail" type="email" name="email" autocomplete="email" inputmode="email" placeholder="tunombre@correo.com" required><span class="f-err">Revisa el correo.</span></div>
        <div class="f" id="e-tel"><label for="eTel">WhatsApp <span class="req">*</span></label><div class="tel-row"><select name="codigo" data-codigos aria-label="Código de país"></select><input id="eTel" type="tel" name="telefono" inputmode="tel" autocomplete="tel-national" placeholder="Tu número" required></div><span class="f-err">Escribe un número de WhatsApp válido.</span></div>
        <input class="f-hp" type="text" name="empresa" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="f-msg" role="alert"></div>
        <button class="btn btn-accent btn-block" type="submit">Anotarme en la lista <span class="ar">→</span></button>
        <p class="f-legal">Al anotarte aceptas la <a href="{up}legal/privacidad.html">política de privacidad</a>. Te puedes borrar cuando quieras.</p>
      </form>
    </div>
    <div class="f-done" id="esperaDone">
      <div class="tick" aria-hidden="true">✓</div>
      <h3>Estás en la lista.</h3>
      <p>Te escribimos por WhatsApp cuando abramos la comunidad. Vas a ser de los primeros en entrar.</p>
      <a class="btn btn-wa btn-block" id="esperaGrupo" hidden target="_blank" rel="noopener">Entrar al grupo de WhatsApp</a>
    </div>
  </div>
</dialog>
"""


def foot(up="../", dock_href="../index.html#guia", dock_txt=("Guía gratis de tu país", f"Datos {CURSO}, directo a tu correo")):
    return f"""</main>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <div class="brand"><span class="brand-mark" aria-hidden="true">SV</span><span class="brand-txt"><b>SLVERA</b><span>Education Advisor</span></span></div>
        <p>Asesoría educativa internacional para latinoamericanos que quieren estudiar afuera con criterio y sin agencias. Fundada por el Abog. Stalin Leonardo Vera Ortega en Cuenca, Ecuador.</p>
        <a class="foot-mail" href="mailto:sac@slvera.com">sac@slvera.com</a>
        <div class="socials"><a href="#" aria-label="Instagram">IG</a><a href="#" aria-label="TikTok">TK</a><a href="#" aria-label="YouTube">YT</a><a href="#" aria-label="LinkedIn">IN</a></div>
      </div>
      <div class="foot-cols">
        <div class="foot-col"><h4>Explora</h4><ul>
          <li><a href="{up}index.html#test">Test de destino</a></li><li><a href="{up}index.html#datos">Datos {CURSO}</a></li><li><a href="{up}index.html#ahorro">Calculadora</a></li><li><a href="{up}index.html#comunidad">Comunidad</a></li><li><a href="{up}index.html#faq">Preguntas</a></li>
        </ul></div>
        <div class="foot-col"><h4>Destinos</h4><ul>
          <li><a href="{up}destinos/australia.html">Australia</a></li><li><a href="{up}destinos/malta.html">Malta</a></li><li><a href="{up}destinos/alemania.html">Alemania</a></li><li><a href="{up}destinos/dubai.html">Dubái</a></li><li><a href="{up}destinos/espana.html">España</a></li>
        </ul></div>
        <div class="foot-col"><h4>Legal</h4><ul>
          <li><a href="{up}legal/terminos.html">Términos y condiciones</a></li><li><a href="{up}legal/privacidad.html">Privacidad</a></li><li><a href="{up}legal/cookies.html">Cookies</a></li><li><a href="{up}legal/aviso-legal.html">Aviso legal</a></li>
        </ul></div>
      </div>
    </div>
    <div class="foot-legal"><p><strong style="color:inherit">Aviso legal.</strong> SLVERA Education Advisor es una marca operada por Stalin Leonardo Vera Ortega, RUC 1103916050001, Cuenca, Azuay, Ecuador. SLVERA no tramita, gestiona ni procesa solicitudes de visa ni actúa como agencia migratoria. Sus servicios se limitan a asesoría en selección de programas académicos internacionales, revisión de contratos educativos y orientación técnica en plataformas de aplicación. Stalin Vera es abogado habilitado en Ecuador; no es agente migratorio certificado MARA, IRCC, RME ni figura equivalente.</p></div>
    <div class="foot-base"><span>© <span id="anio">2026</span> SLVERA Education Advisor · Stalin Leonardo Vera Ortega · RUC 1103916050001</span><span>Cuenca · Azuay · Ecuador</span></div>
  </div>
</footer>

<div id="dock">
  <div class="dk-txt"><b>{dock_txt[0]}</b><span>{dock_txt[1]}</span></div>
  <a href="{dock_href}" class="btn btn-primary btn-sm">Pedirla <span class="ar">→</span></a>
</div>
<div id="cookie" role="dialog" aria-label="Aviso de cookies" hidden>
  <p>Usamos cookies técnicas para que el sitio funcione y, solo si aceptas, cookies analíticas para entender qué te sirve. <a href="{up}legal/cookies.html">Ver la política</a>.</p>
  <div class="ck-btns"><button type="button" class="btn btn-ghost" onclick="rejectCookies()">Solo las necesarias</button><button type="button" class="btn btn-primary" onclick="acceptCookies()">Aceptar</button></div>
</div>
{modal_espera(up)}
<script src="{up}app.js?v=10"></script>
</body>
</html>
"""


def escribir(rel, contenido):
    ruta = ROOT / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8", newline="\n")
    print("  ", rel)


def kpis_html(k):
    return '<div class="kpis">' + "".join(f'<div class="kpi"><span>{E(a)}</span><b>{E(b)}</b><em>{E(c)}</em></div>' for a, b, c in k) + "</div>"


def tabla_html(filas, caption):
    rows = "".join(f'<tr><th scope="row" style="font-family:var(--sans);font-size:.95rem;font-weight:500">{E(a)}</th><td><b>{E(b)}</b></td></tr>' for a, b in filas)
    return (f'<div class="tabla-wrap"><table class="tabla"><caption>{E(caption)}</caption>'
            f'<thead><tr><th scope="col">Opción</th><th scope="col">Precio</th></tr></thead><tbody>{rows}</tbody></table></div>')


def preguntas(s):
    d, ed, p = PUB[s], EDIT[s], PUB[s]["pais"]
    qa = [(f"¿Se puede estudiar en {p} sin agencia?", ed["corta"]),
          (f"¿Cuántas horas puedo trabajar estudiando en {p}?", d["trabajo"]["resumen"]),
          (f"¿Cuánto gana un estudiante por hora en {p}?", d["salario"]["resumen"]),
          (f"¿Cuánto cuesta una habitación en {p}?", d["arriendo"]["resumen"]),
          (f"¿Cuánto cuesta el transporte para estudiantes en {p}?", d["transporte"]["resumen"])]
    if "matricula" in d:
        qa.append((f"¿Hay que pagar matrícula para estudiar en {p}?", d["matricula"]["resumen"]))
    return qa


# ── PÁGINAS DE DESTINO ───────────────────────────────────────────────
def destinos():
    for s in ORDEN:
        d, ed = PUB[s], EDIT[s]
        pais, url = d["pais"], f"{SITE}/destinos/{s}.html"
        qa = preguntas(s)
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "@id": url + "#articulo", "headline": ed["titulo"], "description": ed["desc"],
             "inLanguage": "es", "datePublished": "2026-09-23", "dateModified": HOY,
             "image": f"{SITE}/assets/{ed['img']}", "mainEntityOfPage": url,
             "author": {"@type": "Person", "@id": f"{SITE}/#stalin", "name": "Stalin Leonardo Vera Ortega", "jobTitle": "Abogado y asesor educativo internacional", "url": f"{SITE}/#asesor"},
             "publisher": {"@type": "Organization", "@id": f"{SITE}/#org", "name": "SLVERA Education Advisor", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/og.jpg"}},
             "about": {"@type": "Country", "name": pais if s != "dubai" else "Emiratos Árabes Unidos"},
             "citation": [u for _, u in d["fuentes"]]},
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Destinos", "item": f"{SITE}/#destinos"},
                {"@type": "ListItem", "position": 3, "name": pais, "item": url}]}
        ]}, ensure_ascii=False, indent=1)

        matricula = f'<h2>{E(qa[5][0])}</h2><p>{E(d["matricula"]["resumen"])}</p>' if "matricula" in d else ""
        ciudades = "".join(f"<li><strong>{E(c)}.</strong> {E(t)}</li>" for c, t in d["ciudades"])
        extras = "".join(f"<li>{E(x)}</li>" for x in d["extra"])
        ojo = "".join(f'<div class="pp"><i>{i+1:02d}</i><div><b>{E(t)}</b><span>{E(x)}</span></div></div>' for i, (t, x) in enumerate(ed["ojo"]))
        fuentes = "".join(f'<li><a href="{E(u)}" rel="noopener" target="_blank">{E(n)}</a></li>' for n, u in d["fuentes"])
        otros = "".join(f'<li><a href="{o}.html">Estudiar en {PUB[o]["pais"]}</a></li>' for o in ORDEN if o != s)
        guia = f"../index.html?guia={s}#guia"

        cuerpo = f"""
<section class="page-head">
  <div class="wrap">
    <p class="crumb"><a href="../index.html">Inicio</a> / <a href="../index.html#destinos">Destinos</a> / {E(pais)}</p>
    <div style="max-width:60rem">
      <span class="label">{d['codigo']} · Guía de destino {CURSO}</span>
      <h1 class="display" style="margin:1rem 0 0">Estudiar en {E(pais)} <em class="acc">sin agencia.</em></h1>
      <div class="byline">
        <img src="../assets/stalin-firma.webp" width="44" height="44" alt="Abog. Stalin Vera">
        <div><b>Por el Abog. Stalin Vera</b>Datos para el curso {CURSO} · actualizado el <time datetime="{HOY}">{HOY_TXT}</time></div>
      </div>
    </div>
  </div>
</section>

<section class="sec-tight" style="padding-top:0">
  <div class="wrap prose-grid">
    <article>
      <div class="respuesta respuesta-corta">
        <span class="label">Respuesta corta</span>
        <p>{E(ed['corta'])}</p>
      </div>
      {kpis_html(ed['kpis'])}
      <figure class="dest-hero"><img src="../assets/{ed['img']}" width="880" height="1320" alt="{E(ed['alt'])}"></figure>

      <div class="prose">
        <h2>{E(qa[1][0])}</h2>
        <p>{E(d['trabajo']['resumen'])}</p>

        <h2>{E(qa[2][0])}</h2>
        <p>{E(d['salario']['resumen'])}</p>

        <h2>{E(qa[3][0])}</h2>
        <p>{E(d['arriendo']['resumen'])}</p>
        {tabla_html(d['arriendo']['filas'], 'Fuente: ' + d['arriendo']['fuente'] + '. Precios de referencia; varían por barrio y temporada.')}

        <h2>{E(qa[4][0])}</h2>
        <p>{E(d['transporte']['resumen'])}</p>

        {matricula}

        <h2>¿Cuáles son las mejores ciudades para estudiar en {E(pais)}?</h2>
        <ul>{ciudades}</ul>

        <h2>Lo que casi nadie te dice</h2>
        <ul>{extras}</ul>

        <div class="gancho">
          <span class="label">Solo en la guía</span>
          <p><strong>¿Cuánto dinero te piden demostrar para estudiar en {E(pais)}?</strong> Esa cifra, cómo acreditarla y el presupuesto real del primer año están en la guía gratis de {E(pais)}.</p>
          <a href="{guia}" class="btn btn-primary btn-sm">Quiero la guía de {E(pais)} <span class="ar">→</span></a>
        </div>
      </div>
    </article>

    <aside class="aside-sticky">
      <div class="precio" style="padding:1.5rem">
        <span class="tag">Gratis · PDF</span>
        <h3 style="font-size:1.3rem">La guía de {E(pais)}</h3>
        <p class="muted" style="font-size:.9rem;margin:.5rem 0 1.1rem">Todo esto, más cuánto te piden demostrar, las trampas del contrato y el paso a paso. Te llega al correo.</p>
        <a href="{guia}" class="btn btn-primary btn-block">Quiero la guía <span class="ar">→</span></a>
        <button type="button" class="btn btn-ghost btn-block" style="margin-top:.6rem" data-espera>Lista de espera de la comunidad</button>
      </div>
    </aside>
  </div>
</section>

<section class="sec dark">
  <div class="wrap-md">
    <div class="sec-head">
      <span class="label">Aquí se pierde la plata</span>
      <h2 class="headline">Lo que hay que mirar <em class="acc">en {E(pais)}.</em></h2>
      <p class="lead">Los cuatro puntos donde más gente cae. Ninguno es obvio, y todos están por escrito en algún lado del contrato.</p>
    </div>
    <div class="pp-list">{ojo}</div>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap-md prose">
    <div class="fuentes">
      <h2>Fuentes oficiales</h2>
      <ol>{fuentes}</ol>
      <p style="font-size:.84rem;margin-top:.8rem">Cifras de orientación para el curso {CURSO}, verificadas el {HOY_TXT}. Las condiciones cambian: confirma en la fuente oficial antes de pagar o firmar. SLVERA no tramita visas.</p>
    </div>
    <h2>Otros destinos</h2>
    <ul>{otros}</ul>
  </div>
</section>

<section class="sec dark cta-final" style="background:var(--noche-2)">
  <div class="wrap-md">
    <span class="label" style="justify-content:center">Siguiente paso</span>
    <h2 class="headline">¿Te sirve {E(pais)}? Averigüémoslo.</h2>
    <p class="lead">Descarga la guía completa del país. Y si quieres hacerlo acompañado, anótate en la lista de espera: la comunidad abre pronto.</p>
    <div class="cta-btns">
      <a href="{guia}" class="btn btn-primary">Descargar la guía de {E(pais)} <span class="ar">→</span></a>
      <button type="button" class="btn btn-ghost" data-espera>Unirme a la lista de espera</button>
    </div>
  </div>
</section>
"""
        escribir(f"destinos/{s}.html",
                 head(ed["titulo"] + " | SLVERA", ed["desc"], f"destinos/{s}.html", f"Estudiar en {pais} sin agencia · Datos {CURSO}", jsonld)
                 + cuerpo + foot("../", guia, (f"Guía gratis de {pais}", f"Datos {CURSO}, a tu correo")))


# ── LEGALES ──────────────────────────────────────────────────────────
def legal(rel, corto, h1, title, desc, cuerpo):
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": h1, "url": f"{SITE}/{rel}",
                         "inLanguage": "es", "dateModified": HOY, "publisher": {"@id": f"{SITE}/#org"}}, ensure_ascii=False)
    body = f"""
<section class="page-head">
  <div class="wrap-md">
    <p class="crumb"><a href="../index.html">Inicio</a> / Legal / {corto}</p>
    <span class="label">Documento legal</span>
    <h1 class="headline" style="margin:1rem 0 .8rem">{h1}</h1>
    <p class="muted" style="font-size:.9rem">Titular: Stalin Leonardo Vera Ortega · RUC 1103916050001 · Cuenca, Azuay, Ecuador · Última actualización: {HOY_TXT}</p>
  </div>
</section>
<section class="sec-tight" style="padding-top:.5rem">
  <div class="wrap-md"><div class="prose">
{cuerpo}
    <hr style="margin:3rem 0;border:0;border-top:1px solid var(--line)">
    <p class="muted" style="font-size:.9rem">¿Dudas sobre este documento? Escríbenos a <a href="mailto:sac@slvera.com">sac@slvera.com</a>.</p>
    <p><a href="../index.html">← Volver al inicio</a></p>
  </div></div>
</section>
"""
    escribir(rel, head(title, desc, rel, h1, jsonld, robots="index, follow", og_type="website") + body + foot())


def legales():
    legal("legal/terminos.html", "Términos", "Términos y Condiciones", "Términos y Condiciones | SLVERA",
          "Términos y condiciones del sitio, la guía gratuita, la lista de espera y la comunidad de SLVERA Education Advisor.", """
    <h2>1. Titular e identificación</h2>
    <p>El sitio web y la comunidad son operados por <strong>Stalin Leonardo Vera Ortega</strong>, RUC N.° 1103916050001, domiciliado en Cuenca, Azuay, República del Ecuador, bajo la marca <strong>SLVERA Education Advisor</strong>. Contacto: <a href="mailto:sac@slvera.com">sac@slvera.com</a>.</p>
    <h2>2. Objeto y alcance del servicio</h2>
    <p>SLVERA Education Advisor presta servicios de asesoría educativa internacional con carácter estrictamente informativo. Hoy comprenden:</p>
    <ul>
      <li>Guías informativas gratuitas por país, en formato PDF.</li>
      <li>Revisión de contratos educativos emitidos por instituciones extranjeras, cotizada caso por caso.</li>
      <li>Orientación sobre la aplicación directa en plataformas de instituciones y portales como Uniapplinow o Edu-connector.</li>
      <li>Comunidad privada, que abrirá próximamente (ver punto 3).</li>
    </ul>
    <p>Las sesiones en vivo, la recomendación de instituciones evaluadas y la asesoría VIP 1 a 1 están anunciadas como <strong>próximamente</strong> y no forman parte de la oferta actual.</p>
    <p>Los servicios <strong>NO</strong> comprenden tramitación, gestión o procesamiento de visas, permisos de residencia ni autorización migratoria ante autoridades extranjeras, ni actuación como agente migratorio certificado en ninguna jurisdicción.</p>
    <h2>3. Lista de espera y comunidad</h2>
    <p><strong>3.1. Lista de espera:</strong> inscribirse es gratuito y no genera ningún cobro ni obligación de compra. Sirve para avisarte de la apertura de la comunidad y para invitarte a su grupo de WhatsApp.</p>
    <p><strong>3.2. Costo de la comunidad:</strong> USD $39 mensuales desde su apertura, procesados por la plataforma de pagos que se indique en ese momento. SLVERA no almacena datos de instrumentos de pago.</p>
    <p><strong>3.3. Cancelación:</strong> el miembro puede cancelar en cualquier momento, sin cargos adicionales. El acceso se mantiene hasta el fin del período pagado.</p>
    <p><strong>3.4. Reembolsos:</strong> no se garantizan salvo error técnico comprobable en el procesamiento del pago.</p>
    <h2>4. Guías gratuitas y datos publicados</h2>
    <p>Las guías por país y las cifras publicadas en el sitio tienen carácter orientativo. Se verifican en fuentes oficiales a la fecha indicada, pero las condiciones de cada país cambian. El usuario debe confirmar la información vigente en la fuente oficial antes de tomar decisiones o realizar pagos.</p>
    <h2>5. Propiedad intelectual</h2>
    <p>Todo el contenido es propiedad de Stalin Leonardo Vera Ortega, protegido por la legislación ecuatoriana de derechos de autor y los tratados internacionales. Se prohíbe su reproducción o distribución sin autorización escrita.</p>
    <h2>6. Limitación de responsabilidad</h2>
    <p>SLVERA proporciona información educativa con la mayor diligencia, pero no garantiza resultados en procesos de aplicación o admisión. En ningún caso la responsabilidad de SLVERA superará el valor del último pago efectuado.</p>
    <h2>7. Legislación y jurisdicción</h2>
    <p>Estos términos se rigen por las leyes de la República del Ecuador. Para controversias, son competentes los tribunales de la ciudad de Cuenca, Ecuador.</p>
""")
    legal("legal/privacidad.html", "Privacidad", "Política de Privacidad", "Política de Privacidad | SLVERA",
          "Cómo SLVERA Education Advisor recopila, usa y protege tus datos personales conforme a la LOPDP de Ecuador.", """
    <h2>1. Responsable del tratamiento</h2>
    <p><strong>Stalin Leonardo Vera Ortega</strong> (RUC 1103916050001), Cuenca, Azuay, Ecuador. Correo: <a href="mailto:sac@slvera.com">sac@slvera.com</a>.</p>
    <h2>2. Datos que recopilamos</h2>
    <p><strong>Los que nos das:</strong> nombre, correo electrónico, número de WhatsApp con código de país y, si pides la guía, el país que elegiste.</p>
    <p><strong>Los que se registran solos:</strong> página de origen, parámetros de campaña (UTM), resultado del test de destino si lo hiciste, tipo de dispositivo y, solo si aceptas las cookies analíticas, datos de navegación agregados.</p>
    <p><strong>Datos de pago:</strong> SLVERA NO recopila ni almacena datos de instrumentos de pago.</p>
    <h2>3. Para qué los usamos</h2>
    <ul>
      <li>Enviarte por correo la guía que pediste.</li>
      <li>Escribirte por WhatsApp o correo para orientarte sobre tu proceso.</li>
      <li>Si te anotas en la lista de espera: avisarte cuando abra la comunidad e invitarte a su grupo de WhatsApp.</li>
      <li>Mejorar el contenido del sitio y cumplir obligaciones tributarias ante el SRI del Ecuador.</li>
    </ul>
    <p>La lista de espera es opcional: marcarla en el formulario de la guía o anotarte aparte es siempre una decisión tuya.</p>
    <h2>4. Grupo de WhatsApp</h2>
    <p>Unirte al grupo es voluntario. Ten en cuenta que, según cómo funcione el grupo, otros participantes pueden ver tu número. Puedes salir cuando quieras.</p>
    <h2>5. Dónde se guardan</h2>
    <p>Los datos de los formularios se guardan en una hoja de cálculo privada de Google Drive, con acceso restringido al responsable. No se comparten, venden ni ceden a terceros con fines comerciales.</p>
    <h2>6. Base jurídica</h2>
    <p>Tu consentimiento al enviar cada formulario y el cumplimiento de la Ley Orgánica de Protección de Datos Personales (LOPDP) del Ecuador.</p>
    <h2>7. Tus derechos</h2>
    <p>Conforme a la LOPDP puedes ejercer tus derechos de acceso, rectificación, eliminación, oposición, portabilidad y limitación escribiendo a <a href="mailto:sac@slvera.com">sac@slvera.com</a>. Si pides que borremos tus datos, lo hacemos y te lo confirmamos por escrito.</p>
    <h2>8. Transferencias internacionales</h2>
    <p>Los datos pueden procesarse en servidores de Google y de WhatsApp (Meta) en Estados Unidos, bajo las garantías que reconoce la LOPDP.</p>
""")
    legal("legal/cookies.html", "Cookies", "Política de Cookies", "Política de Cookies | SLVERA",
          "Qué cookies usa slvera.com, para qué sirven y cómo gestionar tu consentimiento.", """
    <h2>1. ¿Qué son las cookies?</h2>
    <p>Son pequeños archivos de texto que un sitio guarda en tu dispositivo para recordar información entre visitas, analizar el uso del sitio y personalizar la experiencia.</p>
    <h2>2. Qué cookies usamos</h2>
    <p><strong>Técnicas (necesarias):</strong> hacen funcionar el sitio y recuerdan tu preferencia de cookies. No requieren consentimiento previo.</p>
    <p><strong>Analíticas:</strong> miden el uso del sitio de forma agregada. <strong>Solo se cargan después de que las aceptas.</strong> Si las rechazas, ningún script de análisis se ejecuta en tu navegador.</p>
    <p><strong>De terceros:</strong> plataformas como WhatsApp o las redes sociales pueden instalar sus propias cookies cuando navegas hacia ellas. SLVERA no las controla.</p>
    <h2>3. Cómo gestionar tu consentimiento</h2>
    <p>La primera vez que entras ves un aviso para aceptar o rechazar las cookies analíticas. Tu elección se guarda 13 meses en una cookie técnica. Puedes cambiarla borrando los datos del sitio en tu navegador o escribiendo a <a href="mailto:sac@slvera.com">sac@slvera.com</a>.</p>
""")
    legal("legal/aviso-legal.html", "Aviso legal", "Aviso Legal y Exención de Responsabilidad", "Aviso Legal | SLVERA",
          "Qué presta y qué no presta SLVERA Education Advisor. SLVERA no tramita ni gestiona visas.", """
    <h2>1. Naturaleza del servicio</h2>
    <p><strong>SLVERA Education Advisor</strong> es una marca operada por Stalin Leonardo Vera Ortega, RUC 1103916050001, Cuenca, Azuay, Ecuador. Sus servicios tienen carácter <strong>estrictamente informativo y de asesoría educativa internacional</strong>.</p>
    <h2>2. Servicios que SLVERA SÍ presta</h2>
    <ul>
      <li>Guías informativas por país.</li>
      <li>Revisión de contratos educativos emitidos por instituciones extranjeras.</li>
      <li>Orientación técnica para aplicar directo en plataformas de instituciones (Uniapplinow / Edu-connector).</li>
      <li>Comunidad privada, próximamente.</li>
    </ul>
    <h2>3. Servicios que SLVERA NO presta</h2>
    <p><strong>SLVERA no tramita, gestiona, procesa ni facilita solicitudes de visa, permisos de residencia ni autorizaciones migratorias</strong> ante autoridades extranjeras. La aplicación a instituciones y cualquier trámite ante autoridades de otros países son responsabilidad exclusiva del estudiante.</p>
    <ul>
      <li>No actúa como agente migratorio certificado MARA en Australia.</li>
      <li>No actúa como RCIC ni bajo el sistema IRCC de Canadá.</li>
      <li>No actúa como agente migratorio en Alemania, Malta, España ni Emiratos Árabes Unidos.</li>
    </ul>
    <h2>4. Resultados</h2>
    <p>SLVERA no garantiza resultados en procesos de admisión ni en ningún trámite ante autoridades extranjeras. Los resultados dependen de decisiones de terceros fuera de su control.</p>
    <h2>5. Legislación y jurisdicción</h2>
    <p>Este aviso se rige por las leyes de la República del Ecuador. Controversias: tribunales competentes de Cuenca, Ecuador.</p>
""")


# ── AEO: robots, sitemap, llms ───────────────────────────────────────
def aeo():
    NO = "Disallow: /guias/\n"
    escribir("robots.txt", f"""# slvera.com
# Abierto a propósito a buscadores y asistentes de IA: queremos que
# ChatGPT, Claude, Perplexity, Gemini, Copilot y Siri nos lean y nos citen.

User-agent: *
Allow: /
{NO}
# Búsqueda con IA y consultas en nombre de un usuario
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Googlebot
User-agent: Bingbot
User-agent: Applebot
User-agent: DuckAssistBot
User-agent: meta-externalfetcher
Allow: /
{NO}
# Entrenamiento de modelos: PERMITIDO a propósito. Para una marca nueva,
# que los modelos "conozcan" SLVERA sin necesidad de buscar es visibilidad.
# Si algún día prefieres bloquearlo, cambia "Allow: /" por "Disallow: /" aquí.
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: meta-externalagent
User-agent: CCBot
Allow: /
{NO}
Sitemap: {SITE}/sitemap.xml
""")
    urls = [("", "weekly", "1.0")] + [(f"destinos/{s}.html", "monthly", "0.9") for s in ORDEN] + \
           [(f"legal/{l}.html", "yearly", "0.2") for l in ["terminos", "privacidad", "cookies", "aviso-legal"]] + \
           [("llms.txt", "monthly", "0.5"), ("datos/destinos-2026.json", "monthly", "0.5")]
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
             "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{HOY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n" for u, c, p in urls) +
             "</urlset>\n")

    def linea(s):
        k = "; ".join(f"{a.lower()}: {b}" for a, b, _ in EDIT[s]["kpis"])
        return f"- [Estudiar en {PUB[s]['pais']} sin agencia ({CURSO})]({SITE}/destinos/{s}.html): {k}."

    escribir("llms.txt", f"""# SLVERA Education Advisor

> Asesoría educativa internacional dirigida por el abogado ecuatoriano Stalin Leonardo Vera Ortega, en Cuenca, Ecuador. Enseña a latinoamericanos a estudiar en el extranjero sin pagar una agencia: a aplicar por su cuenta a instituciones de Australia, Malta, Alemania, Dubái y España, con datos verificados y contratos revisados por un abogado. SLVERA no tramita visas.

Datos clave de la organización:

- Nombre: SLVERA Education Advisor (SLVERA). Sitio: {SITE}/
- Fundador: Abog. Stalin Leonardo Vera Ortega. Registro SENESCYT 1031-2025-3144323. Cuenca, Azuay, Ecuador.
- Guía gratuita: un PDF por país con datos del curso {CURSO} (horas de trabajo, salario por hora, arriendo, transporte, dinero que piden demostrar y trampas del contrato). Se pide en {SITE}/#guia con nombre, correo y WhatsApp.
- Comunidad SLVERA: abre próximamente, con lista de espera gratuita en {SITE}/#comunidad. Costará 39 USD al mes, sin permanencia.
- Servicio disponible hoy: revisión de contratos educativos, cotizada caso por caso.
- Próximamente: sesiones en vivo, recomendación de instituciones evaluadas y asesoría VIP 1 a 1.
- Público: estudiantes de Ecuador y Latinoamérica. Idioma: español.
- Límite legal: SLVERA no tramita, gestiona ni procesa visas. Stalin Vera no es agente migratorio certificado (MARA, IRCC, RME ni equivalente).
- Contacto: sac@slvera.com
- Datos actualizados: {HOY}.

## Guías por destino ({CURSO})

{chr(10).join(linea(s) for s in ORDEN)}

## Datos abiertos

- [Datos {CURSO} por destino (JSON)]({SITE}/datos/destinos-2026.json): trabajo, salario, arriendo y transporte, con sus fuentes oficiales.
- [Versión completa de este resumen]({SITE}/llms-full.txt): todas las respuestas del sitio en texto plano.

## Páginas principales

- [Inicio: estudiar en el extranjero sin agencia]({SITE}/): test de destino, tabla comparativa {CURSO}, calculadora de ahorro y preguntas frecuentes.
- [Comunidad SLVERA y lista de espera]({SITE}/#comunidad)
- [Preguntas frecuentes]({SITE}/#faq)

## Optional

- [Términos y condiciones]({SITE}/legal/terminos.html)
- [Política de privacidad]({SITE}/legal/privacidad.html)
- [Aviso legal: qué hace y qué no hace SLVERA]({SITE}/legal/aviso-legal.html)
""")

    bloques = []
    for s in ORDEN:
        d, ed, p = PUB[s], EDIT[s], PUB[s]["pais"]
        b = [f"## Estudiar en {p} sin agencia (curso {CURSO})", f"URL: {SITE}/destinos/{s}.html", ""]
        for q, a in preguntas(s):
            b += [f"### {q}", a, ""]
        b += [f"### Mejores ciudades para estudiar en {p}"] + [f"- {c}: {t}" for c, t in d["ciudades"]] + [""]
        b += ["### Lo que casi nadie te dice"] + [f"- {x}" for x in d["extra"]] + [""]
        b += ["### Qué revisar en el contrato"] + [f"- {t}: {x}" for t, x in ed["ojo"]] + [""]
        b += ["Fuentes oficiales:"] + [f"- {n}: {u}" for n, u in d["fuentes"]] + [""]
        bloques.append("\n".join(b))

    escribir("llms-full.txt", f"""# SLVERA Education Advisor — contenido completo para modelos de lenguaje

> Asesoría educativa internacional dirigida por el Abog. Stalin Leonardo Vera Ortega (Cuenca, Ecuador). Estudiar en el extranjero sin agencia: Australia, Malta, Alemania, Dubái y España. Guía gratuita por país. Comunidad con lista de espera (39 USD al mes desde su apertura). No tramita visas. Contacto: sac@slvera.com. Actualizado: {HOY}.

Cifras de orientación para el curso {CURSO}, verificadas en fuentes oficiales en la fecha indicada. Las condiciones cambian; confirma siempre en la fuente oficial.

## Preguntas frecuentes

### ¿Se puede estudiar en el extranjero sin agencia?
Sí. Las instituciones aceptan postulaciones directas en sus propias plataformas y en portales como Uniapplinow o Edu-connector. Lo que una agencia cobra (entre 500 y 1.200 dólares por proceso) es por hacer trámites abiertos al público. SLVERA enseña a hacerlos uno mismo, con criterio de abogado.

### ¿SLVERA tramita visas?
No. SLVERA hace asesoría educativa: guías por país, orientación para aplicar directo y revisión de contratos educativos. No tramita, gestiona ni procesa visas, y no actúa como agente migratorio certificado en ningún país.

### ¿Cuánto cuesta la comunidad SLVERA?
Abre próximamente y costará 39 dólares al mes, sin permanencia. La lista de espera es gratuita y no obliga a nada.

### ¿Cuántas horas puede trabajar un estudiante extranjero? (curso {CURSO})
Australia: 48 horas por quincena durante el curso, sin límite en vacaciones. España: hasta 30 horas por semana. Malta: 20 horas por semana. Alemania: 140 días completos o 280 medios días por año. Dubái: habitualmente hasta 15 horas por semana con permiso del MOHRE.

### ¿Cuánto cuesta el transporte para estudiantes? (curso {CURSO})
Malta: gratis con la tarjeta Tallinja personalizada. Brisbane (Australia): A$0,50 por viaje. Alemania: €37,80 al mes con el pase de estudiante para todo el país. Madrid: €10 al mes con el Abono Joven (hasta 25 años). Dubái: 50 % de descuento con la tarjeta Nol de estudiante (hasta 23 años).

### ¿Qué país es más barato para estudiar desde Latinoamérica?
En matrícula, Alemania: la mayoría de sus universidades públicas no cobran. En transporte, Malta: es gratis con la tarjeta Tallinja. En arriendo, España está entre las más accesibles: una habitación cuesta 425 euros al mes en promedio. Y para ganar más por hora, Australia paga el mínimo más alto: A$26,44.

{chr(10).join(bloques)}""")


# ── GUÍAS PDF ────────────────────────────────────────────────────────
def num(x, dec=0):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ingreso(s):
    if s == "australia":
        a, c = 24 * 26.44, 24 * 33.05
        return ("24 horas por semana (48 por quincena) al mínimo", f"≈ A${num(a*52/12)}",
                f"al mes, antes de impuestos. Como casual (A$33,05/h): ≈ A${num(c*52/12)} al mes.")
    if s == "malta":
        a = 20 * 229.44 / 40
        return ("20 horas por semana al mínimo (€5,74/h)", f"≈ €{num(a*52/12)}", "al mes, brutos. Hostelería y turismo suelen pagar algo más que el mínimo.")
    if s == "alemania":
        return ("unas 20 horas por semana en promedio (140 días al año)", f"≈ €{num(20*13.90*52/12)}", "al mes, brutos, al salario mínimo de €13,90 la hora.")
    if s == "dubai":
        return ("15 horas por semana a AED 20–60 la hora", f"AED {num(15*20*52/12)}–{num(15*60*52/12)}", "al mes. En retail y eventos, lo normal es la parte baja del rango.")
    if s == "espana":
        m = .75 * 1221
        return ("30 horas por semana (75 % de la jornada) al mínimo", f"≈ €{num(m)}", f"al mes en 14 pagas (≈ €{num(m*14/12)} si lo repartes en 12). Brutos.")


def css_pdf():
    F = (AQUI / "fuentes").as_uri()
    return (AQUI / "guia.css").read_text(encoding="utf-8").replace("{F}", F)


def guias():
    A = (ROOT / "assets").as_uri()
    tmp = AQUI / ".tmp"
    tmp.mkdir(exist_ok=True)
    (ROOT / "guias").mkdir(exist_ok=True)
    for viejo in (ROOT / "guias").glob("*.pdf"):
        if viejo.name not in PDF.values():
            viejo.unlink()
    css = css_pdf()
    for s in ORDEN:
        d, ed, pv = PUB[s], EDIT[s], PRIV.get(s, {})
        pais = d["pais"]
        t_res, t_monto, t_nota = ingreso(s)
        kp = "".join(f'<div class="kpi"><span>{E(a)}</span><b>{E(b)}</b><em>{E(c)}</em></div>' for a, b, c in ed["kpis"])
        filas = "".join(f"<tr><td>{E(a)}</td><td><b>{E(b)}</b></td></tr>" for a, b in d["arriendo"]["filas"])
        ciud = "".join(f"<div><b>{E(c)}</b><span>{E(t)}</span></div>" for c, t in d["ciudades"])
        tr = "".join(f'<div class="tr"><i>{i+1:02d}</i><div><b>{E(t)}</b>{E(x)}</div></div>' for i, (t, x) in enumerate(ed["ojo"]))
        nadie = "".join(f"<li>{E(x)}</li>" for x in d["extra"])
        fuentes = "".join(f'<li>{E(n)} — <a href="{E(u)}">{E(u)}</a></li>' for n, u in d["fuentes"])
        pie = lambda n: f'<div class="pie"><span>SLVERA · Guía {E(pais)} {CURSO}</span><span>slvera.com</span><span>{n} / 7</span></div>'

        if "fondos" in pv:
            fondos = f'<div class="blk"><h3>El dinero que tienes que demostrar</h3><p>{E(pv["fondos"]["resumen"])}</p><p class="fuente">Fuente: {E(pv["fondos"]["fuente"])}</p></div>'
            if "visa" in pv:
                fondos += f'<div class="blk"><h3>La tasa de la visa</h3><p>{E(pv["visa"]["resumen"])}</p></div>'
            fondo_ref = f" <span class='muted'>(referencia: {E(pv['fondos']['monto'])})</span>"
        else:
            fondos = ('<div class="blk"><h3>El dinero que tienes que demostrar</h3><p>En Malta, el monto depende del tipo y la duración de tu curso, '
                      'y lo confirma la institución junto con la Unidad Central de Visas (Identità). Pídelo por escrito antes de pagar la matrícula: '
                      'si una escuela no te lo sabe decir, es mala señal.</p></div>')
            fondo_ref = " <span class='muted'>(pídelo por escrito)</span>"
        if "matricula" in d:
            fondos += f'<div class="blk"><h3>La matrícula</h3><p>{E(d["matricula"]["resumen"])}</p></div>'
        visa_ref = f" <span class='muted'>(referencia: {E(pv['visa']['monto'])})</span>" if "visa" in pv else ""

        doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Guía {E(pais)} {CURSO} · SLVERA</title><style>{css}</style></head><body>

<section class="pg cover">
  <div class="foto" style="background-image:url('{A}/{ed['img']}')"></div>
  <div class="top"><div class="mark"><i>SV</i><b>SLVERA</b></div><span class="chip">Guía gratuita · {CURSO}</span></div>
  <div class="txt">
    <span class="code">{d['codigo']}</span>
    <h1>Estudiar en<br><em>{E(pais)}.</em></h1>
    <p class="sub">Cuánto se gana por hora, cuánto cuesta vivir y moverte, cuánto te piden y lo que nadie te dice antes de pagar. Sin agencia.</p>
    <div class="by"><img src="{A}/stalin-firma.jpg" alt=""><div><b>Por el Abog. Stalin Vera</b>Datos para el curso {CURSO}, verificados en fuentes oficiales el {HOY_TXT}</div></div>
  </div>
</section>

<section class="pg">
  <span class="lab">01 · {E(pais)} en 30 segundos</span>
  <h2>Lo esencial, <em>primero.</em></h2>
  <div class="corta">{E(ed['corta'])}</div>
  <div class="kpis">{kp}</div>
  <div class="aviso"><b>Antes de seguir:</b> SLVERA hace asesoría educativa. No tramita ni gestiona visas, y Stalin Vera no es agente migratorio certificado en {E(pais)} ni en ningún otro país. Las cifras son de orientación: confírmalas siempre en la fuente oficial (al final de esta guía) antes de pagar o firmar.</div>
  {pie(2)}
</section>

<section class="pg">
  <span class="lab">02 · Trabajar mientras estudias</span>
  <h2>Cuánto puedes <em>trabajar y ganar.</em></h2>
  <div class="blk"><h3>Las horas que te dejan trabajar</h3><p>{E(d['trabajo']['resumen'])}</p><p class="fuente">Fuente: {E(d['trabajo']['fuente'])}</p></div>
  <div class="blk"><h3>Lo que se paga por hora</h3><p>{E(d['salario']['resumen'])}</p><p class="fuente">Fuente: {E(d['salario']['fuente'])}</p></div>
  <div class="big"><span class="lab">Hagamos la cuenta</span><p>Con {E(t_res)}:</p><div class="n">{E(t_monto)}</div><p>{E(t_nota)}</p></div>
  <p class="muted" style="font-size:10.4pt">Ojo: lo que ganes trabajando te ayuda a vivir, pero casi ningún país lo acepta para demostrar los fondos de la visa. Esos tienen que estar antes de que llegues.</p>
  {pie(3)}
</section>

<section class="pg">
  <span class="lab">03 · Dónde vivir y cómo moverte</span>
  <h2>Un techo <em>y el transporte.</em></h2>
  <p>{E(d['arriendo']['resumen'])}</p>
  <table><thead><tr><th>Opción</th><th>Precio de referencia</th></tr></thead><tbody>{filas}</tbody></table>
  <p class="fuente">Fuente: {E(d['arriendo']['fuente'])}. Varía por barrio y temporada.</p>
  <div class="mov"><span class="lab">Transporte</span><b>{E(d['transporte']['tabla'][0])}</b><p>{E(d['transporte']['resumen'])}</p><p class="fuente">Fuente: {E(d['transporte']['fuente'])}</p></div>
  <h3 style="margin-top:6mm">Las ciudades para estudiantes</h3>
  <div class="ciud">{ciud}</div>
  {pie(4)}
</section>

<section class="pg">
  <span class="lab">04 · Cuánto te piden</span>
  <h2>El dinero <em>que tienes que tener.</em></h2>
  {fondos}
  <h3 style="margin-top:6mm">Tu presupuesto del primer año</h3>
  <p class="muted" style="font-size:10.4pt">Llénalo con lo que te cotice la institución. Si una fila queda en blanco, esa es tu siguiente pregunta.</p>
  <table class="ws"><thead><tr><th>Concepto</th><th>Tu cifra</th></tr></thead><tbody>
    <tr><td>Fondos que te piden demostrar{fondo_ref}</td><td></td></tr>
    <tr><td>Matrícula del primer año</td><td></td></tr>
    <tr><td>Tasa de la visa{visa_ref}</td><td></td></tr>
    <tr><td>Seguro médico</td><td></td></tr>
    <tr><td>Pasaje</td><td></td></tr>
    <tr><td>Colchón: tres meses de gastos</td><td></td></tr>
    <tr class="tot"><td>Total para arrancar</td><td></td></tr>
  </tbody></table>
  {pie(5)}
</section>

<section class="pg dark">
  <span class="lab">05 · Aquí se pierde la plata</span>
  <h2>Lo que hay que mirar <em>en el contrato.</em></h2>
  <p>Los cuatro puntos donde más gente cae en {E(pais)}. Ninguno es obvio, y todos están escritos en algún lado del contrato.</p>
  <div style="margin-top:4mm">{tr}</div>
  <div class="nadie"><h3>Lo que casi nadie te dice</h3><ul>{nadie}</ul></div>
  {pie(6)}
</section>

<section class="pg">
  <span class="lab">06 · Tus próximos pasos</span>
  <h2>Por dónde <em>empezar hoy.</em></h2>
  <ol class="chk">
    <li>{E(ed['paso'])}</li>
    <li>Arma tu presupuesto real: fondos exigidos, matrícula, pasaje, seguro y tres meses de colchón.</li>
    <li>Elige tres instituciones y verifica su acreditación en la fuente oficial, no en su web.</li>
    <li>Pide el contrato antes de pagar nada y busca las cuatro cláusulas de la página anterior.</li>
    <li>Aplica directo en la plataforma oficial de la institución.</li>
    <li>Prepara la visa con la información oficial del país. SLVERA no la tramita.</li>
    <li>Reserva alojamiento temporal para tus primeras dos a cuatro semanas y busca lo definitivo allá.</li>
  </ol>
  <div class="cta">
    <div><h3>¿Quieres hacerlo acompañado?</h3><p>La comunidad SLVERA abre pronto. Anótate gratis en la lista de espera y entra de los primeros.</p><p style="margin-top:2.5mm;font-family:Mono;font-size:7.5pt;letter-spacing:.1em">slvera.com/#comunidad</p></div>
    <div class="pr"><b>$39</b><span>USD al mes al abrir</span></div>
  </div>
  <div class="src"><b>Fuentes oficiales</b><ol>{fuentes}</ol>
  <p style="margin-top:3mm">Guía informativa elaborada por SLVERA Education Advisor (Stalin Leonardo Vera Ortega, Cuenca, Ecuador). No constituye asesoría migratoria. ¿Encontraste un dato desactualizado? Escríbenos a sac@slvera.com.</p></div>
  {pie(7)}
</section>

</body></html>"""
        src = tmp / f"guia-{s}.html"
        src.write_text(doc, encoding="utf-8")
        salida = ROOT / "guias" / PDF[s]
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                        "--virtual-time-budget=8000", f"--print-to-pdf={salida}", src.as_uri()],
                       check=True, capture_output=True, timeout=180)
        print(f"   guias/{salida.name}  {salida.stat().st_size // 1024} KB")


if __name__ == "__main__":
    destinos()
    legales()
    aeo()
    if "--sin-pdf" not in sys.argv:
        guias()
    print("Listo.")
