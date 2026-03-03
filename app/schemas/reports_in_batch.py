from pydantic import BaseModel, Field
from typing import List, Optional


class PatientPayload(BaseModel):
    nome: str
    anotacao: str

class ReportsInBatchRequest(BaseModel):
    prompt: str = Field(default=None)
    pacientes: List[PatientPayload]

class ReportInBatchResponse(BaseModel):
    nome: str
    relatorio: Optional[str] = None
    status: str
    erro: Optional[str] = None

class ReportsInBatchResponse(BaseModel):
    resultados: List[ReportInBatchResponse]