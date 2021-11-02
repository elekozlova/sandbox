from fastapi import FastAPI, Body, Response
from util import create_city, clear_file, show_map, get_distance_time
from util import apply_cache_headers, static_response


app = FastAPI()


@app.get("/")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("index.html")


@app.get("/style")
async def _(response: Response):
    apply_cache_headers(response)

    return static_response("style.css")


@app.get("/js")
async def _(response: Response):
    apply_cache_headers(response)
    return static_response("index.js.js")


@app.post("/create_city")
async def _(city:str = Body(...)):
    create_city(city)
    return {"message": f"add new city {city}"}


@app.get("/result")
async def _():
    distance = get_distance_time("db.json")
    return distance


@app.delete("/del")
async def _():
    clear_file("db.json")
    return {"message": "file delete"}


@app.get("/map")
async def _():
    show_map("db.json")
    return static_response("map1.html")
