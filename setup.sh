#!/bin/bash

# Détecter le système d'exploitation
OS="$(uname -s)"

# Fonction pour installer les dépendances sur Linux
install_on_linux() {
    echo "Détection de Linux..."
    apt-get update -y && \
    apt-get install -y python3-pip curl bash && \
    apt-get clean
}

# Fonction pour installer les dépendances sur macOS
install_on_macos() {
    echo "Détection de macOS..."
    # Vérifier si Homebrew est installé
    if ! command -v brew &> /dev/null; then
        echo "Homebrew n'est pas installé. Installation..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew update && \
    brew install python3 curl bash
}

# Installation en fonction de l'OS
case "$OS" in
    Linux*)     install_on_linux ;;
    Darwin*)    install_on_macos ;;
    *)          echo "Système d'exploitation non supporté : $OS" && exit 1 ;;
esac

# Installer Streamlit
echo "Installation de Streamlit..."
pip3 install streamlit pandas plotly
