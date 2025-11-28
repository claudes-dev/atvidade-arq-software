from datetime import datetime
from enum import Enum


class Turno(Enum):
    """Enum para tipos de turno"""
    MATUTINO = "matutino"
    VESPERTINO = "vespertino"
    NOTURNO = "noturno"


class TipoEvento(Enum):
    """Enum para tipos de eventos de ponto"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
