"""Add ItemType and UnlockMethod

Revision ID: 29268ba49dbb
Revises: 71cc79fd09c4
Create Date: 2022-10-13 12:27:32.429507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "29268ba49dbb"
down_revision = "71cc79fd09c4"
branch_labels = None
depends_on = None


item_type_enum = sa.Enum("COLLECTIBLE", "KEY", "POI", name="itemtype")
unlock_method_enum = sa.Enum("QR_CODE", "LOCATION", name="unlockmethod")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    item_type_enum.create(op.get_bind())
    op.add_column("items", sa.Column("item_type", item_type_enum, nullable=True))
    unlock_method_enum.create(op.get_bind())
    op.add_column(
        "questItems", sa.Column("unlock_method", unlock_method_enum, nullable=True)
    )
    op.add_column(
        "quests",
        sa.Column(
            "unlock_method",
            unlock_method_enum,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quests", "unlock_method")
    op.drop_column("questItems", "unlock_method")
    unlock_method_enum.drop(op.get_bind())
    op.drop_column("items", "item_type")
    item_type_enum.drop(op.get_bind())
    # ### end Alembic commands ###