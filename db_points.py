import traceback
import os
from contextlib import closing
from typing import List
from typing import Optional
import psycopg2
from dotenv import load_dotenv, find_dotenv
import urllib.parse as urlparse


load_dotenv(find_dotenv())

url = urlparse.urlparse(os.environ["DATABASE_URL"])
dbname = url.path[1:]
host = url.hostname
password = url.password
user = url.username
#port = url.port
dsn = f"{user=} {password=} {host=} {dbname=}"
print (dsn)



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
                return None

    return rows


def get_coords(city: str) -> Optional[tuple]:
    sql = f"""
        SELECT lat,lon FROM points
        WHERE address = '{city}'
        ;
    """
    r = execute_sql(sql)
    try:
        coords = r[0]
    except IndexError:
        return None
    return coords


def city_exists(city: str) -> bool:
    coords = get_coords(city)
    return coords is not None


def insert_new_point(city: str, lat: int, lon: int) -> None:
    sql = f"""
        INSERT INTO points(address, lat, lon)
        VALUES ('{city}', {lat}, {lon} )
        ;
    """
    execute_sql(sql)


def save_point(city: str, lat: int, lon: int) -> None:
    if city_exists(city):
        get_coords(city)
    else:
        insert_new_point(city, lat, lon)


def create_tables() -> None:
    sql = """
        CREATE TABLE IF NOT EXISTS points(
            address TEXT NOT NULL UNIQUE,
            lat FLOAT NOT NULL DEFAULT 0, 
            lon FLOAT NOT NULL DEFAULT 0
        );
    """

    execute_sql(sql)


def drop_tables() -> None:
    sql = """
            DROP TABLE IF EXISTS points CASCADE;
        """

    execute_sql(sql)
