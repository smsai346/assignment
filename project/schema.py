from pydantic import BaseModel
from typing import List

class PointCreate(BaseModel):
    name: str
    geometry: str  # e.g. "POINT(30 10)"

class PolygonCreate(BaseModel):
    name: str
    geometry: str  # e.g. "POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"

class PointOut(PointCreate):
    id: int

class PolygonOut(PolygonCreate):
    id: int

class MultiplePoints(BaseModel):
    points: List[PointCreate]

class MultiplePolygons(BaseModel):
    polygons: List[PolygonCreate]

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
class LoginSchema(BaseModel):
    username: str
    password: str