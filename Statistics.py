import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données de sortie
fichier_sortie = "output.xlsx"
df = pd.read_excel(fichier_sortie)

# Barre latérale
st.sidebar.title("Options")

# Filtrer par Date d'opération
min_date_op = df["Date d`opération"].min()
max_date_op = df["Date d`opération"].max()
start_date_op = st.sidebar.date_input("Date de début d'opération", min_value=min_date_op, max_value=max_date_op, value=min_date_op)
end_date_op = st.sidebar.date_input("Date de fin d'opération", min_value=min_date_op, max_value=max_date_op, value=max_date_op)

# Filtrer par Service
services_selectionnes = st.sidebar.multiselect("Sélectionner le(s) service(s)", df["Service"].unique())

# Filtrer par Correspondant
correspondants_selectionnes = st.sidebar.multiselect("Sélectionner le(s) correspondant(s)", df["Correspondant"].unique())

# Appliquer les filtres
df_filtré = df.copy()

if start_date_op is not None and end_date_op is not None:
    start_date_op = pd.to_datetime(start_date_op)
    end_date_op = pd.to_datetime(end_date_op)
    df_filtré = df_filtré[(df_filtré["Date d`opération"] >= start_date_op) & (df_filtré["Date d`opération"] <= end_date_op)]

# Filtrer par Service
if services_selectionnes:
    df_filtré = df_filtré[df_filtré["Service"].isin(services_selectionnes)]

# Filtrer par Correspondant
if correspondants_selectionnes:
    df_filtré = df_filtré[df_filtré["Correspondant"].isin(correspondants_selectionnes)]

# Afficher les données filtrées
st.title("Tableau de bord des suspens")
st.dataframe(df_filtré)

# Statistiques
st.title("Statistiques")

# Initialiser les DataFrames
total_non_corrigé = pd.DataFrame(columns=["Service", "Suspens non corrigés"])

# Total des suspens par service (somme des non corrigés)
total_non_corrigé = df_filtré.copy()
total_non_corrigé = total_non_corrigé.groupby("Service").size().reset_index(name='Total des suspens')
total_non_corrigé.loc[len(total_non_corrigé)] = ['Total', total_non_corrigé["Total des suspens"].sum()]

st.dataframe(total_non_corrigé)

# Add a row for the total sum

# Total des suspens par correspondant (somme des non corrigés)
total_non_corrigé_correspondant = df_filtré.copy()
total_non_corrigé_correspondant = total_non_corrigé_correspondant.groupby("Correspondant").size().reset_index(name='Total des suspens')
total_non_corrigé_correspondant.loc[len(total_non_corrigé_correspondant)] = ['Total', total_non_corrigé_correspondant["Total des suspens"].sum()]

st.dataframe(total_non_corrigé_correspondant)

# Diagramme de dispersion pour Suspens créés vs Suspens corrigés (mensuel)
fig_diagramme_dispersion = px.scatter(df_filtré, x="Date d`opération", y="Service",color="Service" ,title="Suspens créés (mensuel)", labels={"Date d'opération": "Date d'opération", "Service": "Service"})
st.plotly_chart(fig_diagramme_dispersion)

# Diagramme à barres pour le total des SUSPENS par Service
fig_total_non_corrigé = px.bar(
    total_non_corrigé,
    x="Service",
    y="Total des suspens",
    title="Total des SUSPENS par Service",
    labels={"Service": "SUSPENS"},
    text="Total des suspens"
)
st.plotly_chart(fig_total_non_corrigé)

# Diagramme à barres pour le total des SUSPENS par Correspondant
fig_total_non_corrigé_correspondant = px.bar(
    total_non_corrigé_correspondant,
    x="Correspondant",
    y="Total des suspens",
    title="Total des SUSPENS par Correspondant",
    labels={"Correspondant": "SUSPENS"},
    text="Total des suspens"
)
st.plotly_chart(fig_total_non_corrigé_correspondant)

# Diagramme en ligne pour Date d'opération vs Date de valeur
fig_diagramme_en_ligne = px.line(df_filtré, x="Date de valeur", y="Date d`opération", color="Service", title="Date d`opération vs Date de valeur")
st.plotly_chart(fig_diagramme_en_ligne)
