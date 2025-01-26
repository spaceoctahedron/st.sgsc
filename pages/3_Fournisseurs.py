# 3_Fournisseurs.py
import streamlit as st
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

# Load the suppliers data
@st.cache_data
def load_suppliers_data():
    df = pd.read_csv("./data/Fournisseurs_de_cereales_en_Afrique_de_lOuest.csv")
    return df

# Manually define coordinates for cities in West Africa
city_coordinates = {
    'Lomé': (6.136629, 1.222186),  # Togo
    'Accra': (5.614818, -0.205874),  # Ghana
    'Ouagadougou': (12.36566, -1.53388),  # Burkina Faso
    'Lagos': (6.45407, 3.39467),  # Nigeria
    'Cotonou': (6.3694, 2.4183),  # Benin
    'Niamey': (13.5137, 2.1098),  # Niger
    'Abidjan': (5.3599, -4.0083),  # Côte d'Ivoire
    'Dakar': (14.716677, -17.467686),  # Senegal
    'Bamako': (12.6392, -8.0029),  # Mali
    'Conakry': (9.5370, -13.7130)  # Guinea
}


# Prepare data for mapping
def prepare_map_data(df):
    map_data = df[df['Ville'].notna()].copy()
    map_data['latitude'] = map_data['Ville'].map(lambda x: city_coordinates.get(x, (None, None))[0])
    map_data['longitude'] = map_data['Ville'].map(lambda x: city_coordinates.get(x, (None, None))[1])
    map_data = map_data.dropna(subset=['latitude', 'longitude'])
    return map_data

# Streamlit page
st.title("Fournisseurs de Céréales en Afrique de l'Ouest")

# Load data
df_suppliers = load_suppliers_data()

# Prepare map data
map_data = prepare_map_data(df_suppliers)

# Display map
if not map_data.empty:
    st.map(map_data[['latitude', 'longitude']])
    
    # Display supplier details
    st.subheader("Détails des Fournisseurs")
    for _, row in map_data.iterrows():
        with st.expander(row['Nom']):
            st.write(f"**Céréales fournies:** {row['Céréales fournies']}")
            st.write(f"**Ville:** {row['Ville']}")
            st.write(f"**Pays:** {row['Pays']}")
            st.write(f"**Téléphone:** {row['Téléphone'] if row['Téléphone'] != '-' else 'Non disponible'}")
            st.write(f"**E-mail:** {row['E-mail'] if row['E-mail'] != '-' else 'Non disponible'}")
else:
    st.warning("Aucun fournisseur avec des coordonnées géographiques n'a été trouvé.")
