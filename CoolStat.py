import streamlit as st
import pandas as pd
import requests
import os

# Configuración de la página
st.set_page_config(page_title="CoolStat", page_icon="⚽", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    eurocopa = pd.read_csv("data/eurocopa_datos.csv")
    copa_america = pd.read_csv("data/copa_america_datos.csv")
    return eurocopa, copa_america


# Menú lateral
with st.sidebar.header("🏆 Campeonatos de fútbol"):

    eurocopa, copa_america = load_data()

    eurocopa["competition"] = eurocopa["competition"].replace("Europe - UEFA Euro", "Eurocopa")
    copa_america["competition"] = copa_america["competition"].replace("South America - Copa America", "Copa América")
    
    # Lista de competiciones disponibles
    competition_list = (
        eurocopa["competition"].unique().tolist() + copa_america["competition"].unique().tolist()
    )
    selected_competition = st.sidebar.selectbox("Selecciona una competición", competition_list)

    # st.sidebar.write(f"📌 Has seleccionado: {selected_competition}")

    # Selección de equipos según la competición elegida
    df_selected = eurocopa if selected_competition in eurocopa["competition"].unique() else copa_america
    
    team_list = sorted(df_selected["home_team"].unique().tolist())
    selected_team = st.sidebar.selectbox("Selecciona un equipo", team_list)

    # st.sidebar.write(f"🏅 Has seleccionado: {selected_team}")

    # Crear nueva columna con los equipos del partido
    eurocopa["match_teams"] = "(" + eurocopa['competition_stage'] + ") " + eurocopa["home_team"] + " " + eurocopa['home_score'].astype(str) + " - " + eurocopa['away_score'].astype(str) + " " + eurocopa["away_team"]

    copa_america["match_teams"] = copa_america["home_team"] + " " + copa_america['home_score'].astype(str) + " - " + copa_america['away_score'].astype(str) + " " + copa_america["away_team"]


    # Filtrar partidos donde el equipo haya jugado
    team_matches = df_selected.loc[(df_selected["home_team"] == selected_team) | (df_selected["away_team"] == selected_team)]

    # Ver partidos del equipo seleccionado
    df_selected_match = st.sidebar.selectbox("Selecciona un partido", team_matches["match_teams"].unique())
    match_details = team_matches[team_matches["match_teams"] == df_selected_match]
    



    #with st.expander('ℹ️ Disclaimer & Info'):
    #    st.write('''
    #    - Todos los datos en esta app provienen del repositorio de datos abiertos de StatsBomb.
    #    - Esta app es solo para fines educativos.
    #    ''')

def main():
    st.title("⚽ CoolStat Streamlit App")
    st.markdown("##### Página web interactiva para visualizar datos de partidos de la Eurocopa y la Copa América")

    st.subheader(f"📊 Estadísticas de la {selected_competition}")
    "\n"

    match_report, data_tab, heatmap_tab, passing_network_tab = st.tabs(['Informe del partido', 
                                                         'Lista de jugadores',
                                                         'Mapa de calor',
                                                         'Red de pases',])

    with match_report:
        st.write(f"Partidos de {selected_team}:")
        st.write(team_matches)

if __name__ == "__main__":
    main()
