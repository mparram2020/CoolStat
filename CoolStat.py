from io import BytesIO
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, to_rgba
from matplotlib.lines import Line2D
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, Sbopen
from statsbombpy import sb
from scipy.stats import gaussian_kde
import plotly.express as px
import plotly.graph_objects as go
import ast

# Configuración de la página
st.set_page_config(page_title="CoolStat", page_icon="logo.png", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    try:
        eurocopa = pd.read_csv("data/eurocopa_datos.csv")
        copa_america = pd.read_csv("data/copa_america_datos.csv")
        return eurocopa, copa_america
    
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Cargar alineaciones
@st.cache_data
def load_lineups():
    try:
        if selected_competition == "UEFA Euro":
            lineups = pd.read_csv("data/euro_lineups.csv")
        else:
            lineups = pd.read_csv("data/copa_america_lineups.csv")
        
        return lineups

    except FileNotFoundError as e:
        st.error(f"Error loading lineups: {e}")
        st.stop()

@st.cache_data
def load_events(selected_competition):
    try:
        if selected_competition == "UEFA Euro":
            events = pd.read_csv("data/euro_all_events.csv", low_memory=False)
        else:
            events = pd.read_csv("data/copa_america_all_events.csv", low_memory=False)
        
        return events
    
    except FileNotFoundError as e:
        st.error(f"Error loading events: {e}")
        st.stop()

# Menú lateral
st.sidebar.header("🏆 Football Championships")

eurocopa, copa_america = load_data()

# Renombrar competiciones
eurocopa["competition"] = eurocopa["competition"].replace("Europe - UEFA Euro", "UEFA Euro")
copa_america["competition"] = copa_america["competition"].replace("South America - Copa America", "Copa América")
    
# Lista de competiciones disponibles
competition_list = (
    eurocopa["competition"].unique().tolist() + copa_america["competition"].unique().tolist()
)
selected_competition = st.sidebar.selectbox("Select a competition", competition_list)

# Selección de equipos según la competición elegida
df_selected = eurocopa if selected_competition in eurocopa["competition"].unique() else copa_america
    
# Lista de equipos ordenada alfabéticamente
team_list = sorted(df_selected["home_team"].unique().tolist())
selected_team = st.sidebar.selectbox("Select a team", team_list)

# Crear nueva columna con los equipos del partido
eurocopa["match_teams"] = "(" + eurocopa['competition_stage'] + ") " + eurocopa["home_team"] + " " + eurocopa['home_score'].astype(str) + " - " + eurocopa['away_score'].astype(str) + " " + eurocopa["away_team"]
copa_america["match_teams"] = "(" + copa_america['competition_stage'] + ") " + copa_america["home_team"] + " " + copa_america['home_score'].astype(str) + " - " + copa_america['away_score'].astype(str) + " " + copa_america["away_team"]

# Filtrar partidos donde el equipo haya jugado
team_matches = df_selected.loc[(df_selected["home_team"] == selected_team) | (df_selected["away_team"] == selected_team)]

# Ver partidos del equipo seleccionado
df_selected_match = st.sidebar.selectbox("Select a match", team_matches["match_teams"].unique())
match_details = team_matches[team_matches["match_teams"] == df_selected_match]


@st.cache_data
def load_passes(match_id):
    # Obtener los eventos del partido seleccionado
    events = load_events(selected_competition)
    passes = events[(events["type"] == "Pass") & (events["match_id"] == match_id)].copy()
    
    # Convertir strings a listas (más seguro con ast.literal_eval)
    passes['location'] = passes['location'].apply(lambda loc: ast.literal_eval(loc) if isinstance(loc, str) else loc)
    passes['pass_end_location'] = passes['pass_end_location'].apply(lambda loc: ast.literal_eval(loc) if isinstance(loc, str) else loc)

    # Filtrar valores válidos
    passes = passes[passes['location'].notnull() & passes['pass_end_location'].notnull()]

    # Separar coordenadas
    passes[['x', 'y']] = pd.DataFrame(passes['location'].tolist(), index=passes.index)
    passes[['pass_end_x', 'pass_end_y']] = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index)

    return passes

