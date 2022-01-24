import pytest

from api.models.image import Image
from marshmallow import ValidationError
from mock import patch
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

@patch(f"{TARGET_MODULE}.imghdr")
def test_image_creation_schema(imghdr_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'test_file.jpg',
        'label': 'test_label',
        'enable_object_detection': True
    }
    imghdr_mock.what.return_value = 'jpg'

    #when
    response = subject.ImageCreationSchema().load(image_creation_body)

    #then
    assert response['file'] == image_creation_body['file']
    assert response['label'] == image_creation_body['label']
    assert response['enable_object_detection'] == image_creation_body['enable_object_detection']


def test_image_creation_schema_file_location_validation(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'failed-location.jpg',
        'label': 'test_label',
        'enable_object_detection': True
    }



    #when
    with pytest.raises(ValidationError) as error:
        subject.ImageCreationSchema().load(image_creation_body)

    #then
    assert error.value.messages['_schema'][0] == 'Must provide correct file location'


@patch(f"{TARGET_MODULE}.imghdr")
def test_image_creation_schema_not_image_file(imghdr_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'test_file.txt',
        'label': 'test_label',
        'enable_object_detection': True
    }
    imghdr_mock.what.return_value = None


    #when
    with pytest.raises(ValidationError) as error:
        subject.ImageCreationSchema().load(image_creation_body)

    #then
    assert error.value.messages['_schema'][0] == 'Must provide valid image format'


def test_image_creation_schema_file_url_not_both_provided_validation(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {
        'file': 'test_file.jpg',
        'url' : 'http://www.abc.com',
    }


    #when
    with pytest.raises(ValidationError) as error:
        subject.ImageCreationSchema().load(image_creation_body)

    # then
    assert error.value.messages['_schema'][0] == 'Only file or URL is needed.'


def test_image_creation_schema_need_file_or_url_provided(get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_creation_body = {'label': 'test_label'}

    #when
    with pytest.raises(ValidationError) as error:
        subject.ImageCreationSchema().load(image_creation_body)

    # then
    assert error.value.messages['_schema'][0] == 'Must provide file or URL for image.'


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
