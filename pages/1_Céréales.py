import streamlit as st
import pandas as pd
import re
from io import BytesIO
from sqlalchemy import text

# Configure Streamlit
st.set_page_config(page_title=None, page_icon="im/cereal_icon.png", 
                   layout="centered", initial_sidebar_state="auto", 
                   menu_items=None)
st.markdown("""
<style>
[data-testid="stSidebar"] img {
    width: 100%;
    height: auto;
    border-radius: 0 !important;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

st.logo("im/cereal_logo.png")

def extract_image_url(html_string):
    pattern = r'src="([^"]+)"'
    matches = re.findall(pattern, html_string)
    return matches[-1] if matches else None

# Function to fetch and refresh data from the database
def fetch_data():
    with conn.session as session:
        df = pd.read_sql(text("SELECT * FROM cereals"), session.bind)
    df['Nom'] = df['Nom'].astype(str)
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    df['Prix'] = pd.to_numeric(df['Prix'], errors='coerce')
    return df[selected_columns].sort_values('Nom')

# Connect to the database
conn = st.connection("sgsc_database")
selected_columns = ["Image", "ID", "Nom", "Description", "Région", "Prix", "Mesure"]
df = fetch_data()

# Define a custom HTML style for left-aligning headers and styling the table
custom_css = """
<style>
    th {
        text-align: left !important;
    }
    td {
        text-align: left !important;
    }
    img {
        border-radius: 50%;
        width: 50px;
        height: 50px;
        object-fit: cover;
    }
    td img {
        display: block;
        margin: 0 auto;
    }
    table {
        width: 100%;
        table-layout: auto;
    }
    td:first-child {
        width: 80px !important;  /* Increase the width of the image column */
    }
</style>
"""

# Function to format the image column for display
def format_image_for_display(image_url):
    return f'<img src="{image_url}" alt="Cereal Image">'

# Function to update a value in the database
def update_value(id, column, new_value):
    if column == "Prix":
        new_value = float(new_value)

    st.write(f"Attempting to update column: {column}, New Value: {new_value}, ID: {id}")

    try:
        with conn.session as session:
            result = session.execute(text('SELECT * FROM cereals WHERE "ID" = :id'), {"id": id}).fetchone()
            st.write("Before Update:", result)

            query = text(f'UPDATE cereals SET "{column}" = :new_value WHERE "ID" = :id')
            session.execute(query, {"new_value": new_value, "id": id})
            session.commit()

            updated_result = session.execute(text('SELECT * FROM cereals WHERE "ID" = :id'), {"id": id}).fetchone()
            st.write("After Update:", updated_result)

            if updated_result[column] == new_value:
                st.success("Valeur mise à jour avec succès!")
            else:
                st.error("La mise à jour a échoué.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Refresh the DataFrame and reset confirmation state
    st.session_state.df = fetch_data()
    st.session_state.show_confirm = False
    st.rerun()

# Function to download DataFrame as Excel
def download_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Streamlit app
st.title("🌾 Aperçu des céréales")

# Display the table
display_df = st.session_state.get('df', df).copy()
display_df['Image'] = display_df['Image'].apply(format_image_for_display)
display_df['Prix'] = display_df['Prix'].apply(lambda x: f"{x:.2f}")  # Format Prix to two decimal places
st.write(custom_css + display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.write(" ")
st.subheader("Mettre à jour la base de données")

# Create two columns for user interaction
col1, col2 = st.columns(2)

with col2:
    st.markdown("**Modifier une valeur**")
    id_to_update = st.number_input("ID de la céréale à modifier", min_value=int(df['ID'].min()), max_value=int(df['ID'].max()))
    column_to_update = st.selectbox("Colonne à modifier", df.columns.drop(['ID', 'Image']))

    if column_to_update == "Prix":
        new_value = st.number_input("Nouvelle valeur", format="%.2f")
    else:
        new_value = st.text_input("Nouvelle valeur")

    # Handle confirmation using session state
    if st.button("Mettre à jour"):
        st.session_state.show_confirm = True  # Set flag to show confirmation

    if st.session_state.get('show_confirm', False):
        with st.container():
            st.warning("**Attention** : Vous êtes sur le point de modifier la base de données. Confirmez-vous cette action ?")
            confirm_col1, confirm_col2 = st.columns(2)

            with confirm_col1:
                if st.button("Oui"):
                    st.session_state.show_confirm = False  # Reset flag before updating
                    update_value(id_to_update, column_to_update, new_value)

            with confirm_col2:
                if st.button("Non"):
                    st.session_state.show_confirm = False  # Reset flag on cancel
                    st.rerun()

with col1:
    st.markdown("**Valeurs actuelles**")
    if id_to_update:
        current_values = df[df['ID'] == id_to_update].iloc[0]
        if current_values['Image']:
            st.image(current_values['Image'], width=50)
        else:
            st.write("Image non disponible")
        for col in df.columns:
            if col != 'ID' and col != 'Image':
                st.text(f"{col}: {current_values[col]}")

# Download button to export the table as Excel
if st.button("Télécharger le tableau en Excel", key="download_excel_button"):
    excel_data = download_excel()
    st.download_button(
        label="Cliquez pour télécharger",
        data=excel_data,
        file_name="cereals_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
