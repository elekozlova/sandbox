from pydantic import BaseModel, Field
from typing import Optional, List


class City(BaseModel):
    id: Optional[int] = Field(None, description="id of city")
    name: str = Field(..., description="city name")


class DistanceAndTime(BaseModel):
    km: float
    hours: float


class Vector(BaseModel):
    from_: City
    to: City
    dt: DistanceAndTime


class Route(BaseModel):
    path: List[Vector]
    total: DistanceAndTime


class SwapInfo(BaseModel):
    id1: int = Field(..., description="id 1")
    id2: int = Field(..., description="id 2")