"""empty message

Revision ID: a7dee3b170ac
Revises: c7197c02cc57
Create Date: 2025-06-29 22:35:41.351055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7dee3b170ac'
down_revision: Union[str, Sequence[str], None] = 'c7197c02cc57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
