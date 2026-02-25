from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "timer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("remaining_seconds", sa.Integer(), nullable=False),
        sa.Column("state", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_timer_state", "timer", ["state"], unique=False)
    op.create_index("ix_timer_updated_at", "timer", ["updated_at"], unique=False)

    op.create_table(
        "timer_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timer_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["timer_id"],
            ["timer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_timer_event_timer_id", "timer_event", ["timer_id"], unique=False)
    op.create_index("ix_timer_event_type", "timer_event", ["event_type"], unique=False)
    op.create_index("ix_timer_event_timestamp", "timer_event", ["timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_timer_event_timestamp", table_name="timer_event")
    op.drop_index("ix_timer_event_type", table_name="timer_event")
    op.drop_index("ix_timer_event_timer_id", table_name="timer_event")
    op.drop_table("timer_event")

    op.drop_index("ix_timer_updated_at", table_name="timer")
    op.drop_index("ix_timer_state", table_name="timer")
    op.drop_table("timer")
