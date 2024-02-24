from typing import List
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
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
from rinha_backend.engine import get_session, get_async_session
from rinha_backend.models import Usuario, Transacao


app = FastAPI()


@app.post(
    '/clientes/{user_id}/transacoes',
    status_code=status.HTTP_200_OK,
    response_model=RespostaTransacao,
)
async def post_transacao(
    user_id: int,
    transacao: TransacaoSchema,
    session: Session = Depends(get_async_session),
):
    async with session() as session:
        db_user = await session.scalar(select(Usuario).where(Usuario.id == user_id))
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
        session.add(db_user)
        session.add(transacao_db)
        await session.commit()
        return RespostaTransacao(limite=db_user.limite, saldo=db_user.saldo)


@app.get('/clientes/{user_id}/extrato', response_model=Extrato)
async def get_extrato(user_id: int, session: Session = Depends(get_async_session)):
    async with session() as session:
        db_user = await session.scalar(select(Usuario).where(Usuario.id == user_id))
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')
        saldo = Saldo(
            limite=db_user.limite,
            data_extracao=datetime.now(),
            total=db_user.saldo,
        )
        db_transacoes = await session.scalars(
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
        return Extrato(saldo=saldo, ultimas_transacoes=list(transacoes))
