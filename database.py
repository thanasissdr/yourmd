import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def set_postgres_db_uri() -> str:
    """
    Returns the database uri to establish the db connection
    """

    host = os.getenv("POSTGRES_DB_HOST")
    db_name = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_DB_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    )

    return connection_string


def _create_engine():
    engine = create_engine(
        set_postgres_db_uri(),
        echo=True,
    )
    return engine


def create_db(txt_file_path: str, column_names: List[str], table_name: str):
    df = pd.read_table(txt_file_path, header=None)
    df.columns = column_names
    df.to_sql(name=table_name, con=_create_engine())


if __name__ == "__main__":

    load_dotenv()

    TEXT_FILEPATH = "./data/phrases.txt"
    COLUMN_NAMES = ["medical_term"]
    TABLE_NAME = "medicalterms"

    create_db(TEXT_FILEPATH, COLUMN_NAMES, TABLE_NAME)
