"""volviendo a generar contactos

Revision ID: 3ab4efec0ad3
Revises: e66cd1c65b2e
Create Date: 2024-10-01 15:49:30.361588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ab4efec0ad3'
down_revision: Union[str, None] = 'e66cd1c65b2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contactos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('direccion', sa.String(length=120), nullable=True),
    sa.Column('telefonos', sa.String(length=50), nullable=True),
    sa.Column('fecha_nac', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contactos')
    # ### end Alembic commands ###
