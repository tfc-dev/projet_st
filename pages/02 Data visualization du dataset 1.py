import streamlit as st
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px

# import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.header("Projet d'aménagement de pistes cyclables")

df = pd.read_csv('emplacement_nb_velos.csv')
nb_velos_par_arrd = df.groupby(['Arrondissement'])['Nombre total de vélos'].max().reset_index()

st.markdown("#### Affichage graphique du nombre total de vélos par arrondissement")
fig=px.bar(nb_velos_par_arrd, x="Arrondissement", y='Nombre total de vélos')
fig.update_layout(title='Nombre total de vélos par arrondissement')
st.plotly_chart(fig)

st.markdown("###### On constate que le 16ème arrondissement a le plus nombre de vélos.")

st.write("    ")

st.markdown("#### Affichage graphique du nombre de vélos et son emplacement de Paris 12")
st.markdown("##### Il s'agit du nombre total de vélos et d'emplacements du 12ème arrondissement.")
	
df2 = pd.read_csv('Paris12.csv')
fig = px.scatter(df2, x='latitude', y= 'longitude', size="Nombre total de vélos",
                 hover_name='Adr_emplacement', title='Nombre de vélos et son emplacement dans Paris 12')
				 
st.plotly_chart(fig)

