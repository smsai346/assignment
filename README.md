# 🛰️ Spatial Data API – FastAPI Backend

A backend API developed using **FastAPI** and **MySQL (Spatial Support)** for storing, retrieving, and managing geospatial data such as **points** and **polygons**.

This project was built as part of the **Backend Developer (Python)** assignment for **Talkinglands**.

---

## 🚀 Features

- 📍 Create and retrieve multiple **Point** records
- 🗺️ Create and retrieve multiple **Polygon** records
- 🔐 Secured using **JWT token-based authentication**
- 🔎 Optional **bounding box filtering** for points
- ⚡ sync support with **SQLAlchemy 2.0**
- 🐳 Fully **Dockerized**

---

## 🛠️ Tech Stack

| Layer        | Tech                          |
|--------------|-------------------------------|
| Framework    | FastAPI                       |
| Database     | MySQL 8 (with spatial index)  |
| ORM          | SQLAlchemy 2.0 (Async)        |
| Auth         | JWT (python-jose)             |
| Geometry     | ST_GeomFromText               |                       
| Container    | Docker                        |

---

## 📥 Sample Payloads

### ✅ Points (POST `/points/`)

```json
{
  "points": [
    { "name": "P1", "geometry": "POINT(12.9716 77.5946)" },
    { "name": "P2", "geometry": "POINT(28.7041 77.1025)" }
  ]
}
