"""added user table

Revision ID: 48012899b5de
Revises: 
Create Date: 2022-10-02 18:52:54.237562

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48012899b5de"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("email", sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_dt", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("disabled", sa.Boolean(), default=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
        sa.UniqueConstraint("email", name=op.f("uq__users__email")),
        sa.UniqueConstraint("username", name=op.f("uq__users__username")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
