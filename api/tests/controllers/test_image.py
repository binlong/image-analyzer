import pytest

from api.models.image import Image
from flask_rebar import errors
from mock import patch
from uuid import uuid4


TARGET_MODULE = "api.controllers.image"


@patch(f"{TARGET_MODULE}.image_service")
def test_get_all_images_returns_all_images(image_service_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_list = [Image(id=str(uuid4()), label="test_label")]
    image_service_mock.get_all_images.return_value = image_list

    #when
    response = subject.get_all_images()

    #then
    assert response[0]['count'] == 1
    assert response[0]['images'] == image_list
    assert response[1] == 200


@patch(f"{TARGET_MODULE}.image_service")
def test_get_image_returns_image(image_service_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_id = uuid4()
    label = "test_label"
    image = Image(id=str(image_id), label=label)
    image_service_mock.get_image_by.return_value = image

    #when
    response = subject.get_image(image_id)

    #then
    assert response[0].id == str(image_id)
    assert response[0].label == label
    assert response[1] == 200


@patch(f"{TARGET_MODULE}.image_service")
def test_get_image_with_image_not_found_raises_not_found(image_service_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    #setup
    image_service_mock.get_image_by.return_value = None

    #when
    with pytest.raises(errors.NotFound):
        subject.get_image(uuid4())
