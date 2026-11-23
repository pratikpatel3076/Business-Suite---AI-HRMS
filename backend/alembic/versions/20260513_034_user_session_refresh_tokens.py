"""Add session_id to user_sessions for refresh-token rotation

Revision ID: 20260513_034
Revises: 20260512_033
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa


revision = "20260513_034"
down_revision = "20260512_033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user_sessions", sa.Column("session_id", sa.String(length=64), nullable=True))
    op.create_index(op.f("ix_user_sessions_session_id"), "user_sessions", ["session_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_sessions_session_id"), table_name="user_sessions")
    op.drop_column("user_sessions", "session_id")
