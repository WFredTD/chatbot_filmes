import os
import sqlite3

DATABASE_NAME = "data/filmes.db"


def criar_tabela_filmes():
    """Cria a tabela de filmes no banco de dados, se ela não existir."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT,
            ano INTEGER,
            diretor TEXT,
            protagonista TEXT
        )
    """
    )
    conn.commit()
    conn.close()
    print(f"Tabela 'filmes' criada ou já existente em {DATABASE_NAME}.")


def popular_filmes_exemplo():
    """Popula a tabela de filmes com dados de exemplo, se estiver vazia."""
    filmes_para_inserir = [
        ("O Poderoso Chefão", "Drama", 1972, "Francis Ford Coppola", "Marlon Brando"),
        ("Um Sonho de Liberdade", "Drama", 1994, "Frank Darabont", "Tim Robbins"),
        (
            "A Lista de Schindler",
            "Drama Histórico",
            1993,
            "Steven Spielberg",
            "Liam Neeson",
        ),
        (
            "Forrest Gump: O Contador de Histórias",
            "Drama/Comédia",
            1994,
            "Robert Zemeckis",
            "Tom Hanks",
        ),
        (
            "Pulp Fiction: Tempo de Violência",
            "Crime/Drama",
            1994,
            "Quentin Tarantino",
            "John Travolta",
        ),
        (
            "O Senhor dos Anéis: A Sociedade do Anel",
            "Fantasia/Aventura",
            2001,
            "Peter Jackson",
            "Elijah Wood",
        ),
        (
            "O Cavaleiro das Trevas",
            "Ação/Crime",
            2008,
            "Christopher Nolan",
            "Christian Bale",
        ),
        (
            "A Origem",
            "Ficção Científica/Ação",
            2010,
            "Christopher Nolan",
            "Leonardo DiCaprio",
        ),
        (
            "Matrix",
            "Ficção Científica/Ação",
            1999,
            "Lana e Lilly Wachowski",
            "Keanu Reeves",
        ),
        ("Clube da Luta", "Drama/Suspense", 1999, "David Fincher", "Edward Norton"),
        (
            "Interestelar",
            "Ficção Científica",
            2014,
            "Christopher Nolan",
            "Matthew McConaughey",
        ),
        ("Gladiador", "Ação/Drama", 2000, "Ridley Scott", "Russell Crowe"),
        ("Django Livre", "Faroeste", 2012, "Quentin Tarantino", "Jamie Foxx"),
        (
            "O Silêncio dos Inocentes",
            "Suspense/Terror",
            1991,
            "Jonathan Demme",
            "Jodie Foster",
        ),
        (
            "Bastardos Inglórios",
            "Guerra/Aventura",
            2009,
            "Quentin Tarantino",
            "Brad Pitt",
        ),
        (
            "O Resgate do Soldado Ryan",
            "Guerra/Drama",
            1998,
            "Steven Spielberg",
            "Tom Hanks",
        ),
        (
            "À Espera de um Milagre",
            "Drama/Fantasia",
            1999,
            "Frank Darabont",
            "Tom Hanks",
        ),
        (
            "O Lobo de Wall Street",
            "Comédia/Crime",
            2013,
            "Martin Scorsese",
            "Leonardo DiCaprio",
        ),
        ("Beleza Americana", "Drama", 1999, "Sam Mendes", "Kevin Spacey"),
        ("Ilha do Medo", "Suspense", 2010, "Martin Scorsese", "Leonardo DiCaprio"),
        (
            "V de Vingança",
            "Ação/Ficção Científica",
            2005,
            "James McTeigue",
            "Hugo Weaving",
        ),
        (
            "De Volta Para o Futuro",
            "Ficção Científica/Aventura",
            1985,
            "Robert Zemeckis",
            "Michael J. Fox",
        ),
        ("O Profissional", "Ação/Drama", 1994, "Luc Besson", "Jean Reno"),
        ("Os Suspeitos", "Crime/Mistério", 1995, "Bryan Singer", "Kevin Spacey"),
        (
            "O Exterminador do Futuro 2: O Julgamento Final",
            "Ficção Científica/Ação",
            1991,
            "James Cameron",
            "Arnold Schwarzenegger",
        ),
        ("Kill Bill: Volume 1", "Ação/Crime", 2003, "Quentin Tarantino", "Uma Thurman"),
        (
            "Guardiões da Galáxia",
            "Ficção Científica/Aventura",
            2014,
            "James Gunn",
            "Chris Pratt",
        ),
        ("Coração Valente", "Histórico/Drama", 1995, "Mel Gibson", "Mel Gibson"),
        ("WALL·E", "Animação/Ficção Científica", 2008, "Andrew Stanton", "WALL·E"),
        (
            "Os Bons Companheiros",
            "Crime/Drama",
            1990,
            "Martin Scorsese",
            "Robert De Niro",
        ),
        (
            "Procurando Nemo",
            "Animação/Aventura",
            2003,
            "Andrew Stanton",
            "Albert Brooks",
        ),
        (
            "O Sexto Sentido",
            "Suspense/Drama",
            1999,
            "M. Night Shyamalan",
            "Bruce Willis",
        ),
        (
            "Up - Altas Aventuras",
            "Animação/Aventura",
            2009,
            "Pete Docter",
            "Edward Asner",
        ),
        ("O Show de Truman", "Drama/Comédia", 1998, "Peter Weir", "Jim Carrey"),
        ("Um Estranho no Ninho", "Drama", 1975, "Miloš Forman", "Jack Nicholson"),
        ("Cães de Aluguel", "Crime/Drama", 1992, "Quentin Tarantino", "Harvey Keitel"),
        ("Parasita", "Drama/Suspense", 2019, "Bong Joon-ho", "Song Kang-ho"),
        (
            "Whiplash: Em Busca da Perfeição",
            "Drama/Musical",
            2014,
            "Damien Chazelle",
            "Miles Teller",
        ),
        ("A Chegada", "Ficção Científica/Drama", 2016, "Denis Villeneuve", "Amy Adams"),
        (
            "Mad Max: Estrada da Fúria",
            "Ação/Ficção Científica",
            2015,
            "George Miller",
            "Tom Hardy",
        ),
        ("A Rede Social", "Drama", 2010, "David Fincher", "Jesse Eisenberg"),
        ("O Grande Lebowski", "Comédia", 1998, "Joel e Ethan Coen", "Jeff Bridges"),
        (
            "Seven: Os Sete Crimes Capitais",
            "Suspense/Crime",
            1995,
            "David Fincher",
            "Brad Pitt",
        ),
        (
            "Amelie Poulain",
            "Comédia Romântica",
            2001,
            "Jean-Pierre Jeunet",
            "Audrey Tautou",
        ),
        (
            "O Labirinto do Fauno",
            "Fantasia/Drama",
            2006,
            "Guillermo del Toro",
            "Ivana Baquero",
        ),
        (
            "Cidade de Deus",
            "Crime/Drama",
            2002,
            "Fernando Meirelles",
            "Alexandre Rodrigues",
        ),
        ("Central do Brasil", "Drama", 1998, "Walter Salles", "Fernanda Montenegro"),
        ("Tropa de Elite", "Ação/Crime", 2007, "José Padilha", "Wagner Moura"),
        (
            "Tropa de Elite 2: O Inimigo Agora é Outro",
            "Ação/Crime",
            2010,
            "José Padilha",
            "Wagner Moura",
        ),
        (
            "O Auto da Compadecida",
            "Comédia/Aventura",
            2000,
            "Guel Arraes",
            "Matheus Nachtergaele",
        ),
        ("Bacurau", "Drama/Thriller", 2019, "Kleber Mendonça Filho", "Sônia Braga"),
        ("Que Horas Ela Volta?", "Drama", 2015, "Anna Muylaert", "Regina Casé"),
        ("Carandiru", "Drama", 2003, "Hector Babenco", "Luiz Carlos Vasconcelos"),
        ("O Homem que Copiava", "Comédia/Drama", 2003, "Jorge Furtado", "Lázaro Ramos"),
        (
            "Lisbela e o Prisioneiro",
            "Comédia Romântica",
            2003,
            "Guel Arraes",
            "Selton Mello",
        ),
        (
            "Minha Mãe É Uma Peça: O Filme",
            "Comédia",
            2013,
            "André Pellenz",
            "Paulo Gustavo",
        ),
        ("Cidade Baixa", "Drama", 2005, "Sérgio Machado", "Lázaro Ramos"),
        ("O Som ao Redor", "Drama", 2012, "Kleber Mendonça Filho", "Irandhir Santos"),
        ("Capitão Fantástico", "Drama/Comédia", 2016, "Matt Ross", "Viggo Mortensen"),
        (
            "A Forma da Água",
            "Fantasia/Drama",
            2017,
            "Guillermo del Toro",
            "Sally Hawkins",
        ),
        ("Corra!", "Terror/Suspense", 2017, "Jordan Peele", "Daniel Kaluuya"),
        (
            "Lady Bird: A Hora de Voar",
            "Comédia/Drama",
            2017,
            "Greta Gerwig",
            "Saoirse Ronan",
        ),
        ("Dunkirk", "Guerra/Histórico", 2017, "Christopher Nolan", "Fionn Whitehead"),
        ("Bohemian Rhapsody", "Biografia/Musical", 2018, "Bryan Singer", "Rami Malek"),
        ("Nasce Uma Estrela", "Musical/Drama", 2018, "Bradley Cooper", "Lady Gaga"),
        (
            "Green Book: O Guia",
            "Biografia/Drama",
            2018,
            "Peter Farrelly",
            "Mahershala Ali",
        ),
        ("Nomadland", "Drama", 2020, "Chloé Zhao", "Frances McDormand"),
        ("O Pai", "Drama", 2020, "Florian Zeller", "Anthony Hopkins"),
        ("Soul", "Animação/Aventura", 2020, "Pete Docter", "Jamie Foxx"),
        (
            "Duna",
            "Ficção Científica/Aventura",
            2021,
            "Denis Villeneuve",
            "Timothée Chalamet",
        ),
        (
            "Não Olhe Para Cima",
            "Comédia/Ficção Científica",
            2021,
            "Adam McKay",
            "Leonardo DiCaprio",
        ),
        (
            "CODA: No Ritmo do Coração",
            "Drama/Musical",
            2021,
            "Sian Heder",
            "Emilia Jones",
        ),
        (
            "Tudo em Todo o Lugar ao Mesmo Tempo",
            "Ação/Comédia",
            2022,
            "Dan Kwan e Daniel Scheinert",
            "Michelle Yeoh",
        ),
        (
            "Os Banshees de Inisherin",
            "Comédia/Drama",
            2022,
            "Martin McDonagh",
            "Colin Farrell",
        ),
        (
            "Avatar: O Caminho da Água",
            "Ficção Científica/Aventura",
            2022,
            "James Cameron",
            "Sam Worthington",
        ),
        ("Oppenheimer", "Biografia/Drama", 2023, "Christopher Nolan", "Cillian Murphy"),
        ("Barbie", "Comédia/Fantasia", 2023, "Greta Gerwig", "Margot Robbie"),
    ]

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Verifica se a tabela está vazia antes de popular
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT OR IGNORE INTO filmes (titulo, genero, ano, diretor, protagonista) VALUES (?, ?, ?, ?, ?)",
            filmes_para_inserir,
        )
        conn.commit()
        print(
            f"{len(filmes_para_inserir)} filmes de exemplo inseridos em {DATABASE_NAME}."
        )
    else:
        print("Tabela 'filmes' já contém dados. Nenhuma inserção realizada.")
    conn.close()


def verificar_e_criar_diretorio_data():
    """Verifica se o diretório 'data' existe e o cria se não existir."""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Diretório 'data/' criado.")


if __name__ == "__main__":
    verificar_e_criar_diretorio_data()
    criar_tabela_filmes()
    popular_filmes_exemplo()
