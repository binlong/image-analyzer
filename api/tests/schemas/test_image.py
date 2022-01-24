import pytest

from api.models.image import Image
from marshmallow import ValidationError
from uuid import uuid4


TARGET_MODULE = "api.schemas.image"


def test_image_schema(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_id = uuid4()
    label = "test_label"
    image = Image(id=str(image_id), label=label)

    #when
    response = subject.ImageSchema().dump(image)

    #then
    assert response['id'] == str(image_id)
    assert response['label'] == label


def test_image_creation_schema(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'test_file.jpg',
        'label': 'test_label',
        'enable_object_detection': True
    }


    #when
    response = subject.ImageCreationSchema().load(image_creation_body)

    #then
    assert response['file'] == image_creation_body['file']
    assert response['label'] == image_creation_body['label']
    assert response['enable_object_detection'] == image_creation_body['enable_object_detection']


def test_image_creation_schema_file_url_validation(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'test_file.jpg',
        'url' : 'http://www.abc.com',
    }


    #when
    with pytest.raises(ValidationError):
        subject.ImageCreationSchema().load(image_creation_body)


def test_image_list_schema(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_id = uuid4()
    label = "test_label"
    image = Image(id=str(image_id), label=label)

    #when
    response = subject.ImageListSchema().dump({'count': 1, 'images': [image]})

    #then
    assert response['count'] == 1
    assert response['images'][0]['id'] == str(image_id)
    assert response['images'][0]['label'] == label
