"""Initial

Revision ID: 529e8c23bdc6
Revises: fd81b0b8a8fd
Create Date: 2023-04-28 12:18:48.783776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '529e8c23bdc6'
down_revision = 'fd81b0b8a8fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dirs',
    sa.Column('dirs_id', sa.BigInteger(), nullable=False),
    sa.Column('name_dir', sa.String(), nullable=False),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('update_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('dirs_id')
    )
    op.create_table('contentsdirs',
    sa.Column('contentsdirs_id', sa.Integer(), nullable=False),
    sa.Column('name_obj', sa.String(), nullable=False),
    sa.Column('additions', sa.String(), nullable=True),
    sa.Column('dirs_id', sa.BigInteger(), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('update_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dirs_id'], ['dirs.dirs_id'], ),
    sa.PrimaryKeyConstraint('contentsdirs_id')
    )
    op.add_column('importsimslog', sa.Column('count_sim_file', sa.Integer(), nullable=True))
    op.add_column('importsimslog', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('importsimslog', sa.Column('created_on', sa.DateTime(), nullable=False))
    op.alter_column('importsimslog', 'state',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    op.alter_column('importsimslog', 'count_import_sim',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('sims', sa.Column('hash_data', sa.String(length=100), nullable=False))
    op.add_column('updatesimlog', sa.Column('state_in_lk', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('updatesimlog', 'state_in_lk')
    op.drop_column('sims', 'hash_data')
    op.alter_column('importsimslog', 'count_import_sim',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('importsimslog', 'state',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    op.drop_column('importsimslog', 'created_on')
    op.drop_column('importsimslog', 'description')
    op.drop_column('importsimslog', 'count_sim_file')
    op.drop_table('contentsdirs')
    op.drop_table('dirs')
    # ### end Alembic commands ###
