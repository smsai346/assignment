from fastapi import FastAPI, Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from project.database import Base,engine,Sessionlocal
from project import model,schema,crud
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from project.database import Base, engine, Sessionlocal
from project.auth import AuthHandler
from typing import List
import bcrypt
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

password = "smsai346"

# # Generate a salt and hash the password
hashed_password = AuthHandler().get_password_hash(password)

def authenticate_user(username: str, password: str):
    # Simulate a dummy user
    dummy_user = {
        "username": "smsai346",
        "password": hashed_password,
        "role": "admin",
        "status": "active"
    }
    
    if username == dummy_user["username"] and AuthHandler().verify_password(password, dummy_user["password"]):
        return dummy_user
    return None

# Define the Login Response model


@app.post("/login", response_model=schema.LoginResponse)
async def login(request:schema.LoginSchema):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate the token using AuthHandler
    token = AuthHandler().encode_token(user_dict={"username": user["username"]})
    
    return {"access_token": token, "token_type": "bearer"}

@app.post("/points/", response_model=List[schema.PointOut])
async def add_multiple_points(data: schema.MultiplePoints, db: Session = Depends(get_db),user=Depends(AuthHandler().auth_wrapper)):
    return  crud.create_multiple_points(db, data)

@app.get("/points/", response_model=List[schema.PointOut])
async def get_all_points(db: Session = Depends(get_db),user=Depends(AuthHandler().auth_wrapper)):
    return  crud.get_points(db)

@app.post("/polygons/", response_model=List[schema.PolygonOut])
async def add_multiple_polygons(data: schema.MultiplePolygons, db: Session = Depends(get_db),user=Depends(AuthHandler().auth_wrapper)):
    return  crud.create_multiple_polygons(db, data)

@app.get("/polygons/", response_model=List[schema.PolygonOut])
async def get_all_polygons(db: Session = Depends(get_db),user=Depends(AuthHandler().auth_wrapper)):
    return  crud.get_polygons(db)