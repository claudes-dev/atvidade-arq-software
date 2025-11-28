import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from enums import Turno, TipoEvento
from modelos import Funcionario


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
