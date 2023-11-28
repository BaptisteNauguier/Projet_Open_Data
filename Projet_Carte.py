import streamlit as st
import pandas as pd
import plotly.express as px

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

# Fonction principale de l'app
def main():
    st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")
    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)
    dataset_options = ["Taux de mortalité", 
                       "Mortalité par type de cancer", 
                       "Taux de mortalité par âge", 
                       "Prévalence de types de cancer", 
                       "Prévalence du cancer", 
                       "Nombre de personnes avec cancer par âge",
                       "Prévalence du cancer par âge", 
                       "Fardeau de la maladie par types de cancer", 
                       "Taux de mortalité standardisé par âge"]
    dataset_choice = st.sidebar.selectbox("Choisissez le dataset", dataset_options)

    st.header("Carte Interactive Mondiale")

    # Affichage du sous-titre qui décrit le dataset choisi
    st.subheader(dataset_choice)
    
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
        color_col = st.sidebar.selectbox("Choisissez la variable pour la coloration", color_options)

    # Affichage de la ligne plus fine qui décrit la coloration choisie et l'année
    if color_col:
        st.caption(f"Coloration : {color_col} pour l'année {year}")

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

    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

# Exécution de l'app
if __name__ == "__main__":
    main()