import streamlit as st
import pandas as pd
import json
import plotly.graph_objs as go

# Dossier contenant les fichiers JSON
DATA_DIR = "data"

# Options disponibles dans la barre latérale
symbols = ["AAPL", "MSFT", "TSLA"]
option = st.sidebar.selectbox("Select Dashboard", symbols)

st.header(f"{option} Dashboard")

# Chemin du fichier JSON pour le symbole sélectionné
file_path = f"{DATA_DIR}/{option}.json"

try:
    # Chargement des données depuis le fichier JSON
    with open(file_path, "r") as file:
        data = json.load(file)
    
    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df = df.rename(columns=lambda x: x.split(". ")[1])
    df.index.name = "Date"
    df.reset_index(inplace=True)  # Convertit l'index en colonne
    
    # Affichage du tableau
    st.write(df)
    
    # Création du graphique en chandeliers
    fig = go.Figure(data=[go.Candlestick(
        x=df["Date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )])
    st.write(fig)
    
except FileNotFoundError:
    st.error(f"Data for {option} not found. Please run the `fetch_data.sh` script.")
except KeyError:
    st.error("Unexpected data format in the JSON file.")
