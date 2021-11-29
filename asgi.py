from fastapi import FastAPI, Response
from util import add_city,  get_route
from db import clear_table, swap_id
from static import apply_cache_headers, static_response
from models import City, SwapInfo
from util_for_map import show_map

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

    return static_response("index.js")


@app.post("/add_city", description="send city as a string")
async def _(city: City):
    city.id = add_city(city.name)

    return city


@app.get("/get_route", description="get all route, km, time and paths of the all route")
async def _():
    result = get_route()

    return result


@app.delete("/del", status_code=204, description="clear the way")
async def _():
    clear_table()


@app.put("/swap", description="swap locations")
async def _(info: SwapInfo):
    swap_id(info.id1, info.id2)
    return {"ok": True}


@app.get("/map", description="show icons on map")
async def _():
    map_io = show_map()

    return Response(content=map_io.read(), media_type="text/html")
