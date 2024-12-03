#!/bin/bash

# Mettre à jour les dépôts et installer les dépendances
apt-get update -y && \
apt-get install -yl python3-pip curl bash && \
apt-get clean

# Installer Streamlit
pip install streamlit
