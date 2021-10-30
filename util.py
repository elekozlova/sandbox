import json
import os
from geopy.geocoders import Nominatim
from geopy import distance
import folium
import mimetypes
from pathlib import Path
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response
import db_points


def create_city(city:str):
    try:
        if os.path.exists("db.json") is False:
            with open("db.json", "w", encoding='utf-8') as db_file:
                json.dump([], db_file)
            with open("db.json", "r", encoding='utf-8') as db_file:
                db = json.load(db_file)
            db.append(city)
            with open("db.json", "w", encoding='utf-8') as db_file:
                json.dump(db, db_file)
        elif os.stat("db.json").st_size == 0:
            with open("db.json", "w", encoding='utf-8') as db_file:
                json.dump([], db_file)
            with open("db.json", "r", encoding='utf-8') as db_file:
                db = json.load(db_file)
            db.append(city)
            with open("db.json", "w", encoding='utf-8') as db_file:
                json.dump(db, db_file)
        else:
            with open("db.json", "r", encoding='utf-8') as db_file:
                db = json.load(db_file)
            db.append(city)
            with open("db.json", "w", encoding='utf-8') as db_file:
                json.dump(db, db_file)
    finally:
        print("it is ok")


def geolocator(*args):
    geolocator = Nominatim(user_agent='API_KEY', timeout=None)
    result = geolocator.geocode(*args)
    return result.latitude, result.longitude


def read_file(file):
    with open(file, "r") as db_file:
        db = json.load(db_file)
        return db


def get_latlongs(file):
    db = read_file(file)
    result = []
    for item in db:
        if db_points.city_exists(item) is True:
            a = db_points.get_coords(item)
            result.append(a)
        else:
            a = geolocator(item)
            db_points.save_point(item, *a)
            result.append(a)
    return result


def get_distance_2_points(locA, locB):
    # use haversine forumla
    city_A = (locA[0], locA[1])
    city_B = (locB[0], locB[1])
    return round(distance.distance(city_A, city_B).km)


def get_all_distance(file):
    arrs = get_latlongs(file)
    result = [get_distance_2_points(*pair) for pair in zip(arrs[1:], arrs)]
    return result


def get_pair(file):
    cities = read_file(file)
    new_list = []
    for p, c in zip(cities, cities[1:]):
        r = p, c
        new_list.append(r)
    return new_list


def get_distance_time(file):
    speed = 70
    list_city = read_file(file)
    cities = get_pair(file)
    distance_km = get_all_distance(file)
    time_lst = []
    for part in distance_km:
        time = round(part / speed)
        time_lst.append(time)
    info = [cities, distance_km, time_lst]
    info_common = [list_city, sum(distance_km), sum(time_lst)]
    response = list(map(list, zip(*info)))
    response_common = info_common + response
    if len(distance_km) == 1:
        return response
    else:
        return response_common


def clear_file(file) -> None:
    open(file, "w").close()


def get_pair_location(file):
    arrs = get_latlongs(file)
    new_list = []
    for p, c in zip(arrs, arrs[1:]):
        r = p, c
        new_list.append(r)
    return new_list



def show_map(file):
    arrs = get_latlongs(file)
    map = folium.Map(location=arrs[0], zoom_start = 8, tiles='OpenStreetMap')
    for coordinates in arrs:
        folium.Marker(location=coordinates, tooltip="Click here for more", icon=folium.Icon(icon="map-pin", prefix='fa')).add_to(map)

    pair_location = get_pair_location(file)
    for pair in pair_location:
        line = folium.PolyLine(locations=pair, weight=1, color='blue')
        map.add_child(line)
        map.save("map1.html")

    return "map1.html"




def apply_cache_headers(response: Response) -> None:
    cache_params = (
        "public",
        "must-revalidate"
    )
    response.headers["Cache-Control"] = ",".join(cache_params)


def static_response(file_name: str) -> Response:
    def get_file_path_safe() -> Path:
        file_path = Path(file_name).resolve()
        if not file_path.is_file():
            raise HTTPException(
                detail=f"file {file_name!r} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return file_path

    def calc_media_type() -> str:
        return mimetypes.guess_type(file_name)[0] or "text/plain"

    file_path = get_file_path_safe()
    media_type = calc_media_type()

    with file_path.open("rb") as stream:
        content = stream.read()
        return Response(content=content, media_type=media_type)

