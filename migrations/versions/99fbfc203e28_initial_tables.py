"""Initial tables

Revision ID: 99fbfc203e28
Revises: 
Create Date: 2024-02-23 22:30:34.452626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99fbfc203e28'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('limite', sa.Integer(), nullable=False),
    sa.Column('saldo', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('valor', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.Enum('c', 'd', name='tipotransacao'), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('realizada_em', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transacoes')
    op.drop_table('usuarios')
    # ### end Alembic commands ###
