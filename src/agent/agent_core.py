def identificar_intencao(pergunta):
    """
    Identifica a intenção da pergunta do usuário com base em palavras-chave.
    Esta é uma forma simplificada de reconhecimento de intenção para o protótipo.

    Args:
        pergunta (str): A pergunta completa do usuário.

    Returns:
        str: A intenção identificada ('factual', 'resumo_geral', 'sair', 'desconhecida').
    """
    pergunta_lower = pergunta.lower()

    # Intenção de Saída
    if (
        "sair" in pergunta_lower
        or "adeus" in pergunta_lower
        or "tchau"
        or "até logo" in pergunta_lower
    ):
        return "sair"

    # Intenções Fatuais (para consulta ao DB)
    palavras_chave_fatuais = [
        "quem",
        "qual",
        "quando",
        "onde",
        "diretor",
        "ano",
        "gênero",
        "genero",
    ]
    if any(keyword in pergunta_lower for keyword in palavras_chave_fatuais):
        return "factual"

    # Intenções de Resumo / Geral (para consulta à LLM sem foco no DB)
    palavras_chave_resumo_geral = [
        "resuma",
        "fale sobre",
        "me conte",
        "o que é",
        "história",
        "sobre",
        "personagem",
        "atores",
        "atrizes",
        "qual a moral",
        "elenco",
    ]
    if any(keyword in pergunta_lower for keyword in palavras_chave_resumo_geral):
        return "resumo_geral"

    # Se não se encaixar em nenhuma das intenções acima
    return "desconhecida"
