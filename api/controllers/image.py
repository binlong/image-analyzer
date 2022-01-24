import flask_rebar

from api.app import registry
from api.schemas.image import (
    ImageSchema,
    ImageCreationSchema,
    ImageListSchema,
    QueryImageSchema,
)
from api.services import image_service, vision_service
from flask_rebar import errors
from uuid import UUID


BASE_URL = "/images"


@registry.handles(
    method="GET",
    rule=f"{BASE_URL}/<uuid:image_id>",
    response_body_schema={200: ImageSchema()},
)
def get_image(image_id: UUID):
    image = image_service.get_image_by_id(str(image_id))

    if image is None:
        raise errors.NotFound("Image not found")

    return image, 200


@registry.handles(
    method="GET",
    rule=f"{BASE_URL}",
    query_string_schema=QueryImageSchema(),
    response_body_schema={200: ImageListSchema()},
)
def get_all_images():
    args = flask_rebar.get_validated_args()
    if 'objects' in args:
        images = image_service.get_image_by_objects(args['objects']
                                                    .strip('"')
                                                    .split(","))

        if images is None or len(images) == 0:
            raise errors.NotFound('No images found with these objects')
    else:
        images = image_service.get_all_images()

    return {'count': len(images), 'images': images}, 200


@registry.handles(
    method="POST",
    rule=BASE_URL,
    request_body_schema=ImageCreationSchema(),
    response_body_schema={201: ImageSchema()},
)
def save_image():
    body = flask_rebar.get_validated_body()

    image_location = body["file"] if "file" in body else body["url"]

    if "label" in body:
        label = body["label"]
    else:
        labels = vision_service.get_image_labels(image_location)
        label = labels[0].description if labels else "generated_label"

    objects = (
        vision_service.get_image_objects(image_location)
        if body["enable_object_detection"]
        else []
    )

    image = image_service.create_image(label, objects)

    return image, 201
