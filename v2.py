import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
from arch import arch_model

# --- Titre de l'application
st.title("Simulation de portefeuille boursier avec Monte Carlo")

# --- Entrées de l'utilisateur
st.sidebar.header("Paramètres de la simulation")

# --- Choix des tickers avec explication
tickers = st.sidebar.text_input(
    "Entrez les tickers des actions (séparés par des virgules)",
    value="",
    help="Un ticker est un symbole unique utilisé pour identifier une action. Par exemple, BNP Paribas : 'BNP.PA'."
)
stockList = [ticker.strip() for ticker in tickers.split(',') if ticker.strip()]

# --- Paramètres de la simulation
initial_investment = st.sidebar.number_input(
    "Montant de l'investissement initial (€)",
    min_value=1000,
    value=10000,
    step=1000
)
T = st.sidebar.number_input("Nombre de jours de simulation", min_value=22, max_value=365, value=22, step=10)
mc_sims = st.sidebar.number_input("Nombre de simulations Monte Carlo", min_value=100, max_value=5000, value=500, step=100)

# --- Période d'observation historique
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=1000)

# --- Fonction pour importer les données de prix
@st.cache_data
def get_data(stocks, start, end):
    stockData = yf.download(stocks, start, end)['Close']
    returns = stockData.pct_change().dropna()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix, returns

# --- Vérification des tickers
if stockList:
    meanReturns, covMatrix, returns = get_data(stockList, startDate, endDate)

    # --- Calcul de la volatilité par le modèle GARCH
    garch_vol = {}
    for stock in stockList:
        try:
            model = arch_model(returns[stock].dropna() * 100, vol='Garch', p=1, q=1)
            res = model.fit(disp='off')
            garch_vol[stock] = res.conditional_volatility.iloc[-1] / 100  # On normalise la volatilité
        except Exception as e:
            st.warning(f"Erreur avec le GARCH pour {stock}: {e}")

    # --- Pondération initiale (également modifiable par l'utilisateur)
    weights = np.array([1 / len(stockList)] * len(stockList))  # Pondération égale

    # --- Simulation Monte Carlo
    np.random.seed(42)
    meanM = np.tile(meanReturns.values.reshape(-1, 1), T)  # (n, T)
    portfolio_sims = np.zeros((T, mc_sims))  # Matrice de simulation (T, M)

    L = np.linalg.cholesky(covMatrix)  # Décomposition de Cholesky
    for m in range(mc_sims):
        Z = np.random.normal(size=(len(stockList), T))  # Variables normales indépendantes (n, T)
        dailyReturns = meanM + (L @ Z)  # On applique la corrélation (n, T)
        portfolio_sims[:, m] = np.cumprod(np.dot(weights, dailyReturns) + 1) * initial_investment

    # --- Calcul des statistiques sur les valeurs finales
    final_values = portfolio_sims[-1, :]
    mean_value = np.mean(final_values)
    max_value = np.max(final_values)
    min_value = np.min(final_values)
    profit_probability = np.sum(final_values > initial_investment) / mc_sims

    # --- Affichage des résultats numériques
    st.write("### Résultats de la simulation")
    st.write(f"**Valeur moyenne du portefeuille : {mean_value:.2f} €**")
    st.write(f"**Valeur maximale atteinte : {max_value:.2f} €**")
    st.write(f"**Valeur minimale atteinte : {min_value:.2f} €**")
    st.write(f"**Probabilité de profit (> {initial_investment} €) : {profit_probability:.2%}**")

    # --- Ajout d'un graphique pour le rendement
    portfolio_returns = (final_values - initial_investment) / initial_investment * 100
    st.write("### Distribution des rendements")
    plt.figure(figsize=(10, 6))
    plt.hist(portfolio_returns, bins=30, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel("Rendement (%)")
    plt.ylabel("Fréquence")
    plt.title("Distribution des rendements du portefeuille")
    st.pyplot(plt)

    # --- Affichage du graphique Monte Carlo
    st.write("### Simulation Monte Carlo")
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_sims)
    plt.ylabel('Valeur du portefeuille (€)')
    plt.xlabel('Jours')
    plt.title('Simulation Monte Carlo du portefeuille')
    st.pyplot(plt)

    # --- Affichage de la volatilité
    st.write("### Analyse de la Volatilité")

    # Préparation des données pour l'affichage
    vol_df = pd.DataFrame({
        'Ticker': garch_vol.keys(),
        'Volatilité GARCH (%)': [v * 100 for v in garch_vol.values()]
    })

    # Afficher le tableau des volatilités
    st.write("#### Volatilité GARCH estimée par action")
    st.dataframe(vol_df)

    st.write(
        """
        **La volatilité** mesure les fluctuations des prix des actions sur une période donnée.
        Une volatilité plus élevée indique un risque et une incertitude plus importants.
        """
    )
