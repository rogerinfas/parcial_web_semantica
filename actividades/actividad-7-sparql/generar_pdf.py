from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Preformatted,
                                Table, TableStyle, PageBreak, Image)
from reportlab.lib.utils import ImageReader

OUT = "actividades/actividad-7-sparql/ACTIVIDAD_7_SPARQL_ROGER_INFA_SANCHEZ.pdf"
LOGO = "logo_web.png"
CAP = "actividades/actividad-7-sparql/capturas"

styles = getSampleStyleSheet()
title_s = styles['Title']
h1 = styles['Heading1']
normal = ParagraphStyle('normal', parent=styles['Normal'], leading=14, alignment=TA_JUSTIFY)
code_style = ParagraphStyle('code', parent=styles['Code'], fontSize=8, leading=10.5, leftIndent=6)
small = ParagraphStyle('small', parent=styles['Normal'], fontSize=8.5, leading=11)
center = ParagraphStyle('center', parent=styles['Normal'], alignment=TA_CENTER, leading=16)
title_big = ParagraphStyle('title_big', parent=styles['Title'], alignment=TA_CENTER, fontSize=22, leading=26)
univ = ParagraphStyle('univ', parent=styles['Normal'], alignment=TA_CENTER, fontSize=13, leading=16)

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=1.8*cm, bottomMargin=1.8*cm,
                        leftMargin=2*cm, rightMargin=2*cm)
story = []
A = story.append

# ---------------- Caratula ----------------
A(Spacer(1, 1*cm))
A(Image(LOGO, width=5*cm, height=5*cm, kind='proportional'))
A(Spacer(1, 0.8*cm))
A(Paragraph("UNIVERSIDAD LA SALLE", univ))
A(Paragraph("FACULTAD DE INGENIERÍA Y ARQUITECTURA", univ))
A(Paragraph("CARRERA PROFESIONAL DE INGENIERÍA DE SOFTWARE", univ))
A(Spacer(1, 1*cm))
A(Paragraph("ACTIVIDAD 7", title_big))
A(Spacer(1, 0.3*cm))
A(Paragraph("Consultas avanzadas con SPARQL", center))
A(Spacer(1, 1*cm))
datos = [
    ["Apellidos y nombres:", "ROGER INFA SANCHEZ"],
    ["Curso:", "Web Semánticas y Ontologías"],
    ["Semestre:", "Octavo"],
    ["Docente:", "Josue Miguel Flores Parra"],
    ["Fecha:", "13-11-2026"],
]
td = Table(datos, colWidths=[5*cm, 8*cm])
td.setStyle(TableStyle([('ALIGN', (0,0), (0,-1), 'RIGHT'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 10)]))
A(td)
A(PageBreak())

# ---------------- Encabezado ----------------
A(Paragraph("Consultas avanzadas con SPARQL", title_s))
A(Spacer(1, 4))

def imagen_ajustada(path, ancho_cm):
    iw, ih = ImageReader(path).getSize()
    ancho = ancho_cm * cm
    return Image(path, width=ancho, height=ancho * ih / iw)

def ejercicio(titulo, archivo, imagen, explicacion, ancho_img=14, salto=True, extra=None):
    if salto:
        A(PageBreak())
    A(Paragraph(titulo, h1))
    A(Paragraph("Consulta ejecutada en Fuseki:", normal))
    A(Spacer(1, 3))
    A(Preformatted(open(archivo).read(), code_style))
    A(Spacer(1, 5))
    A(imagen_ajustada(imagen, ancho_img))
    A(Spacer(1, 5))
    for p in explicacion:
        A(Paragraph(p, normal))
        A(Spacer(1, 3))
    if extra:
        A(Paragraph(extra, small))
    A(Spacer(1, 6))

# ---------------- Ejercicio 1 ----------------
ejercicio(
    "Ejercicio 1. Agregaciones y agrupamiento",
    "actividades/actividad-7-sparql/consultas/ej1_agregacion.rq",
    f"{CAP}/ej1.png",
    [
        "Lo que hice fue agrupar los videojuegos por desarrollador con <b>GROUP BY</b> y contarlos con "
        "<b>COUNT(?videojuego)</b>. El conteo se guarda en <b>?totalVideojuegos</b> con AS, porque si no "
        "la columna sale con el nombre largo de la función.",
        "Para quedarme solo con los que tienen dos o más usé <b>HAVING (COUNT(?videojuego) &gt;= 2)</b>. "
        "Es importante que sea HAVING y no FILTER dentro del WHERE: el WHERE trabaja fila por fila antes de "
        "agrupar, y acá la condición depende del resultado del conteo, o sea, de cada grupo ya formado. "
        "Si lo pongo como FILTER el motor lo rechaza o no da el resultado esperado.",
        "El resultado es una sola fila: <b>Team Cherry con 2 videojuegos</b> (Hollow Knight y Hollow Knight: "
        "Silksong). Los demás desarrolladores (Nintendo, ConcernedApe, Maddy Makes Games, FromSoftware, "
        "CD Projekt Red y Toby Fox) tienen un solo juego cada uno, así que el HAVING los descarta. "
        "Justamente por eso la consulta devuelve 1 resultado y no 7.",
    ],
    ancho_img=15,
    salto=False,
)

