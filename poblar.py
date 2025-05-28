import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)

# Lista de archivos y nombres de tabla
files_and_tables = [
    ('data/eurocopa_datos.csv', 'eurocopa_datos'),
    ('data/euro_lineups.csv', 'euro_lineups'),
    ('data/euro_all_events.csv', 'euro_all_events'),
    ('data/copa_america_datos.csv', 'copa_america_datos'),
    ('data/copa_america_lineups.csv', 'copa_america_lineups'),
    ('data/copa_america_all_events.csv', 'copa_america_all_events'),
    ('data/euro_players_stats.csv', 'euro_players_stats'),
    ('data/euro_goalkeepers_stats.csv', 'euro_goalkeepers_stats'),
]

for file_path, table_name in files_and_tables:
    if os.path.exists(file_path):
        print(f"Uploading {file_path} to table {table_name}...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='fail', index=False)
        print(f"Table {table_name} populated successfully.")
    else:
        print(f"File {file_path} not found.")

print("Database population complete.")