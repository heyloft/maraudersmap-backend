"""Added unlock location to Quest

Revision ID: 109f30cf68bd
Revises: 256308233b41
Create Date: 2022-10-18 09:51:29.680055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "109f30cf68bd"
down_revision = "256308233b41"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "quests",
        sa.Column(
            "location", postgresql.ARRAY(sa.Float(), as_tuple=True), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quests", "location")
    # ### end Alembic commands ###
