"""empty message

Revision ID: 6e011caf7bf7
Revises: 73ba916bd1c6
Create Date: 2024-07-12 02:55:13.811044

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e011caf7bf7'
down_revision = '73ba916bd1c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('simcards', sa.Column('simcards_id', sa.Integer(), nullable=False))
    op.add_column('simcards', sa.Column('apnpassword', sa.Text(), nullable=True))
    op.alter_column('simcards', 'operator',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('simcards', 'iccid',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('simcards', 'msisdn',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('simcards', 'ip',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('simcards', 'date_receipt',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('simcards', 'simcard_id')
    op.drop_column('simcards', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('simcards', sa.Column('password', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('simcards', sa.Column('simcard_id', sa.BIGINT(), autoincrement=True, nullable=False))
    op.alter_column('simcards', 'date_receipt',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('simcards', 'ip',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('simcards', 'msisdn',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('simcards', 'iccid',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('simcards', 'operator',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('simcards', 'apnpassword')
    op.drop_column('simcards', 'simcards_id')
    # ### end Alembic commands ###