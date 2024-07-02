import streamlit as st

def stats_page():
    st.header("À propos de cette application")
    st.write("Cette application prédit les statistiques des Pokémon en utilisant un modèle de régression basé sur Random Forest.")
    st.write("Vous pouvez entrer les statistiques d'un Pokémon et sélectionner la statistique à prédire.")
    st.write("L'application utilisera les données historiques des Pokémon pour faire une prédiction.")
