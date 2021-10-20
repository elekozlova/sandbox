from fastapi import FastAPI, Body
from util import create_city, clear_file, show_map, get_distance_time
from util import apply_cache_headers, static_response
from fastapi.responses import Response



app = FastAPI()


@app.post("/create_city")
async def _(city: str = Body(...)):
    create_city(city)


@app.get("/result")
async def _():
    distance = get_distance_time("db.json")
    return distance


@app.get("/del")
async def _():
    clear_file("db.json")
    return {"message": "file delete"}


@app.get("/map")
async def _():
    show_map("db.json")
    return static_response ("map1.html")


    
   
    
   
















