from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from project.database import Base,engine,Sessionlocal
from project import model,schema,crud
from sqlalchemy.orm import Session
from typing import List
import uvicorn


app=FastAPI(title="sample Project", description="This is a sample project", version="1.0.0")
origins=["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
model.Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/points/", response_model=List[schema.PointOut])
async def add_multiple_points(data: schema.MultiplePoints, db: Session = Depends(get_db)):
    return await crud.create_multiple_points(db, data)

@app.get("/points/", response_model=List[schema.PointOut])
async def get_all_points(db: Session = Depends(get_db)):
    return await crud.get_points(db)

@app.post("/polygons/", response_model=List[schema.PolygonOut])
async def add_multiple_polygons(data: schema.MultiplePolygons, db: Session = Depends(get_db)):
    return  await crud.create_multiple_polygons(db, data)

@app.get("/polygons/", response_model=List[schema.PolygonOut])
async def get_all_polygons(db: Session = Depends(get_db)):
    return  await crud.get_polygons(db)