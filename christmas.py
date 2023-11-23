import streamlit as st
import pandas as pd

link = "christmas_recipes.csv"

df = pd.read_csv(link)

# Zone de recherche
search_zone = st.text_input("Rechercher dans le DataFrame:")

st.write("Temps nécessaire à la préparation :")
selected_time = st.selectbox('Sélectionner une valeur:', ['Toutes'] + df['Time'].unique().tolist())

st.write("Nombre de plats :")
selected_servings = st.selectbox('Sélectionner une valeur:', ['Toutes'] + df['Servings'].unique().tolist())

# Filtrage du dataFrame en fonction des valeurs sélectionnées
filtered_df = df.copy()

if selected_time != 'Toutes':
    filtered_df = filtered_df[filtered_df['Time'] == selected_time]

if selected_servings != 'Toutes':
    filtered_df = filtered_df[filtered_df['Servings'] == selected_servings]

# Filtrage du DataFrame en fonction de la recherche
filtered_df = filtered_df[filtered_df.astype(str).apply(lambda row: row.str.contains(search_zone, case=False).any(), axis=1)]

# Affichage des résultats
st.dataframe(filtered_df)





