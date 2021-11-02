import httpx

url_create_city = "http://localhost:8000/create_city"
url_result = "http://localhost:8000/result"
url_map = "http://localhost:8000/map"
url_del = "http://localhost:8000/del"


add_city1 = 'London'
add_city2 = 'Minsk'
add_city3 = 'Moscow'
add_city4 = 'Milan'


# r = httpx.post(url_create_city, json=add_city1)
# print(r)
# r1 = httpx.post(url_create_city, json=add_city2)
# print(r1)
# r2 = httpx.post(url_create_city, json=add_city3)
# print(r2)
# r3 = httpx.post(url_create_city, json=add_city4)
# print(r3)
# r4 = httpx.get(url_result)
# print(r4)
# print(r4.json())
# show_map = httpx.get(url_map)
r5 = httpx.delete(url_del)
print(r5.json())







