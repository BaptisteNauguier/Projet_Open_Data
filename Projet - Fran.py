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

def clean_column_names2(df):
    # Extraction des noms de maladies à partir des noms de colonnes
    df.columns = [col.split(' - ')[3] if ' - ' in col else col for col in df.columns]
    return df

# Structure de l'application
st.title("Analyse des Données sur le Cancer")

tab1, tab2, tab3, tab4 = st.tabs(["Page d'Accueil", "Carte Interactive Mondiale", "Analyse par Région", "Analyse Approfondie par Pays"])

# Fonction pour générer le graphique en fonction du continent sélectionné
def PlotRegion(df, continent):
    if continent:
        df_filtered = df[df['Continent'] == continent]
    else:
        df_filtered = df[df['Continent'] == "Asia"]

    # Calcul des proportions
    cols_of_interest = df_filtered.columns[4:-1]
    df_deaths_by_continent = df_filtered.groupby('Continent')[cols_of_interest].sum()
    df_proportions = df_deaths_by_continent.div(df_deaths_by_continent.sum(axis=1), axis=0)
    # Appliquer la fonction de nettoyage sur le DataFrame
    df_proportions = clean_column_names(df_proportions)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 8))
    df_proportions.T.plot(kind='bar', stacked=True, ax=ax)
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

