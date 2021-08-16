"""skills in task

Revision ID: 2b627fb26112
Revises: 
Create Date: 2021-08-13 16:24:48.077716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b627fb26112'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('skill', sa.Column('task_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'skill', 'task', ['task_id'], ['id'])
    op.drop_constraint('task_skill_id_fkey', 'task', type_='foreignkey')
    op.drop_column('task', 'skill_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('skill_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('task_skill_id_fkey', 'task', 'skill', ['skill_id'], ['id'])
    op.drop_constraint(None, 'skill', type_='foreignkey')
    op.drop_column('skill', 'task_id')
    # ### end Alembic commands ###