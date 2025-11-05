import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# import statsmodels.api as sm

from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

st.header("Projet d'aménagement de pistes cyclables")

st.sidebar.title("Aménagement de pistes cyclables")

choices =  ["1 Énoncé du projet", "2 Exploration et nettoyage des données", "3 Data Visualisation", "4 Modélisation"]

choice = st.sidebar.radio("Pour le bon suivi du projet, sélectionner le choix par ordre indiqué", choices)

if choice == choices[0]:
    with st.expander("Pour information",  icon="ℹ️", width="stretch"):

        text1 = "L’article L. 228-2 du code de l’environnement impose, à l’occasion des réalisations ou des rénovations des voies urbaines, à l’exception des autoroutes et voies rapides, doivent être mis au point des itinéraires cyclables pourvus d’aménagements prenant la forme de pistes, de bandes cyclables, de voies vertes, de zones de rencontre ou, pour les chaussées à sens unique à une seule file, de marquages au sol, en fonction des besoins et contraintes de la circulation."
        st.markdown(f"**{text1}**")
        
        text2 ="Lorsque la réalisation ou la rénovation de voie vise à créer une voie en site propre destinée aux transports collectifs et que l’emprise disponible est insuffisante pour permettre de réaliser ces aménagements, l’obligation de mettre au point un itinéraire cyclable peut être satisfaite en autorisant les cyclistes à emprunter cette voie, sous réserve que sa largeur permette le dépassement d’un cycliste dans les conditions normales de sécurité prévues au code de la route."
        st.markdown(f"**{text2}**")
 
        st.markdown("""
###### Ce jeu de données d'aménagement de pistes cyclables comprend notamment :

* **le code INSEE de la commune ;**
* **la géolocalisation des aménagements cyclables ;**
* **le type d'aménagement cyclable ;**                    
* **la vitesse de circulation.**
""")
    
    st.markdown("#### Objectif de la problématique")
            
    st.markdown("###### Renforcer la sécurité et le confort des usagers par l'aménagement de pistes cyclables. \
                      Le projet traite uniquement les 20 arrondissements de Paris")
    
    # st.markdown("###### Ce projet est composé de deux datasets.")
    st.markdown("""
                ###### Ce projet est composé de deux datasets.
                * **Dataset 1 : utilisé exclusivement pour extraire les données des emplacements, du nombre de vélos et afficher la représentation graphique d'un arrondissement.** 
                * **Dataset 2 : contient les données du principal projet d'aménagement.**
                """
                )
				
				
    st.markdown("""
    <h4>Le dataset 2</h4>
    <p style="font-size: 17px;">Les données sont issues d’OSM selon un schéma défini. <br>
    La donnée contient l’ensemble des éléments obligatoires attendus dans le schéma national des aménagements cyclables.<br> 
	<a href="https://transport.data.gouv.fr/datasets/amenagements-cyclables-france-metropolitaine/">Obtenir les données aménagement cyclable au format du schéma national.</a> <br>
	<a href="https://geodatamine.fr/">Ou extraire des données OpenStreetMap</a><br>
    Les données Itinéraires cyclables est issue de la base de données libre et ouverte OpenStreetMap (OSM) ©Les contributeurs d'OSM.<br>
    <a href="https://opendata.paris.fr/explore/dataset/amenagements-cyclables/information/">Télechargement du jeu de données.</a>
	</p>
    """, unsafe_allow_html=True)
	
    st.markdown("##### Descriptif de la typologie d’aménagements")
	
	# Installer le module  streamlit[pdf]
    #	pip install streamlit[pdf]
	#   pip install streamlit-pdf-viewer
		
    PDF_PATH = Path("Notice_amenagements_cyclables.pdf")

    if PDF_PATH.exists():
       # 2. Lire le fichier en mode binaire
        with open(PDF_PATH, "rb") as file:
         pdf_data = file.read()
    
       # 3. Créer le bouton de téléchargement
    st.download_button(
        label="Télécharger ce document pour comprendre l'aménagement de pistes cyclables",
		type="primary",
        data=pdf_data,  # Le contenu binaire du fichier
        file_name=PDF_PATH.name,  # Le nom du fichier lors du téléchargement
        mime="application/pdf"  # Le type MIME approprié pour un PDF
    )
	
