from fastapi import APIRouter, BackgroundTasks
from app.schemas.report import *
from app.schemas.batch.request_model import ReportsInBatchRequest
from app.schemas.batch.response_model import BatchJobCreatedResponse, BatchJobStatusResponse, ReportInBatchResponse
from app.services.ai_report_service import AIReport
from app.services.ai_report_batch_service import AIReportInBatch

router = APIRouter()

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



@router.post('/batch', response_model=BatchJobCreatedResponse)
def generate_reports_batch(payload: ReportsInBatchRequest, background_tasks: BackgroundTasks):
    _service = AIReportInBatch()
    return _service.start_batch_job(payload, background_tasks)


@router.get('/batch/status', response_model=BatchJobStatusResponse)
def get_batch_status(job_id: str):
    _service = AIReportInBatch()
    return _service.get_batch_job_status(job_id)
