"""create_netflix_shows_table

Revision ID: f8f33fe87873
Revises: 7892f411fd09
Create Date: 2021-09-26 00:14:22.229681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8f33fe87873'
down_revision = '7892f411fd09'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'netflix_shows',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('netflix_id', sa.String(256), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('date_added', sa.String(), nullable=False),
        sa.Column('release_year', sa.String(), nullable=False),
        sa.Column('rating', sa.String(), nullable=False),
        sa.Column('duration', sa.String(), nullable=False),
    )

    op.create_index('shows_title_idx', 'netflix_shows', ['title'])
    op.create_index('shows_date_added_idx', 'netflix_shows', ['date_added'])


def downgrade():
    op.drop_table('netflix_shows')
