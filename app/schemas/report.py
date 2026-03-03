from pydantic import BaseModel, Field
from typing import List, Optional


class ReportRequest(BaseModel):
    patient_name: str
    notes: str

class ReportResponse(BaseModel):
    patient_name: str
    summary: str
