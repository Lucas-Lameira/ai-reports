from pydantic import BaseModel
from typing import List

class ReportRequest(BaseModel):
    patient_name: str
    notes: str

class ReportResponse(BaseModel):
    patient_name: str
    summary: str
