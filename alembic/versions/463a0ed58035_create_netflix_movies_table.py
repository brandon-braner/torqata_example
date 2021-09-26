"""create_netflix_movies_table

Revision ID: 463a0ed58035
Revises: f8f33fe87873
Create Date: 2021-09-26 00:24:24.915608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '463a0ed58035'
down_revision = 'f8f33fe87873'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'netflix_movies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('netflix_id', sa.String(256), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('date_added', sa.String(), nullable=False),
        sa.Column('release_year', sa.String(), nullable=False),
        sa.Column('rating', sa.String(), nullable=False),
        sa.Column('duration', sa.String(), nullable=False),
    )

    op.create_index('movies_title_idx', 'netflix_movies', ['title'])
    op.create_index('movies_date_added_idx', 'netflix_movies', ['date_added'])
    op.create_index('movies_duration', 'netflix_movies', ['duration'])


def downgrade():
    op.drop_table('netflix_shows')
