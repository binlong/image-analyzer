"""Create required tables

Revision ID: 7bd0ac88a60d
Revises: 
Create Date: 2022-01-23 17:28:01.259474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bd0ac88a60d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detected_objects',
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_index(op.f('ix_detected_objects_name'), 'detected_objects', ['name'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('label', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    op.create_index(op.f('ix_images_label'), 'images', ['label'], unique=False)
    op.create_table('objects_in_image',
    sa.Column('id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('image_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('detected_object_name', sa.VARCHAR(length=64), nullable=False),
    sa.ForeignKeyConstraint(['detected_object_name'], ['detected_objects.name'], ),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objects_in_image_detected_object_name'), 'objects_in_image', ['detected_object_name'], unique=False)
    op.create_index(op.f('ix_objects_in_image_id'), 'objects_in_image', ['id'], unique=False)
    op.create_index(op.f('ix_objects_in_image_image_id'), 'objects_in_image', ['image_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_objects_in_image_image_id'), table_name='objects_in_image')
    op.drop_index(op.f('ix_objects_in_image_id'), table_name='objects_in_image')
    op.drop_index(op.f('ix_objects_in_image_detected_object_name'), table_name='objects_in_image')
    op.drop_table('objects_in_image')
    op.drop_index(op.f('ix_images_label'), table_name='images')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_detected_objects_name'), table_name='detected_objects')
    op.drop_table('detected_objects')
    # ### end Alembic commands ###