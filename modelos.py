import pandas as pd
from datetime import datetime
from enums import Turno, TipoEvento


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
