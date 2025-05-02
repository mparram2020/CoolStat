import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Ranking", page_icon="logo.png", layout="wide")

st.title("Dashboard de estadísticas")

# No coger directamente la URL de Tableau, sino la URL de la vista pública
tableau_url = "https://public.tableau.com/views/Goles-xG/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no"

# Selector de estadísticas generales de las competiciones
selected_stat = st.selectbox("", ("Liga Española", "Premier League", "Serie A", "Bundesliga", "Ligue 1"), index=0)

if selected_stat == "Liga Española":
    st.write("En esta sección se muestran las estadísticas de goles y xG de los jugadores de la liga española.")
    st.write("Para más información, visita el dashboard interactivo a continuación:")
    # Embed Tableau dashboard

    components.iframe(tableau_url, width=1800, height=600, scrolling=True)

st.write("Este dashboard muestra las estadísticas de goles y xG de los jugadores de la liga española.")