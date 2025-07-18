import os

import google.generativeai as genai


def chamar_llm_para_resumo(pergunta_usuario, info_filme=None):
    """
    Gera uma resposta abrangente e estilizada usando a LLM (Google Gemini Pro).
    Esta função é o "cérebro" do chatbot, gerando todas as respostas textuais.

    Args:
        pergunta_usuario (str): A pergunta original do usuário.
        info_filme (tuple, optional): Informações factuais do filme (titulo, diretor, ano, genero) do BD, se encontrado.
                                        Passado como contexto para a LLM.

    Returns:
        str: A resposta gerada pela LLM (precedida de 'Chatbot: ') ou uma mensagem de erro/placeholder.
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return (
            "Chatbot: ERRO: A chave da API do Google Gemini não foi configurada como variável de ambiente 'GOOGLE_API_KEY'. "
            "Para testar a IA, por favor, configure a chave de API (instruções no README)."
        )

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    # --- CONSTRUÇÃO DO PROMPT DETALHADA PARA ABRANGÊNCIA E ESTILO ---

    # 1. Definição de Persona e Regras Globais: (Instruções ESSENCIAIS para o comportamento da LLM)
    system_instruction = (
        "Você é um chatbot cinéfilo, um mestre das histórias das telonas, com uma personalidade dramática, poética e perspicaz. "
        "Seu estilo de resposta deve imitar diálogos de filmes clássicos ou personagens icônicos (como sábio, astuto, ou direto). "
        "Use frases de efeito, metáforas cinematográficas e um tom que evoque a magia das telas, mas nunca sacrifique a verdade pelos floreios. "
        "Sua missão é responder a perguntas sobre filmes de forma abrangente, seja fatual, resumo, sobre personagens, curiosidades ou saudações. "
        "Sempre tente fornecer informações precisas e concisas. Se não souber algo, admita com dignidade e um toque dramático e com elegância. "
        "Se a pergunta parecer não relacionada a filmes, responda educadamente, mas redirecione gentilmente para o tema cinema."
    )

    # 2. Contexto Factual (do Banco de Dados, se o filme foi encontrado):
    contexto_factual = ""
    if info_filme:
        titulo, diretor, ano, genero, protagonista = info_filme
        contexto_factual = (
            f"Informações confirmadas do banco de dados sobre o filme: "
            f"Título: '{titulo}', Diretor: {diretor}, Ano: {ano}, Gênero: {genero}. "
            f"O protagonista principal é {protagonista}. "
            f"Utilize esses fatos em sua resposta com precisão, combinando-os com seu estilo marcante."
        )

    # 3. Exemplos (Few-shot Prompting - CONCEITUALMENTE do pt.txt para guiar o estilo):
    # Estes exemplos moldam a LLM a dar respostas mais ricas e no estilo desejado.
    few_shot_examples = (
        "\n--- Exemplos de Interação Estilizada ---\n"
        "Você: Olá, chatbot!\n"
        "Chatbot: Bem-vindo, buscador de histórias! Qual enigma cinematográfico o aflige hoje?\n"
        "Você: Quem dirigiu Matrix?\n"
        "Chatbot: Ah, 'Matrix'? Foi a mente brilhante das irmãs Wachowski que orquestrou essa epopeia em 1999. Uma verdadeira viagem à realidade.\n"
        "Você: Me resuma 'A Origem'.\n"
        "Chatbot: 'A Origem'... Um labirinto onírico, onde a mente é o campo de batalha. Dirigido por Christopher Nolan em 2010. Prepare-se para ter seus sonhos invadidos por uma equipe de ladrões que plantam ideias. Uma trama intrincada, um verdadeiro desafio à percepção.\n"
        "Você: Fale sobre o personagem Darth Vader.\n"
        "Chatbot: Ah, Lord Vader... A sombra imponente que permeia a galáxia. Um vilão cujas ações moldaram o destino, outrora um herói caído. Sua presença é um lembrete sombrio do poder do Lado Sombrio da Força.\n"
        "Você: Qual o filme mais triste que você conhece?\n"
        "Chatbot: As trilhas da tristeza são muitas nos reinos cinematográficos. Cada lágrima derramada por uma obra... Mas se a dor buscas, 'A Vida é Bela' talvez te mostre a beleza na tragédia, ou 'À Espera de um Milagre', a esperança em meio ao desespero. Escolhas sombrias, mas poderosas.\n"
        "Você: Preciso sair.\n"
        "Chatbot: Que sua jornada continue épica. Até a próxima cena!\n"
    )

    # 4. A Pergunta do Usuário para a LLM:
    user_query = f"Pergunta do usuário: '{pergunta_usuario}'"

    # Constrói o prompt final combinando todas as partes.
    prompt_completo = (
        f"{system_instruction}\n\n"
        f"{contexto_factual}\n"
        f"{few_shot_examples}\n"
        f"{user_query}\n"
        f"Sua resposta (no estilo de filme):"
    )

    # --- FIM DA CONSTRUÇÃO DO PROMPT ---

    try:
        response = model.generate_content(prompt_completo)
        return f"Chatbot: {response.text}"  # Retorna a resposta da LLM.
    except Exception as e:
        # Captura e exibe erros que podem ocorrer na chamada da API (ex: chave inválida, sem internet, etc.)
        return (
            f"Chatbot: ERRO na consulta ao grande oráculo (LLM): {e}. "
            "Minha conexão com o universo do conhecimento está instável. Por favor, tente novamente."
        )
