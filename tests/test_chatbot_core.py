import sqlite3
import unittest
from unittest.mock import patch


# Importa as funções que você vai testar dos módulos.
# O caminho aqui será relativo à raiz do projeto quando rodar o pytest
from src.database.db_utils import consultar_filme_no_bd
from src.llm.llm_utils import chamar_llm_para_resumo


# --- Configuração do Banco de Dados para Testes ---
# Isso cria um banco de dados temporário em memória para os testes de DB.
# Garante que os testes de DB sejam isolados e não dependam do 'filmes.db' real.
def setup_test_db():
    conn = sqlite3.connect(
        ":memory:"
    )  # Banco de dados em memória, volátil para cada teste
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            diretor TEXT NOT NULL,
            ano INTEGER,
            genero TEXT,
            protagonista TEXT
        );
    """
    )
    # Dados de exemplo para o banco de dados de teste (com 5 elementos por filme)
    filmes_exemplo_test = [
        (
            "Matrix",
            "Lana Wachowski, Lilly Wachowski",
            1999,
            "Ficção Científica",
            "Keanu Reeves",
        ),
        ("O Poderoso Chefão", "Francis Ford Coppola", 1972, "Drama", "Marlon Brando"),
        (
            "A Origem",
            "Christopher Nolan",
            2010,
            "Ficção Científica",
            "Leonardo DiCaprio",
        ),
        (
            "Interstellar",
            "Christopher Nolan",
            2014,
            "Ficção Científica",
            "Matthew McConaughey",
        ),
        ("Pulp Fiction", "Quentin Tarantino", 1994, "Crime", "John Travolta"),
        (
            "Senhor dos Anéis: A Sociedade do Anel",
            "Peter Jackson",
            2001,
            "Fantasia",
            "Elijah Wood",
        ),
        (
            "O Cavaleiro das Trevas",
            "Christopher Nolan",
            2008,
            "Ação/Crime",
            "Christian Bale",
        ),
        ("1984", "Michael Radford", 1984, "Ficção Científica", "John Hurt"),
        (
            "A Viagem de Chihiro",
            "Hayao Miyazaki",
            2001,
            "Animação/Fantasia",
            "Rumi Hiiragi",
        ),
    ]
    cursor.executemany(
        "INSERT INTO filmes (titulo, diretor, ano, genero, protagonista) VALUES (?, ?, ?, ?, ?)",
        filmes_exemplo_test,
    )  # Ajustado para 5 placeholders
    conn.commit()
    return conn


# --- Classe de Testes para consultar_filme_no_bd ---
class TestConsultarFilmeNoBD(unittest.TestCase):
    def setUp(self):
        """Configura um banco de dados em memória para cada teste."""
        self.conn = setup_test_db()
        self.patcher = patch("sqlite3.connect", return_value=self.conn)
        self.mock_connect = self.patcher.start()

    def tearDown(self):
        """Fecha a conexão com o banco de dados em memória após cada teste."""
        self.conn.close()
        self.patcher.stop()

    def test_consultar_filme_existente(self):
        """Verifica se a consulta retorna informações de um filme existente."""
        resultado = consultar_filme_no_bd("Matrix")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0], "Matrix")
        self.assertEqual(resultado[1], "Lana Wachowski, Lilly Wachowski")

    def test_consultar_filme_inexistente(self):
        """Verifica se a consulta retorna None para um filme inexistente."""
        resultado = consultar_filme_no_bd("Titanic")
        self.assertIsNone(resultado)

    def test_consultar_filme_por_parte_do_nome(self):
        """Verifica se a consulta funciona com parte do nome do filme."""
        resultado = consultar_filme_no_bd("Chefão")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0], "O Poderoso Chefão")


# --- Classe de Testes para chamar_llm_para_resumo (Conceitualização com Mocks) ---
class TestChamarLLM(unittest.TestCase):
    @patch("google.generativeai.GenerativeModel")  # Mocka a classe GenerativeModel
    @patch(
        "os.getenv", return_value="FAKE_API_KEY"
    )  # Mocka os.getenv para simular que a chave existe
    def test_chamar_llm_com_contexto_db(self, mock_getenv, MockGenerativeModel):
        """
        Verifica se a LLM é chamada com o prompt correto quando há contexto do DB.
        """
        # Configura o mock da LLM para retornar uma resposta pré-definida.
        mock_model_instance = MockGenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = (
            "Mocked: Sua jornada épica sobre Matrix foi dirigida por X."
        )

        info_filme_db = (
            "Matrix",
            "Lana Wachowski, Lilly Wachowski",
            1999,
            "Ficção Científica",
            "Keanu Reeves",
        )
        pergunta = "Quem dirigiu Matrix?"

        resposta = chamar_llm_para_resumo(pergunta, info_filme=info_filme_db)

        # Verifica se a LLM foi chamada
        MockGenerativeModel.assert_called_once_with("gemini-pro")
        mock_model_instance.generate_content.assert_called_once()

        # Verifica se a resposta contém partes do mock.
        self.assertIn("Mocked:", resposta)
        self.assertIn("Matrix", resposta)
        self.assertIn("X", resposta)

    @patch("google.generativeai.GenerativeModel")
    @patch("os.getenv", return_value="FAKE_API_KEY")
    def test_chamar_llm_sem_contexto_db(self, mock_getenv, MockGenerativeModel):
        """
        Verifica se a LLM é chamada com o prompt correto quando não há contexto do DB.
        """
        mock_model_instance = MockGenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = (
            "Mocked: Não encontrei nos registros antigos."
        )

        pergunta = "Me resuma um filme que não existe."
        resposta = chamar_llm_para_resumo(pergunta, info_filme=None)

        MockGenerativeModel.assert_called_once_with("gemini-pro")
        mock_model_instance.generate_content.assert_called_once()
        self.assertIn("Mocked:", resposta)

    @patch(
        "os.getenv", return_value=None
    )  # Mocka os.getenv para simular que a chave NÃO existe
    def test_chamar_llm_sem_api_key(self, mock_getenv):
        """
        Verifica se a função retorna mensagem de erro quando a API Key não está configurada.
        """
        pergunta = "Qualquer pergunta."
        resposta = chamar_llm_para_resumo(pergunta)

        self.assertIn(
            "ERRO: A chave da API do Google Gemini não foi configurada", resposta
        )


if __name__ == "__main__":
    unittest.main()
