import streamlit as st
from streamlit_option_menu import option_menu
from predict import prediction_page
from stats import stats_page

def main():
    st.title('Prédicteur de Statistiques de Pokémon')

    selected = option_menu(
        menu_title=None,
        options=["Prédiction de Statistiques", "Statistiques"],
        icons=["bar-chart", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Prédiction de Statistiques":
        prediction_page()
    elif selected == "Statistiques":
        stats_page()

if __name__ == '__main__':
    main()
