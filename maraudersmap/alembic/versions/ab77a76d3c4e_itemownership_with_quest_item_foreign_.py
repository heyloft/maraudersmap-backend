"""ItemOwnership with quest item foreign key

Revision ID: ab77a76d3c4e
Revises: 97684545f321
Create Date: 2022-10-28 14:05:52.068640

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ab77a76d3c4e"
down_revision = "97684545f321"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "itemOwnerships",
        sa.Column("quest_item_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.drop_constraint(
        "itemOwnerships_item_id_fkey", "itemOwnerships", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "itemOwnerships", "questItems", ["quest_item_id"], ["id"]
    )
    op.drop_column("itemOwnerships", "item_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "itemOwnerships",
        sa.Column("item_id", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "itemOwnerships", type_="foreignkey")
    op.create_foreign_key(
        "itemOwnerships_item_id_fkey", "itemOwnerships", "items", ["item_id"], ["id"]
    )
    op.drop_column("itemOwnerships", "quest_item_id")
    # ### end Alembic commands ###
