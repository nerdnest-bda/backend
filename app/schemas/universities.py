from pydantic import BaseModel, confloat, HttpUrl
from typing import List, Optional
from uuid import UUID

class Coordinates(BaseModel):
    latitude: confloat(ge=-90, le=90) 
    longitude: confloat(ge=-180, le=180) 

class UniversitySchema(BaseModel):
    _id: Optional[UUID]
    name: str
    address: str
    mascot_photo: str
    coordinates: Coordinates
    quadrant: str
    website: str

class UniversityBatchRequest(BaseModel):
    universities: List[UniversitySchema]