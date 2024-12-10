import streamlit as st
import pandas as pd
import json
import plotly.graph_objs as go

# Dossier contenant les fichiers JSON
DATA_DIR = "data"

# Options disponibles dans la barre latérale
st.sidebar.title("Stock Dashboard")
symbols = ["AAPL", "MSFT", "TSLA"]
option = st.sidebar.selectbox("Select Stock Symbol", symbols,
help="“A ticker is a unique symbol used to identify a stock.”")

# Dictionnaire des URLs ou des chemins vers les images
logos = {
    "AAPL": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "MSFT": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
    "TSLA": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Tesla_Motors.svg"
}

if option in logos:
    title_with_logo = f"""
    <div style="display: flex; align-items: center;">
        <img src="{logos[option]}" alt="{option} logo" style="width:40px; margin-right:10px;">
        <h1 style="margin: 0;">{option} Dashboard</h1>
    </div>
    """
    st.markdown(title_with_logo, unsafe_allow_html=True)

st.write("Explore daily stock data with an interactive chart and detailed table.")

# Chemin du fichier JSON pour le symbole sélectionné
file_path = f"{DATA_DIR}/{option}.json"

try:
    # Chargement des données depuis le fichier JSON
    with open(file_path, "r") as file:
        data = json.load(file)

    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df = df.rename(columns=lambda x: x.split(". ")[1])  # Simplification des noms de colonnes
    df.index.name = "Date"
    df.reset_index(inplace=True)  # Convertit l'index en colonne
    df["Date"] = pd.to_datetime(df["Date"])  # Conversion en datetime
    df = df.sort_values("Date")  # Tri par date ascendante
    df = df.rename(columns=str.capitalize)  # Capitaliser les colonnes pour un affichage cohérent

    # Conversion explicite des colonnes nécessaires en float
    numeric_columns = ["Open", "High", "Low", "Close"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Conversion avec gestion des erreurs

    # Vérification des données invalides
    if df[numeric_columns].isnull().values.any():
        st.warning("Some rows contain invalid data and have been excluded from calculations.")
        df = df.dropna(subset=numeric_columns)

    # Ajout d'une sélection de plage de dates
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )
    # Ajouter un GIF personnalisé dans la sidebar (version grande taille)
    gif_html = """
    💻 Powered by Linux</p>
    </div>
    """

    st.sidebar.markdown(gif_html, unsafe_allow_html=True)
    # Filtrage des données selon la plage de dates
    filtered_df = df[(df["Date"] >= pd.Timestamp(start_date)) & (df["Date"] <= pd.Timestamp(end_date))]

    # Affichage d'un résumé des données
    st.subheader("Stock Data Table")
    st.dataframe(filtered_df, use_container_width=True)  # Meilleur affichage du tableau

    # Calcul des variations journalières
    filtered_df["Daily Change"] = filtered_df["Close"] - filtered_df["Open"]
    filtered_df["Change (%)"] = (filtered_df["Daily Change"] / filtered_df["Open"]) * 100

    # Création du graphique en chandeliers avec Plotly
    st.subheader("Interactive Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=filtered_df["Date"],
        open=filtered_df["Open"],
        high=filtered_df["High"],
        low=filtered_df["Low"],
        close=filtered_df["Close"],
        increasing_line_color='green', decreasing_line_color='red',
    )])
    fig.update_layout(
        title=f"Candlestick Chart for {option}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        xaxis_rangeslider_visible=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Ajout d'une section pour les statistiques
    st.subheader("Stock Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Price", f"${filtered_df['High'].max():.2f}")
    col2.metric("Lowest Price", f"${filtered_df['Low'].min():.2f}")
    col3.metric("Average Close", f"${filtered_df['Close'].mean():.2f}")

except FileNotFoundError:
    st.error(f"Data for {option} not found. Please run the `fetch_data.sh` script.")
except KeyError as e:
    st.error(f"Unexpected data format in the JSON file: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")