import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Team Comparison", page_icon="logo.png", layout="wide")

st.title("Dashboard de estadísticas")

# Selección de competición
competition = st.radio("Competición", ["Eurocopa", "Copa América"], index=0)

# Selección de estadística
selected_stat = st.selectbox("Selecciona una estadística", ["Shooting", "Goalkeeping", "Advanced Goalkeeping", "Passing", "Goal Shot Creation"], index=0)

# Mostrar visualizciones según la estadística seleccionada
if selected_stat == "Shooting":
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

    st.info("Explanation of the Shooting dashboard.")

elif selected_stat == "Goalkeeping":
    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Euro_Goalkeeping/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/CopaAmerica_Goalkeeping/GA90-Saves?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    st.info("Explanation of the Goalkeeping dashboard.")

elif selected_stat == "Advanced Goalkeeping":
    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Euro_AdvancedGoalkeeping/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/CopaAmerica_AdvancedGoalkeeping/BarbellPSxG-GA?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )

    st.info("Explanation of the Advanced Goalkeeping dashboard.")

elif selected_stat == "Passing":
    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Euro_Passes/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/CopaAmerica_Passes/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    st.info("Explanation of the Passing dashboard.")


elif selected_stat == "Goal Shot Creation":
    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Euro_GoalAndShotCreation/GCA-SCA90?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/CopaAmerica_GoalAndShotCreation/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    st.info("Explanation of the Goal Shot Creation dashboard.")