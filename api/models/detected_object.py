from api.app import db
import sqlalchemy as sa


class DetectedObject(db.Model):
    __tablename__ = "detected_objects"

    id = sa.Column("id", sa.VARCHAR(36), primary_key=True, nullable=False, index=True)
    image_id = sa.Column(
        "image_id",
        sa.VARCHAR(36),
        sa.ForeignKey("images.id"),
        nullable=False,
        index=True,
    )
    name = sa.Column("name", sa.VARCHAR(64), nullable=False, index=True)
