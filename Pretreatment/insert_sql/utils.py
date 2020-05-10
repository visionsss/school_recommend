import pandas as pd
import sqlite3


def connect_sql(path='../../db.sqlite3') -> (sqlite3.connect, sqlite3.Cursor):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    return conn, c


def read_csv(path, index=False, encoding='utf-8') -> pd.DataFrame:
    if not index:
        df = pd.read_csv(path, encoding=encoding)
    else:
        df = pd.read_csv(path, index_col=0, encoding=encoding)
    return df

