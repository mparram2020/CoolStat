import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components


st.title("Dashboard de estadísticas")

# No coger directamente la URL de Tableau, sino la URL de la vista pública
tableau_url = "https://public.tableau.com/views/Goles-xG/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no"


components.iframe(tableau_url, width=1800, height=600, scrolling=True)
st.write("Este dashboard muestra las estadísticas de goles y xG de los jugadores de la liga española.")