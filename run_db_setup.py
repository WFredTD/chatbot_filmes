from src.database.setup_db import (
    criar_tabela_filmes,
    popular_filmes_exemplo,
)

if __name__ == "__main__":
    print("Iniciando configuração do banco de dados...")
    criar_tabela_filmes()  # Chamar as funções do db_utils
    popular_filmes_exemplo()
    print("Configuração do banco de dados concluída.")
