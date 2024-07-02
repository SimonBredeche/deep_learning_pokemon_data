import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv('data/Pokemon.csv')
    return data

def stats_page():
    st.header("Analyse des Statistiques des Pokémon")

    data = load_data()

    # Afficher les premières lignes du dataset
    st.subheader("Aperçu des données")
    st.write(data.head())

    # Graphique de distribution des Totaux de statistiques
    st.subheader("Distribution des Totaux de Statistiques")
    fig, ax = plt.subplots()
    sns.histplot(data['Total'], kde=True, ax=ax)
    st.pyplot(fig)

    # Boxplot des statistiques par génération
    st.subheader("Boxplot des Statistiques par Génération")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="Generation", y="Total", data=data, ax=ax)
    st.pyplot(fig)

    # Assurez-vous que les colonnes sont de type numérique et ne contiennent pas de valeurs manquantes
    numeric_cols = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
    data = data.dropna(subset=numeric_cols)

    # Moyenne des statistiques par type
    st.subheader("Moyenne des Statistiques par Type")
    mean_stats = data.groupby('Type 1')[numeric_cols].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Type 1', y='Total', data=mean_stats, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Scatter plot des HP vs Attack
    st.subheader("HP vs Attack")
    fig, ax = plt.subplots()
    sns.scatterplot(x='HP', y='Attack', hue='Type 1', data=data, ax=ax)
    st.pyplot(fig)

if __name__ == "__main__":
    stats_page()
