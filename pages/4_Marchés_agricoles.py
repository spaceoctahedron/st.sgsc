import streamlit as st
import yfinance as yf

# Define commodities and their descriptions
grain_futures = {
    'ZC=F': 'Corn Futures',
    'ZW=F': 'Wheat Futures',
    'ZS=F': 'Soybean Futures',
    'ZM=F': 'Soybean Meal Futures',
    'ZL=F': 'Soybean Oil Futures',
    'ZO=F': 'Oat Futures',
    'KE=F': 'KC HRW Wheat Futures',
    'ZR=F': 'Rough Rice Futures'
}

descriptions = {
    'ZC=F': "Les contrats à terme sur le maïs représentent le prix du maïs sur le marché.",
    'ZW=F': "Les contrats à terme sur le blé représentent le prix du blé sur le marché.",
    'ZS=F': "Les contrats à terme sur le soja représentent le prix du soja sur le marché.",
    'ZM=F': "Les contrats à terme sur la farine de soja représentent les prix de la farine de soja transformée.",
    'ZL=F': "Les contrats à terme sur l'huile de soja représentent les prix de l'huile de soja transformée.",
    'ZO=F': "Les contrats à terme sur l'avoine représentent le prix du marché pour l'avoine.",
    'KE=F': "Les contrats à terme sur le blé KC HRW représentent les prix du blé rouge d'hiver dur.",
    'ZR=F': "Les contrats à terme sur le riz brut représentent le prix du riz non transformé."
}

# Streamlit app
st.title("📈 Contrats à terme sur les céréales")

# Dropdown menu for selecting commodity
selected_commodity = st.selectbox(
    "Sélectionnez une céréale :",  # Translated text for the dropdown menu
    options=list(grain_futures.keys()),
    format_func=lambda x: grain_futures[x],
    index=list(grain_futures.keys()).index('ZC=F')  # Default to Corn Futures
)

# Display commodity details
st.subheader(f"{grain_futures[selected_commodity]}")
st.write(descriptions[selected_commodity])

# Fetch current data using yfinance
commodity_ticker = yf.Ticker(selected_commodity)
current_data = commodity_ticker.history(period="2d")  # Fetch at least 2 days for comparison

if not current_data.empty:
    # Correct price calculation: Convert cents to dollars
    current_data['Close'] = current_data['Close'] / 100
    
    # Get the last close and previous close prices
    last_close = current_data['Close'].iloc[-1]
    previous_close = current_data['Close'].iloc[-2] if len(current_data) > 1 else last_close
    
    # Calculate price change and percentage change
    price_change = last_close - previous_close
    percent_change = (price_change / previous_close) * 100 if previous_close != 0 else 0

    # Display metric
    st.metric("Prix actuel (en $)", f"${last_close:.2f}", f"{price_change:.2f} ({percent_change:.2f}%)")
else:
    st.write("Aucune donnée disponible pour cette céréale.")

# Slider for selecting period
st.subheader("Tendance des prix")
period = st.slider(
    "Sélectionnez une période (jours) :",  # Translated text for the slider
    min_value=7, 
    max_value=365*2, 
    value=28, 
    step=1
)

# Fetch historical data
historical_data = commodity_ticker.history(period=f"{period}d")
if not historical_data.empty:
    # Convert cents to dollars
    historical_data['Close'] = historical_data['Close'] / 100

    st.write(f"Tendance des prix pour les {period} derniers jours :")  # Translated
    st.line_chart(historical_data['Close'])
else:
    st.write("Aucune donnée historique disponible pour cette céréale.")