# Fonction pour générer le graphique en fonction du continent sélectionné
def PlotRegionRond(df, continent):
    if continent:
        df_filtered = df[df['Continent'] == continent]
    else:
        df_filtered = df[df['Continent'] == "Asia"]

    # Calcul des proportions
    cols_of_interest = df_filtered.columns[6:-1]
    df_deaths_by_continent = df_filtered.groupby('Continent')[cols_of_interest].sum()
    df_proportions = df_deaths_by_continent.div(df_deaths_by_continent.sum(axis=1), axis=0)
    df_proportions = clean_column_names2(df_proportions)

    # Création du graphique camembert
    fig, ax = plt.subplots(figsize=(8, 8))
    df_proportions.T.plot(kind='pie', subplots=True, ax=ax, autopct='%1.1f%%', startangle=90)
    ax.legend(df_proportions.index, title='Continent', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.axis('equal')  # Assure que le camembert est circulaire
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
    # Récupération de la valeur de l'année du slider
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)

    ## Graphique : Causes de décès par continent _____________________________________________________________
    # Fusion des données de mortalité avec les informations de continent
    df_merged = pd.merge(df_annual_deaths, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)

    # Filtrage des données en fonction de l'année sélectionnée
    df_merged = df_merged[df_merged['Year'] == year]

    # Code pour l'analyse par région
        # Sélecteur de continent
        # Enlever la possiblité de selectionner Nan
    ListCont = list(df_merged['Continent'].unique())
    ListCont = [x for x in ListCont if str(x) != 'nan']
    continent_choice = st.selectbox("Choisissez un continent pour filtrer dessus :", 
                                    ListCont)
    continent_to_filter = None if continent_choice == 'Tous' else continent_choice
    
    st.subheader("Répartition des maladies en "+ continent_choice)
    # Affichage du graphique
    PlotRegion(df_merged, continent_to_filter)

    st.write("Comme on peut le voir la colonne Neoplasms arrive toujours deuxième dans la cause des décès, juste après les maladies cardiovasculaires.")
    
    ## Graphique : Poucentage de la population vivant avec un cancer par continent ________________________________________________
    df_merged = pd.merge(df_share_of_population_with_cancer, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)

    # Filtrage des données en fonction de l'année sélectionnée
    df_merged = df_merged[df_merged['Year'] <= year]
    # Filtrae des données en fonction du continent sélectionné
    df_merged = df_merged[df_merged['Continent'] == continent_choice]

    # Moyenne de la 4ème colonne mise dans la variable Moy
    Moy = df_merged.iloc[:, 3].mean()
    st.subheader("Proportion de la population vivant avec un cancer en "+ continent_choice)
    #Supprime les 2 premières colonnes
    df_merged = df_merged.drop(['Code', 'Entity'], axis=1)
    # Supprime la dernière colonne
    df_merged = df_merged.drop((df_merged.columns[-1]), axis=1)
    # Renome la 2 colonne
    df_merged = df_merged.rename(columns={df_merged.columns[1]: 'Proportion de la population avec un cancer en '+ continent_choice})

    # Groupement par année en moyenne
    Evolution = df_merged.groupby('Year').mean()
    # Faire un graphique en courbe avec les données de la variable df_merged
    fig, ax = plt.subplots(figsize=(10, 8))# Création du graphique
    Evolution.plot(ax=ax) # Affiche le graphique
    plt.ylabel('Proportion') # Nom de l'axe des ordonnées
    plt.xlabel('Année') # Nom de l'axe des abscisses
    plt.legend(bbox_to_anchor=(1.05, 1), loc='lower right') # Légende
    ax.grid() # Affiche la grille
    plt.tight_layout() # Ajuste la taille du graphique
    st.pyplot(fig) # Affiche le graphique

    st.write("Comme on peut le voir, la proportion de la population vivant avec un cancer augmente au fil des années. Actullement, la proportion de la population vivant avec un cancer est de",round(Moy*100,2),"% en", continent_choice,".")

    ## Graphique : Taux de la population vivant avec un cancer par continent _____________________________________________________________
    # Fusion des données de mortalité avec les informations de continent
    df_merged = pd.merge(df_share_of_population_with_cancer_types, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)

    # Filtrage des données en fonction de l'année sélectionnée
    df_merged = df_merged[df_merged['Year'] == year]

    st.subheader("Taux de la population vivant avec un cancer en "+ continent_choice)
    # Affichage du graphique
    PlotRegion(df_merged, continent_to_filter)

    ## Graphique : Taux de mortalité par type de cancer par continent _____________________________________________________________
    # Fusion des données de mortalité avec les informations de continent
    df_merged = pd.merge(df_total_cancer_deaths_by_type, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)

    # Filtrage des données en fonction de l'année sélectionnée
    df_merged = df_merged[df_merged['Year'] == year]

    st.subheader("Taux de mortalité par cancer en "+ continent_choice)
    # Affichage du graphique
    PlotRegion(df_merged, continent_to_filter)

    ## Tableau : Top 3 des cancers les plus mortels par continent _____________________________________________________________
    # Récupère les 3 types de cancer les plus mortels
    df_merged = pd.merge(df_total_cancer_deaths_by_type, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)
    #Selection du continent
    df_Top = df_merged[df_merged['Continent'] == continent_choice]
    # Supprime toutes les années supérieures à l'année sélectionnée
    df_Top = df_Top[df_Top['Year'] <= year] 
    # Supprime les 3 premières colonnes
    df_Top = df_Top.drop(['Code', 'Entity', 'Year'], axis=1)    
    df_Top = df_Top.groupby('Continent').sum()
    # Appliquer la fonction de nettoyage sur le DataFrame
    df_Top=clean_column_names(df_Top)
    # Supprime la 1 premières colonnes
    df_Top = df_Top.drop((df_Top.columns[0]), axis=1)
    # Inverse les colonnes et les lignes
    df_Top = df_Top.T
    # Trie par ordre décroissant
    df_Top = df_Top.sort_values(by=continent_choice, ascending=False)
    # Affiche les 3 premières lignes
    st.subheader("Top 3 des cancers les plus mortels en "+ continent_choice)
    st.write(df_Top.head(3))
    st.write("Comme on peut le voir, le cancer du poumon est le plus mortel ne sont pas les plus commun. La prostate par exemple se soigne très bien.")

    ## Graphique : Taux de mortalité par âge par continent _____________________________________________________________
    # Fusion des données de mortalité avec les informations de continent
    df_merged = pd.merge(df_cancer_death_rates_by_age, df_iso_convert[['ISO', 'Continent']], left_on='Code', right_on='ISO', how='left')
    df_merged.drop('ISO', axis=1, inplace=True)

    # Filtrage des données en fonction de l'année sélectionnée
    df_merged = df_merged[df_merged['Year'] == year]

    st.subheader("Taux de mortalité par âge en "+ continent_choice)
    # Affichage du graphique
    PlotRegionRond(df_merged, continent_to_filter)
    st.write("Comme on peut le voir, le cancer est plus mortel chez les personnes âgées. Surement de pars la faiblesse du système immunitaire. Et la récupération est plus longue.")

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