@st.cache_data
def filter_passes(player, match_id):
    passes = load_passes(match_id)

    # Eliminar los saques de banda
    passes = passes[passes["pass_type"] != "Throw-in"]

    # Filtrar los pases del jugador
    player_passes = passes[passes["player"] == player]

    # Dividir en exitosos y fallidos
    successful_passes = player_passes[player_passes["pass_outcome"].isnull()]  # Exitosos tienen outcome "nan"
    unsuccessful_passes = player_passes[player_passes["pass_outcome"].notnull()]  # Fallidos tienen outcome "Incomplete"

    return successful_passes, unsuccessful_passes





@st.cache_data
def pass_map(player, match_id):
    # Obtener los pases del jugador
    successful_passes, unsuccessful_passes = filter_passes(player, match_id)

    # Dibujar el campo de fútbol
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b')
    fig, ax = pitch.draw(figsize=(14, 9), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('white')

    # Dibujar flechas para los pases exitosos
    pitch.arrows(successful_passes["x"], successful_passes["y"],
                 successful_passes["pass_end_x"], successful_passes["pass_end_y"],
                 width=3, headwidth=5, headlength=5, color="green", ax=ax, label='Successful passes')

    # Dibujar flechas para los pases fallidos
    pitch.arrows(unsuccessful_passes["x"], unsuccessful_passes["y"],
                 unsuccessful_passes["pass_end_x"], unsuccessful_passes["pass_end_y"],
                 width=3, headwidth=5, headlength=5, color="red", ax=ax, label='Unsuccessful passes')

    # Leyenda
    ax.legend(facecolor='white', handlelength=4, edgecolor='black', fontsize=13, loc='upper left', bbox_to_anchor=(-0.01, 1.055))

    # Título
    ax.set_title(f"{player}'s Passes", x=0.5, y=1.075, fontsize=22, color='black')

    st.pyplot(fig)


@st.cache_data
def filter_pass_network(team, match_id):
    parser = Sbopen()
    df, related, freeze, tactics = parser.event(match_id)  # ID del partido

    # Filtrar equipo
    df = df[df['team_name'] == team]

    # Filtrar pases
    passes = df[df['type_name'] == 'Pass']
    passes = passes[['id','minute','player_id','player_name','x','y','end_x', 'end_y',
                    'pass_recipient_id','pass_recipient_name','outcome_id','outcome_name']]

    # Filtrar pases exitosos antes del primer cambio
    successful = passes[passes['outcome_name'].isnull()]
    subs = df[df['type_name'] == 'Substitution']['minute']
    firstSub = subs.min()
    successful = successful[successful['minute'] < firstSub]

    # Obtener dorsales y apodos
    df_lineup = parser.lineup(match_id)
    jersey_data = df_lineup[['player_id', 'player_nickname', 'jersey_number']]

    # Añadir jersey del pasador
    successful = pd.merge(successful, jersey_data, on='player_id')
    successful.rename(columns={'jersey_number': 'passer'}, inplace=True)

    jersey_data = jersey_data.rename(columns={'player_id': 'pass_recipient_id'})
    successful = pd.merge(successful, jersey_data, on='pass_recipient_id')
    successful.rename(columns={'jersey_number': 'recipient'}, inplace=True)

    # Crear diccionario dorsal-nombre
    dorsal_to_name = dict(zip(successful['passer'], successful['player_nickname_x']))

    # Media de las ubicaciones
    average_locations = successful.groupby('passer').agg({'x': 'mean', 'y': 'mean', 'id': 'count'})
    average_locations.rename(columns={'id': 'count'}, inplace=True)

    # Pases entre jugadores
    pass_between = successful.groupby(['passer', 'recipient']).id.count().reset_index()
    pass_between.rename(columns={'id': 'pass_count'}, inplace=True)

    # Añadir ubicaciones
    pass_between = pd.merge(pass_between, average_locations, on='passer')
    average_locations_end = average_locations.rename_axis('recipient').reset_index()
    pass_between = pd.merge(pass_between, average_locations_end, on='recipient', suffixes=['', '_end'])

    pass_between = pass_between[pass_between['pass_count'] > 1]

    return pass_between, average_locations, dorsal_to_name


def pass_network(team, match_id):
    # Obtener los pases del equipo
    pass_between, average_locations, dorsal_to_name = filter_pass_network(team, match_id)

    # Dibujar el campo
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor("#22312b")

    # Dibujar líneas de pase
    pitch.lines(1.2*pass_between.x, 0.8*pass_between.y,
                    1.2*pass_between.x_end, 0.8*pass_between.y_end,
                    lw=pass_between.pass_count * 0.5,
                    color='white', zorder=1, ax=ax)

    # Dibujar nodos
    pitch.scatter(1.2*average_locations.x, 0.8*average_locations.y,
                    s=40*average_locations['count'].values, color='red',
                    edgecolors='black', linewidth=1, ax=ax, zorder=1)

    # Añadir dorsales y nombres
    for index, row in average_locations.iterrows():
        x = 1.2 * row.x
        y = 0.8 * row.y

        # Dorsal
        pitch.annotate(index, xy=(x, y), c='white', va='center',
                    ha='center', fontweight='bold', size=13, ax=ax)
        
    
    # Añadir leyenda a la derecha con nombres y dorsales
    sorted_dorsals = sorted(dorsal_to_name.keys())
    legend_text = "\n".join([f"{dorsal}: {dorsal_to_name[dorsal]}" for dorsal in sorted_dorsals])
    ax.text(125, 40, legend_text, fontsize=12, color='white', va='center', ha='left', linespacing=2.5)

    # De 0 a 5 pases un color
    # de 6 a 10 otro color, etc

    # Añadir leyenda
    legend_elements = [
        Line2D([0], [0], color='white', lw=4, label='More passes between players (thicker line)'),
        Line2D([0], [0], marker='o', color='white', label='More passes by player (larger node)', markerfacecolor='red', markeredgecolor='black', markersize=12)
    ]
    
    # Leyenda
    ax.legend(handles=legend_elements, loc='upper left', fontsize=12, facecolor='#22312b', edgecolor='white', labelcolor='white', bbox_to_anchor=(0.022, 1))

    # Título
    ax.set_title(f"{team}'s Passing Network", y=1.05, color='white', fontsize=20)

    st.pyplot(fig)


@st.cache_data
def filter_heatmap(team, match_id):
    # Obtener los eventos del partido seleccionado
    events = load_events(selected_competition)

    # Filtrar eventos del partido seleccionado
    match_events = events[events["match_id"] == match_id]

    # Filtrar pases del equipo seleccionado
    team_passes = match_events[(match_events["type"] == "Pass") & (match_events["team"] == team)].copy()

    # Convertir las ubicaciones de los pases a listas
    team_passes['location'] = team_passes['location'].apply(lambda loc: ast.literal_eval(loc) if isinstance(loc, str) else loc)

    # Separar las coordenadas de inicio de los pases
    team_passes[['x', 'y']] = pd.DataFrame(team_passes['location'].tolist(), index=team_passes.index)

    return team_passes


def heatmap(team, match_id):
    # Filtrar los pases del equipo seleccionado
    team_passes = filter_heatmap(team, match_id)

    # Crear el mapa de calor
    fig, ax = plt.subplots(figsize=(8, 6))
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    pitch.draw(ax=ax)

    # Crear kernel density estimation para la localización de inicio del pase
    kde = gaussian_kde([team_passes['x'], team_passes['y']])
    xi, yi = np.mgrid[0:120:100j, 0:80:100j]
    zi = kde(np.vstack([xi.flatten(), yi.flatten()]))

    # Dibujar el mapa de calor
    heatmap = ax.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap='hot', alpha=0.6)

    # Leyenda visual
    norm = Normalize(vmin=zi.min(), vmax=zi.max())
    sm = ScalarMappable(norm=norm, cmap='hot')
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)

    # Texto encima del colorbar
    cbar.ax.text(2.3, 1.05, 'Pass Density', ha='center', va='bottom', fontsize=10, transform=cbar.ax.transAxes)

    # Flecha de dirección de ataque
    ax.annotate('', xy=(70, 83), xytext=(50, 83),
                arrowprops=dict(facecolor='black', width=1, headwidth=4))
    ax.text(60, 85, 'Attacking direction', ha='center', fontsize=8)

    # Título
    ax.set_title(f"{team}'s Passing Heatmap", fontsize=16, color='black')

    # Ejes del campo
    ax.set_xlim(0, 120)
    ax.set_ylim(-10, 90)

    st.pyplot(fig)