# ---------------- Ejercicio 2 ----------------
ejercicio(
    "Ejercicio 2. Información opcional",
    "actividades/actividad-7-sparql/consultas/ej2_optional.rq",
    f"{CAP}/ej2.png",
    [
        "Acá el patrón del nombre es obligatorio, porque todo videojuego tiene nombre, pero la calificación "
        "va dentro de un <b>OPTIONAL</b>. Eso significa que si el juego no tiene calificación registrada, la "
        "consulta igual lo devuelve y la variable <b>?calificacion</b> queda sin valor (UNBOUND), que en la "
        "tabla se ve como la celda vacía.",
        "Se nota en el resultado: salen los 8 videojuegos, pero <b>Hollow Knight: Silksong</b> y "
        "<b>Undertale</b> aparecen sin calificación. Esos dos son los individuos a los que no se les cargó "
        "ese dato en el TTL, y el OPTIONAL justamente sirve para no perderlos.",
        "Si en vez de OPTIONAL hubiera puesto <b>:calificacion ?calificacion</b> como parte del patrón normal, "
        "esos dos juegos desaparecerían del resultado y solo vería 6 filas. Por eso el OPTIONAL es la forma "
        "correcta cuando el dato puede faltar.",
    ],
    ancho_img=13,
)

# ---------------- Ejercicio 3 ----------------
ejercicio(
    "Ejercicio 3. Consulta de existencia",
    "actividades/actividad-7-sparql/consultas/ej3_ask.rq",
    f"{CAP}/ej3.png",
    [
        "Con <b>ASK</b> no se piden filas, solo se pregunta si existe al menos una coincidencia. El patrón "
        "busca un videojuego con <b>:anioLanzamiento ?anio</b> y el <b>FILTER (?anio &gt; 2020)</b> deja pasar "
        "solo los años posteriores a 2020.",
        "El resultado es <b>true</b>, o sea que sí existe al menos un juego que cumple. En el conjunto de datos "
        "el caso es <b>Elden Ring</b>, lanzado en 2022. Cyberpunk 2077 es de 2020, así que no entra porque el "
        "filtro pide mayor estrictamente, no mayor o igual.",
        "Si ningún juego hubiera pasado el filtro, Fuseki devolvería <b>false</b>. La consulta termina en el "
        "primer testigo que encuentra, no necesita recorrer todo ni contar cuántos hay.",
        "<i>Nota: en la pestaña Table la UI de Fuseki 6 muestra un error al pintar resultados ASK, por eso la "
        "evidencia está tomada en la pestaña Response, donde se ve el JSON con \"boolean\": true.</i>",
    ],
    ancho_img=15,
)

# ---------------- Ejercicio 4 ----------------
ejercicio(
    "Ejercicio 4. Construcción de un nuevo grafo",
    "actividades/actividad-7-sparql/consultas/ej4_construct.rq",
    f"{CAP}/ej4.png",
    [
        "A diferencia de SELECT, <b>CONSTRUCT</b> devuelve triples, no una tabla. En la plantilla puse dos "
        "cosas por cada juego: su <b>:nombre</b> y una propiedad nueva, <b>:esRecomendado true</b>. Ese "
        "<i>true</i> se guarda como literal booleano (<b>\"true\"^^xsd:boolean</b>), que es como corresponde "
        "en RDF y no como el texto \"true\".",
        "El WHERE exige que el juego tenga calificación y el <b>FILTER (?calificacion &gt;= 8)</b> deja pasar "
        "a los de 8 a más. Son 6 juegos (Hollow Knight, Zelda BOTW, Stardew Valley, Celeste, Elden Ring y "
        "Cyberpunk 2077), y como cada uno genera 2 triples, el resultado tiene <b>12 triples</b>. Silksong y "
        "Undertale no aparecen porque no tienen calificación registrada, no porque su nota sea baja.",
        "Algo importante: <b>el grafo original no se modifica</b>. CONSTRUCT solo arma un grafo nuevo como "
        "resultado de la consulta, y ese resultado se ve en pantalla o se descarga, pero no se guarda en el "
        "dataset. Si quisiera dejarlo persistido tendría que hacer un INSERT con SPARQL Update. Por eso, si "
        "vuelvo a consultar :esRecomendado en el dataset, no va a existir todavía.",
    ],
    ancho_img=12.5,
)

doc.build(story)
print("PDF OK:", OUT)
