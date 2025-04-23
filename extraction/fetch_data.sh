#!/bin/bash

# Vérifie que la clé API est définie
if [ -z "$API_KEY" ]; then
  echo "Erreur : la variable API_KEY n'est pas définie."
  exit 1
fi

# Liste des symboles à récupérer
SYMBOLS=("AAPL" "MSFT" "TSLA")

# Dossier de sortie pour les fichiers JSON
OUTPUT_DIR="data"
mkdir -p "$OUTPUT_DIR"

# Récupération des données pour chaque symbole
for SYMBOL in "${SYMBOLS[@]}"
do
  echo "Fetching data for $SYMBOL..."
  URL="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=$SYMBOL&apikey=$API_KEY"
  curl -s "$URL" -o "$OUTPUT_DIR/$SYMBOL.json"
done

echo "Data fetched and saved in $OUTPUT_DIR."
