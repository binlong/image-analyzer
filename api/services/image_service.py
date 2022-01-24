from sqlalchemy import func

from api.app import db
from api.models.detected_object import DetectedObject
from api.models.image import Image
from uuid import uuid4


def create_image(label, objects):
    image = Image(id=str(uuid4()), label=label)
    db.session.add(image)

    object_name_list = []
    for object_ in objects:
        object_name = object_.name
        if object_name not in object_name_list:
            object_name_list.append(object_name)
            detected_object = DetectedObject(
                id=str(uuid4()), image_id=image.id, name=object_.name
            )
            db.session.add(detected_object)

    db.session.commit()

    return image


def get_all_images():
    return Image.query.all()


def get_image_by_id(image_id):
    return Image.query.filter_by(id=image_id).one_or_none()


def get_image_by_objects(objects):
    image_ids = (
        db.session.query(DetectedObject.image_id)
        .filter(DetectedObject.name.in_(objects))
        .group_by(DetectedObject.image_id)
        .having(func.count(DetectedObject.image_id) == len(objects))
        .scalar_subquery()
    )
    return db.session.query(Image).filter(Image.id.in_(image_ids)).all()
