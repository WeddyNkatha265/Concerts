"""Create initial tables

Revision ID: ef943e9bac8d
Revises: 
Create Date: 2024-09-16 14:20:08.425579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef943e9bac8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables
    op.create_table(
        'bands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('hometown', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'venues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'concerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('band_id', sa.Integer(), nullable=False),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['band_id'], ['bands.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id'])
    )

def downgrade():
    # Drop tables
    op.drop_table('concerts')
    op.drop_table('venues')
    op.drop_table('bands')