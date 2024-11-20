#!/bin/bash

# Vérification des droits super-utilisateur
if [ "$EUID" -ne 0 ]; then
  echo "Veuillez exécuter ce script avec des droits super-utilisateur (sudo)."
  exit 1
fi

echo "Mise à jour des paquets..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  echo "Détection de macOS. Installation des dépendances avec Homebrew..."
  
  # Vérification si Homebrew est installé
  if ! command -v brew &> /dev/null; then
    echo "Homebrew n'est pas installé. Installation en cours..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi

  echo "Installation de jq et curl..."
  brew install jq curl

else
  # Linux
  echo "Détection de Linux. Installation des dépendances avec apt..."
  apt update
  apt install -y jq curl
fi

# Création d'un environnement pour les fichiers générés
OUTPUT_DIR="extracted_data"
if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Création du dossier '$OUTPUT_DIR'..."
  mkdir -p "$OUTPUT_DIR"
fi

# Vérification des installations
echo "Vérification des installations..."
if ! command -v jq &> /dev/null; then
  echo "jq n'a pas été installé correctement."
  exit 1
fi

if ! command -v curl &> /dev/null; then
  echo "curl n'a pas été installé correctement."
  exit 1
fi

echo "Toutes les dépendances sont installées et le système est prêt pour exécuter votre script."
