"""Construye repositorio-universitario.owl desde cero (P4)."""
from owlready2 import *

onto = get_ontology("http://example.org/repositorio-universitario#")

with onto:
    class Publicacion(Thing): pass
    class PublicacionDigital(Publicacion): pass
    class PublicacionImpresa(Publicacion): pass
    class PublicacionMultiautor(Publicacion): pass
    class PublicacionDigitalPDF(PublicacionDigital): pass  # se redefine como equivalente abajo
    class Autor(Thing): pass
    class Formato(Thing): pass
    class Licencia(Thing): pass
    class LicenciaAbierta(Licencia): pass

    class escritoPor(ObjectProperty):
        domain = [Publicacion]
        range = [Autor]
    class disponibleEn(ObjectProperty):
        domain = [Publicacion]
        range = [Formato]
    class tieneLicencia(ObjectProperty):
        domain = [Publicacion]
        range = [Licencia]
    class titulo(DataProperty):
        domain = [Publicacion]
        range = [str]

    # Disjuncion exigida
    AllDisjoint([PublicacionDigital, PublicacionImpresa])

    # Clases definidas (necesarias y suficientes -> inferencia automatica)
    PublicacionMultiautor.equivalent_to = [Publicacion & (escritoPor.min(2, Autor))]
    # digital disponible en PDF (hasValue sobre el individuo formatoPDF, creado mas abajo)
    # se asigna despues de crear formatoPDF

    # Restricciones de coherencia
    Publicacion.is_a.append(escritoPor.some(Autor))
    Publicacion.is_a.append(disponibleEn.some(Formato))

    # Individuos de apoyo
    formatoPDF = Formato("formatoPDF")
    formatoEPUB = Formato("formatoEPUB")
    formatoTapaBlanda = Formato("formatoTapaBlanda")

    autor1 = Autor("autor1")
    autor2 = Autor("autor2")
    autor3 = Autor("autor3")
    AllDifferent([autor1, autor2, autor3])

    licCC = LicenciaAbierta("licCC_BY")

    # Individuos de prueba
    pub1 = PublicacionDigital("pub1_TesisIA")
    pub1.titulo = ["Tesis de IA aplicada"]
    pub1.escritoPor = [autor1, autor2]
    pub1.disponibleEn = [formatoPDF]
    pub1.tieneLicencia = [licCC]

    pub2 = PublicacionDigital("pub2_ArticuloRedes")
    pub2.titulo = ["Articulo de redes"]
    pub2.escritoPor = [autor1]
    pub2.disponibleEn = [formatoEPUB]

    pub3 = PublicacionImpresa("pub3_LibroHistoria")
    pub3.titulo = ["Libro de historia regional"]
    pub3.escritoPor = [autor3]
    pub3.disponibleEn = [formatoTapaBlanda]

    # Definicion pendiente (requiere formatoPDF ya creado)
    PublicacionDigitalPDF.equivalent_to = [PublicacionDigital & (disponibleEn.value(formatoPDF))]

onto.save(file="repositorio-universitario.owl", format="rdfxml")
print("OWL guardado: repositorio-universitario.owl")

# --- Verificacion con HermiT ---
print("Sincronizando razonador HermiT...")
sync_reasoner_hermit(infer_property_values=True)
print("--- Tipos inferidos ---")
for pub in [pub1, pub2, pub3]:
    print(pub.name, "->", sorted(c.name for c in pub.is_a if isinstance(c, ThingClass)))
print("--- pub1 es Multiautor?", PublicacionMultiautor in pub1.is_a)
print("--- pub1 es DigitalPDF?", PublicacionDigitalPDF in pub1.is_a)
print("--- pub2 es Multiautor?", PublicacionMultiautor in pub2.is_a)
print("--- Inconsistente?", onto.inconsistent if hasattr(onto, 'inconsistent') else 'n/a')
onto.save(file="repositorio-universitario.owl", format="rdfxml")
print("OK")
