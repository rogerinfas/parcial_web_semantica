"""P4-b/c: verifica inferencias esperadas con HermiT (sin modificar el OWL)."""
from owlready2 import *

onto = get_ontology("repositorio-universitario.owl").load()
P = onto.Publicacion
PD, PI = onto.PublicacionDigital, onto.PublicacionImpresa
PM = onto.PublicacionMultiautor
PPDF = onto.PublicacionDigitalPDF

print("== Tipos ASERTADOS (antes de HermiT) ==")
for i in onto.individuals():
    if isinstance(i, P):
        print(f"  {i.name}: {[c.name for c in i.is_a if isinstance(c, ThingClass)]}")

print("\n== Ejecutando HermiT ... ==")
sync_reasoner_hermit(infer_property_values=True)

print("\n== Tipos tras HermiT (asertado + INFERIDO) ==")
for i in onto.individuals():
    if isinstance(i, P):
        print(f"  {i.name}: {[c.name for c in i.is_a if isinstance(c, ThingClass)]}")

pub1 = onto.search_one(iri="*pub1_TesisIA")
pub2 = onto.search_one(iri="*pub2_ArticuloRedes")
print("\n== Comprobaciones P4 ==")
print("pub1 es PublicacionMultiautor (2 autores distintos)?", PM in pub1.is_a)
print("pub1 es PublicacionDigitalPDF (digital + PDF)?  ", PPDF in pub1.is_a)
print("pub2 es PublicacionMultiautor (1 solo autor)?   ", PM in pub2.is_a, "(esperado: False)")
print("pub2 es PublicacionDigitalPDF (es EPUB)?         ", PPDF in pub2.is_a, "(esperado: False)")
