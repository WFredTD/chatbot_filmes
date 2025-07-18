import os

import google.generativeai as genai


def extrair_titulo_da_pergunta(pergunta):
    """
    Extrai um possível título de filme de uma pergunta do usuário usando a LLM.
    Esta abordagem é mais robusta para títulos não padronizados ou em frases complexas,
    delegando a inteligência de PLN à LLM.

    Args:
        pergunta (str): A pergunta completa do usuário.

    Returns:
        str: O título do filme extraído pela LLM, ou uma string vazia se não for encontrado.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # Retorna uma mensagem de erro ou vazio se a chave não estiver configurada para não travar.
        # Em produção, isso seria logado e tratado.
        return ""

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prompt para instruir a LLM a extrair o título
    prompt_extracao = (
        "Você é um assistente de extração de títulos de filmes. "
        "Sua tarefa é identificar e retornar APENAS o título do filme presente na frase do usuário. "
        "Retorne APENAS o título do filme, sem nenhuma outra palavra ou pontuação. "
        "Se não for um filme, ou se não conseguir identificar um título claro, retorne a palavra 'NENHUM'.\n\n"
        "Exemplos:\n"
        "Frase: 'Quem dirigiu Matrix?'\n"
        "Título: Matrix\n"
        "Frase: 'Me resuma O Poderoso Chefão.'\n"
        "Título: O Poderoso Chefão\n"
        "Frase: 'Fale sobre Interstellar.'\n"
        "Título: Interstellar\n"
        "Frase: 'Qual a história de Star Wars?'\n"
        "Título: Star Wars\n"
        "Frase: 'Olá chatbot, como vai?'\n"
        "Título: NENHUM\n"
        "Frase: 'Me resuma 1984.'\n"
        "Título: 1984\n"
        f"Frase: '{pergunta}'\n"
        "Título:"
    )

    try:
        response = model.generate_content(prompt_extracao)
        titulo_extraido = response.text.strip()
        if titulo_extraido.lower() == "nenhum":
            return ""
        return titulo_extraido
    except Exception as e:
        # Se houver erro na API, retorna vazio para que a lógica principal chame a LLM para resposta geral
        print(f"Erro na extração de título pela LLM: {e}")
        return ""
