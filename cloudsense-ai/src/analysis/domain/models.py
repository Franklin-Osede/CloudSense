from pydantic import BaseModel
from typing import List
from datetime import date

class Anomaly(BaseModel):
    account_id: str
    date: date
    service_name: str
    expected_amount: float
    actual_amount: float
    reason: str

class Recommendation(BaseModel):
    account_id: str
    service_name: str
    action: str
    estimated_savings: float
    
class AnalysisResult(BaseModel):
    anomalies: List[Anomaly]
    recommendations: List[Recommendation]
    summary_text: str
