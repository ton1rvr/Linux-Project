#!/bin/bash

# Arrêter tous les conteneurs utilisant l'image my_app
docker ps -q --filter "ancestor=my_app" | while read container_id; do
    echo "Stopping container $container_id using image my_app..."
    docker stop "$container_id"
    echo "Removing container $container_id..."
    docker rm "$container_id"
done

# Supprimer l'image my_app
echo "Removing image my_app..."
docker rmi my_app

echo "All containers using 'my_app' have been stopped and removed, and the image has been deleted."
