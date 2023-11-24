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

# Conversion de la colonne 'Time' en string
selection['Time'] = selection['Time'].astype(str)
# Remplacement des virgules suivies d'un espace par une virgule suivie d'un saut de ligne
selection['Ingredients'] = selection['Ingredients'].str.replace(', ', ',\n')
# Suppression des crochets et des apostrophes de la colonne 'Ingredients'
selection['Ingredients'] = selection['Ingredients'].str.replace("[\[\]']", '', regex=True)
# Division de la chaîne à chaque virgule,
# Ajout du préfixe "-" suivi d'un espace à chaque élément, 
# On rejoint deux éléments avec un saut de ligne.
selection['Ingredients'] = selection['Ingredients'].apply(lambda x: '\n'.join(['- ' + i.strip() for i in x.split(',')]))
# Remplacement des points suivis d'un espace par un point suivi d'un saut de ligne.
selection['Instructions'] = selection['Instructions'].str.replace('. ', '.\n')
# Division de la chaîne à chaque saut de ligne, 
# Ajoute du préfixe du numéro de ligne suivi d'un point et d'un espace à chaque élément, 
# On rejoint deux éléments avec un saut de ligne.
selection['Instructions'] = selection['Instructions'].apply(lambda x: '\n'.join([str(i+1) + '. ' + instruction.strip() for i, instruction in enumerate(x.split('\n'))]))

numbered_instructions = []
for index, row in df.iterrows():
    instructions_list = row['Instructions'].split('\n')
    numbered_instructions.extend([f"{index + 1}. {instruction}" for instruction in instructions_list])

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

    liste_ingredients = list(selection.loc[selected_row, 'Ingredients'])
    st.markdown("**Ingredients :**")
    num_lines = len(liste_ingredients[0].split('\n'))
    st.text_area(label='', value=liste_ingredients[0], height=(num_lines + 1) * 20)

    liste_instructions = list(selection.loc[selected_row, 'Instructions'])
    st.markdown("**Instructions :**")
    num_lines = len(liste_instructions[0].split('\n'))
    st.text_area(label='', value=liste_instructions[0], height=(num_lines + 1) * 20)
    
    st.markdown('<h3 style="color:red;">Enjoy your meal and Happy Christmas !', unsafe_allow_html=True)
