"""Move user location and remove extra item location

Revision ID: 6115668980db
Revises: d8cdf6fca749
Create Date: 2022-10-19 16:26:24.246559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6115668980db"
down_revision = "d8cdf6fca749"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("items", "location")
    op.drop_column("questParticipations", "location")
    op.add_column(
        "users",
        sa.Column(
            "location", postgresql.ARRAY(sa.Float(), as_tuple=True), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "location")
    op.add_column(
        "questParticipations",
        sa.Column(
            "location",
            postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "location",
            postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
