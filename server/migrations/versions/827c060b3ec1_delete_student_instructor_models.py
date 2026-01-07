"""Delete Student, Instructor models

Revision ID: 827c060b3ec1
Revises: 54e93f292cbd
Create Date: 2025-12-15 14:43:08.816414
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827c060b3ec1'
down_revision = '54e93f292cbd'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.drop_column('instructor_id')

    op.drop_table('lessons')
    op.drop_table('instructors')


def downgrade():
    # 1) Recreate referenced tables first
    op.create_table(
        'instructors',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(), nullable=True),
        sa.Column('email', sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'lessons',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=True),
        sa.Column('content', sa.TEXT(), nullable=True),
        sa.Column('course_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ['course_id'],
            ['courses.id'],
            name=op.f('fk_lessons_course_id_courses')
        ),
        sa.PrimaryKeyConstraint('id')
    )

    # 2) Then add column + FK back to courses
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instructor_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f('fk_courses_instructor_id_instructors'),
            'instructors',
            ['instructor_id'],
            ['id']
        )