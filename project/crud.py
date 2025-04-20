from sqlalchemy.orm import Session
from .model import PointData, PolygonData
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

def create_multiple_points(db: Session, data):
    try:
        new_objects = []
        for point in data.points:
            obj = PointData(
                name=point.name,
                geometry=func.ST_GeomFromText(point.geometry, 4326)
            )
            db.add(obj)
            new_objects.append(obj)

        db.commit()

        # Refresh to populate auto-generated IDs
        for obj in new_objects:
            db.refresh(obj)

        new_ids = [obj.id for obj in new_objects]

        results = db.query(
            PointData.id,
            PointData.name,
            func.ST_AsText(PointData.geometry).label("wkt")
        ).filter(PointData.id.in_(new_ids)).all()

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "message": "Points created successfully",
                "data": [{"id": r.id, "name": r.name, "geometry": r.wkt} for r in results]
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Database error: {str(e)}"}
        )
def create_multiple_polygons(db: Session, data):
    try:
        new_objects = []
        for poly in data.polygons:
            obj = PolygonData(
                name=poly.name,
                geometry=func.ST_GeomFromText(poly.geometry, 4326)
            )
            db.add(obj)
            new_objects.append(obj)

        db.commit()

        # Refresh objects to access their auto-generated IDs
        for obj in new_objects:
            db.refresh(obj)

        # Query just the newly created polygons using their IDs
        new_ids = [obj.id for obj in new_objects]

        results = db.query(
            PolygonData.id,
            PolygonData.name,
            func.ST_AsText(PolygonData.geometry).label("wkt")
        ).filter(PolygonData.id.in_(new_ids)).all()

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "message": "Polygons created successfully",
                "data": [{"id": r.id, "name": r.name, "geometry": r.wkt} for r in results]
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Database error: {str(e)}"}
        )
   

def get_points(db: Session):
    try:
        result = db.query(
            PointData.id,
            PointData.name,
            func.ST_AsText(PointData.geometry).label("geometry")
        ).all()

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Points retrieved successfully",
                "data": [{"id": r.id, "name": r.name, "geometry": r.geometry} for r in result]
            }
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Error retrieving points: {str(e)}"}
        )
def get_polygons(db: Session):
    try:
        result = db.query(
            PolygonData.id,
            PolygonData.name,
            func.ST_AsText(PolygonData.geometry).label("geometry")
        ).all()

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Polygons retrieved successfully",
                "data": [{"id": r.id, "name": r.name, "geometry": r.geometry} for r in result]
            }
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Error retrieving polygons: {str(e)}"}
        )
def update_point(db: Session, point_id: int, data):
    try:
        point = db.query(PointData).filter(PointData.id == point_id).first()
        if not point:
            return JSONResponse(status_code=404, content={
                "status": "error",
                "message": "Point not found"
            })

        if data.name:
            point.name = data.name
        if data.geometry:
            point.geometry = func.ST_GeomFromText(data.geometry, 4326)

        db.commit()
        db.refresh(point)

        updated = db.query(
            PointData.id,
            PointData.name,
            func.ST_AsText(PointData.geometry).label("geometry")
        ).filter(PointData.id == point_id).first()

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Point updated successfully",
            "data": {"id": updated.id, "name": updated.name, "geometry": updated.geometry}
        })

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": f"Error updating point: {str(e)}"
        })

def update_polygon(db: Session, polygon_id: int, data):
    try:
        polygon = db.query(PolygonData).filter(PolygonData.id == polygon_id).first()
        if not polygon:
            return JSONResponse(status_code=404, content={
                "status": "error",
                "message": "Polygon not found"
            })

        if data.name:
            polygon.name = data.name
        if data.geometry:
            polygon.geometry = func.ST_GeomFromText(data.geometry, 4326)

        db.commit()
        db.refresh(polygon)

        updated = db.query(
            PolygonData.id,
            PolygonData.name,
            func.ST_AsText(PolygonData.geometry).label("geometry")
        ).filter(PolygonData.id == polygon_id).first()

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Polygon updated successfully",
            "data": {"id": updated.id, "name": updated.name, "geometry": updated.geometry}
        })

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": f"Error updating polygon: {str(e)}"
        })