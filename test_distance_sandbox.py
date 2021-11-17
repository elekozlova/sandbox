import httpx

""" First way testing: Interactive API documentation and exploration web user interfaces:
     http://localhost:8000/docs """


"""Second way testing """


url_add_city = "http://localhost:8000/add_city"
url_get_route = "http://localhost:8000/get_route"
url_map = "http://localhost:8000/map"
url_del = "http://localhost:8000/del"
url_swap = "http://localhost:8000/swap"


add_city1 = {"name": "London"}
add_city2 = {"name": "Minsk"}
add_city3 = {"name": "Moscow"}
add_city4 = {"name": "Milan"}
change = {"id1": 1, "id2": 2}


r = httpx.post(url_add_city, json=add_city1)
print(r)
r1 = httpx.post(url_add_city, json=add_city2)
print(r1)
r2 = httpx.post(url_add_city, json=add_city3)
print(r2)
r3 = httpx.post(url_add_city, json=add_city4)
print(r3)
# r4 = httpx.get(url_result)
# print(r4)
# print(r4.json())
#
# show_map = httpx.get(url_map)
#
# r5 = httpx.delete(url_del)
# print(r5)
#
# change = httpx.post(url_swap, json=change)
# print(change)
# print(change.json())







