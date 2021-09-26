"""create user table

Revision ID: 7892f411fd09
Revises: 
Create Date: 2021-09-25 23:25:18.227894

"""

# revision identifiers, used by Alembic.
revision = '7892f411fd09'
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(256), nullable=False),
        sa.Column('password', sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table('user')