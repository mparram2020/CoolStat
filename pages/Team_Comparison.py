import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Team Comparison", page_icon="logo.jpg", layout="wide")

# Selección de competición
competition = st.radio("Select a competition", ["Eurocopa", "Copa América"], index=0)

st.write("")

# Selección de estadística
selected_stat = st.selectbox("Select a statistic", ["Goalkeeping", "Advanced Goalkeeping", "Defensive", 
                                                    "Passing", "Goal Shot Creation", "Shooting"], index=0)

# Mostrar visualizciones según la estadística seleccionada
if selected_stat == "Goalkeeping":
    with st.expander("ℹ️ Explanation of the Goalkeeping dashboard"):
                         
            st.markdown("""
            Scatter plot of the goalkeeper's performance in the Eurocopa and Copa América.
            - The x-axis represents the goals conceeded normalized per 90 minutes
            - The y-axis represents the goalkeeper's saves percentage.
            """)

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
    

elif selected_stat == "Advanced Goalkeeping":
    with st.expander("ℹ️ Explanation of the Advanced Goalkeeping dashboard"):
                         
            st.markdown("""
            Barbell chart that compares the goals conceeded (GA) with the post-shot expected goals (PSxG)
            - A positive value indicates a good performance, while a negative value indicates a poor performance.
            """)

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

elif selected_stat == "Defensive":
    with st.expander("ℹ️ Explanation of the Defensive dashboard"):
            st.markdown("""
            Scatter plot and bar graph of the teams' defensive performance.
            - The scatter plot shows the relationship between tackles done and tackles won.
            - The bar chart shows in which area of the pitch each team has made their tackles.
            """)

    if competition == "Eurocopa":
        components.iframe(
            "https://public.tableau.com/views/Euro_Defensive/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )
    elif competition == "Copa América":
        components.iframe(
            "https://public.tableau.com/views/CopaAmerica_Defensive/Dashboard1?:embed=true&:display_count=yes&:showVizHome=no",
            width=1800,
            height=600,
            scrolling=True
        )


elif selected_stat == "Passing":
    with st.expander("ℹ️ Explanation of the Passing dashboard."):           
        st.markdown("""
                Scatter plot and bar graph of the teams' passing performance.
                - The scatter plot shows the passing accuracy.
                - The bar chart shows the percentage of passes completed in the final third,
                    key passes and passes into the penalty area.
                """)
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
    

elif selected_stat == "Goal Shot Creation":
    with st.expander("ℹ️ Explanation of the Goal Shot Creation dashboard."):
        st.markdown("""
            Scatter plot of the goal shot creation performance of the teams.
            - The x-axis represents the two offensive actions directly leading to a goal
            - The y-axis represents the two offensive actions directly leading to a shot.
            """)

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

elif selected_stat == "Shooting":
    with st.expander("ℹ️ Explanation of the Shooting dashboard."):
        st.markdown("""
            Scatter plot of the shooting performance of the teams.
            - The x-axis represents the expected goals (xG) normalized per 90 minutes.
            - The y-axis represents the goals scored normalized per 90 minutes.
            """)

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

    