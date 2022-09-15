from sqlalchemy import Column, Integer, String

from maraudersmap.database.base_class import Base
from maraudersmap.extra_types import LatLongColumnType


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    position = Column(LatLongColumnType)


class POI(Base):
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    position = Column(LatLongColumnType)
