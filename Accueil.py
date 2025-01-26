import streamlit as st
from streamlit_carousel import carousel
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

# Sidebar
#st.sidebar.title("Navigation")

# Main
st.title("Système de gestion des stocks de céréales 🌾")

# Read Excel file
df = pd.read_excel("./data/cereals_info.xlsx")

carousel_items = []
for _, row in df.iterrows():
    carousel_items.append(
        dict(
            title=row['Nom'],
            text=row['Description'],
            img=row['Image'],
            link="#",  # Replace with a relevant link if needed
        )
    )

# Display the carousel
st.write(" ")
carousel(items=carousel_items)






