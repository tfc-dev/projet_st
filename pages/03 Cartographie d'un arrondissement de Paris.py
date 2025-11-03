import streamlit as st
import pandas as pd
import shapely
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
import geopandas as gpd
import pandas_geojson as pdg
import folium
from streamlit_folium import st_folium

# pip install streamlit_folium

st.set_page_config(layout="wide")
st.header("Projet de d'aménagement de pistes cyclables")

st.write("### Tracé de la carte du 12ème arrondissement de Paris.")

st.write("**Pour tracer le polygone de Paris 12, on a téléchargé le fichier GeoJSON (Geo_Paris12.geojson) du site Open Data de la Ville de Paris.**") 

geodf_Paris12 = gpd.read_file('Geo_Paris12.geojson', driver='GEOJSON')  # 'Geo_Paris12.geojson' est fourni par Open Data de la Ville de Paris

st.write("**Voici le contenu de ce fichier**")
st.dataframe(geodf_Paris12.head())

## Utilisez WGS 84 (epsg:4326) comme système de coordonnées géographiques

geodf_Paris12 = geodf_Paris12.to_crs(epsg=4326)


# Tracé de la cartographie du 12ème arrdt de Paris à l'aide de la bibliothèque Folium

lat_avg = geodf_Paris12['geometry'].centroid.x.mean()
lon_avg = geodf_Paris12['geometry'].centroid.y.mean()

# Latitude : 48.866667; Longitude : 2.333333 de la ville de Paris

carte = folium.Map([lon_avg, lat_avg], zoom_start=13, tiles="Cartodb dark_matter")   # tiles="OpenStreetMap"

for _, r in geodf_Paris12.iterrows():
    sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.005)  # tolerance=0.005
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "green"})
    folium.Popup(r["l_ar"]).add_to(geo_j)
    geo_j.add_to(carte)

# Insérer les data du fichier Paris12.geojson sur la carte

gdf = gpd.read_file("Paris12.geojson")

gdf = gdf.rename(columns={'Nombre de velos': 'Nb_velos'})

from shapely.geometry import Point

def filter_points_in_district(df, boundaries):
    points = [Point(lon, lat) for lon, lat in zip(df['longitude'], df['latitude'])]
    gdf_points = gpd.GeoDataFrame(df, geometry=points, crs='EPSG:4326')
    # Garder seulement les points dans les limites
    points_in_district = gpd.sjoin(gdf_points, boundaries, predicate='within')

    return points_in_district
	
# df : gdf
# boundaries : geodf_Paris12

gdf_bis = filter_points_in_district(gdf, geodf_Paris12)

folium.GeoJson(
    gdf_bis,
    name="Nombre de vélos et son emplacement"
 ).add_to(carte)

for index, row in gdf_bis.iterrows():
    folium.Marker(
        location=[gdf.iloc[index]['latitude'], gdf.iloc[index]['longitude']], icon=folium.Icon(icon='star'),   
        tooltip = "Nombre de vélos : {} <br> Emplacement : {}".format(row['Nb_velos'], row['Adr_emplacement'])
    ).add_to(carte)

folium.LayerControl().add_to(carte)

st.set_page_config(layout="wide")

# st_folium(carte, width=1024)    

st_folium(carte, width="100%")

txt = """
**Pour ajouter plus de marqueurs, on peut étendre le polygone du 12ème arrondissement en ajoutant une marge.**

**Il faut utiliser la librairie scipy spatial et la méthode ConvexHull. Le codage est plus complexe.**

**Pour des raisons du manque de temps, nous n'avons pas pu le faire.**
"""

st.markdown(txt)

