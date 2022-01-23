from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from api.app import db


class Image(db.Model):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
