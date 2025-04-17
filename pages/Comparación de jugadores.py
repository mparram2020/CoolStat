import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances


categoria = st.pills("Selecciona una posición", ['Portero', 'Defensa', 'Centrocampista', 'Delantero'])

# Simulación de un dataset de jugadores
data = {
    "Player": ["Modric", "De Bruyne", "Pedri", "Kroos", "Bellingham", "Valverde", "Gundogan", "Camavinga"],
    "Key Passes": [85, 90, 75, 80, 78, 70, 82, 68],
    "Prog Passes": [78, 88, 70, 84, 76, 74, 83, 72],
    "Duels%": [65, 55, 60, 58, 72, 76, 61, 74],
    "Def Actions": [70, 60, 68, 66, 74, 79, 63, 75],
    "Carrying": [80, 85, 77, 79, 83, 82, 78, 81],
    "Fwd Passes": [90, 95, 85, 88, 86, 84, 89, 87],
    "Fwd Pass%": [85, 90, 80, 83, 84, 82, 86, 81]
}
df_players = pd.DataFrame(data)
categories = list(data.keys())[1:]

# Normalizamos para similitud
scaler = MinMaxScaler()
normalized_stats = scaler.fit_transform(df_players[categories])
df_norm = pd.DataFrame(normalized_stats, columns=categories)
df_norm["Player"] = df_players["Player"]

# Interfaz Streamlit
st.title("📊 Comparador de Jugadores + Sugerencias de Similares")

col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Jugador 1", df_players["Player"], index=0)
with col2:
    player2 = st.selectbox("Jugador 2", df_players["Player"], index=1)

# Extraer valores
values1 = df_players[df_players["Player"] == player1][categories].values.flatten()
values2 = df_players[df_players["Player"] == player2][categories].values.flatten()

# Crear DataFrame para radar
df_radar = pd.DataFrame({
    "theta": categories,
    player1: values1,
    player2: values2
})

# Plot con Plotly
fig = px.line_polar(df_radar, r=player1, theta="theta", line_close=True, name=player1)
fig.add_scatterpolar(r=values2, theta=categories, fill='toself', name=player2, line=dict(color='orange'))
fig.update_traces(fill='toself')
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True
)
st.plotly_chart(fig)

# Calcular jugadores similares al segundo
selected_vector = df_norm[df_norm["Player"] == player2][categories].values
distances = euclidean_distances(df_norm[categories], selected_vector).flatten()
df_players["Distance"] = distances
df_similar = df_players[df_players["Player"] != player2].sort_values("Distance").head(5)

# Mostrar resultados
st.subheader(f"🔍 Jugadores similares a {player2}")
st.table(df_similar[["Player", "Distance"]])