
import logging
import time
from google import genai
from google.genai.types import InlinedResponse
from typing import List

from app.enums.status import Status
from app.core.config import GEMINI_API_KEY
from app.schemas.reports_in_batch import *
from app.utils.text_processing import build_default_prompt

logger = logging.getLogger('LOGGER_NAME')


class AIReportInBatch():
    def __init__(self):
        self.gemini_api_client = genai.Client(api_key=GEMINI_API_KEY) 


    def generate_report_in_batch(self, data: ReportsInBatchRequest) -> ReportsInBatchResponse:
        resultados: List[ReportInBatchResponse] = []

        inputs = []

        for paciente in data.pacientes:
            final_prompt = self.build_prompt(paciente, data.prompt)
            inputs.append({'contents': [{
                'parts': [{'text': final_prompt}] 
            }]})

        try:
            batch_job = self.gemini_api_client.batches.create(
                model='gemini-2.5-flash',
                src=inputs,
                config={
                    'display_name': "ai-reports-job",
                }
            )

            job_name = batch_job.name

            logger.info(f"Created batch job: {job_name}")
            logger.info(f"Polling status for job: {job_name}")
            
            # Poll the job status until it's completed.
            while True:
                batch_job_inline = self.gemini_api_client.batches.get(name=job_name)

                if batch_job.state.name in ('JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED'):
                    break
                
                logger.info(f"Job not finished. Current state: {batch_job.state.name}. Waiting 30 seconds...")
                time.sleep(30)

            logger.info(f"Job finished with state: {batch_job.state.name}")

            if batch_job.state.name == 'JOB_STATE_FAILED':
                logger.info(f"Error: {batch_job.error}")
            else:                
                for i, inline_response in enumerate[InlinedResponse](batch_job_inline.dest.inlined_responses, start=1):
                    logger.info(f"\n--- Response {i} ---")

                    if inline_response.response:
                        logger.info(inline_response.response.text)

                        resultados.append(
                            ReportInBatchResponse(
                                nome=paciente.nome,
                                relatorio=inline_response.response.text,
                                status=Status.GERADO,
                            )
                        )

        except Exception as e:
            logger.exception(e)

            resultados.append(
                ReportInBatchResponse(
                    nome=paciente.nome,
                    status=Status.ERRO,
                    erro=str(e),
                )
            )

        return ReportsInBatchResponse(resultados=resultados)


    def build_prompt(self, data: PatientPayload, prompt: str) -> str:
        if not prompt:
            return build_default_prompt(data)

        prompt_final = f"""{prompt}
            PACIENTE: {data.nome}
            ANOTAÇÕES:
            {data.anotacao}
        """

        return prompt_final
