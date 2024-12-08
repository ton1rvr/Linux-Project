# Utiliser une image Ubuntu comme base
FROM ubuntu:20.04

# Définir le répertoire de travail
WORKDIR /app

# Copier les scripts dans le conteneur
COPY . /app/

# Rendre les scripts exécutables
RUN chmod +x /app/setup.sh /app/extraction/fetch_data.sh /app/launch_app.sh

# Exécuter le script setup.sh pour l'installation
RUN /app/setup.sh

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Définir le point d'entrée
ENTRYPOINT ["/bin/bash", "-c", "/app/launch_app.sh"]
