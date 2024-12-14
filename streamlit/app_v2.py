import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
from arch import arch_model


# Set page configuration
st.set_page_config(
    page_title="Portfolio Monte Carlo Simulator",
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

# --- Ticker Selection via Dropdown
available_tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'BNP.PA', 'AIR.PA', 'OR.PA']
selected_tickers = st.sidebar.multiselect(
    "Select Stock Tickers (up to 5)",
    options=available_tickers,
    default=['AAPL', 'MSFT'],
    help="A ticker is a unique symbol used to identify a stock on the exchange, you can add one to the list by writing it."
)

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

# --- Historical Observation Period
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=1000)

# --- Function to Import Price Data
@st.cache_data
def get_data(stocks, start, end):
    stockData = yf.download(stocks, start, end)['Close']
    returns = stockData.pct_change().dropna()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix, returns

# --- Retrieve Market Data
meanReturns, covMatrix, returns = get_data(selected_tickers, startDate, endDate)

# --- Calculate Volatility Using GARCH Model
garch_vol = {}
for stock in selected_tickers:
    try:
        model = arch_model(returns[stock].dropna() * 100, vol='Garch', p=1, q=1)
        res = model.fit(disp='off')
        garch_vol[stock] = res.conditional_volatility.iloc[-1] / 100  
    except Exception as e:
        st.warning(f"Error with GARCH model for {stock}: {e}")

# --- Initial Weighting (also user-modifiable)
weights = np.array([1 / len(selected_tickers)] * len(selected_tickers))  

# --- Monte Carlo Simulation
np.random.seed(42)
meanM = np.tile(meanReturns.values.reshape(-1, 1), T)  
portfolio_sims = np.zeros((T, mc_sims)) 

L = np.linalg.cholesky(covMatrix) 
for m in range(mc_sims):
    Z = np.random.normal(size=(len(selected_tickers), T)) 
    dailyReturns = meanM + (L @ Z) 
    portfolio_sims[:, m] = np.cumprod(np.dot(weights, dailyReturns) + 1) * initial_investment

# --- Calculate Statistics on Final Values
final_values = portfolio_sims[-1, :]
mean_value = np.mean(final_values)
max_value = np.max(final_values)
min_value = np.min(final_values)
profit_probability = np.sum(final_values > initial_investment) / mc_sims


st.write("### Simulation Results")

st.markdown("""
<div style='
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 15px;
'>
""" + 
f"""
**Average Portfolio Value:** <span style='color: blue'>{mean_value:.2f} €</span><br>

**Maximum Value Reached:** <span style='color: blue'>{max_value:.2f} €</span><br>

**Minimum Value Reached:** <span style='color: blue'>{min_value:.2f} €</span><br>

**Profit Probability (> {initial_investment} €):** <span style='color: blue'>{profit_probability:.2%}</span>
""" + 
"""
</div>
""", unsafe_allow_html=True)


plt.figure(figsize=(8, 5))
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
plt.plot(portfolio_sims, alpha=0.3)

cmap = plt.get_cmap("Spectral")  
num_colors = portfolio_sims.shape[1]  

for i in range(num_colors):
    plt.plot(portfolio_sims[:, i], color=cmap(i / num_colors), alpha=0.4) 
plt.plot(np.mean(portfolio_sims, axis=1), color='red', linewidth=2, label='Mean trajectory') 
plt.ylabel('Portfolio Value (€)')
plt.xlabel('Days')
plt.legend(loc='upper left')
plt.title('Portfolio Monte Carlo Simulation')
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
