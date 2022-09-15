from sqlalchemy import Float
from sqlalchemy.dialects.postgresql import ARRAY

LatLong = tuple[float, float]
LatLongColumnType = ARRAY(Float, as_tuple=True)
