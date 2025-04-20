from sqlalchemy.orm import Session
from shapely import wkt
from .model import PointData, PolygonData
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

def create_multiple_points(db: Session, data):
    try:
        # Insert using ORM + SQL function ST_GeomFromText
        for point in data.points:
            db.add(
                PointData(
                    name=point.name,
                    geometry=func.ST_GeomFromText(point.geometry, 4326)  # 🧠 Converts WKT string into geometry
                )
            )
        db.commit()

        # Query using ORM and convert geometry to WKT or GeoJSON
        results = db.query(
            PointData.id,
            PointData.name,
            func.ST_AsText(PointData.geometry).label("wkt")
        ).all()

        return [
            {
                "id": r.id,
                "name": r.name,
                "geometry": r.wkt  # or use: wkt_to_geojson(r.wkt)
            }
            for r in results
        ]

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction if an error occurs
        # Log the error or print a message
        print(f"Error occurred: {str(e)}")
        return {"error": "An error occurred while processing the points."}
def create_multiple_polygons(db: Session, data):
    try:
        for poly in data.polygons:
            db.add(
                    PolygonData(
                        name=poly.name,
                        geometry=func.ST_GeomFromText(poly.geometry, 4326)  # 🧠 Converts WKT string into geometry
                    )
                )
        db.commit()
        results = db.query(
                PolygonData.id,
                PolygonData.name,
                func.ST_AsText(PolygonData.geometry).label("wkt")
            ).all()

        return [{"id": r.id, "name": r.name, "geometry": r.wkt} for r in results]
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return {"error": "An error occurred while processing the points."}

def get_points(db: Session):
    try:
        # Query to retrieve points from the database
        result =  db.query(
            PointData.id,
            PointData.name,
            func.ST_AsText(PointData.geometry).label("geometry")
        ).all()

        # Return the result as a list of dictionaries
        return [{"id": r.id, "name": r.name, "geometry": r.geometry} for r in result]

    except SQLAlchemyError as e:
        # Handle database-related errors
        print(f"Error occurred: {str(e)}")
        return {"error": "An error occurred while retrieving the points."}

def get_polygons(db: Session):
    try:
        # Query to retrieve points from the database
        result =  db.query(
            PolygonData.id,
            PolygonData.name,
            func.ST_AsText(PolygonData.geometry).label("geometry")
        ).all()

        # Return the result as a list of dictionaries
        return [{"id": r.id, "name": r.name, "geometry": r.geometry} for r in result]

    except SQLAlchemyError as e:
        # Handle database-related errors
        print(f"Error occurred: {str(e)}")
        return {"error": "An error occurred while retrieving the points."}

    