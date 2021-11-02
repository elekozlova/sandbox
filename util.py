from geopy.geocoders import Nominatim
from geopy import distance
import db
from typing import List


def geolocator(*args):
    # API
    geolocator = Nominatim(user_agent='API_KEY', timeout=None)
    result = geolocator.geocode(*args)
    return result.latitude, result.longitude


def create_city(city:str):
    # add city into db with lat and long
    lat_long = geolocator(city)
    db.save_point(city, *lat_long)


def get_distance_2_points(locA, locB):
    # use haversine forumla
    # get distance between two cities
    city_A = (locA[0], locA[1])
    city_B = (locB[0], locB[1])
    return round(distance.distance(city_A, city_B).km)


def get_all_distance():
    # get distance for two and more than two points
    list_latlong = db.get_latlon()
    result = [get_distance_2_points(*pair) for pair in zip(list_latlong[1:], list_latlong)]
    return result


def get_pair_cities(list_cities: List):
    pair_cities = []
    for p, c in zip(list_cities, list_cities[1:]):
        r = p, c
        pair_cities.append(r)
    return pair_cities


def get_distance_time():
    SPEED = 70

    list_city = db.get_list_cities()
    distance_km = get_all_distance()

    time_lst = []
    for part in distance_km:
        time = round(part / SPEED)
        time_lst.append(time)

    cities = get_pair_cities(list_city)
    info = [cities, distance_km, time_lst]
    info_common = [list_city, sum(distance_km), sum(time_lst)]

    response = list(map(list, zip(*info)))
    response_common = info_common + response

    if len(distance_km) == 1:
        return response
    else:
        return response_common
