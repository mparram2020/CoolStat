import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances


# Configuración de la página
st.set_page_config(page_title="Comparación de jugadores", page_icon="logo.png", layout="wide")

@st.cache_data
def load_data():
    try:
        euro_goalkeepers = pd.read_csv("data/euro_goalkeepers_stats.csv")
        euro_players = pd.read_csv("data/euro_players_stats.csv")
        return euro_goalkeepers, euro_players

    except FileNotFoundError as e:
        st.error(f"Error al cargar los datos: {e}")
        st.stop()

st.title("📊 Comparador de Jugadores + Sugerencias de Similares")
st.write("Selecciona la posición de los jugadores a comparar:")

# Cargar los datos
euro_goalkeepers, euro_players = load_data()
euro_stats = pd.concat([euro_goalkeepers, euro_players], ignore_index=True)

# Para porteros
# Añadir una columna llamada GA90, en la que se divide los Goals Conceeded entre los 90s
euro_stats['GA90'] = euro_stats['Goals Conceeded'] / euro_stats['90s']

euro_stats['Touches per 90s'] = euro_stats['Touches'] / euro_stats['90s']

# Para jugadores de campo
# Añadir una columna llamada G90, en la que se divide los Goals entre los 90s
euro_stats['G90'] = euro_stats['Goals'] / euro_stats['90s']


if 'posicion_seleccionada' not in st.session_state:
    st.session_state.posicion_seleccionada = None

# Definimos las posiciones
posiciones = ["Portero", "Defensa", "Centrocampista", "Delantero"]

# Botones para seleccionar la posición
col1, col2, col3, col4 = st.columns(4)

# Usa los botones para actualizar el estado de la sesión
if col1.button("PORTERO", use_container_width=True):
    st.session_state.posicion_seleccionada = "Portero"
elif col2.button("DEFENSA", use_container_width=True):
    st.session_state.posicion_seleccionada = "Defensa"
elif col3.button("CENTROCAMPISTA", use_container_width=True):
    st.session_state.posicion_seleccionada = "Centrocampista"
elif col4.button("DELANTERO", use_container_width=True):
    st.session_state.posicion_seleccionada = "Delantero"

if st.session_state.posicion_seleccionada:
    # Filtrar los jugadores por la posición seleccionada
    if st.session_state.posicion_seleccionada == "Portero":
        jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Goalkeeper")]
    elif st.session_state.posicion_seleccionada == "Defensa":
        jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Defender")]
    elif st.session_state.posicion_seleccionada == "Centrocampista":
        jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Midfielder")]
    elif st.session_state.posicion_seleccionada == "Delantero":
        jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Forward")]

    # Lista de jugadores
    players_names = sorted(jugadores_filtrados["Player"].unique())

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Jugador 1")
        player1 = st.selectbox("Selecciona el Jugador 1", players_names, key="player1")
        # Mostrar estadísticas del jugador 1
        st.dataframe(jugadores_filtrados[jugadores_filtrados["Player"] == player1])
    
    with col2:
        st.subheader("Jugador 2")
        player2 = st.selectbox("Selecciona el Jugador 2", players_names, key="player2")
        st.dataframe(jugadores_filtrados[jugadores_filtrados["Player"] == player2])