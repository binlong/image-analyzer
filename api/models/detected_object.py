from api.app import db
import sqlalchemy as sa


class DetectedObject(db.Model):
    __tablename__ = "detected_objects"

    name = sa.Column("name", sa.VARCHAR(64), primary_key=True, nullable=False, index=True)
