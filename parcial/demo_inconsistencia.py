"""P4-d: prueba de incompatibilidad Digital vs Impresa con HermiT."""
from owlready2 import *
from owlready2.base import OwlReadyInconsistentOntologyException

onto = get_ontology("repositorio-universitario.owl").load()
pub3 = onto.search_one(iri="*pub3_LibroHistoria")
print("Tipos iniciales de pub3:", [c.name for c in pub3.is_a if isinstance(c, ThingClass)])
print("Disjuncion declarada: PublicacionDigital DisjointWith PublicacionImpresa")

print("\n-- Asignando pub3 tambien a PublicacionDigital ... --")
pub3.is_a.append(onto.PublicacionDigital)
print("Tipos ahora:", [c.name for c in pub3.is_a if isinstance(c, ThingClass)])
print("\n== Ejecutando HermiT ... ==")
try:
    sync_reasoner_hermit(infer_property_values=True)
    print("HermiT NO reporto error (inesperado).")
except OwlReadyInconsistentOntologyException:
    print("RESULTADO: ONTOLOGIA INCONSISTENTE (HermiT lanza")
    print("OwlReadyInconsistentOntologyException).")
    print("Explicacion: pub3 pertenece a dos clases disjuntas a la vez,")
    print("lo cual es logicamente imposible; HermiT lo detecta y se niega")
    print("a razonar hasta corregir el modelo.")
