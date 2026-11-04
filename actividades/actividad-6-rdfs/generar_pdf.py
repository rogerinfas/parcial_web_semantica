from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, PageBreak, Image

OUT = "actividades/actividad-6-rdfs/ACTIVIDAD_6_RDFS_ROGER_INFA_SANCHEZ.pdf"
LOGO = "logo_web.png"

styles = getSampleStyleSheet()
title_s = styles['Title']
h1 = styles['Heading1']
h2 = styles['Heading2']
normal = styles['Normal']
normal.leading = 14
code_style = ParagraphStyle('code', parent=styles['Code'], fontSize=8, leading=10, leftIndent=6)
small = ParagraphStyle('small', parent=styles['Normal'], fontSize=9, leading=12)

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
story = []
A = story.append
center = ParagraphStyle('center', parent=styles['Normal'], alignment=TA_CENTER, leading=16)
title_big = ParagraphStyle('title_big', parent=styles['Title'], alignment=TA_CENTER, fontSize=22, leading=26)
univ = ParagraphStyle('univ', parent=styles['Normal'], alignment=TA_CENTER, fontSize=13, leading=16)

# ---- Caratula estilo parcial ----
A(Spacer(1, 1*cm))
try:
    A(Image(LOGO, width=5*cm, height=5*cm, kind='proportional'))
except Exception:
    pass
A(Spacer(1, 0.8*cm))
A(Paragraph("UNIVERSIDAD LA SALLE", univ))
A(Paragraph("FACULTAD DE INGENIERÍA Y ARQUITECTURA", univ))
A(Paragraph("CARRERA PROFESIONAL DE INGENIERÍA DE SOFTWARE", univ))
A(Spacer(1, 1*cm))
A(Paragraph("ACTIVIDAD 6", title_big))
A(Spacer(1, 0.3*cm))
A(Paragraph("Modelado e inferencia con RDF Schema (RDFS)<br/>Catálogo de videojuegos", center))
A(Spacer(1, 1*cm))
datos = [
    ["Apellidos y nombres:", "ROGER INFA SANCHEZ"],
    ["Curso:", "Web Semánticas y Ontologías"],
    ["Semestre:", "Octavo"],
    ["Docente:", "Josue Miguel Flores Parra"],
    ["Fecha:", "04-11-2026"],
]
td = Table(datos, colWidths=[5*cm, 8*cm])
td.setStyle(TableStyle([('ALIGN', (0,0), (0,-1), 'RIGHT'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('FONTSIZE', (0,0), (-1,-1), 10)]))
A(td)
A(PageBreak())

A(Paragraph("Modelado e inferencia con RDF Schema (RDFS)", title_s))
A(Spacer(1, 6))
info = [
    ["Apellidos y nombres", "ROGER INFA SANCHEZ"],
    ["Curso", "Web Semánticas y Ontologías"],
    ["Docente", "Josue Miguel Flores Parra"],
    ["Problema", "Catálogo de videojuegos"],
    ["Entrega", "catalogo.ttl + PDF"],
]
t = Table(info, colWidths=[4.5*cm, 10.5*cm])
t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, HexColor('#888888')), ('BACKGROUND', (0,0), (0,-1), HexColor('#eeeeee'))]))
A(t)
A(Spacer(1, 8))
A(Spacer(1, 6))

A(Paragraph("Parte 1. Clases y jerarquias", h1))
A(Paragraph("Aca declare 5 clases. La central es Videojuego y de ahi cuelgan VideojuegoIndependiente y VideojuegoDeEstrategia. Desarrollador y Genero las deje aparte porque no son juegos, son otra cosa. Al principio dude si Genero debia ser subclase de algo, pero no, va suelta.", normal))
A(Spacer(1,4))
A(Preformatted("""@prefix ex:   <http://example.org/videojuegos#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Videojuego a rdfs:Class .
ex:VideojuegoIndependiente a rdfs:Class ;
    rdfs:subClassOf ex:Videojuego .
ex:VideojuegoDeEstrategia a rdfs:Class ;
    rdfs:subClassOf ex:Videojuego .
ex:Desarrollador a rdfs:Class .
ex:Genero a rdfs:Class .""", code_style))
A(Spacer(1,4))
A(Paragraph("Yo lo entiendo asi: con <b>rdfs:subClassOf</b> digo que todo lo que sea Independiente tambien es Videojuego, es inclusion nomas. No es que sean lo mismo. Por eso funciona la regla <b>rdfs9</b>: si Stardew es Independiente, solito cae que tambien es Videojuego. Lo mismo con Age of Empires y Estrategia. Me sirvio pensarlo como los if de programacion: si eres de la hija, eres de la mama.", normal))

A(Paragraph("Parte 2. Propiedades, dominio y rango", h1))
A(Paragraph("Aca me confundia al inicio dominio con rango, asi que lo anote asi para no olvidarme: dominio = quien habla, rango = de quien se habla.", normal))
A(Preformatted("""ex:desarrolladoPor a rdf:Property ;
    rdfs:domain ex:Videojuego ;
    rdfs:range ex:Desarrollador .

ex:perteneceAGenero a rdf:Property ;
    rdfs:domain ex:Videojuego ;
    rdfs:range ex:Genero .""", code_style))
