import os  # Importa o módulo 'os' para interagir com o sistema operacional, como verificar a existência de arquivos.
import sys  # Importa o módulo 'sys' para funções relacionadas ao sistema, como sair do script em caso de erro.

import nltk  # Importa a biblioteca Natural Language Toolkit, essencial para processamento de linguagem natural.
from nltk.tokenize import (
    word_tokenize,
)  # Importa a função específica para dividir texto em palavras (tokenização).


class TextProcessor:
    """
    Classe para encapsular e gerenciar o processo de pré-processamento de dados textuais.

    Esta classe organiza as etapas de limpeza e preparação de texto, que são
    fundamentais antes de alimentar os dados para modelos de Machine Learning ou IA.
    """

    def __init__(self, lang="portuguese"):
        """
        Inicializa o processador de texto, garantindo que os recursos NLTK necessários estejam disponíveis.

        Args:
            lang (str): Idioma para o processamento, 'portuguese' por padrão.
        """
        self.lang = lang
        # Verifica se os modelos de tokenização do NLTK ('punkt') para o idioma especificado já estão baixados.
        try:
            nltk.data.find(f"tokenizers/punkt/{lang}.pickle")
        except LookupError:
            # Se não encontrar, informa e tenta baixar os recursos automaticamente.
            print(f"Recursos NLTK para '{lang}' não encontrados. Baixando 'punkt'...")
            # 'quiet=True' evita que uma janela pop-up de download apareça se o recurso já estiver lá.
            nltk.download("punkt", quiet=True)

    def preprocess(self, text):
        """
        Aplica as etapas de pré-processamento básicas a uma única string de texto.

        As etapas incluem:
        1. Tokenização: Divide a string em palavras (tokens).
        2. Lowercasing: Converte todas as palavras para minúsculas.
        3. Filtragem: Remove tokens que não são puramente alfabéticos (ex: pontuações, números soltos).

        Args:
            text (str): A string de texto a ser pré-processada.

        Returns:
            list: Uma lista de tokens (palavras) limpos e em minúsculas.
        """
        # Utiliza o tokenizador específico para o idioma para lidar com nuances (ex: contrações).
        tokens = word_tokenize(text, language=self.lang)

        # List comprehension para aplicar lowercasing e filtrar.
        # 'word.isalpha()' verifica se todos os caracteres na palavra são letras.
        processed_tokens = [word.lower() for word in tokens if word.isalpha()]
        return processed_tokens

    def load_and_preprocess_dataset(self, file_path, max_lines=None):
        """
        Carrega linhas de um arquivo de dataset e aplica o pré-processamento.

        Projetado para lidar com datasets grandes, processando-os linha por linha
        e permitindo um limite de linhas para demonstrações.

        Args:
            file_path (str): Caminho completo para o arquivo do dataset (ex: 'pt.txt').
            max_lines (int, optional): Número máximo de linhas a processar.
                                        Se None, processa todas as linhas.
                                        Útil para demonstrações com datasets muito grandes.

        Returns:
            list: Uma lista consolidada de todos os tokens processados do dataset.
        """
        # Verifica se o arquivo existe antes de tentar lê-lo.
        if not os.path.exists(file_path):
            # Imprime um erro para a saída padrão de erro (sys.stderr) e encerra o script.
            print(
                f"ERRO: O arquivo do dataset '{file_path}' não foi encontrado.",
                file=sys.stderr,
            )
            print(
                "Por favor, certifique-se de que o caminho de 'data/pt.txt' está correto.",
                file=sys.stderr,
            )
            sys.exit(1)  # Sai do script com um código de erro (indicando falha)

        all_tokens = []  # Lista para armazenar todos os tokens de todas as linhas.
        try:
            # Abre o arquivo em modo de leitura ('r') com codificação UTF-8, essencial para textos com caracteres variados.
            with open(file_path, "r", encoding="utf-8") as f:
                # Itera sobre cada linha do arquivo, com um contador 'i'.
                for i, line in enumerate(f):
                    if (
                        max_lines and i >= max_lines
                    ):  # Verifica se o limite de linhas foi atingido.
                        break  # Para a leitura se o limite for definido e alcançado.

                    # Pré-processa a linha atual (removendo espaços extras nas pontas) e estende a lista geral.
                    all_tokens.extend(self.preprocess(line.strip()))
        except Exception as e:
            # Captura qualquer exceção inesperada durante a leitura ou pré-processamento.
            print(
                f"ERRO: Falha grave ao ler ou pré-processar o arquivo '{file_path}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)  # Encerra o script com erro.

        return all_tokens  # Retorna a lista final de todos os tokens pré-processados.


def main():
    """
    Função principal que orquestra a execução do script de pré-processamento de dados.
    Esta função simula a fase inicial de um pipeline de treinamento para um modelo de NLP.
    """
    print("--- Iniciando o Pré-processamento do Dataset (Fase de Treino) ---")

    processor = TextProcessor(
        lang="portuguese"
    )  # Instancia o processador de texto, definindo o idioma.

    dataset_file = (
        "data/pt.txt"  # Define o nome do arquivo do dataset a ser processado.
    )

    # Chama a função para carregar e pré-processar o dataset.
    # 'max_lines=1000' é usado para processar apenas uma amostra, ideal para demonstrações rápidas.
    # Em um cenário de treinamento real, este valor seria muito maior ou nulo.
    processed_data = processor.load_and_preprocess_dataset(dataset_file, max_lines=1000)

    # Verifica se algum dado foi realmente processado.
    if not processed_data:
        print(
            "\nNenhum dado foi processado. Verifique o arquivo do dataset ou o processo de leitura."
        )
        return  # Sai da função main se não houver dados.

    # Exibe informações sobre os dados processados para validação.
    print(f"\nTotal de tokens processados (amostra): {len(processed_data)}")
    print("Primeiros 20 tokens processados:")
    print(processed_data[:20])

    print("\n--- Próximos Passos no Pipeline de Treinamento (Conceitualização) ---")
    print(
        "Com estes dados pré-processados, as próximas etapas cruciais para construir um modelo de IA seriam:"
    )
    print(
        "1.  **Criação de Embeddings:** Converter palavras em vetores numéricos densos. Isso permite que modelos de ML/DL 'entendam' as palavras. Pode ser feito com técnicas como Word2Vec, GloVe, ou utilizando embeddings contextuais de modelos pré-treinados maiores (como BERT ou GPT) através da biblioteca HuggingFace Transformers."
    )
    print(
        "2.  **Definição da Arquitetura do Modelo:** Projetar a estrutura da rede neural (utilizando frameworks como PyTorch ou TensorFlow). Para geração de diálogo ou chatbots, arquiteturas como Seq2Seq (Encoder-Decoder) com LSTMs ou mecanismos de atenção (Transformers) são comuns. Redes Neurais Convolucionais (CNNs) podem ser usadas nessas arquiteturas para extração de características de texto (ex: identificar padrões locais em frases)."
    )
    print(
        "3.  **Treinamento do Modelo:** Alimentar a rede neural com os dados pré-processados para que ela aprenda a realizar a tarefa (ex: mapear perguntas a respostas, ou gerar respostas no estilo OpenSubtitles). Este processo é computacionalmente intensivo, requer grandes volumes de dados e poder computacional (GPUs)."
    )
    print(
        "4.  **Avaliação e Ajuste Fino:** Testar o desempenho do modelo com métricas de NLP (ex: BLEU, ROUGE) e fazer ajustes finos para otimizar sua performance em cenários reais."
    )
    print(
        "\nEste script serve como a base fundamental para a fase de preparação de dados de um modelo de Processamento de Linguagem Natural (NLP) mais completo, simulando o início de um pipeline de treinamento."
    )
    print("--- Pré-processamento Concluído ---")


if __name__ == "__main__":
    main()  # Inicia a execução do script chamando a função principal.
