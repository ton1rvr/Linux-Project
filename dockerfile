# Utiliser une image CentOS de base
FROM centos:7

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires : jq, curl, bash et autres
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y jq curl bash && \
    yum clean all

# Copier les fichiers du projet dans le conteneur
COPY setup.sh get_current_movies.sh /app/

# Donner les permissions d'exécution aux scripts
RUN chmod +x /app/setup.sh /app/get_current_movies.sh

# Créer le dossier pour les données extraites
RUN mkdir -p /app/extracted_data

# Définir le script par défaut à exécuter lorsque le conteneur démarre
ENTRYPOINT ["/app/get_current_movies.sh"]
