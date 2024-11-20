# Utiliser une image Ubuntu comme base
FROM ubuntu:20.04

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y jq curl bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier les scripts dans le conteneur
COPY setup.sh get_current_movies.sh /app/

# Rendre les scripts exécutables
RUN chmod +x /app/setup.sh /app/get_current_movies.sh

# Créer le répertoire pour les fichiers générés
RUN mkdir -p /app/extracted_data

# Définir le point d'entrée
ENTRYPOINT ["/app/get_current_movies.sh"]
