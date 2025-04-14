import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Simulamos datos de un mediocampista
categories = ["Key Passes", "Prog Passes", "Duels%", "Def Actions", "Carrying", "Fwd Passes", "Fwd Pass%"]
values = np.random.rand(len(categories)) * 100  # Valores aleatorios normalizados al 100

# Crear DataFrame
df = pd.DataFrame(dict(theta=categories, r=values))

# Crear gráfico de radar con Plotly
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fillcolor='rgba(50, 150, 255, 0.3)', line=dict(color='blue'))  # Color de relleno y línea
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False
)

# Interfaz en Streamlit
st.title("📊 Comparación de jugadores")
st.write("Introduce el nombre del jugador y visualiza sus estadísticas.")
player_name = st.text_input("Nombre del jugador", "Ejemplo")
st.plotly_chart(fig)
