from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

class ServiceCost(BaseModel):
    service_name: str
    amount: float
    currency: str = "USD"

class AccountSpend(BaseModel):
    account_id: str
    date: date
    total_amount: float
    services: List[ServiceCost]

class CostData(BaseModel):
    start_date: date
    end_date: date
    accounts: List[AccountSpend]
