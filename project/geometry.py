from sqlalchemy.types import UserDefinedType

class Geometry(UserDefinedType):
    def __init__(self, geometry_type='GEOMETRY', srid=None):
        self.geometry_type = geometry_type.upper()
        self.srid = srid

    def get_col_spec(self, **kw):
        return f"{self.geometry_type}"  # Avoid SRID in column definition (set during insert)