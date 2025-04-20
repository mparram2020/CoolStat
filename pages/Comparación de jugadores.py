import time
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from soccerplots.radar_chart import Radar
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

st.subheader("📊 Comparador de Jugadores + Sugerencias de Similares")
st.write("Selecciona la posición de los jugadores a comparar:")

# Cargar los datos
euro_goalkeepers, euro_players = load_data()
euro_stats = pd.concat([euro_goalkeepers, euro_players], ignore_index=True)

# Redondear los valores de las estadísticas a 2 decimales
# Para porteros
euro_stats['GC/90s'] = (euro_stats['Goals Conceeded'] / euro_stats['90s'])

# Para jugadores de campo
euro_stats['G/90s'] = (euro_stats['Goals'] / euro_stats['90s']).round(2)
euro_stats['Touches/90s'] = (euro_stats['Touches'] / euro_stats['90s']).round(2)
euro_stats['Balls Recovered/90s'] = (euro_stats['Ball Recovered'] / euro_stats['90s']).round(2)
euro_stats['Fouls Committed/90s'] = (euro_stats['Fouls Commited'] / euro_stats['90s']).round(2)
euro_stats['Tackles Won/90s'] = (euro_stats['Tackles Won'] / euro_stats['90s']).round(2)
euro_stats['Tackles Lost/90s'] = (euro_stats['Tackles Lost'] / euro_stats['90s']).round(2)
euro_stats['Interceptions/90s'] = (euro_stats['Interceptions'] / euro_stats['90s']).round(2)
euro_stats['Key Passes/90s'] = (euro_stats['Key Passes'] / euro_stats['90s']).round(2)
euro_stats['Shots/90s'] = (euro_stats['Shots'] / euro_stats['90s']).round(2)
euro_stats['xA/90s'] = (euro_stats['Expected Assists'] / euro_stats['90s']).round(2)
euro_stats['xG/90s'] = (euro_stats['Expected Goals'] / euro_stats['90s']).round(2)
euro_stats['Assists/90s'] = (euro_stats['Assists'] / euro_stats['90s']).round(2)

if 'posicion_seleccionada' not in st.session_state:
    st.session_state.posicion_seleccionada = None

# Botones para seleccionar la posición
col1, col2, col3, col4 = st.columns(4)

# Cambiar el borde del botón
st.markdown("""
    <style>
        div.stButton > button {
            border: 2px solid #566573;
        }
        </style>
    """, unsafe_allow_html=True)

# Usa los botones para actualizar el estado de la sesión
if col1.button("PORTERO", use_container_width=True):
    st.session_state.posicion_seleccionada = "Portero"
if col2.button("DEFENSA", use_container_width=True):
    st.session_state.posicion_seleccionada = "Defensa"
if col3.button("CENTROCAMPISTA", use_container_width=True):
    st.session_state.posicion_seleccionada = "Centrocampista"
if col4.button("DELANTERO", use_container_width=True):
    st.session_state.posicion_seleccionada = "Delantero"

if st.session_state.posicion_seleccionada:
    # Filtrar los jugadores por la posición seleccionada
    if st.session_state.posicion_seleccionada == "Portero":
        df_jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Goalkeeper")]
        params = ["Saves %", "Clean Sheets %", "GC/90s", "Passing Accuracy %", "Touches/90s"]
    
    elif st.session_state.posicion_seleccionada == "Defensa":
        df_jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Defender")]
        params = ["Balls Recovered/90s", "Tackles Won/90s", "Tackles Lost/90s", "Interceptions/90s",
                  "Passing Accuracy %", "Fouls Committed/90s", "Crosses/90s"]

    elif st.session_state.posicion_seleccionada == "Centrocampista":
        df_jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Midfielder")]
        params = ["Passing Accuracy %", "Touches/90s", "Key Passes/90s", "Shots/90s",
                  "Assists/90s", "xA/90s", "xG/90s", "G/90s"]

    elif st.session_state.posicion_seleccionada == "Delantero":
        df_jugadores_filtrados = euro_stats[euro_stats["Pos"].str.contains("Forward")]
        params = ["G/90s", "xG/90s", "Shots/90s", "xA/90s", "Assists/90s", "Touches/90s", "Key Passes/90s"]


    # Lista de jugadores
    players_names = sorted(df_jugadores_filtrados["Player"].unique())

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)


    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Selecciona el Jugador 1", players_names, key="player1")
        df_player1 = df_jugadores_filtrados[df_jugadores_filtrados["Player"] == player1][["Player"] + params].reset_index(drop=True)
        st.dataframe(df_player1.set_index("Player"), use_container_width=True)
    
    with col2:
        # Eliminar el jugador 1 de la lista para evitar selección duplicada
        players_names.remove(player1)
        player2 = st.selectbox("Selecciona el Jugador 2", players_names, key="player2")
        df_player2 = df_jugadores_filtrados[df_jugadores_filtrados["Player"] == player2][["Player"] + params].reset_index(drop=True)
        st.dataframe(df_player2.set_index("Player"), use_container_width=True)
        
    if st.button("Comparar Jugadores", use_container_width=True):
        st.write(f"Comparando a {player1} y {player2}...")
        col1, col2, col3 = st.columns([0.75, 2, 0.75])
        
        # Pausa de 2 segundos
        time.sleep(2)

        df = df_jugadores_filtrados[(df_jugadores_filtrados['Player'] == player1) | (df_jugadores_filtrados['Player'] == player2)].reset_index()

        # Preparar los datos para el radar
        ranges = []
        a_values = []
        b_values = []

        for param in params:
            if param == "Passing Accuracy %" or param == "Saves %" or param == "Clean Sheets %":
                a = 0
                b = 100
            else:
                a = min(df[param])
                b = max(df[param])
                
            # Asegurarse de que el rango no sea (0, 0)
                if a == b:
                    a = 0
                    b = a + 1

                a = a - (a * 0.25)  # Reducir un 25% para el rango mínimo
                b = b + (b * 0.25)  # Aumentar un 25% para el rango máximo

            ranges.append((a, b))

        for x in range(len(df['Player'])):
            if df['Player'][x] == player1:
                a_values = df.loc[x, params].values.tolist()
            if df['Player'][x] == player2:
                b_values = df.loc[x, params].values.tolist()

        values = [a_values, b_values]

        # Configuración del título
        title = dict(
            title_name=player1,
            title_color='#B6282F',
            subtitle_name=st.session_state.posicion_seleccionada,
            subtitle_color='#B6282F',
            title_name_2=player2,
            title_color_2='#344D94',
            subtitle_name_2=st.session_state.posicion_seleccionada,
            subtitle_color_2='#344D94',
            title_fontsize=16,
            subtitle_fontsize=13
        )
        endnote = 'Hecho por Marcos Parra'

        # Crear el radar
        with col2:
            radar = Radar()
            fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values,
                                    radar_color=['#B6282F', '#344D94'],
                                    alphas=[.75, .6], title=title, endnote=endnote, compare=True)

            st.pyplot(fig)


        # Sugerencias de jugadores similares
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.subheader("Sugerencias de jugadores similares")
        
