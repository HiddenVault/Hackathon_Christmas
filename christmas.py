import streamlit as st
import pandas as pd
from PIL import Image

# Chargement du csv
link = "christmas_recipes.csv"
df = pd.read_csv(link, sep=',', encoding='UTF-8')

# Affichage de l'image de présentation
image_url= 'https://st4.depositphotos.com/2627021/31189/i/450/depositphotos_311897692-stock-photo-christmas-tree-with-baubles-and.jpg'
code_html = f"<img src='{image_url}' width='100%'/>"
st.markdown(code_html, unsafe_allow_html = True)
st.markdown('<h1 style="color:red;">Christmas Recipes', unsafe_allow_html=True)

# Zone de recherche
search_zone = st.text_input("Search for ingredients :")
selected_time = st.selectbox('Preparation time :', ['All'] + df['Time'].unique().tolist())
selected_servings = st.selectbox('Number of covers :', ['All'] + df['Servings'].unique().tolist())

# Affichage des résultats
def dataframe_with_selections(df):
    # Filtrage du DataFrame en fonction de la zone de recherche 'search_zone'
    df = df[df.astype(str).apply(lambda row: row.str.contains(search_zone, case=False).any(), axis=1)]
    # Zone de liste modifiable sur la colonne 'Time' si 'selected_time' n'est pas égal à 'All'
    if selected_time != 'All':
        df = df[df['Time'] == selected_time]
    # Zone de liste modifiable sur la colonne 'Servings' si 'selected_time' n'est pas égal à 'All'
    if selected_servings != 'All':
        df = df[df['Servings'] == selected_servings]
    # Copie du DataFrame filtré
    filtered_df = df.copy()
    # Ajout d'une colonne 'Select' avec des valeurs initiales à False
    filtered_df.insert(0, "Select", False)

    # Utilisation du data_editor de Streamlit pour afficher le DataFrame avec une colonne de cases à cocher
    edited_df = st.data_editor(
        filtered_df,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Sélection des lignes où la colonne 'Select' est True et suppression de la colonne 'Select'
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

# Affichage de la recette sélectionnée
if not selection.empty:
    selected_row = selection.index

    # Extraction du titre de la recette de la sélection
    liste_titre = list(selection.loc[selected_row, 'Title'])
    st.markdown("**Recipe :**")
    st.text(liste_titre[0])

    # Extraction de l'image de la recette de la sélection
    liste_image = list(selection.loc[selected_row, 'Image'])
    image_url = liste_image[0]
    st.image(image_url)

    # Extraction du temps de préparation de la recette de la sélection
    liste_temps = list(selection.loc[selected_row, 'Time'])
    st.markdown("**Preparation time in minutes :**")
    st.text(liste_temps[0])

    # Extraction du nombre de couverts de la recette de la sélection
    liste_couverts = list(selection.loc[selected_row, 'Servings'])
    st.markdown("**Number of covers :**")
    st.text(liste_couverts[0])

    # Extraction des ingrédients de la sélection
    liste_ingredients = list(selection.loc[selected_row, 'Ingredients'])
    st.markdown("**Ingredients :**")
    # Calcul du nombre de lignes dans la liste d'ingrédients en utilisant les sauts de ligne
    num_lines = len(liste_ingredients[0].split('\n'))
    # Utilisation de text_area de Streamlit pour afficher les ingrédients avec une zone de texte modifiable
    st.text_area(label='', value=liste_ingredients[0], height=(num_lines + 1) * 20)

    # Extraction des Instructions de la sélection
    liste_instructions = list(selection.loc[selected_row, 'Instructions'])
    st.markdown("**Instructions :**")
    # Calcul du nombre de lignes dans la liste d'instructions en utilisant les sauts de ligne
    num_lines = len(liste_instructions[0].split('\n'))
    # Utilisation de text_area de Streamlit pour afficher les ingrédients avec une zone de texte modifiable
    st.text_area(label='', value=liste_instructions[0], height=(num_lines + 1) * 20)
    
    # Message de fin
    st.markdown('<h3 style="color:red;">Enjoy your meal and Happy Christmas !', unsafe_allow_html=True)
