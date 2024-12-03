# Utiliser une image Ubuntu comme base
FROM ubuntu:20.04

# Définir le répertoire de travail
WORKDIR /app

# Copier les scripts dans le conteneur
COPY setup.sh extraction launch_app.sh streamlit/app.py /app/

# Rendre les scripts exécutables
RUN chmod +x /app/setup.sh /app/extraction/fetch_data.sh /app/launch_app.sh

# Exécuter le script setup.sh pour l'installation
RUN /app/setup.sh

# Créer le répertoire pour les fichiers générés
RUN mkdir -p /app/data

# Définir le point d'entrée
ENTRYPOINT ["/bin/bash", "-c", "/app/launch_app.sh"]
