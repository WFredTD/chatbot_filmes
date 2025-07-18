import os

from dotenv import load_dotenv  # Para carregar variáveis de ambiente do .env

from src.agent.agent_core import \
    identificar_intencao  # Lógica central do agente
# Importações dos módulos internos do projeto (do pacote 'src')
from src.database.db_utils import consultar_filme_no_bd  # Funções de DB
from src.llm.llm_utils import chamar_llm_para_resumo  # Funções de LLM
from src.nlp.nlp_utils import \
    extrair_titulo_da_pergunta  # Funções de NLP (extração de título)

# Carrega as variáveis de ambiente do arquivo .env.
# Isso deve ser feito logo no início do script para que as chaves estejam disponíveis.
load_dotenv() 


def main():
    """
    Função principal do chatbot que orquestra a interação com o usuário,
    a consulta ao banco de dados e a geração de respostas pela LLM.
    """

    # O setup_database.py deve ser executado UMA VEZ antes de rodar o chatbot.py.

    # Mensagens iniciais do chatbot, geradas pela LLM para 100% de estilo.
    print(chamar_llm_para_resumo('Saudação inicial para um chatbot cinéfilo.')) 
    print(chamar_llm_para_resumo('Instrução para o usuário sobre como interagir, incluindo como perguntar sobre filmes e como sair.')) 

    while True:
        pergunta_usuario = input("Você: ")
        

        # 1. Identificar a Intenção do Usuário (Agent Core)
        intencao = identificar_intencao(pergunta_usuario)

        if intencao == "sair":
            print(chamar_llm_para_resumo('Mensagem de despedida do chatbot cinéfilo.'))
            break

        # --- LÓGICA DE AGENTE REFINADA: EXTRAÇÃO DE INTENÇÃO E CONTEXTO ---
        
        # 1. Tentar extrair o título do filme da pergunta do usuário usando a função extrair_titulo_da_pergunta
        titulo_identificado = extrair_titulo_da_pergunta(pergunta_usuario)
        
        info_filme_do_bd = None
        if titulo_identificado: # Se um título foi extraído da pergunta
            # 2. Consultar o banco de dados se um título foi identificado
            info_filme_do_bd = consultar_filme_no_bd(titulo_identificado)
        
        # 3. Chamar a LLM para gerar a resposta, passando o contexto do BD se o filme foi encontrado.
        # A LLM é o cérebro que gera todas as respostas estilizadas.
        # A lógica de estilização e abrangência está toda no prompt da LLM.
        resposta_final_chatbot = chamar_llm_para_resumo(pergunta_usuario, info_filme=info_filme_do_bd)
        print(resposta_final_chatbot)


if __name__ == '__main__':
    # Garante que a função principal seja chamada apenas quando o script é executado diretamente.
    main()