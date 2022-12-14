"""Fixed QuestParticipation primary key name

Revision ID: bf1c9e8dd140
Revises: 2823eb3b2f6f
Create Date: 2022-10-11 22:50:36.081630

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bf1c9e8dd140'
down_revision = '2823eb3b2f6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questParticipations', sa.Column('quest_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.drop_index('ix_questParticipations_qust_id', table_name='questParticipations')
    op.create_index(op.f('ix_questParticipations_quest_id'), 'questParticipations', ['quest_id'], unique=False)
    op.drop_constraint('questParticipations_qust_id_fkey', 'questParticipations', type_='foreignkey')
    op.create_foreign_key(None, 'questParticipations', 'quests', ['quest_id'], ['id'])
    op.drop_column('questParticipations', 'qust_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questParticipations', sa.Column('qust_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'questParticipations', type_='foreignkey')
    op.create_foreign_key('questParticipations_qust_id_fkey', 'questParticipations', 'quests', ['qust_id'], ['id'])
    op.drop_index(op.f('ix_questParticipations_quest_id'), table_name='questParticipations')
    op.create_index('ix_questParticipations_qust_id', 'questParticipations', ['qust_id'], unique=False)
    op.drop_column('questParticipations', 'quest_id')
    # ### end Alembic commands ###
