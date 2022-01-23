from api.app import registry
from api.schemas.image import ImageSchema

BASE_URL = "/images"


@registry.handles(
    method="GET",
    rule=BASE_URL,
    response_body_schema={200: ImageSchema()},
)
def get_images():
    return {"id": "image_id"}
