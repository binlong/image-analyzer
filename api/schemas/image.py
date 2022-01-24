from typing import Any

from flask_rebar import ResponseSchema, RequestSchema
from marshmallow import fields, validates_schema, ValidationError


class ImageSchema(ResponseSchema):
    id = fields.UUID()
    label = fields.String()


class ImageCreationSchema(RequestSchema):
    file = fields.String()
    url = fields.URL()
    label = fields.String(allow_none=True)
    enable_object_detection = fields.Boolean(default=False)

    @validates_schema
    def validate_file_or_url_provided(self, data: Any, **kwargs) -> None:
        if 'file' in data and 'url' in data:
            raise ValidationError('Only file or URL is needed.')

        if 'file' not in data and 'url' not in data:
            raise ValidationError('Must provide file or URL for image.')


class ImageListSchema(ResponseSchema):
    count = fields.Number()
    items = fields.List(fields.Nested(ImageSchema), default=[])
