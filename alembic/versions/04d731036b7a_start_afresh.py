"""start afresh

Revision ID: 04d731036b7a
Revises: 919d7da0adc2
Create Date: 2023-10-14 17:00:04.032791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '04d731036b7a'
down_revision: Union[str, None] = '919d7da0adc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('email', sa.String, unique=True, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('firstname', sa.String, nullable=True),
    sa.Column('lastname', sa.String, nullable=True),
    sa.Column('phone', sa.String, nullable=True),
    sa.Column('sex', sa.String, nullable=True),
    sa.Column('image', sa.String, nullable=True),
    sa.Column('is_active', sa.Boolean, default=True),
    sa.Column('verification_code', sa.Integer, default=100001, nullable=False),
    sa.Column('email_verified', sa.Integer, default=0, nullable=False),
    sa.Column('date_created', sa.TIMESTAMP(timezone=False), server_default=text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )

    op.create_table('business', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
    sa.Column('owner_id', sa.Integer(), nullable=False, index=True),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('about', sa.Text, nullable=True),
    sa.Column('category', sa.String, nullable=True),
    sa.Column('work_experience', sa.String, nullable=True),
    sa.Column('years_of_experience', sa.String, nullable=True),
    sa.Column('address', sa.String, nullable=True),
    sa.Column('city', sa.String, nullable=True),
    sa.Column('state', sa.String, nullable=True),
    sa.Column('country', sa.String, nullable=True),
    sa.Column('days', sa.String, nullable=True),
    sa.Column('hour_from', sa.String, nullable=True),
    sa.Column('hour_to', sa.String, nullable=True),
    sa.Column('website', sa.String, nullable=True),
    sa.Column('facebook', sa.String, nullable=True),
    sa.Column('instagram', sa.String, nullable=True),
    sa.Column('twitter', sa.String, nullable=True),
    sa.Column('linkedin', sa.String, nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('comments', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
    sa.Column('msg', sa.Text(), nullable=False),
    sa.Column('business_id', sa.Integer, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('parentuser_id', sa.Integer, nullable=False),
    sa.Column('date_created', sa.TIMESTAMP(timezone=False), server_default=text('now()')),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('category', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Integer, nullable=False),
    sa.Column('parentcat_id', sa.Integer, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    pass



def downgrade() -> None:
    op.drop_table("comments")
    op.drop_table("category")
    pass
