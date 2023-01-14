import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f"sqlite:///data/exchange.db")


def add_table(table_name, data: dict):
    df = pd.DataFrame(data=data)
    df.to_sql(table_name, con=engine, if_exists="append", index=None)


def get_table(table_name) -> pd.DataFrame:
    df = pd.read_sql_table(table_name, con=engine)
    return df
