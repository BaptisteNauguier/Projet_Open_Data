import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import openpyxl as xl

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
df_iso_convert = pd.read_excel(data_path + 'ISO_Convert.xlsx')  # Assurez-vous que le chemin est correct

# Fusion des données de mortalité avec les informations de continent
df_merged = pd.merge(df_annual_deaths, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
df_merged.drop('ISO', axis=1, inplace=True)

# Fonction pour le traitement des données pour le graphique
def prepare_data_for_graph(df, continent=None):
    # Filtrer par continent si spécifié
    if continent:
        df_filtered = df[df['Continent'] == continent]
    else:
        df_filtered = df

    # Calcul des totaux par continent
    cols_of_interest = df_filtered.columns[4:-1]  # Colonnes de causes de décès
    df_deaths_by_continent = df_filtered.groupby('Continent')[cols_of_interest].sum()

    # Calcul des proportions
    df_proportions = df_deaths_by_continent.div(df_deaths_by_continent.sum(axis=1), axis=0)
    return df_proportions

def clean_column_names(df):
    # Extraction des noms de maladies à partir des noms de colonnes
    df.columns = [col.split(' - ')[1] if ' - ' in col else col for col in df.columns]
    return df

# Structure de l'application
st.title("Analyse des Données sur le Cancer")

tab1, tab2, tab3, tab4 = st.tabs(["Page d'Accueil", "Carte Interactive Mondiale", "Analyse par Région", "Analyse Approfondie par Pays"])

# Fonction pour générer le graphique en fonction du continent sélectionné
def plot_death_causes_by_continent(df, continent=None):
    if continent:
        df_filtered = df[df['Continent'] == continent]
    else:
        df_filtered = df

    # Calcul des proportions
    cols_of_interest = df_filtered.columns[4:-1]
    df_deaths_by_continent = df_filtered.groupby('Continent')[cols_of_interest].sum()
    df_proportions = df_deaths_by_continent.div(df_deaths_by_continent.sum(axis=1), axis=0)
    # Appliquer la fonction de nettoyage sur le DataFrame
    df_proportions = clean_column_names(df_proportions)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 8))
    df_proportions.T.plot(kind='bar', stacked=True, ax=ax)
    plt.title(f"Proportion des Causes de Décès {'Mondiale' if not continent else 'en ' + continent}")
    plt.ylabel('Proportion')
    plt.xlabel('Causes de Décès')
    plt.legend(title='Continent', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=90)
    # Ajouter les annotations de proportions en pourcentage
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        if height > 0:  # pour éviter d'ajouter des textes sur des barres vides
            ax.annotate(f'{height:.1%}', (x + width/2 + 0.1, y + height + 0.005), ha='center', fontsize=8)  # Taille de police réduite et format en pourcentage
    plt.tight_layout()
    st.pyplot(fig)

    


with tab1:
    st.header("Bienvenue dans l'Analyse des Données sur le Cancer")
    st.write("Description de l'application et informations générales.")

with tab2:
    st.header("Carte Interactive Mondiale")
    # Code pour la carte interactive

with tab3:
    st.header("Analyse par Région")
    # Code pour l'analyse par région
        # Sélecteur de continent
        # Enlever la possiblité de selectionner Nan
    ListCont = list(df_merged['Continent'].unique())
    ListCont = [x for x in ListCont if str(x) != 'nan']
    continent_choice = st.selectbox("Choisissez un continent pour filtrer dessus :", 
                                    ListCont)
    continent_to_filter = None if continent_choice == 'Tous' else continent_choice

    # Affichage du graphique
    plot_death_causes_by_continent(df_merged, continent_to_filter)


with tab4:
    st.header("Analyse Approfondie par Pays")
    # Code pour l'analyse approfondie par pays


# Fonction principale de l'app
def main():
    st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")

    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)

    st.header("Carte Interactive Mondiale")
    # Code pour la carte interactive ici

    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

# Exécution de l'app
if __name__ == "__main__":
    main()
