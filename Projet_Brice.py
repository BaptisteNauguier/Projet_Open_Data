import streamlit as st
import pandas as pd
import plotly.express as px

# Chemin de base pour les fichiers de données
data_path = "./"

# Chargement des données
df_annual_deaths = pd.read_csv(data_path + '01 annual-number-of-deaths-by-cause.csv')
df_cancer_deaths_rate_and_age_standardized_rate_index = pd.read_csv(data_path + '09 cancer-deaths-rate-and-age-standardized-rate-index.csv')

# Fonction pour créer une carte choroplèthe
def plot_choropleth(df, location_col, hover_data, title):
    fig = px.choropleth(
        df,
        locations=location_col,
        color=hover_data[0],  # Colonne pour la couleur
        hover_name=location_col,  # Nom du pays à afficher au survol
        hover_data=hover_data,  # Données supplémentaires à afficher au survol
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="natural earth"
    )
    fig.update_layout(title=title)
    return fig

# Fonction principale de l'app
def main():
    st.title("Analyse Globale des Tendances du Cancer et des Décès (1990-2019)")

    st.sidebar.title("Paramètres")
    year = st.sidebar.slider("Sélectionnez une année", 1990, 2019, 2019)
    dataset_choice = st.sidebar.selectbox("Choisissez le dataset", 
                                          ["Taux de mortalité", "Taux de cancer"])

    st.header("Carte Interactive Mondiale")
    
       # Filtrage des données pour l'année sélectionnée
    if dataset_choice == "Taux de mortalité":
        df_filtered = df_annual_deaths[df_annual_deaths['Year'] == year]
        value_col = 'Deaths - Neoplasms - Sex: Both - Age: All Ages (Number)'  # Mettez à jour avec le nom de colonne correct
    else:
        df_filtered = df_cancer_deaths_rate_and_age_standardized_rate_index[df_cancer_deaths_rate_and_age_standardized_rate_index['Year'] == year]
        value_col = 'Deaths - Neoplasms - Sex: Both - Age: Age-standardized (Rate)'
    
    # Modification des codes de pays
    df_filtered['Code'] = df_filtered['Code'].apply(lambda x: x if isinstance(x, str) and len(x) == 3 else None)

    # Affichage de la carte choroplèthe
    map_fig = plot_choropleth(
        df_filtered,
        location_col='Code',
        hover_data=['Entity', value_col],  # Assurez-vous que ces colonnes existent dans df_filtered
        title=f'{dataset_choice} par pays pour l\'année {year}'
    )
    st.plotly_chart(map_fig)

    st.sidebar.header("À propos")
    st.sidebar.info("Cette application est conçue pour analyser les tendances du cancer et des décès à l'échelle mondiale.")

# Exécution de l'app
if __name__ == "__main__":
    main()