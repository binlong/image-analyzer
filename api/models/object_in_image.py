from api.app import db
from uuid import uuid4

import sqlalchemy as sa


class ObjectInImage(db.Model):
    __tablename__ = "objects_in_image"

    id = sa.Column("id", sa.VARCHAR(36), primary_key=True, nullable=False, default=uuid4, index=True)
    image_id = sa.Column("image_id", sa.VARCHAR(36), sa.ForeignKey("images.id"), nullable=False, index=True)
    detected_object_name = sa.Column("detected_object_name", sa.VARCHAR(64), sa.ForeignKey("detected_objects.name"), nullable=False, index=True)
