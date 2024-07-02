import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Mapping for Pokémon types
type_mapping = {
    "Flying" : 0,
    "Ground" : 1,
    "Poison" : 2,
    "Psychic" : 3,
    "Fighting" : 4,
    "Grass" : 5,
    "Fairy" : 6,
    "Steel" : 7,
    "Dark" : 8,
    "Dragon" : 9,
    "Water" : 10,
    "Ghost" : 11,
    "Ice" : 12,
    "Rock" : 13,
    "Fire" : 14,
    "Electric" : 15,
    "Normal" : 16,
    "Bug" : 17
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
    # Transform string into number
    data['Legendary'] = data['Legendary'].map({True: 1, False: 0})
    data['Type 1'] = data['Type 1'].map(lambda x: applyOnNaN(x))
    data['Type 2'] = data['Type 2'].map(lambda x: applyOnNaN(x))

    data = data.drop(columns=['#', 'Name'])
    return data

def trainModel(data, key):
    # Features and target variable
    X = data.drop(columns=[key])
    y = data[key]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f'Mean Squared Error: {mse}')

    return model

def predict(pokemon, key):
    data = loadData()
    data = cleanData(data)
    model = trainModel(data, key)
    columns_to_predict = list(data.columns)
    columns_to_predict.remove(key)
    pokemon_df = pd.DataFrame({col: [pokemon[col]] for col in columns_to_predict})
    new_pokemon_value = model.predict(pokemon_df)
    if(key == "Type 1" or key == "Type 2"):
        st.write(f'Predicted {key} stat for new Pokémon: {numberToType(round(new_pokemon_value[0]))}')
    else:
        st.write(f'Predicted {key} stat for new Pokémon: {new_pokemon_value[0]}')

def numberToType(index):
    for key in type_mapping:
        if(type_mapping[key] == index):
            return key
    return ""

def drawNumberInput(selected_stat,field_name,default_value):
    field = 0
    if(selected_stat != field_name):
        field = st.sidebar.number_input(field_name, step=1, value=default_value)
    return field

def drawTypeChoices(selected_stat,field_name):
    type = 'Fire'
    if(selected_stat != field_name):
        type = st.sidebar.selectbox(field_name, list(type_mapping.keys()))
    return type

def prediction_page():
    st.title('Pokémon Stat Predictor')

    st.sidebar.subheader('Select Stat to Predict:')

    choices = ('Type 1','Type 2','Total','Attack','Defense','Sp. Atk','Sp. Def','Speed','Generation','HP','Legendary')

    selected_stat = st.sidebar.selectbox('',choices)

    st.sidebar.subheader('Enter Pokémon Stats:')


    type_1 = drawTypeChoices(selected_stat,'Type 1') 
    type_2 = drawTypeChoices(selected_stat,'Type 2') 
    total = drawNumberInput(selected_stat,'Total',325)
    attack = drawNumberInput(selected_stat,'Attack',50)
    defense = drawNumberInput(selected_stat,'Defense',50)
    sp_atk = drawNumberInput(selected_stat,'Sp. Atk',65)
    sp_def = drawNumberInput(selected_stat,'Sp. Def',65)
    speed = drawNumberInput(selected_stat,'Speed',45)
    generation = drawNumberInput(selected_stat,'Generation',1)
    hp = drawNumberInput(selected_stat,'HP',50)
    legendary = False
    if(selected_stat != 'Legendary'):
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



    if st.button('Predict'):
        predict(pokemon, selected_stat)
