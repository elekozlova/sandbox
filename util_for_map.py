import folium


def get_pair_location(list_cities):
    arrs = get_latlong(list_cities)
    new_list = []
    for p, c in zip(arrs, arrs[1:]):
        r = p, c
        new_list.append(r)
    return new_list


def show_map(file):
    cities = get_list_cities(file)

    lat_longs = get_latlong(cities)
    map = folium.Map(location=lat_longs[0], zoom_start = 8, tiles='OpenStreetMap')
    for coordinates in lat_longs:
        folium.Marker(location=coordinates, tooltip="Click here for more", icon=folium.Icon(icon="map-pin", prefix='fa')).add_to(map)

    pair_location = get_pair_location(cities)
    for pair in pair_location:
        line = folium.PolyLine(locations=pair, weight=1, color='blue')
        map.add_child(line)
        map.save("map1.html")

    return "map1.html"
