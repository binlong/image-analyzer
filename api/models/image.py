from api.app import db
from uuid import uuid4

import sqlalchemy as sa



class Image(db.Model):
    __tablename__ = "images"

    id = sa.Column("id", sa.VARCHAR(36), primary_key=True, nullable=False, default=uuid4, index=True)
    label = sa.Column("label", sa.VARCHAR(64), nullable=True, index=True)
