#!/bin/bash

# Fichier de lancement global pour l'extraction des données et démarrage de l'interface Streamlit

# Donner les permissions d'exécution au script d'extraction
chmod +x extraction/fetch_data.sh

# Lancer l'extraction des données
echo "Lancement de l'extraction des données..."
extraction/fetch_data.sh
if [ $? -ne 0 ]; then
  echo "Erreur lors de l'extraction des données."
  exit 1
fi
echo "Extraction des données terminée avec succès."

# Lancer Streamlit
echo "Démarrage de l'interface Streamlit..."
streamlit run streamlit/app.py
