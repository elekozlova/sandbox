from geopy.geocoders import Nominatim
from geopy import distance
import db
from models import City, Vector, DistanceAndTime, Route
from typing import Tuple

SPEED: int = 700


def get_coords(city: str) -> Tuple[float, float]:
    """Nominatim - geoservice provides coordinates (latitude, longitude)"""
    geolocator = Nominatim(user_agent="API_KEY", timeout=None)
    result = geolocator.geocode(city)
    return result.latitude, result.longitude


def add_city(city: str) -> int:
    """creates a city record with coords, returning id"""
    lat_long = get_coords(city)
    id_ = db.insert_new_point(city, *lat_long)
    id = id_[0][0]
    return id


def calculate_distance(location_a, location_b: Tuple[float, float]) -> int:
    """
    :param location_a: lat and lon of the first  city
    :param location_b: lat and lon of the second  city
    :return: distance between two cities in km"""

    city_a = (location_a[0], location_a[1])
    city_b = (location_b[0], location_b[1])

    return round(distance.distance(city_a, city_b).km, 2)


def get_route():

    list_cities = db.cities_rows()

    cities = [
        City(
            id=row[0],
            name=row[1],
        )
        for row in list_cities
    ]

    pairs_cities = zip(cities, cities[1:])

    list_latlong = db.get_latlon()

    distance = [
        calculate_distance(*pair) for pair in zip(list_latlong[1:], list_latlong)
    ]

    time = list(map(lambda x: round((x / SPEED)), distance))

    path_details = list(map(list, zip(pairs_cities, distance, time)))


    vectors = [
        Vector(
            from_=item[0][0],
            to=item[0][1],
            dt=DistanceAndTime(km=item[1], hours=item[2]),
        )
        for item in path_details
    ]

    total = DistanceAndTime(
        km=round(sum(distance), 2),
        hours=round(sum(time))
    )

    route = Route(
        path=vectors,
        total=total,
    )

    return route