if choice == choices[1] : 
    st.write("##### Exploration et nettoyage des données")
	
    st.markdown("""
    <h4 style="font-weight: bold; font-size: 17px;">Pour mener à bien cette étude, nous allons : </h3>
    <ol>
    <li> Extraire les données et bien les comprendre </li>
    <li> Réaliser des dataviz explicites </li>
    <li> Enrichir notre jeu de données avec de nouvelles variables </li>
    <li> Faire la modélisation</li>
    <li> Tester le modèle </li>
    </ol>
    """, unsafe_allow_html=True)
	
    ## Lecture du fichier CSV
    df = pd.read_csv("amenagements-cyclables.csv" ,sep=';')
	
    if 'df_orig' not in st.session_state:
        st.session_state['df_orig'] = df
	
    ## Traiter et nettoyage des données
    df['Date export'] = pd.to_datetime(df['Date export'], errors='coerce', utc=True)
	
    df_sorted = df.sort_values(by='Date export', ascending=True)
		
    df['Vitesse maximale autorisée'] = df['Vitesse maximale autorisée'].astype(str)
    df['Vitesse maximale autorisée'] = df['Vitesse maximale autorisée'].str.replace(' km/h', '', regex=False)
    df['Vitesse maximale autorisée'] = pd.to_numeric(df['Vitesse maximale autorisée'], errors='coerce')
       
    df_sorted = df.sort_values(by='Vitesse maximale autorisée', ascending=False)
	
    agree = st.checkbox("VOIR LE JEU DE DONNEES ET LE NOMBRE DE VALEURS MANQUANTES")

    if agree:
        st.dataframe(df.head())
        st.write("...")
        st.dataframe(df.tail())
        
        st.write(f"Nombre de lignes : **{df.shape[0]}**.")
        st.write(f"Nombre de colonnes : **{df.shape[1]}**")
		
        txt = """
##### Les variables quantitatives sont :
**Arrondissement, Vitesse maximale autorisée et Longueur**
"""
        st.markdown(txt)

        txt = """
##### Les variables catégorielles sont :
**Nom, Aménagement, Côté aménagement, Sens, Surface, Bois,  Aménagement temporaire,  Infrastructure bidirectionnelle,  Voie à sens unique, 
Position aménagement**
"""
        st.markdown(txt)
		
        Texte = """
##### Les types d'aménagement qui nous intéressent sont :
* **piste cyclable (séparée physiquement de la chaussée par un terre plein non franchissable**
* **bande cyclable (marquage au sol)**
* **voie piétonne**
* **couloir bus ouvert aux vélos**
* **double-sens cyclable simple (pour la sécurité)**
"""
        st.markdown(Texte)
	
        st.markdown("##### Visualisation des valeurs manquantes par colonne.")
	
