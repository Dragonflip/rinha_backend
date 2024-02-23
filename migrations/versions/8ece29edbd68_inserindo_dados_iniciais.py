"""inserindo_dados_iniciais

Revision ID: 8ece29edbd68
Revises: 9516855246c5
Create Date: 2024-02-23 11:37:45.256827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ece29edbd68'
down_revision: Union[str, None] = '9516855246c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO usuarios (limite, saldo) 
        VALUES (100000, 0),(80000, 0),(1000000, 0),(10000000, 0),(500000, 0);
        """
    )

def downgrade() -> None:
    op.execute("DELETE FROM usuarios;")
