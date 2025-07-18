import unittest

if __name__ == "__main__":
    # 'discover' procura por todos os arquivos 'test_*.py' dentro da pasta 'tests'.
    # Isso garante que todos os seus testes sejam encontrados e executados.
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        "tests", pattern="test_*.py"
    )  # Procura em 'tests/' por arquivos 'test_*.py'

    # Executa a suíte de testes.
    unittest.TextTestRunner(verbosity=2).run(test_suite)
