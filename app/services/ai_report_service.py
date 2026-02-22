import logging
from openai import OpenAI
from google import genai
from google.genai import types
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL, GEMINI_API_KEY
from app.schemas.report import ReportRequest


logger = logging.getLogger('LOGGER_NAME')


class AIReport():
    def __init__(self):
        self.open_ai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.gemini_api_client = genai.Client(api_key=GEMINI_API_KEY) 

    def request_open_ai(self, prompt: str) -> str:
        response = self.open_ai_client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            temperature=0.2
        )

        return response.output_text


    def request_gemini(self, prompt: str):
        response = self.gemini_api_client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                system_instruction="Você é um psicólogo que vai redigir relatórios clínicos semanais."
            ),
            contents=prompt
        )

        return response.text
    

    def generate_report(self, data: ReportRequest) -> str:
        try:
            prompt = self.get_default_prompt(data)

            response = self.request_open_ai(prompt)

            return response
        except Exception as e:
            logger.exception(e)
            
            return ''


    def get_default_prompt(self, data: ReportRequest) -> str:
        prompt = f"""Você é um psicólogo que vai redigir relatórios clínicos semanais.
            
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
            paciente: {data.patient_name}
            {data.notes}
        """

        return prompt
