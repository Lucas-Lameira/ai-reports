from app.schemas.reports_in_batch import PatientPayload

def join_notes(notes: list[str]) -> str:
    return " ".join(notes)


def build_default_prompt(data: PatientPayload) -> str:
    prompt = f"""Com base nas anotações abaixo, gere um relatório com:
        - Queixa principal
        - Evolução na semana
        - Intervenções realizadas
        - Respostas do paciente
        - Pontos de atenção
        - Plano para próxima sessão
        Use linguagem técnica, objetiva e ética.
        Não invente informações que não estejam nas anotações.
        paciente: {data.nome}
        Anotações:
        {data.anotacao}
    """

    return prompt