# Calcule le nombre de valeurs manquantes par colonne (Series)
        missing_counts = df.isna().sum()

        if missing_counts.sum() == 0:
            st.info("Le DataFrame ne contient aucune valeur manquante (NaN).")
        else:
           # Crée le graphique à barres et capture l'objet Axes
            ax = missing_counts.plot(kind="bar", figsize=(4, 2), color='darkblue')
          
           # Ajoute les titres et labels
            ax.set_title("Nombre de valeurs manquantes par colonne", fontsize=12)
            
            ax.set_ylabel("Nombre de valeurs manquantes", fontsize=10)
            plt.xticks(rotation=90) # Rotation des labels pour plus de lisibilité
    
          # Récupère la Figure (l'objet conteneur) à partir des Axes
            fig = ax.figure
           
            st.pyplot(fig)
    
        st.markdown("""
###### Constat

* **Les colonnes "Nom", "sens", "surface" et "vitesse" contiennent des valeurs manquantes.**
* **Celles-ci vont être remplacées respectivement par leurs modes ("Nom","sens","surface") et la médiane pour la vitesse.**
     """)
    
    df["Nom"]=df["Nom"].fillna(df["Nom"].mode()[0])
    df["Sens"]=df["Sens"].fillna(df["Sens"].mode()[0])
    df["Surface"]=df["Surface"].fillna(df["Surface"].mode()[0])


    df["Date export"]=df["Date export"].fillna(df["Date export"].mode()[0])

    # Médiane "vitesse":
    Vitesse_mediane=df["Vitesse maximale autorisée"].median()

    # Remplacement des NaN par la médiane de "Vitesse":
    df["Vitesse maximale autorisée"] = df["Vitesse maximale autorisée"].fillna(Vitesse_mediane)
	
    if 'df' not in st.session_state:
        st.session_state['df'] = df   # Stocke df de la session
	
	
## Dataviz

if choice == choices[2] :
    if 'df' in st.session_state:
          df = st.session_state['df']		# Récupère df après 
 
    df['Année'] = pd.to_datetime(df['Date export'], errors='coerce').dt.year
	
    # Grouper par année et type d'aménagement
    df_type = df.groupby(['Année', 'Aménagement']).size().reset_index(name='Nombre')

    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 1 </h4>", unsafe_allow_html=True)
    st.write("##### Observation de l'évolution des aménagements de le Ville de Paris de 2015 à 2025")
	
    fig = px.line(
    df_type,
    x='Année',
    y='Nombre',
    color='Aménagement',
    markers=True,
    title="Évolution des aménagements cyclables à Paris par type",
    labels={'Année': 'Année', 'Nombre': 'Nombre d’aménagements'}
    )

    fig.update_layout(legend_title_text='Type d’aménagement', template='plotly_white')

    st.plotly_chart(fig, use_container_width=True)
    
    st.write("###### L'aménagement des pistes cyclables a connu un pic entre 2024 et 2025.")
    
    ## 2ème visu
    
    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 2 </h4>", unsafe_allow_html=True)
    st.write("##### Observation de la répartition des aménagements par arrondissement")
	
    fig = px.bar(
    df.groupby('Arrondissement').size().reset_index(name='Nombre'),
    x='Arrondissement',
    y='Nombre',
    color='Nombre',
    title="Nombre d'aménagements cyclables par arrondissement",
    labels={'Nombre': 'Nombre d’aménagements'},
    height=500
    )

    fig.update_layout(xaxis={'categoryorder':'total descending'}, template='plotly_white')
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("###### Le 12ème arrondissement est celui qui est le plus doté en aménagement cyclable.")
    
    ## 3eme visu
    
    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 3 </h4>", unsafe_allow_html=True)
    st.write("##### Observation de la distribution des vitesses maximales par type d'aménagement.")

    fig = px.histogram( 
    df,
    x='Vitesse maximale autorisée',
    color='Aménagement',
    nbins=20,
    title='Distribution des vitesses maximales autorisées par type d’aménagement',
    labels={'Vitesse maximale autorisée': 'Vitesse (km/h)', 'count': 'Nombre d’aménagements'},
    opacity=0.75
    )
    
    fig.update_layout(
    yaxis_title='Nombre d’aménagements',
    template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.write("###### Les aménagements en zone 30 km/h sont les plus fréquents.")
    
    ## 4eme visu
    
    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 4 </h4>", unsafe_allow_html=True)
    st.write("##### Observation des aménagements selon leur longueur")
    
    fig = px.histogram(
    df,
    x='Longueur',
    nbins=50,
    color='Aménagement',
    title="Distribution des longueurs d'aménagements cyclables",
    labels={'Longueur': 'Longueur (m)', 'count': 'Nombre d’aménagements'},
    opacity=0.75,barmode='overlay'
    )

    fig.update_layout(
    yaxis_title='Nombre d’aménagements',
    xaxis_title='Longueur (m)',
    template='plotly_white',
    bargap=0.1,
    height=500
    )
    st.plotly_chart(fig, use_container_width=True)
 
    st.write("###### Les aménagements fréquents sont les plus courts (moins de 150m).")
    
    ## 5eme visu
    
    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 5 </h4>", unsafe_allow_html=True)
    st.write("##### Observation des aménagements selon leur surface")
	
    fig = px.histogram(
    df,
    x='Surface',
    color='Aménagement',
    title="Distribution des surfaces d'aménagements cyclables",
    labels={'Surface': 'Type de surface', 'count': 'Nombre d’aménagements'},
    opacity=0.75
    )

    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    st.write("###### L'asphate est le revêtement dominant.")
    
    ## 6ème visu
    
    st.markdown("<h4 style='font-weight: bold; font-size: 17px;'>Affichage 6 </h4>", unsafe_allow_html=True)
    st.write("##### Visualisation de la répartion des longueurs d'aménagement selon l'arrondissement et le type d'aménagement")

    fig = px.treemap(
    df,
    path=['Arrondissement', 'Aménagement'],
    values='Longueur',
    title='Treemap des aménagements cyclables par arrondissement et type',
    color='Longueur',
    color_continuous_scale='Viridis'
    )
    
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True)

    st.write("###### Le 12ème arrondissement concentre la plus grande part de la longueur totale des pistes cyclables.")

