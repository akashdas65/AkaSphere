"""create message reactions table

Revision ID: b13a21ca43a4
Revises: 51b55b7a0f0d
Create Date: 2026-08-22 13:33:24.507661

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b13a21ca43a4"
down_revision: Union[str, Sequence[str], None] = "51b55b7a0f0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create message_reactions table."""

    op.create_table(
        "message_reactions",

        sa.Column(
            "id",
            sa.String(length=36),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "message_id",
            sa.String(length=36),
            sa.ForeignKey(
                "messages.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.String(length=36),
            sa.ForeignKey(
                "users.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "emoji",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "message_id",
            "user_id",
            "emoji",
            name="uq_message_reaction_user_emoji",
        ),
    )

    op.create_index(
        "ix_message_reactions_message_id",
        "message_reactions",
        ["message_id"],
    )

    op.create_index(
        "ix_message_reactions_user_id",
        "message_reactions",
        ["user_id"],
    )


def downgrade() -> None:
    """Drop message_reactions table."""

    op.drop_index(
        "ix_message_reactions_user_id",
        table_name="message_reactions",
    )

    op.drop_index(
        "ix_message_reactions_message_id",
        table_name="message_reactions",
    )

    op.drop_table("message_reactions")