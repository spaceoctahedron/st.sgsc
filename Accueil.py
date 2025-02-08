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
df = pd.read_excel("./data/cereals_info.xlsx", engine='openpyxl')

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

st.write(" ")
# Functionality Description

st.subheader("Fonctionnalités Actuelles")
st.markdown("""
**🌾 Céréales**  
- Connexion à la base de données et affichage d'une vue d'ensemble des produits avec images.  
- Mise à jour des valeurs : noms, descriptions, prix, etc.

**🌿 Stocks**  
- Affichage des valeurs de stock avec des alertes pour les stocks faibles.

**🌏 Fournisseurs**  
- Visualisation des fournisseurs régionaux sur une carte avec leurs contacts (téléphone et email).

**📈 Marchés agricoles**  
- Affichage des cours des matières premières agricoles via yFinance.
""")


st.subheader("Fonctionnalités Futures")
st.markdown("""
**🌿 Stocks**  
- Rapports automatiques (quotidiens, hebdomadaires).  
- Alertes automatiques par email/SMS en cas de stock faible.  
- Intégration avec capteurs IoT pour la surveillance en temps réel des niveaux de stock.

**🌏 Fournisseurs**  
- Envoi d'emails automatiques aux fournisseurs pour demander la disponibilité et les prix.  
- Intégration avec des plateformes de commande en ligne.

**📈 Marchés agricoles**  
- Adaptation des prix régionaux pour l'Afrique de l'Ouest.  
- Intégration des données réelles des marchés locaux.

**👥 Équipe**  
- Affichage des membres de l'équipe avec leurs coordonnées et horaires de travail.  
- Chat interne pour une communication rapide entre les membres de l'équipe.

**📊 Tableau de bord**  
- Tableau de bord interactif pour l'analyse des tendances de vente et des stocks.  
- Prévisions basées sur l'IA pour la gestion proactive des stocks.

**🗓️ Gestion des Tâches**  
- Planification et suivi des tâches pour la gestion des inventaires et des livraisons.  
- Intégration avec des outils de gestion de projet.
""")
