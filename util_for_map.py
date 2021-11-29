import io

import folium
from typing import List

from db import get_list_cities, get_latlon


def get_pair_cities(lst: List):
    pair_cities = []
    for p, c in zip(lst, lst[1:]):
        r = p, c
        pair_cities.append(r)
    return pair_cities


def get_pair_location(lst: List):
    new_list = []
    for p, c in zip(lst, lst[1:]):
        r = p, c
        new_list.append(r)
    return new_list


def show_map() -> io.BytesIO:
    buffer = io.BytesIO()

    cities = get_list_cities()
    lat_longs = get_latlon()
    if len(lat_longs) != 0:
        map_ = folium.Map(location=lat_longs[0], zoom_start=10, tiles='OpenStreetMap')
        for coordinates in lat_longs:
            folium.Marker(location=coordinates,  tooltip="Click here for more",
                          icon=folium.Icon(icon="map-pin", prefix='fa')).add_to(map_)

        pair_location = get_pair_location(lat_longs)

        for pair in pair_location:
            line = folium.PolyLine(locations=pair, weight=2, color='blue')
            map_.add_child(line)
        map_.save(buffer, close_file=False)
    else:
        map_ = folium.Map(location=(53.9000000, 27.5666700), zoom_start=10, tiles='OpenStreetMap')
        folium.Marker(location=(53.9000000, 27.5666700),
                      icon=folium.Icon(icon="map-pin", prefix='fa')).add_to(map_)
        map_.save(buffer, close_file=False)

    buffer.seek(0)

    return buffer
