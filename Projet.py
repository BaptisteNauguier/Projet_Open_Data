import streamlit as st
import pandas as pd
import plotly.express as px

# Chemin de base pour les fichiers de données
data_path = "C:/Users/brice/OneDrive/Bureau/MIASHS/M2/Open_data/Projet_Open_Data/"

# Chargement des données
df_annual_deaths = pd.read_csv(data_path + '01 annual-number-of-deaths-by-cause.csv')
df_total_cancer_deaths_by_type = pd.read_csv(data_path + '02 total-cancer-deaths-by-type.csv')
df_cancer_death_rates_by_age = pd.read_csv(data_path + '03 cancer-death-rates-by-age.csv')
df_share_of_population_with_cancer_types = pd.read_csv(data_path + '04 share-of-population-with-cancer-types.csv')
df_share_of_population_with_cancer = pd.read_csv(data_path + '05 share-of-population-with-cancer.csv')
df_number_of_people_with_cancer_by_age = pd.read_csv(data_path + '06 number-of-people-with-cancer-by-age.csv')
df_share_of_population_with_cancer_by_age = pd.read_csv(data_path + '07 share-of-population-with-cancer-by-age.csv')
df_disease_burden_rates_by_cancer_types = pd.read_csv(data_path + '08 disease-burden-rates-by-cancer-types.csv')
df_cancer_deaths_rate_and_age_standardized_rate_index = pd.read_csv(data_path + '09 cancer-deaths-rate-and-age-standardized-rate-index.csv')

# Fonction pour créer un graphique linéaire
def plot_line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title)
    return fig

# Fonction pour créer un graphique en barres
def plot_bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    return fig

# Fonction principale de l'app
def main():
    st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")

    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)

    # Filtrage des données par année
    df_filtered = df_annual_deaths[df_annual_deaths['Year'] == year]

    st.header("Carte Interactive Mondiale")
    # Code pour la carte interactive ici

    st.header("Graphiques et Analyses")
    st.plotly_chart(plot_line_chart(df_filtered, 'Entity', 'Deaths', 'Mortalité par pays'))

    st.header("Analyse par Type de Cancer")
    df_cancer_filtered = df_total_cancer_deaths_by_type[df_total_cancer_deaths_by_type['Year'] == year]
    st.plotly_chart(plot_bar_chart(df_cancer_filtered, 'Type', 'Deaths', 'Décès par type de cancer'))

    st.header("Analyse Approfondie")
    # Analyse des corrélations et autres statistiques avancées

    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

# Exécution de l'app
if __name__ == "__main__":
    main()
