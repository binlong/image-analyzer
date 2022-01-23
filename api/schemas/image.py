from flask_rebar import ResponseSchema
from marshmallow import fields


class ImageSchema(ResponseSchema):
    id = fields.String()
