import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Team Comparison", page_icon="logo.png", layout="wide")

st.title("Dashboard de estadísticas")

# Selección de competición
competition = st.radio("Competición", ["Eurocopa", "Copa América"], index=0)

# Selector de estadísticas
selected_stat = st.selectbox("Selecciona una estadística", ["Goals-xG per 90'", "Top Scorers", "Most Asists", "Bundesliga", "Ligue 1"], index=0)

# Mostrar iframe solo si coincide
if selected_stat == "Goals-xG per 90'":
    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Book2_17464506741000/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/Book3_17464790157420/ScatterPlotGoalsxGnormalizedper90?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )

st.info("Este dashboard muestra las estadísticas de goles y xG normalizadas por 90 minutos.")

"""elif selected_stat == "Top Scorers":
    if competition == "Eurocopa":
        components.iframe(
            "",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "",
            width=1800,
            height=600,
            scrolling=True
        )
    st.info("Este dashboard muestra los máximos goleadores de la competición seleccionada.")"""