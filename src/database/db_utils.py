import sqlite3


def consultar_filme_no_bd(titulo_filme):
    """
    Consulta o banco de dados 'filmes.db' para buscar informações de um filme.

    Args:
        titulo_filme (str): O título do filme a ser buscado.

    Returns:
        tuple or None: Uma tupla com (titulo, diretor, ano, genero) do filme se encontrado,
                        ou None se o filme não for encontrado.
    """
    conn = None
    try:
        conn = sqlite3.connect("data/filmes.db")
        cursor = conn.cursor()

        # SQL para buscar o filme. Usa LIKE para uma busca flexível (parte do nome, case-insensitive).
        # A tupla (f'%{titulo_filme}%',) é crucial para passar o parâmetro de forma segura.
        cursor.execute(
            "SELECT titulo, diretor, ano, genero, protagonista FROM filmes WHERE titulo LIKE ?",
            (f"%{titulo_filme}%",),
        )

        resultado = (
            cursor.fetchone()
        )  # Pega apenas o primeiro resultado correspondente.

        return resultado

    except sqlite3.Error as e:
        print(
            f"Erro ao consultar o banco de dados: {e}"
        )  # Imprime o erro, mas não encerra o programa.
        return None
    finally:
        if conn:
            conn.close()  # Garante que a conexão com o banco de dados seja fechada.
