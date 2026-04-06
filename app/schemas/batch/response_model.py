from pydantic import BaseModel
from typing import List, Optional

class BatchJobCreatedResponse(BaseModel):
    job_id: str
    status: str
    message: str


class ReportInBatchResponse(BaseModel):
    name: str
    report: Optional[str] = None
    status: str
    error: Optional[str] = None


class BatchJobStatusResponse(BaseModel):
    job_id: str
    status: str
    completed_count: int = 0
    total_count: int = 0
    results: Optional[List[ReportInBatchResponse]] = None
