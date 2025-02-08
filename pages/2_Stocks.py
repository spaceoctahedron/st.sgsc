# 2_Stocks.py
import streamlit as st
import os
from data.inventory import df_inventory
import pandas as pd

# Configure Streamlit
st.set_page_config(page_title=None, page_icon="im/cereal_icon.png", 
                   layout="centered", initial_sidebar_state="auto", 
                   menu_items=None)
st.markdown("""
<style>
[data-testid="stSidebar"] img {
    width: 100%;
    height: auto;
}
</style>
""", unsafe_allow_html=True)
st.logo("im/cereal_logo.png")

image_base_path = os.path.abspath("./im/001/")

# Stock Status Overview

st.title("🌿 Aperçu de l'état des stocks")
status_df = df_inventory[[
    'ID', 'Nom', 'Stock actuel', 'Stock maximum', 'Niveau critique', 'Quantité à commander']]
st.dataframe(status_df, column_config={
    "ID": st.column_config.NumberColumn(format="%d")
})

# Overview of all products
st.header("Aperçu du produit")

# Multiselect dropdown for products
selected_products = st.multiselect(
    "Sélectionnez les produits à afficher", 
    df_inventory['Nom'].tolist(),
   placeholder="Sélectionnez un ou plusieurs produits"
)

# Display selected products
for product_name in selected_products:
    row = df_inventory[df_inventory['Nom'] == product_name].iloc[0]
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(row["Image"], width=100)
    
    with col2:
        st.subheader(row['Nom'])
        st.write(f"Description: {row['Description']}")
        st.write(f"Région: {row['Région']}")
        st.write(f"Stock actuel: {row['Stock actuel']}")
        st.write(f"Stock maximum: {row['Stock maximum']}")
        
        # Alert system
        if row['Stock actuel'] <= row['Niveau critique']:
            st.warning(f"Alerte stock bas ! Stock actuel : {row['Stock actuel']}")
            st.info(f"Commander {row['Quantité à commander']} unités pour atteindre le stock maximum")

