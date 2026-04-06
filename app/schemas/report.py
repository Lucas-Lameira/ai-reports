from pydantic import BaseModel


class ReportRequest(BaseModel):
    patient_name: str
    notes: str

class ReportResponse(BaseModel):
    patient_name: str
    summary: str
