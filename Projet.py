import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Chemin de base pour les fichiers de données
data_path = "./"

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

# Structure de l'application
st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")

tab1, tab2, tab3, tab4 = st.tabs(["Page d'Accueil", "Carte Interactive Mondiale", "Analyse par Région", "Analyse Approfondie par Pays"])

with tab1:
    st.header("Bienvenue dans l'Analyse des Données sur le Cancer")
    st.write("""
        Cette application offre une analyse approfondie des tendances globales du cancer et des décès associés de 1990 à 2019. 
        Elle est structurée en plusieurs sections, chacune accessible via des onglets :

        **1. Page d'Accueil**
        - **Titre** : "Analyse Globale des Tendances du Cancer et des Décès (1990-2019)"
        - **Description** : Une introduction sur l'objectif de l'application et un résumé des données disponibles.

        **2. Carte Interactive Mondiale**
        - **Fonctionnalités** : Affichage des taux de cancer et de mortalité par pays pour l'année sélectionnée.
        - **Interactivité** : Possibilité de survoler les pays pour afficher des statistiques détaillées, telles que le nombre de cas de cancer et le taux de mortalité.

        **3. Analyse par Région**
        - **Sélection** : Choix de différentes régions (Amérique, Europe, Asie, etc.) pour des visualisations et analyses spécifiques.
        - **Visualisations** : Graphiques et tableaux récapitulatifs pour une comparaison claire entre les régions.

        **4. Analyse Approfondie par Pays**
        - **Exploration** : Corrélations entre les taux de cancer et divers facteurs socio-économiques comme le PIB par habitant, le niveau de vie, et l'accès aux soins de santé.
        - **Graphiques Interactifs** : Outils de visualisation interactifs pour examiner ces corrélations en détail et explorer les tendances dans le temps et par pays.
        
        Naviguez entre les onglets pour explorer les différentes perspectives et obtenir des insights sur la situation mondiale du cancer.
    """)
    st.subheader("Explorer les Jeux de Données")
    dataset_name = st.selectbox("Choisissez un jeu de données", 
                            ("01 - Nombre annuel de décès par cause", 
                            "02 - Décès par cancer par type", 
                            "03 - Taux de mortalité par cancer par âge", 
                            "04 - Part de la population avec types de cancer", 
                            "05 - Part de la population avec cancer", 
                            "06 - Nombre de personnes avec cancer par âge", 
                            "07 - Part de la population avec cancer par âge", 
                            "08 - Taux de charge de la maladie par types de cancer", 
                            "09 - Taux de mortalité par cancer et indice standardisé selon l'âge"))

    # Charger le jeu de données sélectionné
    if dataset_name == "01 - Nombre annuel de décès par cause":
        df_selected = df_annual_deaths
    elif dataset_name == "02 - Décès par cancer par type":
        df_selected = df_total_cancer_deaths_by_type
    elif dataset_name == "03 - Taux de mortalité par cancer par âge":
        df_selected = df_cancer_death_rates_by_age
    elif dataset_name == "04 - Part de la population avec types de cancer":
        df_selected = df_share_of_population_with_cancer_types
    elif dataset_name == "05 - Part de la population avec cancer":
        df_selected = df_share_of_population_with_cancer
    elif dataset_name == "06 - Nombre de personnes avec cancer par âge":
        df_selected = df_number_of_people_with_cancer_by_age
    elif dataset_name == "07 - Part de la population avec cancer par âge":
        df_selected = df_share_of_population_with_cancer_by_age
    elif dataset_name == "08 - Taux de charge de la maladie par types de cancer":
        df_selected = df_disease_burden_rates_by_cancer_types

# Filtres basés sur les colonnes du jeu de données sélectionné
    if not df_selected.empty:
        st.write("Filtres (sélectionnez les options pour filtrer les données) :")
        # Exemple de filtre par année (ajustez en fonction des colonnes disponibles)
        if 'Year' in df_selected.columns:
            years = st.multiselect('Année', df_selected['Year'].unique())
            df_selected = df_selected[df_selected['Year'].isin(years)] if years else df_selected

        # Afficher les données filtrées
        st.write("Aperçu des données filtrées :")
        st.dataframe(df_selected)

with tab2:
    st.header("Carte Interactive Mondiale")
    # Code pour la carte interactive

with tab3:
    st.header("Analyse par Région")
    # Code pour l'analyse par région

with tab4:
    st.header("Analyse Approfondie par Pays")
    # Code pour l'analyse approfondie par pays


# Fonction principale de l'app
def main():
    
    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)


    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

# Exécution de l'app
if __name__ == "__main__":
    main()
