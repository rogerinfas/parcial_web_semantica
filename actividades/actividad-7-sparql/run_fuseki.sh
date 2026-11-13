#!/usr/bin/env bash
# Levanta Fuseki y carga el dataset de la Actividad 7.
# Requiere Java 17+ y fuseki-server en el PATH (o ajustar FUSEKI_HOME).
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
FUSEKI_HOME="${FUSEKI_HOME:-$HOME/apache-jena-fuseki-6.2.0}"
PORT="${PORT:-3030}"

cd "$FUSEKI_HOME"
./fuseki-server --mem --update --port "$PORT" /ds > /tmp/fuseki-act7.log 2>&1 &
echo "Fuseki arrancando en http://localhost:$PORT (log: /tmp/fuseki-act7.log)"
sleep 8

curl -s -X POST -H "Content-Type: text/turtle" \
     --data-binary @"$DIR/dataset.ttl" \
     "http://localhost:$PORT/ds/data?default" -o /dev/null -w "dataset cargado: HTTP %{http_code}\n"

echo "UI: http://localhost:$PORT/#/dataset/ds/query"
