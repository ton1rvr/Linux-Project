#!/bin/bash

MIN_DATE="2024-01-01"
MAX_DATE="2024-12-31"
BASE_URL="https://api.themoviedb.org/3/discover/movie"
INCLUDE_ADULT="false"
INCLUDE_VIDEO="false"
LANGUAGE="en-US"
TOTAL_PAGES=5
SORT_BY="popularity.desc"
WITH_RELEASE_TYPE="2|3"
OUTPUT_FILE="extracted_data/all_movies.json"
API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1N2U1MTYyYTU1ZTgyMDBmY2M0MzczYjhlNDhiM2YyZSIsIm5iZiI6MTczMjA5MTUxOC40NDQyNTQ0LCJzdWIiOiI2NTRhYjgzMDYzMzJmNzAwYzYzN2IwYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CycVLVOVr4AkJjX58Jbb6el4JIb8rC89yBsdhmOtHpc"

# Initialiser le fichier de sortie
mkdir -p "$(dirname "$OUTPUT_FILE")"
echo "[]" > "$OUTPUT_FILE"

for PAGE in $(seq 1 "$TOTAL_PAGES"); do
  FULL_URL="${BASE_URL}?include_adult=${INCLUDE_ADULT}&include_video=${INCLUDE_VIDEO}&language=${LANGUAGE}&page=${PAGE}&sort_by=${SORT_BY}&with_release_type=${WITH_RELEASE_TYPE}&release_date.gte=${MIN_DATE}&release_date.lte=${MAX_DATE}"

  RESPONSE=$(curl --silent --request GET \
  --url "$FULL_URL" \
  --header "Authorization: Bearer $API_KEY" \
  --header "accept: application/json")

  if [ -z "$RESPONSE" ]; then
    echo "Erreur : aucune réponse de l'API pour la page $PAGE."
    continue
  fi

  # Tenter d'utiliser jq, sinon utiliser Python
  if command -v jq &> /dev/null; then
    echo "Utilisation de jq pour traiter la réponse JSON."
    MOVIE_RESULTS=$(echo "$RESPONSE" | jq '.results')

    jq -s '.[0] + .[1]' "$OUTPUT_FILE" <(echo "$MOVIE_RESULTS") > tmp.json && mv tmp.json "$OUTPUT_FILE"

  else
    echo "jq non trouvé. Utilisation de Python pour traiter la réponse JSON."
    
    python3 - <<END
import json

# Charger la réponse JSON actuelle
new_data = json.loads('''$RESPONSE''')

# Charger les données existantes depuis le fichier
try:
    with open("$OUTPUT_FILE", "r") as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

# Ajouter les résultats de la nouvelle page aux données existantes
existing_data.extend(new_data["results"])

# Sauvegarder les données mises à jour dans le fichier de sortie
with open("$OUTPUT_FILE", "w") as f:
    json.dump(existing_data, f, indent=4)

print(f"Page {PAGE} traitée et ajoutée au fichier $OUTPUT_FILE.")
END
  fi

  echo "Page $PAGE traitée et ajoutée au fichier $OUTPUT_FILE."
done

echo "Traitement terminé. Les données sont disponibles dans : $OUTPUT_FILE."