@st.cache_data
def filter_shots(team, match_id):
    # Obtener los eventos del partido seleccionado
    events = load_events(selected_competition)

    # Filtrar eventos del partido seleccionado
    match_events = events[events["match_id"] == match_id]

    # Filtrar tiros
    shots = match_events[(match_events["type"] == "Shot") & (match_events["team"] == team)].reset_index(drop=True).copy()

    # Convertir 'location' a listas
    shots['location'] = shots['location'].apply(lambda loc: ast.literal_eval(loc) if isinstance(loc, str) else loc)

    return shots

def shot_map(team, match_id):
    # Obtener los tiros del equipo
    shots = filter_shots(team, match_id)

    # Excluir los penaltis
    shots = shots[shots["shot_type"] != "Penalty"]

    # Crear el campo de fútbol en orientación vertical
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', half=True)
    fig, ax = pitch.draw(figsize=(10, 10), constrained_layout=True, tight_layout=False)

    # Dibujar los tiros
    for shot in shots.to_dict(orient='records'):
        is_goal = shot['shot_outcome'] == 'Goal'

        pitch.scatter(
            x=shot['location'][0],
            y=shot['location'][1],
            ax=ax,
            s=2000 * shot['shot_statsbomb_xg'],  # Tamaño proporcional al xG
            color='green' if is_goal else 'red',  # Verde si es gol, rojo si fallo
            edgecolors='black',
            alpha=1 if is_goal else 0.6,  # Opacidad mayor si es gol
            marker='o' if is_goal else 'x',  # Marcador diferente para goles y no goles
            linewidth=2 if not is_goal else 1,
            zorder=1 if is_goal else 1.5  # Z-order para superposición
        )

    # Leyenda
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Goal', markerfacecolor='green', markeredgecolor='black', markersize=10),
        Line2D([0], [0], marker='x', color='w', label='Miss', markeredgecolor='red', markersize=10),
        #Line2D([0], [0], marker='o', color='w', label='xG: 0.1', markerfacecolor='gray', markersize=7),
        #Line2D([0], [0], marker='o', color='w', label='xG: 0.3', markerfacecolor='gray', markersize=12),
        #Line2D([0], [0], marker='o', color='w', label='xG: 0.5', markerfacecolor='gray', markersize=17),
    ]

    ax.legend(handles=legend_elements, loc='upper left', fontsize=12, facecolor='white', edgecolor='black')

    ax.set_title(f"{team}'s shots", x=0.5, y=1.03, fontsize=17, color='black')
    ax.text(x=0.3, y=0.96, s='Lower xG', fontsize=11, color='white', ha='center', transform=ax.transAxes)
    ax.text(x=0.7, y=0.96, s='Higher xG', fontsize=11, color='white', ha='center', transform=ax.transAxes)  # Texto "Mayor xG" a la derecha de "Menor xG"

    # Círculos entre "Menor xG" y "Mayor xG"
    circle_positions = [0.38, 0.46, 0.54, 0.62]  # Posiciones horizontales
    circle_sizes = [40, 90, 140, 190]
    for pos, size in zip(circle_positions, circle_sizes):
        ax.scatter(x=pos, y=0.97, s=size, facecolor='none', edgecolor='white', transform=ax.transAxes)
    
    # Mostrar el gráfico
    st.pyplot(fig)


