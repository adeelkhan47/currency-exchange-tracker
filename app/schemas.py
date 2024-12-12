from pydantic import BaseModel
from typing import Optional

class ExchangeRateSchemaChanges(BaseModel):
    currency: str
    rate: float
    change: float
class ExchangeRateSchema(BaseModel):
    currency: str
    rate: float
