import logging
import json
import os
import uuid
import time
from fastapi import BackgroundTasks

from google import genai
from google.genai import types

from app.enums.status import Status
from app.core.config import GEMINI_API_KEY
from app.schemas.batch.request_model import *
from app.schemas.batch.response_model import *
from app.utils.text_processing import build_default_prompt

logger = logging.getLogger('LOGGER_NAME')

JOBS_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jobs')
os.makedirs(JOBS_DATA_DIR, exist_ok=True)

class AIReportInBatch:
    def __init__(self):
        self.gemini_api_client = genai.Client(api_key=GEMINI_API_KEY)

    def _get_job_file_path(self, job_name: str) -> str:
        return os.path.join(JOBS_DATA_DIR, f"{job_name}.json")

    def start_batch_job(self, data: ReportsInBatchRequest, background_tasks: BackgroundTasks) -> BatchJobCreatedResponse:
        try:
            job_id = f"batch_{uuid.uuid4().hex[:12]}"
            job_file = self._get_job_file_path(job_id)

            initial_state = {
                "status": "processing",
                "completed_count": 0,
                "total_count": len(data.users),
                "results": []
            }
            with open(job_file, 'w', encoding='utf-8') as f:
                json.dump(initial_state, f)

            logger.info(f"Created local background job tracking id: {job_id}")

            background_tasks.add_task(self._process_batch_in_background, job_id, data)

            return BatchJobCreatedResponse(
                job_id=job_id,
                status="processing",
                message="Batch job running."
            )

        except Exception as e:
            logger.exception(e)
            return BatchJobCreatedResponse(
                job_id="",
                status="error",
                message=str(e)
            )

    def _process_batch_in_background(self, job_id: str, data: ReportsInBatchRequest):
        job_file = self._get_job_file_path(job_id)
        results = []
        total_count = len(data.users)
        completed_count = 0

        try:
            for user in data.users:
                try:
                    prompt_final = self.build_prompt(user, data.prompt)
                    
                    response = self.gemini_api_client.models.generate_content(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=data.system_instruction
                        ),
                        contents=prompt_final
                    )

                    report_text = response.text if response.text else ""

                    results.append({
                        "name": user.name,
                        "report": report_text,
                        "status": Status.GERADO
                    })

                except Exception as inner_e:
                    logger.exception(inner_e)
                    results.append({
                        "name": user.name,
                        "report": None,
                        "status": "erro",
                        "error": str(inner_e)
                    })
                
                completed_count += 1
                
                mid_state = {
                    "status": "processing",
                    "completed_count": completed_count,
                    "total_count": total_count,
                    "results": results
                }
                with open(job_file, 'w', encoding='utf-8') as f:
                    json.dump(mid_state, f)

                time.sleep(3.5)

            final_state = {
                "status": "completed",
                "completed_count": completed_count,
                "total_count": total_count,
                "results": results
            }
            
            with open(job_file, 'w', encoding='utf-8') as f:
                json.dump(final_state, f)

        except Exception as e:
            logger.exception(e)
            error_state = {
                "status": "failed",
                "completed_count": completed_count,
                "total_count": total_count,
                "results": results
            }
            with open(job_file, 'w', encoding='utf-8') as f:
                json.dump(error_state, f)


    def get_batch_job_status(self, job_name: str) -> BatchJobStatusResponse:
        job_file = self._get_job_file_path(job_name)

        if not os.path.exists(job_file):
            return BatchJobStatusResponse(
                job_id=job_name,
                status="error" 
            )

        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                state = json.load(f)

            return BatchJobStatusResponse(
                job_id=job_name,
                status=state.get("status", "processing"),
                completed_count=state.get("completed_count", 0),
                total_count=state.get("total_count", 0),
                results=state.get("results", [])
            )
            
        except Exception as e:
            logger.exception(e)
            return BatchJobStatusResponse(
                job_id=job_name,
                status="error"
            )

    def build_prompt(self, data: User, prompt: str) -> str:
        if not prompt:
            return build_default_prompt(data)

        final_prompt = f"{prompt}\nPACIENTE: {data.name}\nANOTAÇÕES:\n{data.note}"
        return final_prompt
