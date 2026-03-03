from fastapi import APIRouter
from app.schemas.report import *
from app.schemas.reports_in_batch import *
from app.services.ai_report_service import AIReport

router = APIRouter()


@router.get('/')
def root():
    return {'message': 'ok'}


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
    _service = AIReport()

    return _service.generate_report_in_batch(payload)
