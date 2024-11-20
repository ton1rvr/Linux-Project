# Utiliser une image Ubuntu comme base
FROM ubuntu:20.04

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip jq curl bash && \
    apt-get clean

# Installer Streamlit via pip
RUN pip3 install streamlit

# Copier les scripts dans le conteneur
COPY setup.sh get_current_movies.sh launch_app.sh dataprocess.py /app/

# Rendre les scripts exécutables
RUN chmod +x /app/setup.sh /app/get_current_movies.sh launch_app.sh

# Créer le répertoire pour les fichiers générés
RUN mkdir -p /app/extracted_data

# Définir le point d'entrée
ENTRYPOINT ["/bin/bash", "-c", "/app/get_current_movies.sh && /app/launch_app.sh"]
