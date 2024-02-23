from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)

from .schemas import TipoTransacao


class Base(MappedAsDataclass, DeclarativeBase):
    ...


class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    limite: Mapped[int]
    saldo: Mapped[int]


class Transacao(Base):
    __tablename__ = 'transacoes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))
    valor: Mapped[int]
    tipo: Mapped[TipoTransacao]
    descricao: Mapped[str]
    realizada_em: Mapped[datetime]
