"""inserindo dados

Revision ID: d2930559878f
Revises: 99fbfc203e28
Create Date: 2024-02-23 22:30:53.768363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2930559878f'
down_revision: Union[str, None] = '99fbfc203e28'
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
