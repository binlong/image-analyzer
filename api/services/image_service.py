from api.app import db
from api.models.image import Image
from uuid import uuid4


def create_image(label):
    image = Image(id=str(uuid4()), label=label)
    db.session.add(image)
    db.session.commit()

    return image


def get_all_images():
    return Image.query.all()


def get_image_by(image_id):
    return Image.query.filter_by(id=image_id).one_or_none()
