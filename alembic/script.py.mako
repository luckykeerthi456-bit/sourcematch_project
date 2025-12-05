% if dunder %>
"""A generic migration script template used by alembic when autogenerating
revisions. This file is intentionally minimal; the regular alembic init uses
this template.
"""
% endif

from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
