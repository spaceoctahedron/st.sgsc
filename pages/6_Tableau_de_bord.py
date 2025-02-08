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

st.title("📊 Tableau de bord")