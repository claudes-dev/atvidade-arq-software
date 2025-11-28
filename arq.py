import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class Turno(Enum):
    """Enum para tipos de turno"""
    MATUTINO = "matutino"
    VESPERTINO = "vespertino"
    NOTURNO = "noturno"


class TipoEvento(Enum):
    """Enum para tipos de eventos de ponto"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


# ============================================================================
# CLASSES DE MODELO
# ============================================================================

class Funcionario:
    """Representa um funcionário do sistema"""
    
    def __init__(self, matricula: str, nome: str, idade: int, turno: Turno):
        self.matricula = matricula
        self.nome = nome
        self.idade = idade
        self.turno = turno
    
    def registrar_entrada(self, sistema: 'SistemaPonto', data: str = None, hora: str = None) -> bool:
        """Registra entrada do funcionário"""
        return sistema.registrar_evento(self.matricula, TipoEvento.ENTRADA, data, hora)
    
    def registrar_saida(self, sistema: 'SistemaPonto', data: str = None, hora: str = None) -> bool:
        """Registra saída do funcionário"""
        return sistema.registrar_evento(self.matricula, TipoEvento.SAIDA, data, hora)
    
    def consultar_horarios(self, sistema: 'SistemaPonto') -> pd.DataFrame:
        """Consulta horários registrados do funcionário"""
        return sistema.consultar_eventos(self.matricula)


class EventoPonto:
    """Representa um evento de ponto (entrada/saída)"""
    
    id_counter = 1
    
    def __init__(self, id: int, data_hora: datetime, tipo: TipoEvento):
        self.id = id if id else EventoPonto.id_counter
        if id is None:
            EventoPonto.id_counter += 1
        self.data_hora = data_hora
        self.tipo = tipo


class RelatorioPonto:
    """Representa um relatório de ponto"""
    
    def __init__(self, periodo_inicial: datetime, periodo_final: datetime, funcionario: Funcionario):
        self.periodo_inicial = periodo_inicial
        self.periodo_final = periodo_final
        self.funcionario = funcionario
    
    def calcular_horas_trabalhadas(self) -> float:
        """Calcula total de horas trabalhadas"""
        pass


class Administrador:
    """Representa um administrador do sistema"""
    
    def __init__(self, nome: str):
        self.nome = nome
    
    def gerar_relatorio(self, sistema: 'SistemaPonto') -> None:
        """Gera relatório de ponto"""
        sistema.gerar_relatorio_completo()
    
    def gerar_grafico_idade(self, sistema: 'SistemaPonto') -> None:
        """Gera gráfico de funcionários por idade"""
        sistema.grafico_barras_idade()
    
    def gerar_grafico_turno(self, sistema: 'SistemaPonto') -> None:
        """Gera gráfico de funcionários por turno"""
        sistema.grafico_pizza_turno()


# ============================================================================
# SISTEMA PRINCIPAL
# ============================================================================

class SistemaPonto:
    """Sistema de gerenciamento de ponto"""
    
    def __init__(self):
        self.funcionarios_df = pd.DataFrame(columns=['matricula', 'nome', 'idade', 'turno'])
        self.registros_ponto_df = pd.DataFrame(columns=['matricula', 'nome', 'data', 'entrada', 'saida'])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
    
    # ---- GERENCIAMENTO DE FUNCIONÁRIOS ----
    
    def cadastrar_funcionario(self, matricula: str, nome: str, idade: int, turno: str) -> bool:
        """Cadastra novo funcionário"""
        turnos_validos = [t.value for t in Turno]
        if turno.lower() not in turnos_validos:
            print(f"❌ Turno deve ser: {', '.join(turnos_validos)}")
            return False
        
        if matricula in self.funcionarios_df['matricula'].values:
            print(f"❌ Matrícula {matricula} já existe!")
            return False
        
        novo = pd.DataFrame({
            'matricula': [matricula],
            'nome': [nome],
            'idade': [idade],
            'turno': [turno.lower()]
        })
        self.funcionarios_df = pd.concat([self.funcionarios_df, novo], ignore_index=True)
        print(f"✅ {nome} cadastrado!")
        return True
    
    def listar_funcionarios(self) -> None:
        """Lista todos os funcionários"""
        if self.funcionarios_df.empty:
            print("📋 Nenhum funcionário cadastrado.")
            return
        print("\n" + "="*70)
        print(self.funcionarios_df.to_string(index=False))
        print("="*70 + "\n")
    
    def get_funcionario(self, matricula: str) -> Funcionario:
        """Obtém funcionário pela matrícula"""
        if matricula not in self.funcionarios_df['matricula'].values:
            return None
        
        row = self.funcionarios_df[self.funcionarios_df['matricula'] == matricula].iloc[0]
        turno_str = row['turno']
        turno = Turno(turno_str) if turno_str in [t.value for t in Turno] else None
        
        return Funcionario(row['matricula'], row['nome'], row['idade'], turno)
    
    # ---- REGISTRO DE PONTO ----
    
    def registrar_evento(self, matricula: str, tipo: TipoEvento, data: str = None, hora: str = None) -> bool:
        """Registra evento de entrada/saída"""
        if tipo == TipoEvento.ENTRADA:
            return self._registrar_entrada(matricula, data, hora)
        elif tipo == TipoEvento.SAIDA:
            return self._registrar_saida(matricula, data, hora)
        return False
    
    def _registrar_entrada(self, matricula: str, data: str = None, hora: str = None) -> bool:
        """Registra entrada"""
        if matricula not in self.funcionarios_df['matricula'].values:
            print(f"❌ Funcionário não existe!")
            return False
        
        data = data or datetime.now().strftime("%d/%m/%Y")
        hora = hora or datetime.now().strftime("%H:%M")
        nome = self.funcionarios_df[self.funcionarios_df['matricula'] == matricula]['nome'].values[0]
        
        novo = pd.DataFrame({
            'matricula': [matricula],
            'nome': [nome],
            'data': [data],
            'entrada': [hora],
            'saida': [None]
        })
        self.registros_ponto_df = pd.concat([self.registros_ponto_df, novo], ignore_index=True)
        print(f"✅ Entrada registrada para {nome}")
        return True
    
    def _registrar_saida(self, matricula: str, data: str = None, hora: str = None) -> bool:
        """Registra saída"""
        if self.registros_ponto_df.empty:
            print("❌ Nenhum registro disponível!")
            return False
        
        data = data or datetime.now().strftime("%d/%m/%Y")
        hora = hora or datetime.now().strftime("%H:%M")
        
        registros = self.registros_ponto_df[
            (self.registros_ponto_df['matricula'] == matricula) & 
            (self.registros_ponto_df['data'] == data) &
            (self.registros_ponto_df['saida'].isna())
        ]
        
        if registros.empty:
            print(f"❌ Nenhuma entrada registrada hoje!")
            return False
        
        indice = registros.index[0]
        self.registros_ponto_df.at[indice, 'saida'] = hora
        nome = self.funcionarios_df[self.funcionarios_df['matricula'] == matricula]['nome'].values[0]
        print(f"✅ Saída registrada para {nome}")
        return True
    
    def consultar_eventos(self, matricula: str) -> pd.DataFrame:
        """Consulta eventos de um funcionário"""
        return self.registros_ponto_df[self.registros_ponto_df['matricula'] == matricula]
    
    def listar_registros_ponto(self) -> None:
        """Lista todos os registros de ponto"""
        if self.registros_ponto_df.empty:
            print("📋 Nenhum registro de ponto.")
            return
        print("\n" + "="*80)
        print(self.registros_ponto_df.to_string(index=False))
        print("="*80 + "\n")
    
    # ---- RELATÓRIOS E GRÁFICOS ----
    
    def gerar_relatorio_completo(self) -> None:
        """Gera relatório com estatísticas"""
        if self.funcionarios_df.empty:
            print("❌ Nenhum funcionário cadastrado!")
            return
        
        print("\n" + "="*70)
        print("RELATÓRIO DE PONTO".center(70))
        print("="*70)
        print(f"\n📊 Total de funcionários: {len(self.funcionarios_df)}")
        print(f"📊 Total de registros: {len(self.registros_ponto_df)}")
        
        print("\n📈 Funcionários por turno:")
        for turno, count in self.funcionarios_df['turno'].value_counts().items():
            print(f"   • {turno.capitalize()}: {count}")
        
        media_idade = self.funcionarios_df['idade'].mean()
        print(f"\n📈 Idade média: {media_idade:.1f} anos")
        print(f"📈 Idade mínima: {self.funcionarios_df['idade'].min()} anos")
        print(f"📈 Idade máxima: {self.funcionarios_df['idade'].max()} anos")
        print("\n" + "="*70 + "\n")
    
    def grafico_barras_idade(self) -> None:
        """Gráfico de funcionários por idade"""
        if self.funcionarios_df.empty:
            print("❌ Nenhum funcionário cadastrado!")
            return
        
        df = self.funcionarios_df.sort_values('idade')
        plt.figure(figsize=(12, 6))
        plt.bar(df['nome'], df['idade'], color='steelblue', edgecolor='navy', alpha=0.7)
        plt.xlabel('Funcionário', fontsize=12, fontweight='bold')
        plt.ylabel('Idade', fontsize=12, fontweight='bold')
        plt.title('Funcionários por Idade', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def grafico_pizza_turno(self) -> None:
        """Gráfico de funcionários por turno"""
        if self.funcionarios_df.empty:
            print("❌ Nenhum funcionário cadastrado!")
            return
        
        turno_counts = self.funcionarios_df['turno'].value_counts()
        cores = {'matutino': '#FFD700', 'vespertino': '#87CEEB', 'noturno': '#2F4F4F'}
        cores_lista = [cores.get(turno, '#808080') for turno in turno_counts.index]
        
        plt.figure(figsize=(10, 8))
        plt.pie(turno_counts.values,
                labels=[f"{t.capitalize()}\n({c})" for t, c in zip(turno_counts.index, turno_counts.values)],
                autopct='%1.1f%%',
                colors=cores_lista,
                startangle=90)
        plt.title('Distribuição por Turno', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()


# ============================================================================
# MENUS
# ============================================================================

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


def dados_exemplo(sistema: SistemaPonto) -> None:
    """Carrega dados de exemplo"""
    sistema.cadastrar_funcionario('001', 'João Silva', 28, 'matutino')
    sistema.cadastrar_funcionario('002', 'Maria Santos', 35, 'vespertino')
    sistema.cadastrar_funcionario('003', 'Pedro Oliveira', 42, 'noturno')
    sistema.cadastrar_funcionario('004', 'Ana Costa', 26, 'matutino')
    
    sistema.registrar_evento('001', TipoEvento.ENTRADA, '28/11/2025', '08:00')
    sistema.registrar_evento('001', TipoEvento.SAIDA, '28/11/2025', '17:30')
    
    sistema.registrar_evento('002', TipoEvento.ENTRADA, '28/11/2025', '13:00')
    sistema.registrar_evento('002', TipoEvento.SAIDA, '28/11/2025', '22:00')
    
    print("✅ Dados de exemplo carregados!\n")


if __name__ == "__main__":
    sistema = SistemaPonto()
    
    # Descomente para carregar dados de exemplo
    # dados_exemplo(sistema)
    
    menu_principal(sistema)
