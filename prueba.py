from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5432/coolstat')
with engine.connect() as connection:
    print("Connected to the database")
    