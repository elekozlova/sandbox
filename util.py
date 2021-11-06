from geopy.geocoders import Nominatim
from geopy import distance
import db
from models import City, Vector, DistanceAndTime, Route
from typing import Tuple


def get_coords(city: str) -> Tuple[float, float]:
    """Nominatim - geoservice provides coordinates (latitude, longitude) """
    geolocator = Nominatim(user_agent='API_KEY', timeout=None)
    result = geolocator.geocode(city)
    return result.latitude, result.longitude

print(get_coords("London"))
print(get_coords("Minsk"))



def create_city(city: str) -> int:
    """creates a city record with coords, returning id, lat, lon"""
    lat_long = get_coords(city)
    id_ = db.insert_new_point(city, *lat_long)
    id = id_[0][0]
    return id


def calculate_distance(location_a, location_b: Tuple[float, float]) -> int:
    """
    :param location_a:
    :param location_b:
    :return: distance between two cities in km """

    city_a = (location_a[0], location_a[1])
    city_b = (location_b[0], location_b[1])
    return round((distance.distance(city_a, city_b).km), 2)


def get_route():

    list_cities = db.cities_rows()

    cities = [
        City(id=row[0],
             name=row[1],
        )
    for row in list_cities
    ]
    # Show the cities of departure and arrival

    pairs = zip(cities, cities[1:])


    list_latlong = db.get_latlon()
    distance = [calculate_distance(*pair) for pair in zip(list_latlong[1:], list_latlong)]

    SPEED: int = 70
    time = list(map(lambda x: round((x / SPEED), 2), distance))

    items = list(map(list, zip(distance, time)))

    distance_time = [
        DistanceAndTime(
            km=item[0],
            hours=item[1],
        )
        for item in items
    ]
    #Show distances and times between cities of departure and arrival

    vectors = [
        Vector(
            from_=pair[0],
            to=pair[1],
            dt=distance_time[0],
        )
        for pair in pairs
    ]

    total = DistanceAndTime(
        hours=sum(time),
        km=sum(distance),
    )
    # Show distance and time the whole route

    route = Route(
        path=vectors,
        total=total,
    )

    return route