import logging
from google import genai
from google.genai import types
from typing import List

from app.enums.status import Status
from app.core.config import GEMINI_API_KEY
from app.schemas.report import ReportRequest
from app.schemas.reports_in_batch import *


logger = logging.getLogger('LOGGER_NAME')


class AIReport():
    def __init__(self):
        self.gemini_api_client = genai.Client(api_key=GEMINI_API_KEY) 

    def request_gemini(self, prompt: str):
        response = self.gemini_api_client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Você é um psicólogo que vai redigir relatórios clínicos semanais."
            ),
            contents=prompt
        )

        return response.text


    def generate_report(self, data: ReportRequest) -> str:
        try:
            prompt = self.get_default_prompt(data)

            response = self.request_gemini(prompt)

            return response
        except Exception as e:
            logger.exception(e)
            
            return ''


    def get_default_prompt(self, data: PatientPayload) -> str:
        prompt = f"""
            Elabore um relatório terapêutico no modelo TIP (Treino de Independência Pessoal), com linguagem técnica, clara e objetiva, organizado nos seguintes tópicos:

            Com base nas anotações que vou te passar, gere um relatório com:

            1. Objetivos Terapêuticos:
            Descrever objetivos voltados para autonomia no momento do lanche/refeição, independência ao servir-se, habilidade de comer sozinho(a), permanência à mesa, organização funcional e coordenação motora, conforme aplicável ao caso.

            2. Programas de Intervenção e Atividades Desenvolvidas:
            Descrever detalhadamente:
                •	Atividade principal realizada (ex: kit cozinha, treino de servir-se, organização de utensílios, transferência de alimentos, etc.);
                •	Participação da criança (nível de engajamento);
                •	Tipo de mediação necessária (verbal, gestual, física leve, suporte mínimo, supervisão);
                •	Desempenho na permanência à mesa e postura;
                •	Nível de autonomia ao comer sozinho(a);
                •	Habilidade de transferir alimentos/organizar utensílios;
                •	Indícios de evolução (coordenação motora, planejamento da ação, compreensão de comandos);
                •	Presença de oscilações atencionais ou necessidade de redirecionamento.

            3. Observações:
            Descrever:
                •	Nível de engajamento geral;
                •	Necessidade de mediação;
                •	Compreensão das instruções;
                •	Pontos de evolução;
                •	Aspectos que ainda demandam intervenção;
                •	Considerações clínicas sobre autonomia e organização funcional.

            Utilizar linguagem profissional voltada para contexto clínico terapêutico.

            Anotações:
            paciente: {data.nome}
            {data.anotacao}
        """

        return prompt


    def generate_report_in_batch(self, data: ReportsInBatchRequest) -> ReportsInBatchResponse:
        resultados: List[ReportInBatchResponse] = []

        for paciente in data.pacientes:
            try:
                prompt_final = self.build_prompt(paciente, data.prompt)
                relatorio = self.request_gemini(prompt_final)

                resultados.append(
                    ReportInBatchResponse(
                        nome=paciente.nome,
                        relatorio=relatorio,
                        status=Status.GERADO,
                    )
                )

            except Exception as e:
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
            return self.get_default_prompt(data)

        prompt_final = f"""{prompt}
            PACIENTE: {data.nome}
            ANOTAÇÕES:
            {data.anotacao}
        """

        return prompt_final
