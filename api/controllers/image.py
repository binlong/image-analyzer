import flask_rebar

from api.app import registry
from api.schemas.image import ImageSchema, ImageCreationSchema, ImageListSchema
from api.services import image_service
from flask_rebar import errors
from uuid import UUID


BASE_URL = "/images"


@registry.handles(
    method="GET",
    rule=BASE_URL,
    response_body_schema={200: ImageListSchema()},
)
def get_all_images():
    images = image_service.get_all_images()

    return {"count": len(images), "images": images}, 200


@registry.handles(
    method="GET",
    rule=f"{BASE_URL}/<uuid:image_id>",
    response_body_schema={200: ImageSchema()},
)
def get_image(image_id: UUID):
    image = image_service.get_image_by(str(image_id))

    if image is None:
        raise errors.NotFound("Image not found")

    return image, 200


@registry.handles(
    method="POST",
    rule=BASE_URL,
    request_body_schema=ImageCreationSchema(),
    response_body_schema={201: ImageSchema()},
)
def save_image():
    body = flask_rebar.get_validated_body()
    if 'label' in body:
        label = body['label']
    else:
        label = "generated_label"

    image = image_service.create_image(label)

    return image, 201
