"""01_initial-db

Revision ID: 568975ee3a98
Revises: 
Create Date: 2023-05-30 22:55:45.531825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '568975ee3a98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URLs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('target_url', sa.String(), nullable=True),
    sa.Column('short_url_id', sa.String(), nullable=True),
    sa.Column('short_url', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('URLs')
    # ### end Alembic commands ###