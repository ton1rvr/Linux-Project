#!/bin/bash

MIN_DATE="2024-01-01"
MAX_DATE="2024-12-31" 
BASE_URL="https://api.themoviedb.org/3/discover/movie"
INCLUDE_ADULT="false"
INCLUDE_VIDEO="false"
LANGUAGE="en-US"
PAGE=2
SORT_BY="popularity.desc"
WITH_RELEASE_TYPE="2|3"
API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1N2U1MTYyYTU1ZTgyMDBmY2M0MzczYjhlNDhiM2YyZSIsIm5iZiI6MTczMjA5MTUxOC40NDQyNTQ0LCJzdWIiOiI2NTRhYjgzMDYzMzJmNzAwYzYzN2IwYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CycVLVOVr4AkJjX58Jbb6el4JIb8rC89yBsdhmOtHpc"

FULL_URL="${BASE_URL}?include_adult=${INCLUDE_ADULT}&include_video=${INCLUDE_VIDEO}&language=${LANGUAGE}&page=${PAGE}&sort_by=${SORT_BY}&with_release_type=${WITH_RELEASE_TYPE}&release_date.gte=${MIN_DATE}&release_date.lte=${MAX_DATE}"

RESPONSE=$(curl --silent --request GET \
  --url "$FULL_URL" \
  --header "Authorization: Bearer $API_KEY" \
  --header "accept: application/json")

if [ -z "$RESPONSE" ]; then
  echo "Erreur : aucune réponse de l'API."
  exit 1
fi

echo "Réponse de l'API :"
echo "$RESPONSE"

MOVIE_TITLE=$(echo "$RESPONSE" | jq -r '.results[0].title')
echo "Le film le plus populaire dans cette période est : $MOVIE_TITLE"

if [ $? -eq 0 ]; then

  echo "$RESPONSE" > extracted_data/movies.json
  echo "Les données ont été enregistrées dans movies.json."
  
  streamlit run dataprocess.py
else
  echo "La requête API a échoué."
fi