def main():
    st.title("⚽ CoolStat Streamlit App")
    
    st.markdown("##### Interactive web page to visualize UEFA Euro and Copa América match data")

    st.subheader(f"📊 {selected_competition} 2024 Statistics")

    # Obtener los eventos del partido seleccionado
    events = load_events(selected_competition)

    # Filtrar eventos del partido seleccionado
    match_id = match_details["match_id"].values[0]
    match_events = events[events["match_id"] == match_id]

    match_report, data_tab, heatmap_tab, pass_map_tab, pass_network_tab, shot_map_tab = st.tabs(['Match Report', 
                                                                                                    'Lineups',
                                                                                                    'Heatmap',
                                                                                                    'Pass Map',
                                                                                                    'Pass Network',
                                                                                                    'Shot Map'])

    # Primera pestaña
    with match_report:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        
        # Resultado y goleadores
        goals = match_events[match_events["shot_outcome"] == "Goal"]  # Filtrar eventos de tipo "Goal"
        own_goals = match_events[match_events["type"] == "Own Goal Against"] # Filtrar eventos de tipo "Own Goal"
        missed_penalties = match_events[(match_events["shot_outcome"] == "Saved") & (match_events["shot_type"] == "Penalty")] # Filtrar penaltis fallados

        # Filtrar goles por equipo
        home_goals = goals[goals["team"] == match_details.iloc[0]["home_team"]]
        away_goals = goals[goals["team"] == match_details.iloc[0]["away_team"]]

        # Filtrar goles en propia puerta
        home_own_goals = own_goals[own_goals["team"] == match_details.iloc[0]["home_team"]]
        away_own_goals = own_goals[own_goals["team"] == match_details.iloc[0]["away_team"]]

        # Filtrar penaltis fallados
        home_missed_penalties = missed_penalties[missed_penalties["team"] == match_details.iloc[0]["home_team"]]
        away_missed_penalties = missed_penalties[missed_penalties["team"] == match_details.iloc[0]["away_team"]]

        # Filtrar goles en la tanda de penaltis
        shootout_goals = match_events[(match_events["shot_outcome"] == "Goal") & (match_events["period"] == 5)]
        home_shootout_goals = shootout_goals[shootout_goals["team"] == match_details.iloc[0]["home_team"]].shape[0]
        away_shootout_goals = shootout_goals[shootout_goals["team"] == match_details.iloc[0]["away_team"]].shape[0]


        col1, col2, col3, col4, col5, col6 = st.columns([1, 0.8, 0.4, 0.4, 0.7, 0.9])
        with col1:
            # Local
            st.markdown(f"<h4 style='text-align: center;'>{match_details.iloc[0]['home_team']}</h4>", unsafe_allow_html=True)
        
        with col2:
            st.image(f"img/{match_details.iloc[0]['home_team']}.jpg", width=80)
            
            # Construir texto para los goles del equipo local
            home_goals_text = ""
            if home_goals.empty and away_own_goals.empty and home_missed_penalties.empty:
                home_goals_text = ""
            else:
                for _, goal in home_goals.iterrows():
                    player = goal["player"]
                    minute = goal["minute"] + 1 if goal["minute"] == 0 else goal["minute"] # Sumar 1 al minuto si fue en los primeros segundos
                    is_penalty = goal["shot_type"] == "Penalty"  # Verificar si el gol fue de penalti
                    penalty_marker = " (p)" if is_penalty else ""
                    home_goals_text += f"⚽ <b>{player}{penalty_marker}</b> - {minute}'<br>"

                for _, own_goal in away_own_goals.iterrows():
                    player = own_goal["player"]
                    minute = own_goal["minute"] + 1 if own_goal["minute"] == 0 else own_goal["minute"] # Sumar 1 al minuto si fue en los primeros segundos
                    home_goals_text += f"🛑 <b>{player}</b> (Own Goal) - {minute}'<br>"

                for _, penalty in home_missed_penalties.iterrows():
                    player = penalty["player"]
                    minute = penalty["minute"] + 1 if penalty["minute"] == 0 else penalty["minute"] # Sumar 1 al minuto si fue en los primeros segundos
                    home_goals_text += f"❌ <b>{player}</b> (Missed Penalty) - {minute}'<br>"

            # Consolidar todo en un único st.markdown
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="margin-top: 30px;"></div>
                    <div style="text-align: left;">
                        <p>{home_goals_text}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <h3 style='text-align: center;'>
                    {match_details.iloc[0]['home_score']} - {match_details.iloc[0]['away_score']}
                </h3>
            """, unsafe_allow_html=True)

            # Mostrar los goles en la tanda de penaltis solo si existen
            if not shootout_goals.empty:
                st.markdown(f"""
                    <h4 style='text-align: center; color: gray;'>
                        ({home_shootout_goals} - {away_shootout_goals})
                    </h4>
                """, unsafe_allow_html=True)
    
        with col5:
            st.image(f"img/{match_details.iloc[0]['away_team']}.jpg", width=80)

            # Construir texto para los goles del equipo visitante
            away_goals_text = ""
            for _, goal in away_goals.iterrows():
                player = goal["player"]
                minute = goal["minute"] + 1 if goal["minute"] == 0 else goal["minute"] # Sumar 1 al minuto si fue en los primeros segundos
                is_penalty = goal["shot_type"] == "Penalty"  # Verificar si el gol fue de penalti
                penalty_marker = " (p)" if is_penalty else ""
                away_goals_text += f"⚽ <b>{player}{penalty_marker}</b> - {minute}'<br>"

            for _, own_goal in home_own_goals.iterrows():
                player = own_goal["player"]
                minute = own_goal["minute"] + 1 if own_goal["minute"] == 0 else own_goal["minute"]
                away_goals_text += f"🛑 <b>{player}</b> (Own Goal) - {minute}'<br>"

            for _, penalty in away_missed_penalties.iterrows():
                player = penalty["player"]
                minute = penalty["minute"] + 1 if penalty["minute"] == 0 else penalty["minute"] # Sumar 1 al minuto si fue en los primeros segundos
                away_goals_text += f"❌ <b>{player}</b> (Missed Penalty) - {minute}'<br>"
            
            # Consolidar todo en un único st.markdown
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="margin-top: 30px;"></div>
                    <div style="text-align: left;">
                        <p>{away_goals_text}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col6:
            # Visitante
            st.markdown(f"<h4 style='text-align: left;'>{match_details.iloc[0]['away_team']}</h4>", unsafe_allow_html=True)

        # Separador
        st.divider()

        st.write("🧍 Home coach: ", match_details.iloc[0]["home_managers"])
        st.write("🧍 Away coach: ", match_details.iloc[0]["away_managers"])
        formatted_date = pd.to_datetime(match_details.iloc[0]["match_date"]).strftime("%d/%m/%Y")
        st.write("📅 Date: ", formatted_date)
        st.write("📣 Referee: ", match_details.iloc[0]["referee"])
        st.write("🏟️ Stadium: ", match_details.iloc[0]["stadium"])


    # Segunda pestaña
    with data_tab:
        # Cargar las alineaciones
        lineups = load_lineups()

        # Filtrar por el partido seleccionado usando match_id y quitar el índice
        match_id = match_details["match_id"].values[0]
        match_lineups = lineups[lineups["match_id"] == match_id]

        # Obtener los nombres de los equipos en el partido
        home_team = match_details["home_team"].values[0]
        away_team = match_details["away_team"].values[0]

        # Separar las alineaciones por equipo
        home_team_lineup = match_lineups[match_lineups["country"] == home_team].sort_values(by="jersey_number")
        away_team_lineup = match_lineups[match_lineups["country"] == away_team].sort_values(by="jersey_number")

        # Jugadores que salieron de inicio
        home_team_starting = home_team_lineup[
            home_team_lineup["positions"].apply(lambda pos: any(d.get("from") == "00:00" for d in eval(pos)))].reset_index(drop=True)

        away_team_starting = away_team_lineup[
            away_team_lineup["positions"].apply(lambda pos: any(d.get("from") == "00:00" for d in eval(pos)))].reset_index(drop=True)

        # Jugadores restantes
        home_team_subs = home_team_lineup[
            home_team_lineup["positions"].apply(lambda pos: not any(d.get("from") == "00:00" for d in eval(pos)))].reset_index(drop=True)
        
        away_team_subs = away_team_lineup[
            away_team_lineup["positions"].apply(lambda pos: not any(d.get("from") == "00:00" for d in eval(pos)))].reset_index(drop=True)

        # Mostrar en columnas
        col1, col2 = st.columns(2)

        with col1:
            #st.image("")
            st.write("")
            st.markdown(f"<h4>{home_team} Starting XI</h4>", unsafe_allow_html=True)
            df = home_team_starting[["jersey_number", "player_name"]]
            st.dataframe(df.set_index("jersey_number"), use_container_width=True)

            st.divider()

            st.markdown("<h4>Substitutes</h4>", unsafe_allow_html=True)
            df = home_team_subs[["jersey_number", "player_name"]]
            st.dataframe(df.set_index("jersey_number"), use_container_width=True)

        with col2:
            st.write("")
            st.markdown(f"<h4>{away_team} Starting XI</h4>", unsafe_allow_html=True)
            df = away_team_starting[["jersey_number", "player_name"]]
            st.dataframe(df.set_index("jersey_number"), use_container_width=True)

            st.divider()

            st.markdown("<h4>Substitutes</h4>", unsafe_allow_html=True)
            df = away_team_subs[["jersey_number", "player_name"]]
            st.dataframe(df.set_index("jersey_number"), use_container_width=True)

    
    # Tercera pestaña
    with heatmap_tab:

        with st.expander("ℹ️ Explanation of the heatmap"):
                         
            st.markdown("""
            Numerical values on the colorbar represent the relative density of passes across different areas of the pitch, calculated using Kernel Density Estimation (KDE).

                Higher values → areas with a higher concentration of passes (more passes started in or near that zone).

                Lower values (closer to 0) → areas with low or no passing activity.
            """)
        
        # Seleccionar equipo para el mapa de calor
        selected_team_for_heatmap = st.radio("Select a team:", [home_team, away_team])
        
        col1, col2, col3 = st.columns([0.3, 0.9, 0.3])
        with col2:
            # Crear el mapa de calor
            heatmap(selected_team_for_heatmap, match_id)


    # Cuarta pestaña
    with pass_map_tab:

        home_team_played = home_team_lineup[
            home_team_lineup["positions"].apply(lambda pos: len(eval(pos)) > 0)
        ]
        
        away_team_played = away_team_lineup[
            away_team_lineup["positions"].apply(lambda pos: len(eval(pos)) > 0)
        ]   

        col1, col2 = st.columns(2)

        with col1:
            local_player_selected = st.selectbox("Home team player", home_team_played["player_name"].tolist())
            st.write("")

            # Mostrar el mapa de pases del jugador local seleccionado
            pass_map(local_player_selected, home_team_played["match_id"].iloc[0])

        with col2:
            away_player_selected = st.selectbox("Away team player", away_team_played["player_name"].tolist())
            st.write("")
            
            # Mostrar el mapa de pases del jugador visitante seleccionado
            pass_map(away_player_selected, away_team_played["match_id"].iloc[0])

        st.warning("⚠️ Throw-ins are not included in the pass maps.")


    # Quinta pestaña
    with pass_network_tab:
        st.info("ℹ️ This passing network shows the connections between the starting players before the first substitution.")

        selected_team = st.radio("Select a team:", [home_team, away_team], key="pass_network_team")

        col1, col2, col3 = st.columns([0.3, 0.9, 0.3])

        with col2:
            pass_network(selected_team, match_id)
        

    # Sexta pestaña
    with shot_map_tab:
        home_team_played = home_team_lineup[
            home_team_lineup["positions"].apply(lambda pos: len(eval(pos)) > 0)
        ]
        
        away_team_played = away_team_lineup[
            away_team_lineup["positions"].apply(lambda pos: len(eval(pos)) > 0)
        ]

        # Explicación del xG
        st.info((
            "ℹ️ xG (Expected Goals) is a metric that estimates the quality of a shot based on various factors such as "
            "distance from goal, angle, and type of shot. A higher xG value indicates a better chance of scoring."
        ))
        
        col1, col2 = st.columns(2)

        with col1:
            st.write("")
            shot_map(home_team, home_team_played["match_id"].iloc[0])
    
        with col2:
            st.write("")
            shot_map(away_team, away_team_played["match_id"].iloc[0])

        st.warning("⚠️ Penalties are not included in the shot maps.")


    # st.divider()
    #with st.expander('ℹ️ Disclaimer & Info'):
    #    st.write('''
    #   - Todos los datos en esta app provienen del repositorio de datos abiertos de StatsBomb.
    #   - Esta app es solo para fines educativos.
    #''')


if __name__ == "__main__":
    main()