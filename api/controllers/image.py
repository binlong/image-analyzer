import flask_rebar

from api.app import registry
from api.schemas.image import ImageSchema, ImageCreationSchema
from uuid import uuid4, UUID

BASE_URL = "/images"


@registry.handles(
    method="GET",
    rule=BASE_URL,
    response_body_schema={200: ImageSchema()},
)
def get_images():
    return {"id": uuid4()}


@registry.handles(
    method="GET",
    rule=f"{BASE_URL}/<uuid:image_id>",
    response_body_schema={200: ImageSchema()},
)
def get_image(image_id: UUID):
    return {"id": image_id}


@registry.handles(
    method="POST",
    rule=BASE_URL,
    request_body_schema=ImageCreationSchema,
    response_body_schema={200: ImageSchema()},
)
def save_image():
    body = flask_rebar.get_validated_body()
    image = {"id": uuid4()}

    if 'label' in body:
        image['label'] = body['label']
    else:
        image['label'] = "generated_label"

    return image
