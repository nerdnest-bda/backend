from pydantic import BaseModel, confloat, HttpUrl
from typing import List, Optional
from uuid import UUID

class StatsSchema(BaseModel):
    _id: Optional[UUID]
    name: str
    program: str
    degree: str
    decision: str
    semester: str
    origin: str
    gpa: float
    quant: float
    verbal: float
    awa: float
    total_score: float

class StatsBatchRequest(BaseModel):
    stats: List[StatsSchema]
