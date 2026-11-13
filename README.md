# Web Semánticas y Ontologías — ROGER INFA SANCHEZ

Carpeta del curso. El parcial y las tareas van separados.

## Estructura

```
.
├── logo_web.png                # logo compartido (carátulas)
├── parcial/                    # EXAMEN PARCIAL (no tocar salvo corrección)
│   ├── INFORME_PARCIAL_ROGER_INFA_SANCHEZ.pdf / .tex / .md
│   ├── body.tex
│   ├── Roger.owl
│   ├── capturas/p4_*.png
│   ├── actual/
│   ├── DOC_PASO_2/ , DOC_PASO_5/
│   ├── indicaciones_clasroom.md
│   └── build_ontology.py, verificar_inferencias.py, demo_inconsistencia.py, run_evidencias.sh
└── actividades/
    ├── actividad-6-rdfs/        # Actividad 6 — RDFS catálogo videojuegos
    │   ├── catalogo.ttl
    │   ├── ACTIVIDAD_6_RDFS_ROGER_INFA_SANCHEZ.pdf
    │   └── generar_pdf.py
    └── actividad-7-sparql/      # Actividad 7 — SPARQL avanzado
        ├── dataset.ttl
        ├── consultas/           # ej1..ej4 (.rq)
        ├── capturas/            # evidencias de Fuseki
        ├── ACTIVIDAD_7_SPARQL_ROGER_INFA_SANCHEZ.pdf
        ├── capturar.py
        ├── generar_pdf.py
        └── run_fuseki.sh
```

## Actividades

Cada tarea nueva va en `actividades/actividad-N-nombre/` con su propio `.ttl` + `.pdf` + script si aplica.
No mezclar con `parcial/`.
