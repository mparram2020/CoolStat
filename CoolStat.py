import streamlit as st
import pandas as pd
import requests
import os

# Cargar variables de entorno
API_KEY = os.getenv("FOOTBALL_API_KEY", "3c0b865ba2cb4764b7a049d09e6fe28b")  # Usa una variable de entorno

# Diccionario de ligas con sus códigos
LEAGUES = {
    "🇩🇪 Bundesliga": "BL1",
    "🇪🇸 LaLiga": "PD",
    "🇫🇷 Ligue 1": "FL1",
    "🇬🇧 Premier League": "PL",
    "🇮🇹 Serie A": "SA"
}

@st.cache_data
def get_matches(league_code):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/matches"
    headers = {"X-Auth-Token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return []
    
@st.cache_data
def get_standings(league_code):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    headers = {"X-Auth-Token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("standings", [])
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return []
    


def main():
    st.set_page_config(page_title="CoolStat", page_icon=":soccer:", layout="wide")
    st.title(":soccer: CoolStat Streamlit App")

    # Barra lateral para seleccionar liga
    st.sidebar.header("Top Competitions")
    selected_league = st.sidebar.radio("Select a league", list(LEAGUES.keys()))

    # Obtener código de la liga seleccionada
    league_code = LEAGUES.get(selected_league)

    # Cargar datos según la liga seleccionada
    matches = get_matches(league_code)
    df_matches = pd.DataFrame(matches)

    standings = get_standings(league_code)
    df_standings = pd.DataFrame(standings)

    if df_matches.empty:
        st.warning(f"No se encontraron datos para {selected_league}.")
    else:
        st.write(f"**Partidos de {selected_league}:**")
        st.dataframe(df_matches)

        st.write(f"**Tabla de posiciones de {selected_league}:**")
        st.dataframe(df_standings)