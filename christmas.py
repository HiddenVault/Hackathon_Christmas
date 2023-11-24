import streamlit as st
import pandas as pd
from PIL import Image

link = "christmas_recipes.csv"

df = pd.read_csv(link, sep=',', encoding='UTF-8')

image_url= 'https://st4.depositphotos.com/2627021/31189/i/450/depositphotos_311897692-stock-photo-christmas-tree-with-baubles-and.jpg'
code_html = f"<img src='{image_url}' width='100%'/>"
st.markdown(code_html, unsafe_allow_html = True)
st.markdown('<h1 style="color:red;">Christmas Recipes', unsafe_allow_html=True)

# Zone de recherche
search_zone = st.text_input("Search for ingredients :")

selected_time = st.selectbox('Preparation time :', ['All'] + df['Time'].unique().tolist())

selected_servings = st.selectbox('Number of covers :', ['All'] + df['Servings'].unique().tolist())

# Filtrage du dataFrame en fonction des valeurs sélectionnées
# Filtrage du DataFrame en fonction de la recherche

# Affichage des résultats
def dataframe_with_selections(df):
    df = df[df.astype(str).apply(lambda row: row.str.contains(search_zone, case=False).any(), axis=1)]
    if selected_time != 'All':
        df = df[df['Time'] == selected_time]
    if selected_servings != 'All':
        df = df[df['Servings'] == selected_servings]
    filtered_df = df.copy()
    filtered_df.insert(0, "Select", False)

    edited_df = st.data_editor(
        filtered_df,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

selection = dataframe_with_selections(df)

selection['Time'] = selection['Time'].astype(str)
selection['Ingredients'] = selection['Ingredients'].str.replace(', ', ',\n')
selection['Instructions'] = selection['Instructions'].str.replace('. ', '.\n')

# Affichage de la recette sélectionnée
if not selection.empty:
    selected_row = selection.index

    liste_titre = list(selection.loc[selected_row, 'Title'])
    st.markdown("**Recipe :**")
    st.text(liste_titre[0])

    liste_image = list(selection.loc[selected_row, 'Image'])
    image_url = liste_image[0]
    st.image(image_url)

    liste_temps = list(selection.loc[selected_row, 'Time'])
    st.markdown("**Preparation time in minutes :**")
    st.text(liste_temps[0])

    liste_couverts = list(selection.loc[selected_row, 'Servings'])
    st.markdown("**Number of covers :**")
    st.text(liste_couverts[0])

    liste_ingrédients = list(selection.loc[selected_row, 'Ingredients'])
    st.markdown("**Ingredients :**")
    st.text(liste_ingrédients[0].replace('[','').replace(']','').replace("'",''))


    liste_instructions = list(selection.loc[selected_row, 'Instructions'])
    st.markdown("**Instructions :**")
    st.text(liste_instructions[0])
    
    st.markdown('<h3 style="color:red;">Enjoy your meal and Happy Christmas !', unsafe_allow_html=True)
