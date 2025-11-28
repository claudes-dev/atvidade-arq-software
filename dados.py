from sistema import SistemaPonto
from enums import TipoEvento


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
