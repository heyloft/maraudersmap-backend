"""Add items and POIs

Revision ID: 8ebf59d2523f
Revises: 
Create Date: 2022-09-15 10:34:20.469118

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8ebf59d2523f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "position", postgresql.ARRAY(sa.Float(), as_tuple=True), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_items_description"), "items", ["description"], unique=False
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=False)
    op.create_index(op.f("ix_items_title"), "items", ["title"], unique=False)
    op.create_table(
        "pois",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "position", postgresql.ARRAY(sa.Float(), as_tuple=True), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pois_description"), "pois", ["description"], unique=False)
    op.create_index(op.f("ix_pois_id"), "pois", ["id"], unique=False)
    op.create_index(op.f("ix_pois_title"), "pois", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_pois_title"), table_name="pois")
    op.drop_index(op.f("ix_pois_id"), table_name="pois")
    op.drop_index(op.f("ix_pois_description"), table_name="pois")
    op.drop_table("pois")
    op.drop_index(op.f("ix_items_title"), table_name="items")
    op.drop_index(op.f("ix_items_id"), table_name="items")
    op.drop_index(op.f("ix_items_description"), table_name="items")
    op.drop_table("items")
    # ### end Alembic commands ###
