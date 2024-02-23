from typing import List
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import parse_obj_as

from rinha_backend.schemas import (
    Extrato,
    Saldo,
    Extrato,
    HistoricoTransacao,
    Transacao as TransacaoSchema,
    RespostaTransacao,
)
from rinha_backend.engine import get_session
from rinha_backend.models import Usuario, Transacao


app = FastAPI()


@app.post('/clients/{user_id}/transacao', response_model=RespostaTransacao)
def post_transacao(
    user_id: int,
    transacao: TransacaoSchema,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(Usuario).where(Usuario.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    if transacao.tipo.value == 'd':
        saldo = db_user.saldo - transacao.valor
        if db_user.limite < -saldo:
            raise HTTPException(status_code=422, detail='Not enought limit')
        db_user.saldo = saldo
    else:
        db_user.saldo += transacao.valor
    transacao_db = Transacao(
        user_id=user_id,
        valor=transacao.valor,
        tipo=transacao.tipo,
        descricao=transacao.descricao,
        realizada_em=datetime.now(),
    )
    session.add(transacao_db)
    session.commit()
    return RespostaTransacao(limite=db_user.limite, saldo=db_user.saldo)


@app.get('/clientes/{user_id}/extrato', response_model=Extrato)
def get_extrato(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(Usuario).where(Usuario.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    saldo = Saldo(
        limite=db_user.limite,
        data_extracao=datetime.now(),
        total=db_user.saldo,
    )
    db_transacoes = session.scalars(
        select(Transacao)
        .where(Transacao.user_id == user_id)
        .order_by(Transacao.realizada_em.desc())
        .limit(10)
    )
    transacoes = [
        HistoricoTransacao(
            valor=transacao.valor,
            tipo=transacao.tipo,
            descricao=transacao.descricao,
            realizada_em=transacao.realizada_em,
        )
        for transacao in db_transacoes.all()
    ]
    print(transacoes)
    return Extrato(saldo=saldo, ultimas_transacoes=list(transacoes))
