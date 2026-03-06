# from google import genai
# from app.core.config import GEMINI_API_KEY
from fastapi import APIRouter
from app.schemas.report import *
from app.schemas.reports_in_batch import *
from app.services.ai_report_service import AIReport
from app.services.ai_report_batch_service import AIReportInBatch

router = APIRouter()
# GEMINI_API_CLIENT =  genai.Client(api_key=GEMINI_API_KEY) 

@router.get('/')
def root():
    return {'message': 'ok'}


@router.get("/health")
def health():
    return {"status": "running"}


@router.post('/', response_model=ReportResponse)
def create_report(data: ReportRequest):
    _service = AIReport()

    summary = _service.generate_report(data)

    return ReportResponse(
        patient_name=data.patient_name,
        summary=summary
    )


@router.post('/relatorios/batch', response_model=ReportsInBatchResponse)
def generate_reports_batch(payload: ReportsInBatchRequest):
    # _service = AIReportInBatch()
    _service = AIReport()

    return _service.generate_report_in_batch(payload)
