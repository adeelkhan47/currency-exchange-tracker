from pydantic import BaseModel
from datetime import date

class ExchangeRate(BaseModel):
    currency: str  # The currency code (e.g., 'USD', 'EUR') as a string
    rate: float  # The exchange rate as a float (e.g., 1.15)
    date: date  # The date of the exchange rate as a 'date' type (e.g., 2024-12-13)
    change: float = None  # The change in the exchange rate (optional field, default value is None)