A(Spacer(1,4))
A(Paragraph("Con <b>desarrolladoPor</b> le digo que el sujeto tiene que ser un Videojuego (<b>rdfs2</b>) y el objeto un Desarrollador (<b>rdfs3</b>). O sea, si veo <b>X desarrolladoPor Y</b> ya se que X es juego e Y es desarrollador, aunque no lo haya escrito. Con <b>perteneceAGenero</b> igual: el sujeto es Videojuego y el objeto es Genero. En mi cabeza dominio y rango no prohiben nada, solo completan lo que falta.", normal))
A(Paragraph("Al inicio pense que si ponia mal un rango me iba a salir error, pero no. Despues entendi que RDFS solo suma tipos.", normal))

A(Paragraph("Parte 3. Individuos", h1))
A(Paragraph("A proposito solo puse el tipo de los dos juegos. A ConcernedApe, WorldsEdge, Simulacion y Estrategia no les puse tipo a mano, los deje sin tipar para que el razonador los saque por dominio y rango. Eso es lo que despues analizo en la Parte 4. Para los IRI tuve que quitar espacios y el apostrofe: use WorldsEdge y en el label puse \"World's Edge\" para que se lea bonito.", normal))
A(Spacer(1,4))
A(Preformatted("""ex:StardewValley a ex:VideojuegoIndependiente ;
    rdfs:label "Stardew Valley" ;
    ex:desarrolladoPor ex:ConcernedApe ;
    ex:perteneceAGenero ex:Simulacion .

ex:AgeOfEmpires a ex:VideojuegoDeEstrategia ;
    rdfs:label "Age of Empires" ;
    ex:desarrolladoPor ex:WorldsEdge ;
    ex:perteneceAGenero ex:Estrategia .

ex:ConcernedApe rdfs:label "ConcernedApe" .
ex:WorldsEdge rdfs:label "World's Edge" .
ex:Simulacion rdfs:label "Simulacion" .
ex:Estrategia rdfs:label "Estrategia" .""", code_style))
A(Spacer(1,4))
A(Paragraph("Con esto cubro lo que pedia el profe: los 2 tipos y las 6 relaciones. Lo corri en rdflib y me dio 39 triples tal cual, sin errores de sintaxis.", normal))

A(Paragraph("Parte 4. Inferencias", h1))
A(Paragraph("Aca use las tres reglas que vimos en clase: <b>rdfs9</b> para herencia, <b>rdfs2</b> para dominio y <b>rdfs3</b> para rango. Hice el cierre a mano con un script y pase de 39 a 45 triples, ahi vi clarito que era lo inferido.", normal))
rows = [
    ["Recurso", "Tipo inferido", "Explicito / inferido", "Justificacion"],
    ["Stardew\nValley", "Videojuego", "Inferido", "Yo no lo escribi. Sale por rdfs9 porque es Independiente y esa es hija de Videojuego. Tambien saldria por rdfs2."],
    ["Stardew\nValley", "Videojuego\nIndependiente", "Explicito", "Este si lo declare yo en la Parte 3."],
    ["Age of\nEmpires", "Videojuego", "Inferido", "Sale por rdfs9 porque es de Estrategia, que es subclase de Videojuego."],
    ["Age of\nEmpires", "VideojuegoDe\nEstrategia", "Explicito", "Declarado por mi, no es inferencia."],
    ["ConcernedApe", "Desarrollador", "Inferido", "Nunca lo tipé. Se infiere por rdfs3 porque aparece como objeto de desarrolladoPor."],
    ["World's Edge\n(WorldsEdge)", "Desarrollador", "Inferido", "Igual que el anterior, por rdfs3 del rango."],
    ["Simulacion", "Genero", "Inferido", "Por rdfs3, porque es objeto de perteneceAGenero."],
    ["Estrategia", "Genero", "Inferido", "Por rdfs3, igual que Simulacion."],
]
# wrap in Paragraphs
from reportlab.platypus import Paragraph as P
rows_p = [[P(c.replace("\n","<br/>"), small) for c in row] for row in rows]
tt = Table(rows_p, colWidths=[2.6*cm, 2.8*cm, 2.8*cm, 6.8*cm], repeatRows=1)
tt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,HexColor('#888888')),('BACKGROUND',(0,0),(-1,0),HexColor('#dddddd')),('VALIGN',(0,0),(-1,-1),'TOP')]))
A(tt)
A(Spacer(1,4))
A(Paragraph("Lo que me quedo claro es que los desarrolladores y generos sacan su tipo solo por inferencia, yo no los tipé. Y los juegos tienen doble camino para llegar a Videojuego, por la jerarquia y por el dominio, pero con uno basta.", normal))

A(Paragraph("Parte 5. Analisis conceptual", h1))
A(Paragraph("Esto me costo al inicio porque yo pensaba que si ponia dominio y rango el sistema me iba a botar error si me equivocaba, como una llave foranea en base de datos. Pero no, en RDFS es al reves: no valida, solo suma. Trabaja con mundo abierto, o sea, asume que lo que no sabe puede ser verdad y lo completa.", normal))
A(Paragraph("Un ejemplo que probe: si me equivoco y pongo <b>ex:StardewValley ex:desarrolladoPor ex:Simulacion</b>, o sea pongo un genero donde iba un desarrollador, RDFS no me dice nada. Lo que hace es inferir que <b>Simulacion tambien es Desarrollador</b> por el rango, y encima Stardew sigue siendo Videojuego por el dominio. Al final Simulacion queda con dos tipos a la vez y nadie reclama. Por eso para validar de verdad habria que usar SHACL o ShEx, que esos si revisan y avisan.", normal))
A(Spacer(1,6))
A(Paragraph("Todo el codigo esta en catalogo.ttl y lo verifique con rdflib. Me dio 39 triples escritos por mi y 45 con inferencias.", small))

doc.build(story)
print("PDF OK:", OUT)
