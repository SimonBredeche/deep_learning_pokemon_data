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
    st.write(data.head(n=15))

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

    # Nouveau graphique : Nombre de légendaires par génération
    st.subheader("Nombre de Pokémon Légendaires par Génération")
    legendary_count = data[data['Legendary'] == True]['Generation'].value_counts().sort_index()
    fig, ax = plt.subplots()
    sns.barplot(x=legendary_count.index, y=legendary_count.values, ax=ax)
    ax.set_xlabel("Génération")
    ax.set_ylabel("Nombre de Légendaires")
    ax.set_title("Nombre de Pokémon Légendaires par Génération")
    st.pyplot(fig)

    # Nouveau graphique : Nombre de types par génération
    st.subheader("Nombre de Types par Génération")
    type_generation_count = data.groupby(['Generation', 'Type 1']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 8))
    type_generation_count.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel("Génération")
    ax.set_ylabel("Nombre de Types")
    ax.set_title("Nombre de Types de Pokémon par Génération")
    st.pyplot(fig)

if __name__ == "__main__":
    stats_page()
