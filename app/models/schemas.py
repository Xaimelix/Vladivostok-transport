from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class StationOut(BaseModel):
    id: int
    name: str
    x: Optional[int]
    y: Optional[int]
    status: Optional[str]
    time: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class RouteRequest(BaseModel):
    start: str  # можно id или name
    end: str

class RouteOut(BaseModel):
    route: List[int]  # список station ids (или names)
    lines: List[int] = []