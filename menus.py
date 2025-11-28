from modelos import Funcionario, Administrador
from sistema import SistemaPonto
from enums import TipoEvento


def menu_funcionario(funcionario: Funcionario, sistema: SistemaPonto) -> None:
    """Menu do funcionário"""
    while True:
        print(f"\n{'='*50}")
        print(f"Bem-vindo, {funcionario.nome}!".center(50))
        print("="*50)
        print("1 - Registrar Entrada")
        print("2 - Registrar Saída")
        print("3 - Ver Meus Horários")
        print("0 - Sair")
        print("="*50)
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            data = input("Data (DD/MM/YYYY) ou Enter: ").strip() or None
            hora = input("Hora (HH:MM) ou Enter: ").strip() or None
            funcionario.registrar_entrada(sistema, data, hora)
        
        elif opcao == '2':
            data = input("Data (DD/MM/YYYY) ou Enter: ").strip() or None
            hora = input("Hora (HH:MM) ou Enter: ").strip() or None
            funcionario.registrar_saida(sistema, data, hora)
        
        elif opcao == '3':
            registros = funcionario.consultar_horarios(sistema)
            if registros.empty:
                print("\n📋 Nenhum horário registrado.")
            else:
                print("\n" + registros.to_string(index=False))
        
        elif opcao == '0':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")


def menu_administrador(admin: Administrador, sistema: SistemaPonto) -> None:
    """Menu do administrador"""
    while True:
        print(f"\n{'='*50}")
        print(f"Painel Admin - {admin.nome}".center(50))
        print("="*50)
        print("1 - Cadastrar Funcionário")
        print("2 - Listar Funcionários")
        print("3 - Ver Registros de Ponto")
        print("4 - Gerar Relatório")
        print("5 - Gráfico: Idade")
        print("6 - Gráfico: Turno")
        print("0 - Sair")
        print("="*50)
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            matricula = input("Matrícula: ").strip()
            nome = input("Nome: ").strip()
            idade = int(input("Idade: ").strip())
            turno = input("Turno (matutino/vespertino/noturno): ").strip()
            sistema.cadastrar_funcionario(matricula, nome, idade, turno)
        
        elif opcao == '2':
            sistema.listar_funcionarios()
        
        elif opcao == '3':
            sistema.listar_registros_ponto()
        
        elif opcao == '4':
            admin.gerar_relatorio(sistema)
        
        elif opcao == '5':
            admin.gerar_grafico_idade(sistema)
        
        elif opcao == '6':
            admin.gerar_grafico_turno(sistema)
        
        elif opcao == '0':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")


def menu_principal(sistema: SistemaPonto) -> None:
    """Menu principal"""
    while True:
        print(f"\n{'='*50}")
        print("SISTEMA DE PONTO".center(50))
        print("="*50)
        print("1 - Funcionário")
        print("2 - Administrador")
        print("0 - Sair")
        print("="*50)
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            matricula = input("Matrícula: ").strip()
            funcionario = sistema.get_funcionario(matricula)
            
            if funcionario is None:
                print("❌ Funcionário não encontrado!")
                continue
            
            menu_funcionario(funcionario, sistema)
        
        elif opcao == '2':
            nome = input("Nome do Admin: ").strip()
            admin = Administrador(nome)
            menu_administrador(admin, sistema)
        
        elif opcao == '0':
            print("\n👋 Encerrando...")
            break
        else:
            print("❌ Opção inválida!")
