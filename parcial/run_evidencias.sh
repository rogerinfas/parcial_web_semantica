#!/bin/bash
# Evidencias P4 con HermiT (mismo motor que usa Protege). Pausas para captura.
H=/usr/lib/python3.14/site-packages/owlready2/hermit/HermiT.jar
cd /home/roger/Proyectos/personal/parcial_web_semantica
clear
echo "================================================================"
echo " P4-c: HermiT -k (consistencia) sobre repositorio-universitario.owl"
echo "================================================================"
java -cp "$H" org.semanticweb.HermiT.cli.CommandLine -k repositorio-universitario.owl 2>&1 | head -12
echo
echo ">>> Ontologia CONSISTENTE. Ahora las inferencias con owlready2+HermiT:"
python3 verificar_inferencias.py 2>&1 | grep -v "Deprecat\|Hermit took\|java -Xmx"
echo
echo "================================================================"
echo " P4-d: HermiT -k (consistencia) sobre repositorio-INCONSISTENTE.owl"
echo " (pub3_LibroHistoria tipado como Digital E Impresa, disjuntas)"
echo "================================================================"
java -cp "$H" org.semanticweb.HermiT.cli.CommandLine -k /tmp/repositorio-inconsistente.owl 2>&1 | head -25
echo
echo ">>> FIN DE EVIDENCIAS (dejar ventana abierta para captura)"
sleep 1000
