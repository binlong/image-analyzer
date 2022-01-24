import sqlalchemy as sa

from api.app import db
from sqlalchemy.orm import relationship


class Image(db.Model):
    __tablename__ = "images"

    id = sa.Column("id", sa.VARCHAR(36), primary_key=True, nullable=False, index=True)
    label = sa.Column("label", sa.VARCHAR(64), nullable=True, index=True)
    detected_objects = relationship("DetectedObject")
