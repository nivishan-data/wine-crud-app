# app/schemas.py

from pydantic import BaseModel
from typing import Optional

class WineBase(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    quality: int

class WineCreate(WineBase):
    pass

class WineUpdate(BaseModel):
    fixed_acidity: Optional[float] = None
    volatile_acidity: Optional[float] = None
    citric_acid: Optional[float] = None
    residual_sugar: Optional[float] = None
    chlorides: Optional[float] = None
    free_sulfur_dioxide: Optional[float] = None
    total_sulfur_dioxide: Optional[float] = None
    density: Optional[float] = None
    pH: Optional[float] = None
    sulphates: Optional[float] = None
    alcohol: Optional[float] = None
    quality: Optional[int] = None

class Wine(WineBase):
    id: int

    class Config:
        orm_mode = True
