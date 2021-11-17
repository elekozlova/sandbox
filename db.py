import traceback
import os
from contextlib import closing
from typing import List
from typing import Optional
import psycopg2
from dotenv import load_dotenv
import urllib.parse as urlparse
import psycopg2.extras


load_dotenv()

url = urlparse.urlparse(os.environ["DATABASE_URL"])
dbname = url.path[1:]
host = url.hostname
password = url.password
user = url.username
dsn = f"{user=} {password=} {host=} {dbname=}"


def execute_sql(sql: str) -> List[tuple]:
    rows = []
    with closing(psycopg2.connect(dsn)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            connection.commit()

            try:
                if cursor.rowcount:
                    rows = cursor.fetchall()
            except psycopg2.ProgrammingError:
                None

    return rows



def get_latlon() -> Optional[tuple]:
    sql = f"""
        SELECT lat,lon FROM points order by id;
    """

    result = execute_sql(sql)
    return result



def clear_table():
    sql = f"""
        TRUNCATE points restart identity;
    """

    execute_sql(sql)


def get_list_cities():
    sql = f"""
        SELECT address FROM points order by id;
    """
    r = execute_sql(sql)
    result = []
    for row in r:
        result.append(row[0])
    return result


def cities_rows():
    sql = f"""
        SELECT id, address FROM points order by id;
    """
    result = execute_sql(sql)
    return result


def insert_new_point(city: str, lat: float, lon: float):
    sql = f"""
        INSERT INTO points(address, lat, lon)
        VALUES ('{city}', {lat}, {lon} )
        RETURNING id, lat, lon
        ;
    """
    result = execute_sql(sql)
    return result


def create_table() -> None:
    sql = """
        CREATE TABLE IF NOT EXISTS points(
            id serial PRIMARY KEY,
            address TEXT,
            lat FLOAT NOT NULL DEFAULT 0, 
            lon FLOAT NOT NULL DEFAULT 0
        );
    """

    execute_sql(sql)


def drop_table() -> None:
    sql = """
            DROP TABLE IF EXISTS points CASCADE;
        """

    execute_sql(sql)


def swap_id(id1: int, id2: int):
    sql = f"""
    BEGIN;
        UPDATE points SET id = -1 WHERE id = {id1};
        UPDATE points SET id = {id1} where id = {id2};
        UPDATE points SET id = {id2} where id = -1;
    COMMIT; """

    execute_sql(sql)