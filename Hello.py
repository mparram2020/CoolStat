import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch


st.title("\u26BD CoolStat Streamlit App")
st.subheader("FIlter to any team/player to see all of their shots taken!")

df = pd.read_csv("euros_2024_shot_map.csv")
df = df[df["type"] == "Shot"].reset_index(drop=True)

df['location'] = df['location'].apply(json.loads)

team = st.selectbox("Select a team", df['team'].sort_index().unique(), index=None)
player = st.selectbox("Select a player", df[df['team'] == team]['player'].sort_values().unique(), index=None)

def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]

    if player:
        df = df[df['player'] == player]

    return df


filtered_df = filter_data(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True, pad_top=0.1, pad_bottom=0.1)
fig, ax = pitch.draw(figsize=(10, 7))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = float(x['location'][0]),
            y = float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'red',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
        )
plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