##  Modelisation

if choice == choices[3] :
    st.write("##### Modélisation")
 
    st.markdown( 
 """
 **Nous avons 'Vitesse maximale autorisée' et 'Longueur' comme variables numériques.**
 **Nous allons afficher un graphique de nuages de points et une droite de régression linéaire afin de vérifier s'il y a une une liaison entre ces deux variables.**
 """
     )
	 
    if 'df_orig' in st.session_state:
        df_orig = st.session_state['df_orig']		# Récupère df_orig
			
		## Tracé de la droite linéaire de variables qualitatives : longueur et vitesse 

        df_orig['Vitesse maximale autorisée'] = df_orig['Vitesse maximale autorisée'].astype(str)
        df_orig['Vitesse maximale autorisée'] = df_orig['Vitesse maximale autorisée'].apply(lambda x : x.split(' km/h')[0])
		
        df_orig['Vitesse maximale autorisée'].replace('non définie', '0', inplace=True)
			
        df_orig['Vitesse maximale autorisée'] = pd.to_numeric(df_orig['Vitesse maximale autorisée'], errors='coerce')
		
        df_orig['Longueur'] = df_orig['Longueur'].round(0).astype(int)

    st.markdown("###### Le temps d'affichage est un peu long, merci de patienter.")
			  
    plt.figure(figsize=[100, 100])
				
    fig = px.scatter(df_orig, x='Longueur', y='Vitesse maximale autorisée', trendline="ols", title="Nuage de points avec Ligne de Tendance Linéaire")
	
    st.plotly_chart(fig, use_container_width=True)
	
    rep = st.checkbox("CONSTAT ET CONCLUSION")
	
    if rep:
        st.markdown(
	"""
	###### D'après le graphique, il n'y a pas de relation linéaire entre les deux variables.
    """	
    )
		
        st.markdown("""
	###### 	Le jeu de données nous apprend par la visualisation de l'évolution de l'aménagement de pistes cyclables de la Ville de Paris.
	**Nous n'avons pas pu modéliser le problème de l'objectif qui est la sécurité dû au manque de données complémentaires.**
	**Par contre, avec le dataset 1, nous avons appris à utiliser les librairies Python Geopandas et Folium pour réaliser la cartographie.** 
    """
	    )
