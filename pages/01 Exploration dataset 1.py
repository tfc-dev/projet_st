### Page exploration du dataset1 

import streamlit as st
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
# import plotly.graph_objects as go

st.header("Projet d'aménagement de pistes cyclables")

df = pd.read_csv('stationnement-voie-publique-emplacements.csv', sep=';')

df = df.rename(columns={'Nombre places réelles': 'Nombre total de vélos'})

df['Numéro voie'] =  df['Numéro voie'].fillna("")

df['Numéro voie'] = df['Numéro voie'].astype('str')

df['Numéro voie'] = df['Numéro voie'].apply(lambda x : x.split('.')[0])

# Dataframe uniquement pour les variables retenues

list_columns = ['Régime prioritaire', 'Régime particulier', 'Nombre total de vélos', 'Numéro voie', 'Type voie', 'Nom voie', 'Arrondissement', 'geo_shape', 'geo_point_2d']
df_tmp = (df['Régime prioritaire'] == '2 ROUES') & (df['Régime particulier'] == 'Vélos') & (df['Arrondissement'] <= 20)

df1 = df.loc[df_tmp, list_columns].reset_index(drop=True)

df1['Arrondissement'] = df1['Arrondissement'].astype('str')
df1['Adr_emplacement'] = df1['Numéro voie'] + ' ' + df1['Type voie'] + ' ' + df1['Nom voie'] + ' ' + 'Paris' + ' ' + df1['Arrondissement']

df1['Arrondissement'] = df1['Arrondissement'].astype('int')
df1[['latitude', 'longitude']] = df['geo_point_2d'].str.split(',', expand=True).astype(float)

# On retire les col Numéro voie', 'Type voie', 'Nom voie', 'geo_shape', 'geo_point_2d'
liste = ['Numéro voie', 'Type voie', 'Nom voie', 'geo_shape', 'geo_point_2d']
df1 = df1.drop(liste, axis=1)


st.markdown("#### Dataset d'origine")

st.dataframe(df.head(10))

# Ajout des variables qu'on traite de ce dataset.

st.write(f"Nombre de lignes : **{df.shape[0]}**.")
st.write(f"Nombre de colonnes : **{df.shape[1]}**")

Texte = """
###### Les variables à extraire sont :

* **Régime prioritaire : 2 ROUES**
* **Régime particulier : Vélos**
* **Nombre places réelles : il s'agit du nombre de vélos**
* **Numéro de voie**
* **Type voie**
* **Nom voie**
* **Arrondissement**
* **geo_shape : forme géographique**
* **geo_point_2d : coordonnées géographiques**
"""

st.markdown(Texte)

st.write(f"**Les valeurs manquantes sont traitées implicitement.**")

st.write("**Une variable 'Adr_emplacement' est créée en concaténant les colonnes 'Numéro voie', 'Type voie', 'Nom voie' et 'Arrondissement'**")
st.write("**Voici l'instruction**")
st.write("   df1['Adr_emplacement'] = df1['Numéro voie'] + ' ' + df1['Type voie'] + ' ' + df1['Nom voie'] + ' ' + 'Paris' + ' ' + df1['Arrondissement']")

st.markdown("#### Dataset après extraction des variables dont on a besoin. Sauvegarde ce dataset en 'emplacement_nb_velos.csv'")
st.dataframe(df1.head())

st.write(f"Nombre de lignes : **{df1.shape[0]}**.")
st.write(f"Nombre de colonnes : **{df1.shape[1]}**")

df1.to_csv('emplacement_nb_velos.csv', index=False)

st.markdown(
"""
**Le dataframe, après extraction des variables, nommé df1 contient toutes les données des 20 arrondissements de Paris du dataset1.**

**Il est divisé en sous dataframes par arrondissement comme df_Paris01, df_Paris02 etc.**

**Ces dataframes par arrondissement sont sauvegardés en format CSV (Paris01.csv, Paris02.csv ...** 

**Pour la suite, ces fichiers seront utilisés pour l'exploitation, la data visualisation et la cartographie de chaque arrondissement.**
""" )


## On continue l'exploration et le traitement pour la suite 

