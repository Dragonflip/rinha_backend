from enum import Enum
from typing import Sequence
from datetime import datetime

from pydantic import BaseModel, Field


class TipoTransacao(Enum):
    c: str = 'c'
    d: str = 'd'


class Transacao(BaseModel):
    valor: int
    tipo: TipoTransacao
    descricao: str = Field(..., max_length=10)


class RespostaTransacao(BaseModel):
    limite: int
    saldo: int


class Saldo(BaseModel):
    total: int
    data_extracao: datetime
    limite: int


class HistoricoTransacao(Transacao):
    realizada_em: datetime


class Extrato(BaseModel):
    saldo: Saldo
    ultimas_transacoes: Sequence[HistoricoTransacao]
