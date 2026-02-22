from fastapi import APIRouter
from app.schemas.report import ReportRequest, ReportResponse
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
