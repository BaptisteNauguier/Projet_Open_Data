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

# Chargement des données
@st.cache
def load_data():
    return df_share_of_population_with_cancer

data = load_data()

# Titre de l'application
st.title('Analyse de la prévalence du cancer')

# Sélection de l'entité
entity = st.multiselect('Sélectionnez l\'entité (pays ou région):', data['Entity'].unique())

# Filtre des données en fonction de l'entité sélectionnée
filtered_data = data[data['Entity'].isin(entity)]

# Création du graphique en ligne
if not filtered_data.empty:
    fig, ax = plt.subplots()
    for name, group in filtered_data.groupby('Entity'):
        ax.plot(group['Year'], group['Prevalence - Neoplasms - Sex: Both - Age: Age-standardized (Percent)'], label=name)
    ax.set_xlabel('Année')
    ax.set_ylabel('Prévalence du cancer (%)')
    ax.set_title('Tendance de la prévalence du cancer au fil du temps')
    ax.legend()
    st.pyplot(fig)
else:
    st.write('Veuillez sélectionner au moins une entité pour afficher le graphique.')
