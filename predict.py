import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Mapping pour les types de Pokémon
type_mapping = {
    "Flying": 0,
    "Ground": 1,
    "Poison": 2,
    "Psychic": 3,
    "Fighting": 4,
    "Grass": 5,
    "Fairy": 6,
    "Steel": 7,
    "Dark": 8,
    "Dragon": 9,
    "Water": 10,
    "Ghost": 11,
    "Ice": 12,
    "Rock": 13,
    "Fire": 14,
    "Electric": 15,
    "Normal": 16,
    "Bug": 17
}

def loadData():
    data = pd.read_csv('data/Pokemon.csv')
    return data

def applyOnNaN(x):
    if pd.isna(x):
        return -1
    else:
        return type_mapping[x]

def cleanData(data):
    # Transformer les chaînes en nombres
    data['Legendary'] = data['Legendary'].map({True: 1, False: 0})
    data['Type 1'] = data['Type 1'].map(lambda x: applyOnNaN(x))
    data['Type 2'] = data['Type 2'].map(lambda x: applyOnNaN(x))

    data = data.drop(columns=['#', 'Name'])
    return data

def trainModel(data, key):
    # Variables explicatives et cible
    X = data.drop(columns=[key])
    y = data[key]

    # Séparer les données
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f'Erreur Quadratique Moyenne: {mse}')

    return model

def predict(pokemon, key):
    data = loadData()
    data = cleanData(data)
    model = trainModel(data, key)
    columns_to_predict = list(data.columns)
    columns_to_predict.remove(key)
    pokemon_df = pd.DataFrame({col: [pokemon[col]] for col in columns_to_predict})
    new_pokemon_value = model.predict(pokemon_df)
    if key in ["Type 1", "Type 2"]:
        st.write(f'Valeur prédite pour {key} du nouveau Pokémon: {numberToType(round(new_pokemon_value[0]))}')
    else:
        st.write(f'Valeur prédite pour {key} du nouveau Pokémon: {new_pokemon_value[0]}')

def numberToType(index):
    for key in type_mapping:
        if type_mapping[key] == index:
            return key
    return ""

def prediction_page():
    st.sidebar.subheader('Sélectionnez la statistique à prédire:')

    choices = ('Type 1', 'Type 2', 'Total', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'HP', 'Legendary')

    selected_stat = st.sidebar.selectbox('', choices)

    st.sidebar.subheader('Entrez les statistiques du Pokémon:')
    type_1 = st.sidebar.selectbox('Type 1', list(type_mapping.keys()))
    type_2 = st.sidebar.selectbox('Type 2', list(type_mapping.keys()))
    total = st.sidebar.number_input('Total', step=1, value=325)
    attack = st.sidebar.number_input('Attack', step=1, value=50)
    defense = st.sidebar.number_input('Defense', step=1, value=50)
    sp_atk = st.sidebar.number_input('Sp. Atk', step=1, value=65)
    sp_def = st.sidebar.number_input('Sp. Def', step=1, value=65)
    speed = st.sidebar.number_input('Speed', step=1, value=45)
    generation = st.sidebar.number_input('Generation', step=1, value=1)
    hp = st.sidebar.number_input('HP', step=1, value=50)
    legendary = st.sidebar.checkbox('Legendary')

    pokemon = {
        'Type 1': type_mapping[type_1],
        'Type 2': type_mapping[type_2],
        'Total': total,
        'Attack': attack,
        'Defense': defense,
        'Sp. Atk': sp_atk,
        'Sp. Def': sp_def,
        'Speed': speed,
        'Generation': generation,
        'HP': hp,
        'Legendary': 1 if legendary else 0,
    }

    if st.button('Prédire'):
        predict(pokemon, selected_stat)
