from sistema import SistemaPonto
from menus import menu_principal
from dados import dados_exemplo


if __name__ == "__main__":
    sistema = SistemaPonto()
    
    # Descomente para carregar dados de exemplo
    # dados_exemplo(sistema)
    
    menu_principal(sistema)
