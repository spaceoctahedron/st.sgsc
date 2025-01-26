import streamlit as st
import pandas as pd
from io import BytesIO
import re

def extract_image_url(html_string):
    pattern = r'src="([^"]+)"'
    matches = re.findall(pattern, html_string)
    return matches[-1] if matches else None

# Read the Excel file
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_data():
    df = pd.read_excel("./data/cereals_info.xlsx")
    # Remove the line that applies extract_image_url
    return df[["Image", "ID", "Nom", "Description", "Région", "Prix", "Mesure"]].sort_values('Nom')

df_display = load_data()

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
</style>
"""

# Function to format the image column for display
def format_image_for_display(image_url):
    return f'<img src="{image_url}" alt="Cereal Image">'

# Function to update a value in the DataFrame
def update_value(id, column, new_value):
    global df_display
    if column == 'Image':
        new_value = extract_image_url(new_value) or new_value
    df_display.loc[df_display['ID'] == id, column] = new_value
    df_display.to_excel("./data/cereals_info.xlsx", index=False)

# Function to download DataFrame as Excel
def download_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_display.to_excel(writer, index=False)
    return output.getvalue()

# Streamlit app
st.header("Aperçu des céréales - Tableau")

# Display the table
display_df = df_display.copy()
display_df['Image'] = display_df['Image'].apply(format_image_for_display)
st.write(custom_css + display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Modifier une valeur")
    id_to_update = st.number_input("ID de la céréale à modifier", min_value=df_display['ID'].min(), max_value=df_display['ID'].max())
    column_to_update = st.selectbox("Colonne à modifier", df_display.columns[2:])  # Exclude 'ID' and 'Image'
    new_value = st.text_input("Nouvelle valeur")
    if st.button("Mettre à jour"):
        update_value(id_to_update, column_to_update, new_value)
        st.success("Valeur mise à jour avec succès!")
        st.rerun()

with col2:
    st.subheader("Valeurs actuelles")
    if id_to_update:
        current_values = df_display[df_display['ID'] == id_to_update].iloc[0]
        if current_values['Image']:
            st.image(current_values['Image'], width=50)
        else:
            st.write("Image not available")
        for col in df_display.columns[1:]:  # Include 'Image', but still exclude 'ID'
            if col != 'Image':
                st.text(f"{col}: {current_values[col]}")

# Download button
if st.button("Télécharger le tableau en Excel", key="download_excel_button"):
    excel_data = download_excel()
    st.download_button(
        label="Cliquez pour télécharger",
        data=excel_data,
        file_name="cereals_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
