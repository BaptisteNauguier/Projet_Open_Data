import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
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
df_iso_convert = pd.read_excel(data_path + 'ISO_Convert.xlsx')  

# Fonction pour créer une carte choroplèthe
def plot_choropleth(df, location_col, hover_data, color_col):
    fig = px.choropleth(
        df,
        locations=location_col,
        color=color_col,
        hover_name='Entity',
        hover_data=hover_data,
        color_continuous_scale=px.colors.sequential.Turbo,
        projection="natural earth",
    )
    # Suppression du titre de la légende pour éviter d'avoir un titre trop long
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=""
        )
    )
    return fig

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


# Fonction principale de l'app
def main():
    # Structure de l'application
    st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")

    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)


    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

    tab1, tab2, tab3, tab4 = st.tabs(["Page d'Accueil", "Carte Interactive Mondiale", "Analyse par Région", "Analyse Approfondie par Pays"])


    with tab1:
        st.header("Bienvenue dans l'Analyse des Données sur le Cancer")
        st.write("""

            Cette application offre une analyse approfondie des tendances globales du cancer et des décès associés de 1990 à 2019. 
            Elle est structurée en plusieurs sections, chacune accessible via des onglets :

            # description des onglets

            **L'onglet 2 : Carte Interactive Mondiale**

            **Fonctionnalités :**
            - Visualisation des données à travers une carte choroplèthe mondiale.
            - Sélection d'une année spécifique via un curseur pour afficher les données correspondantes.
            - Choix parmi différents ensembles de données (datasets) pour afficher des informations spécifiques telles que les taux de mortalité, la prévalence du cancer par âge, ou le fardeau de la maladie par types de cancer.

            **Interactivité :**
            - Les utilisateurs peuvent survoler les pays sur la carte pour voir des détails supplémentaires, comme le nombre de décès ou la prévalence du cancer pour le pays et l'année sélectionnés.
            - Une boîte de sélection permet de choisir la variable à utiliser pour la coloration de la carte, offrant une visualisation personnalisée en fonction de la mesure choisie.
            - En cas d'absence de données pour l'année sélectionnée, un message d'erreur informe l'utilisateur et l'invite à choisir une autre année.

           **Onglet 3 : Analyse par Région**

            - Sélection : Choix d'une régions (Amérique, Europe, Asie, etc.) pour des visualisations et analyses spécifiques.
            - Visualisations : Graphiques et tableaux récapitulatifs par régions.
            - Affichage des maladies mortelles
            - Evolution de la moyenne de cancer
            - Répartition personnes vivant avec des cancers
            - Répartition mortes à cause d'un type de cancers
            - Répartition des cancers par tranches d'age

            **Onglet 4 : Analyse Approfondie par Pays**
            - **Exploration** : exploration de différents dataframe avec une ACP (Analyse en Composantes Principales)
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
        elif dataset_name == "09 - Taux de mortalité par cancer et indice standardisé selon l'âge":
            df_selected = df_cancer_deaths_rate_and_age_standardized_rate_index

        # Filtres basés sur les colonnes du jeu de données sélectionné
        if not df_selected.empty:
            st.write("Filtres (sélectionnez les options pour filtrer les données) :")
            # Exemple de filtre par année (ajustez en fonction des colonnes disponibles)
            if 'Year' in df_selected.columns:
                years = st.multiselect('Année', df_selected['Year'].unique())
                df_selected = df_selected[df_selected['Year'].isin(years)] if years else df_selected

            # Calculer le pourcentage de valeurs remplies et nulles pour chaque colonne
            percent_filled = df_selected.notna().mean() * 100
            percent_na = df_selected.isna().mean() * 100
            info_columns = pd.DataFrame({
                'Pourcentage Rempli (%)': percent_filled.round(2),
                'Pourcentage NA (%)': percent_na.round(2),
                'Valeur la Plus Fréquente': df_selected.apply(lambda x: x.value_counts().index[0] if not x.empty else None),
                'Moyenne': df_selected.mean(),
                'Médiane': df_selected.median(),
                'Écart-Type': df_selected.std(),
                'Min': df_selected.min(),
                'Max': df_selected.max()
            }).transpose()


            # Afficher les informations sur les colonnes
            st.write("Informations sur les colonnes :")
            st.dataframe(info_columns)

            # Afficher les données filtrées
            st.write("Aperçu des données filtrées :")
            #st.dataframe(df_selected,column_config = {'Year',format="% .0f"})
            st.dataframe(df_selected.style.format({'Year': lambda x: f"{int(x)}"}))

    with tab2:
        st.header("Carte Interactive Mondiale")
        dataset_options = ["Taux de mortalité", 
                       "Mortalité par type de cancer", 
                       "Taux de mortalité par âge", 
                       "Prévalence de types de cancer", 
                       "Prévalence du cancer", 
                       "Nombre de personnes avec cancer par âge",
                       "Prévalence du cancer par âge", 
                       "Fardeau de la maladie par types de cancer", 
                       "Taux de mortalité standardisé par âge"]
        dataset_choice = st.selectbox("Choisissez le dataset", dataset_options)
        # Code pour la carte interactive
        # Affichage du sous-titre qui décrit le dataset choisi
        # st.subheader(dataset_choice)
        
        # Définition de la variable color_col
        color_col = None

        # Définition des différents datasets et de leur contenu pour hover_data
        if dataset_choice == dataset_options[0]:
            df_filtered = df_annual_deaths[df_annual_deaths['Year'] == year]
            hover_data = ['Deaths - Neoplasms - Sex: Both - Age: All Ages (Number)']
        elif dataset_choice == dataset_options[1]:
            df_filtered = df_total_cancer_deaths_by_type[df_total_cancer_deaths_by_type['Year'] == year]
            hover_data = df_total_cancer_deaths_by_type.columns.tolist()[3:]
        elif dataset_choice == dataset_options[2]:
            df_filtered = df_cancer_death_rates_by_age[df_cancer_death_rates_by_age['Year'] == year]
            hover_data = df_cancer_death_rates_by_age.columns.tolist()[3:]
        elif dataset_choice == dataset_options[3]:
            df_filtered = df_share_of_population_with_cancer_types[df_share_of_population_with_cancer_types['Year'] == year]
            hover_data = df_share_of_population_with_cancer_types.columns.tolist()[3:]
        elif dataset_choice == dataset_options[4]:
            df_filtered = df_share_of_population_with_cancer[df_share_of_population_with_cancer['Year'] == year]
            hover_data = df_share_of_population_with_cancer.columns.tolist()[3:]
        elif dataset_choice == dataset_options[5]:
            df_filtered = df_number_of_people_with_cancer_by_age[df_number_of_people_with_cancer_by_age['Year'] == year]
            hover_data = df_number_of_people_with_cancer_by_age.columns.tolist()[3:]
        elif dataset_choice == dataset_options[6]:
            df_filtered = df_share_of_population_with_cancer_by_age[df_share_of_population_with_cancer_by_age['Year'] == year]
            hover_data = df_share_of_population_with_cancer_by_age.columns.tolist()[3:]
        elif dataset_choice == dataset_options[7]:
            df_filtered = df_disease_burden_rates_by_cancer_types[df_disease_burden_rates_by_cancer_types['Year'] == year]
            hover_data = df_disease_burden_rates_by_cancer_types.columns.tolist()[3:]
        elif dataset_choice == dataset_options[8]:
            df_filtered = df_cancer_deaths_rate_and_age_standardized_rate_index[df_cancer_deaths_rate_and_age_standardized_rate_index['Year'] == year]
            hover_data = df_cancer_deaths_rate_and_age_standardized_rate_index.columns.tolist()[3:]

        # Si il n'y a pas de données pour l'année sélectionnée, afficher un message d'erreur
        if 'df_filtered' in locals():
            if df_filtered.empty:
                st.error(f"Aucune donnée disponible pour l'année {year} dans le dataset sélectionné.")

        # Après avoir défini df_filtered et hover_data pour chaque condition:
        if 'df_filtered' in locals() and not df_filtered.empty:
            color_options = [col for col in hover_data if col not in ['Entity', 'Code']]
            color_col = st.selectbox("Choisissez la variable pour la coloration", color_options)

        # Affichage de la ligne plus fine qui décrit la coloration choisie et l'année
        if color_col:
            # st.caption(f"Coloration : {color_col} pour l'année {year}")

            # Modification des codes de pays
            df_filtered['Code'] = df_filtered['Code'].apply(lambda x: x if isinstance(x, str) and len(x) == 3 else None)

            # Affichage de la carte choroplèthe
            map_fig = plot_choropleth(
                df_filtered,
                location_col='Code',
                hover_data=hover_data,
                color_col=color_col  # Colonne utilisée pour la coloration
            )
            st.plotly_chart(map_fig)

    with tab3:
        st.header("Analyse par Région")
        # Code pour l'analyse par région
        #year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)

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

        # Étape 1 : Choix du fichier CSV
        dataset_name = st.selectbox(
            "Choisissez un jeu de données pour l'ACP",
            ("02 total-cancer-deaths-by-type.csv", "03 cancer-death-rates-by-age.csv", "05 share-of-population-with-cancer.csv", "06 number-of-people-with-cancer-by-age.csv", "07 share-of-population-with-cancer-by-age.csv", "08 disease-burden-rates-by-cancer-types.csv", "09 cancer-deaths-rate-and-age-standardized-rate-index.csv")
        )

        # Étape 2 : Chargement des données CSV
        df = pd.read_csv(data_path + dataset_name)

        # Vérifiez si 'Entity' est dans le DataFrame et définissez-le comme index si nécessaire
        if 'Entity' in df.columns:
            df = df.set_index('Entity')
        
        # Gardez uniquement les colonnes numériques pour l'ACP
        df_numeric = df.select_dtypes(include=[np.number])

        # Si une colonne 'Country' est présente, l'utiliser comme index
        if 'Entity' in df.columns:
            df_numeric = df_numeric.set_index(df['Entity'])
            df_numeric.drop('Entity', axis=1, inplace=True)

        # Étape 3 : Appliquer l'ACP
        pca = PCA(n_components=2)  # Réduction à 2 dimensions
        pca_result = pca.fit_transform(df_numeric.values)

        # Créer un DataFrame avec les résultats de l'ACP
        pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=df_numeric.index)

        # Étape 4 : Afficher le résultat de l'ACP dans un graphique
        fig = px.scatter(pca_df, x='PC1', y='PC2', text=df_numeric.index)
        fig.update_traces(textposition='top center')
        fig.update_layout(height=600, width=800)

        st.plotly_chart(fig)



    
    

# Exécution de l'app
if __name__ == "__main__":
    main()
