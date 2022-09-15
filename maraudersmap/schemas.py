from pydantic import BaseModel

from maraudersmap.extra_types import LatLong


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    position: LatLong


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class POIBase(BaseModel):
    title: str
    description: str | None = None
    position: LatLong


class POICreate(POIBase):
    pass


class POI(POIBase):
    id: int

    class Config:
        orm_mode = True
