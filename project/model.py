from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from .geometry import Geometry

class PointData(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(255))
    geometry = Column(Geometry('POINT'))

class PolygonData(Base):
    __tablename__ = 'polygons'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(255))
    geometry = Column(Geometry('POLYGON'))

