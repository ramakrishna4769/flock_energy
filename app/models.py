from typing import Optional, List
from pydantic import BaseModel


class Meter(BaseModel):
    meter_number: str
    serial_number: str
    manufacturer: str
    phase: str
    status: str
    distribution_transformer: str


class MeterListResponse(BaseModel):
    count: int
    meters: List[Meter]