# Séparer le dataframe df1 en sous dataframe par arrondissement
df_Paris01 = df1.loc[(df1['Arrondissement'] == 1), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris02 = df1.loc[(df1['Arrondissement'] == 2), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris03 = df1.loc[(df1['Arrondissement'] == 3), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris04 = df1.loc[(df1['Arrondissement'] == 4), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris05 = df1.loc[(df1['Arrondissement'] == 5), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris06 = df1.loc[(df1['Arrondissement'] == 6), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris07 = df1.loc[(df1['Arrondissement'] == 7), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)

df_Paris08 = df1.loc[(df1['Arrondissement'] == 8), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris09 = df1.loc[(df1['Arrondissement'] == 9), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris10 = df1.loc[(df1['Arrondissement'] == 10), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)

df_Paris11 = df1.loc[(df1['Arrondissement'] == 11), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris12 = df1.loc[(df1['Arrondissement'] == 12), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris13 = df1.loc[(df1['Arrondissement'] == 13), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris14 = df1.loc[(df1['Arrondissement'] == 14), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris15 = df1.loc[(df1['Arrondissement'] == 15), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris16 = df1.loc[(df1['Arrondissement'] == 16), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris17 = df1.loc[(df1['Arrondissement'] == 17), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)

df_Paris18 = df1.loc[(df1['Arrondissement'] == 18), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris19 = df1.loc[(df1['Arrondissement'] == 19), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)
df_Paris20 = df1.loc[(df1['Arrondissement'] == 20), ['Nombre total de vélos', 'Adr_emplacement', 'latitude', 'longitude']].reset_index(drop=True)

def save_df_Paris_x():
    df_Paris01.to_csv('./Paris_CSV/Paris01.csv', index=False)
    df_Paris02.to_csv('./Paris_CSV/Paris02.csv', index=False)
    df_Paris03.to_csv('./Paris_CSV/Paris03.csv', index=False)
    df_Paris04.to_csv('./Paris_CSV/Paris04.csv', index=False)
    df_Paris05.to_csv('./Paris_CSV/Paris05.csv', index=False)
    df_Paris06.to_csv('./Paris_CSV/Paris06.csv', index=False)
    df_Paris07.to_csv('./Paris_CSV/Paris07.csv', index=False)
    df_Paris08.to_csv('./Paris_CSV/Paris08.csv', index=False)
    df_Paris09.to_csv('./Paris_CSV/Paris09.csv', index=False)
    df_Paris10.to_csv('./Paris_CSV/Paris10.csv', index=False)
    df_Paris11.to_csv('./Paris_CSV/Paris11.csv', index=False)
    df_Paris12.to_csv('./Paris_CSV/Paris12.csv', index=False)
    df_Paris13.to_csv('./Paris_CSV/Paris13.csv', index=False)
    df_Paris14.to_csv('./Paris_CSV/Paris14.csv', index=False)
    df_Paris15.to_csv('./Paris_CSV/Paris15.csv', index=False)
    df_Paris16.to_csv('./Paris_CSV/Paris16.csv', index=False)
    df_Paris17.to_csv('./Paris_CSV/Paris17.csv', index=False)
    df_Paris18.to_csv('./Paris_CSV/Paris18.csv', index=False)
    df_Paris19.to_csv('./Paris_CSV/Paris19.csv', index=False)
    df_Paris20.to_csv('./Paris_CSV/Paris20.csv', index=False)

    return
	
# Sauvegarde des dataframes créés en CSV
# save_df_Paris_x()

st.markdown("#### Afficher par exemple le contenu du dataframe de Paris 12")
st.dataframe(df_Paris12.head())


st.markdown(
"""
**On choisit au hasard un fichier CSV, Paris12.csv par exemple, et on va générer un fichier de format GeoJSON nommé 'Paris12.geojson'.**
**Ce dernier sera utilisé pour tracer la cartoraphie du 12ème arrondissement à l'aide de la librairie Folium.** 
"""
)


# générer un fichier GeoJSON nommé Paris12.geojson

import pandas_geojson as pdg
geojson = pdg.GeoJSON()

from pandas_geojson.core import Point

for index, row in df_Paris12.iterrows():
    point = Point(geometry=[ row.latitude, row.longitude ], properties={'Nombre de velos': row['Nombre total de vélos'] ,'Adr_emplacement': row.Adr_emplacement,
                                                                        'latitude': float(row.latitude), 'longitude': float(row.longitude)})
    geojson.add_features([point])  # Ajout le point dans le fichier geojson
	
# Sauvegarde du fichier geojson
pdg.save_geojson(geojson,'Paris12.geojson', indent=4)

# Test de Paris12.geojson généré avec Geopandas, utile pour la cartoraphie.
import geopandas as gpd

gdf = gpd.read_file("Paris12.geojson")

# gdf.to_crs(epsg=4326)

gdf = gdf.rename(columns={'Nombre de velos': 'Nb_velos'})

gdf.to_file("Paris12.geojson", driver='GeoJSON')










