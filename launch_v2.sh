#!/bin/bash

# Vérifie si Streamlit est installé
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit n'est pas installé. Installation en cours..."
    pip install streamlit
fi

# Vérifie si le module 'arch' est installé
if ! python3 -c "import arch" &> /dev/null
then
    echo "Le module 'arch' n'est pas installé. Installation en cours..."
    pip install arch
fi

# Définir le chemin du script Streamlit
APP_PATH="./streamlit/app_v2.py"

# Vérifie si le fichier existe
if [ -f "$APP_PATH" ]; then
    echo "Lancement de l'application Streamlit..."
    # Lancer l'application Streamlit
    streamlit run "$APP_PATH"
else
    echo "Erreur : Le fichier $APP_PATH est introuvable."
    exit 1
fi
