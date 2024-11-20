#!/bin/bash

# Définir les variables pour la requête API
MIN_RELEASE_DATE="2024-09-01"
MAX_RELEASE_DATE="2024-12-31"
URL="https://api.themoviedb.org/3/discover/movie"
API_KEY="Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1N2U1MTYyYTU1ZTgyMDBmY2M0MzczYjhlNDhiM2YyZSIsIm5iZiI6MTczMjAzMjc2Ni41NDg0MTc2LCJzdWIiOiI2NTRhYjgzMDYzMzJmNzAwYzYzN2IwYjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.zMGN5nfBXnE78dm_-3qD99C7FUkBnksqaBCtKXrKLc8"

# Effectuer la requête API
response=$(curl -s -X GET "$URL" \
-H "Authorization: $API_KEY" \
-H "accept: application/json" \
-G \
--data-urlencode "primary_release_date.gte=$MIN_RELEASE_DATE" \
--data-urlencode "primary_release_date.lte=$MAX_RELEASE_DATE")

if [ $? -eq 0 ]; then
  # Sauvegarder la réponse dans movies.json
  echo "$response" > movies.json
  echo "Les données ont été enregistrées dans movies.json."
  
  # Appeler le script Python pour traiter les données
  python3 dataprocess.py movies.json
else
  echo "La requête API a échoué."
fi

