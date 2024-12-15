# Application Streamlit

Ce projet permet de lancer une application Streamlit avec différentes versions de l'application. Suivez les étapes ci-dessous pour exécuter l'application et accéder à l'interface graphique.

## Prérequis

Avant de lancer l'application, assurez-vous d'avoir Docker installé sur votre machine. Si vous n'avez pas Docker, vous pouvez le télécharger et l'installer depuis [le site officiel de Docker](https://www.docker.com/get-started).

## Lancer l'application

Pour lancer l'application, vous devez exécuter le script `launch_all.sh` avec un argument correspondant à la version de l'application que vous souhaitez utiliser.

1. **Cloner ce dépôt (si ce n'est pas déjà fait) :**
   
   ```bash
   git clone https://github.com/morganjowitt/linux-project.git
   cd <nom_du_dossier_du_repertoire>
    ```

2. **Cloner ce dépôt (si ce n'est pas déjà fait) :**
    Exécutez le script launch_all.sh pour démarrer l'application. Spécifiez la version de l'application souhaitée en passant 1 ou 2 comme argument.

    - **Pour lancer la version 1** :
    
        ```bash
        sh launch_all.sh 1
         ```

    - **Pour lancer la version 2** :
    
        ```bash
        sh launch_all.sh 2
         ```

3. **Accéder à l'interface graphique :**
    Une fois l'application démarrée, ouvrez un navigateur web et accédez à l'adresse suivante pour utiliser l'interface graphique : http://23.100.8.30:5005/

4. **Fin de l'utilisation / Changement de version de l'app:**
    Une fois l'application utilisé pour utiliser une autre version ou tout simplement l'arrêter executez ce script :
    ```bash
        sh stop_all.sh
     ```
