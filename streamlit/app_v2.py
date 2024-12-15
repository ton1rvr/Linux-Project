import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
from arch import arch_model

# Set page configuration
st.set_page_config(
    page_title="Invest Vision",
    page_icon="📈"
)

# Custom CSS for improved aesthetics
st.markdown("""
    <style>
    /* Sidebar styling */
    .css-1aumxhk {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Titre de l'application
st.title("Monte Carlo Stock Portfolio Simulation")
st.markdown("This application allows you to simulate the evolution of a stock portfolio based on Monte Carlo simulations.")

# --- Simulation Parameters in Sidebar
st.sidebar.header("📊 Simulation Parameters")

@st.cache_data
def get_all_tickers():
    """
    Fetches a comprehensive list of tickers available from Yahoo Finance.
    For demonstration purposes, we're using S&P 500 tickers via wikepedia list.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500 = pd.read_html(url)[0]
    tickers = sp500['Symbol'].tolist()
    return tickers

def get_ticker_info(ticker):
    """
    Fetch brief information about a stock ticker using yfinance.
    Returns a dictionary containing the company's name, sector, industry,
    and annual revenue for 2023 and 2022 if available.
    """
    def format_revenue(value):
        """Format revenue into billions or millions."""
        try:
            value = float(value)
            if value >= 1e9:
                return f"{value / 1e9:.2f} B$"  # En milliards
            elif value >= 1e6:
                return f"{value / 1e6:.2f} M$"  # En millions
            else:
                return f"{value:.2f} $"  # Pas d'échelle
        except (ValueError, TypeError):
            return "N/A"
        
    try:
        ticker_obj = yf.Ticker(ticker)
        ticker_info = ticker_obj.info

        # Récupération des revenus
        financials = ticker_obj.financials  # Récupère les états financiers
        revenue_2023 = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else "N/A"
        revenue_2022 = financials.loc['Total Revenue'].iloc[1] if 'Total Revenue' in financials.index else "N/A"

        if revenue_2022 and revenue_2023:
            sales_ratio = (revenue_2023 -revenue_2022) / revenue_2022
        else:
            sales_ratio = None

        revenue_2023_formatted = format_revenue(revenue_2023)
        revenue_2022_formatted = format_revenue(revenue_2022)

        return {
            "name": ticker_info.get("longName", "Unknown"),
            "sector": ticker_info.get("sector", "Unknown"),
            "industry": ticker_info.get("industry", "Unknown"),
            "revenue_2023": revenue_2023_formatted,
            "revenue_2022": revenue_2022_formatted,
            "sales_ratio": f"{sales_ratio * 100:.2f}%" if sales_ratio else "N/A" 
        }
    except Exception as e:
        return {
            "name": "Unknown",
            "sector": "Unknown",
            "industry": "Unknown",
            "revenue_2023": "N/A",
            "revenue_2022": "N/A"
        }
# Chargement des tickers
all_tickers = get_all_tickers()

# --- Liste déroulante de sélection
selected_tickers = st.sidebar.multiselect(
    "✅ Select tickers (up to 3) :",
    options=all_tickers,
    default=[],
    help="Select the tickers of the actions to be included in the simulation."
)

if len(selected_tickers) > 3:
    st.sidebar.warning("You can only select up to 3 tickers. Please deselect some tickers.")
    st.stop()  # Stoppe l'exécution de l'application si plus de 3 tickers sont sélectionnés

if len(selected_tickers) == 0:
    st.sidebar.warning("Please select at least one ticker to start the simulation.")
    st.stop()

# --- Additional Investment and Simulation Parameters
st.sidebar.subheader("💰 Initial Investment")
initial_investment = st.sidebar.number_input(
    "Initial Investment Amount (€)",
    min_value=1000,
    value=10000,
    step=1000
)

st.sidebar.subheader("📅 Temporal Parameters")
T = st.sidebar.slider(
    "Number of Simulated Days",
    min_value=22,
    max_value=365,
    value=252,
    step=10,
    help="Number of days the simulation spans (default: 252 days = 1 trading year)."
)

mc_sims = st.sidebar.slider(
    "Number of Monte Carlo Simulations",
    min_value=100,
    max_value=5000,
    value=500,
    step=100,
    help="Number of simulated trajectories to model potential portfolio values."
)

gif_html = """
<div style="text-align: center; margin-top: 20px;">
    <img src="https://media.giphy.com/media/4N5ddOOJJ7gtKTgNac/giphy.gif" 
         alt="Linux Animation" style="width:250px; border-radius:10px;">
    <p style="font-size:14px; color:gray; margin-top: 10px;">💻 Powered by Linux</p>
</div>
"""
st.sidebar.markdown(gif_html, unsafe_allow_html=True)

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
if selected_tickers:
    meanReturns, covMatrix, returns = get_data(selected_tickers, startDate, endDate)

    # --- Calcul de la volatilité par le modèle GARCH
    garch_vol = {}
    for stock in selected_tickers:
        try:
            model = arch_model(returns[stock].dropna() * 100, vol='Garch', p=1, q=1)
            res = model.fit(disp='off')
            garch_vol[stock] = res.conditional_volatility.iloc[-1] / 100  # On normalise la volatilité
        except Exception as e:
            st.warning(f"Erreur avec le GARCH pour {stock}: {e}")

    # --- Pondération initiale (également modifiable par l'utilisateur)
    weights = np.array([1 / len(selected_tickers)] * len(selected_tickers))  # Pondération égale

    # --- Simulation Monte Carlo
    np.random.seed(42)
    meanM = np.tile(meanReturns.values.reshape(-1, 1), T)  # (n, T)
    portfolio_sims = np.zeros((T, mc_sims))  # Matrice de simulation (T, M)

    L = np.linalg.cholesky(covMatrix.values)  # Décomposition de Cholesky
    for m in range(mc_sims):
        Z = np.random.normal(size=(len(selected_tickers), T))  # Variables normales indépendantes (n, T)
        dailyReturns = meanM + (L @ Z)  # On applique la corrélation (n, T)
        portfolio_sims[:, m] = np.cumprod(np.dot(weights, dailyReturns) + 1) * initial_investment

    # --- Calcul des statistiques sur les valeurs finales
    final_values = portfolio_sims[-1, :]
    mean_value = np.mean(final_values)
    max_value = np.max(final_values)
    min_value = np.min(final_values)
    profit_probability = np.sum(final_values > initial_investment) / mc_sims

# Affichage des résultats avec des couleurs
    st.markdown("---")
    st.markdown(
    f"✅ **Average portfolio value :** "
    f"<span style='color: orange; font-weight: bold;'>{mean_value:.2f} €</span>",
    unsafe_allow_html=True
)
    st.markdown(
    f"📈 **Maximum value reached :** "
    f"<span style='color: green; font-weight: bold;'>{max_value:.2f} €</span>",
    unsafe_allow_html=True
)
    st.markdown(
    f"📉 **Minimum value reached :** "
    f"<span style='color: red; font-weight: bold;'>{min_value:.2f} €</span>",
    unsafe_allow_html=True
)
    st.markdown(
    f"🎯 **Probability of profit (> {initial_investment} €) :** "
    f"<span style='color: white; font-weight: bold;'>{profit_probability:.2%}</span>",
    unsafe_allow_html=True
)
    st.markdown("---")

    
    # --- Returns Histogram
    portfolio_returns = (final_values - initial_investment) / initial_investment * 100
    st.write("### Returns Distribution")

    plt.hist(portfolio_returns, bins=30, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel("Return (%)")
    plt.ylabel("Frequency")
    plt.title("Portfolio Returns Distribution")
    st.pyplot(plt)

    # --- Monte Carlo Simulations Plot
    st.write("### Monte Carlo Simulations")
    plt.figure(figsize=(8, 5))

    cmap = plt.get_cmap("Spectral")  
    num_colors = portfolio_sims.shape[1]  

    days = np.arange(0, T) 
    for m in range(mc_sims):
        plt.plot(days, portfolio_sims[:, m], color=cmap(m/ num_colors), alpha=0.25)

    plt.plot(days, np.mean(portfolio_sims, axis=1), color='red', linewidth=2, label='Mean trajectory')
    plt.xlabel('Days')
    plt.ylabel('Portfolio Value (€)')
    plt.title('Portfolio Monte Carlo Simulation')
    plt.legend()
    st.pyplot(plt)

    # --- GARCH Volatility Table
    st.write("### Volatility Analysis")
    vol_df = pd.DataFrame({
        'Ticker': garch_vol.keys(),
        'GARCH Volatility (%)': [v * 100 for v in garch_vol.values()]
    })

    st.write("#### Estimated GARCH Volatility per Stock")
    st.dataframe(vol_df.style
        .format({'GARCH Volatility (%)': '{:.2f}'})
        .background_gradient(cmap='coolwarm', axis=0), use_container_width=True)

    st.write("""
        **Volatility** measures share price fluctuations over a given period.
        - GARCH volatility**: Based on historical data, it represents a dynamic estimate of future conditional volatility.
    """)

    st.write(
        """
         ***GARCH volatility interpretation:***  
        Higher volatility (e.g. 2% or more) means that the share price can fluctuate widely, indicating higher risk but also the potential for greater gains.  

        Lower volatility (less than 1%) reflects a relatively stable share price, generally associated with lower risk but also more modest potential returns.
        """
    ) 

# --- Afficher les informations pour les tickers sélectionnés
if selected_tickers:
    st.subheader("📄 Company information on selected tickers")
    ticker_details = []
    for ticker in selected_tickers:
        info = get_ticker_info(ticker)
        ticker_details.append(info)
        st.markdown(f"""
        **{ticker}** - {info['name']}  
        - 🏢 **Sector** : {info['sector']}  
        - 🏭 **Industry** : {info['industry']}  
        - 💰 **Annual sales 2022** : {info['revenue_2022']}  
        - 💰 **Annual sales 2023** : {info['revenue_2023']} 
        - 📊 **Sales Growth Ratio (2023/2022)** :  {info['sales_ratio']}        """)
