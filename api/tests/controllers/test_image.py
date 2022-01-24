import pytest
from munch import DefaultMunch

from api.models.image import Image
from flask_rebar import errors
from mock import patch
from uuid import uuid4


TARGET_MODULE = "api.controllers.image"


@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_get_all_images_returns_without_objects_all_images(
        flask_rebar_mock, image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    flask_rebar_mock.get_validated_args.return_value = {}
    image_list = [Image(id=str(uuid4()), label="test_label")]
    image_service_mock.get_all_images.return_value = image_list

    # when
    response = subject.get_all_images()

    # then
    assert response[0]["count"] == 1
    assert response[0]["images"] == image_list
    assert response[1] == 200


@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_get_all_images_with_objects_returns_list_of_images(
    flask_rebar_mock, image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    image_list = [Image(id=str(uuid4()), label="test_label")]
    flask_rebar_mock.get_validated_args.return_value = {"objects": '"x,y,z"'}
    image_service_mock.get_image_by_objects.return_value = image_list

    # when
    response = subject.get_all_images()

    # then
    assert response[0]["count"] == 1
    assert response[0]["images"] == image_list
    assert response[1] == 200


@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_get_all_images_with_objects_with_none_found_raises_not_found(
    flask_rebar_mock, image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    flask_rebar_mock.get_validated_args.return_value = {"objects": '"x,y,z"'}
    image_service_mock.get_image_by_objects.return_value = None

    # when
    with pytest.raises(errors.NotFound):
        subject.get_all_images()


@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_get_all_images_with_objects_with_len_zero_raises_not_found(
    flask_rebar_mock, image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    #  setup
    flask_rebar_mock.get_validated_args.return_value = {"objects": '"x,y,z"'}
    image_service_mock.get_image_by_objects.return_value = []

    # when
    with pytest.raises(errors.NotFound):
        subject.get_all_images()


@patch(f"{TARGET_MODULE}.image_service")
def test_get_image_returns_image(image_service_mock, get_handler):
    subject = get_handler(TARGET_MODULE)

    # setup
    image_id = uuid4()
    label = "test_label"
    image = Image(id=str(image_id), label=label)
    image_service_mock.get_image_by_id.return_value = image

    # when
    response = subject.get_image(image_id)

    # then
    assert response[0].id == str(image_id)
    assert response[0].label == label
    assert response[1] == 200


@patch(f"{TARGET_MODULE}.image_service")
def test_get_image_with_image_not_found_raises_not_found(
    image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    image_service_mock.get_image_by_id.return_value = None

    # when
    with pytest.raises(errors.NotFound):
        subject.get_image(uuid4())


@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_save_image_with_provided_label_returns_image(
    flask_rebar_mock, image_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    #  setup
    label = "provided_label"
    image = Image(id=str(uuid4()), label=label)
    flask_rebar_mock.get_validated_body.return_value = {
        "file": "test.jpg",
        "label": label,
        "enable_object_detection": False,
    }
    image_service_mock.create_image.return_value = image
    # when
    response = subject.save_image()

    # then
    assert response[0].id == image.id
    assert response[0].label == label
    assert response[1] == 201


@patch(f"{TARGET_MODULE}.vision_service")
@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_save_image_without_provided_label_returns_image(
    flask_rebar_mock, image_service_mock, vision_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    label = "label_from_image_analyzer"
    image = Image(id=str(uuid4()), label=label)
    flask_rebar_mock.get_validated_body.return_value = {
        "file": "test.jpg",
        "enable_object_detection": False,
    }
    vision_service_mock.get_image_labels.return_value = [
        DefaultMunch.fromDict({"description": label})
    ]
    image_service_mock.create_image.return_value = image

    # when
    response = subject.save_image()

    # then
    assert response[0].id == image.id
    assert response[0].label == label
    assert response[1] == 201


@patch(f"{TARGET_MODULE}.vision_service")
@patch(f"{TARGET_MODULE}.image_service")
@patch(f"{TARGET_MODULE}.flask_rebar")
def test_save_image_with_enable_object_detection_true_returns_image(
    flask_rebar_mock, image_service_mock, vision_service_mock, get_handler
):
    subject = get_handler(TARGET_MODULE)

    # setup
    label = "provided_label"
    image = Image(id=str(uuid4()), label=label)
    flask_rebar_mock.get_validated_body.return_value = {
        "file": "test.jpg",
        "label": label,
        "enable_object_detection": True,
    }
    vision_service_mock.get_image_objects.return_value = [
        DefaultMunch.fromDict({"name": "object_Name"})
    ]
    image_service_mock.create_image.return_value = image

    # when
    response = subject.save_image()

    # then
    assert response[0].id == image.id
    assert response[0].label == label
    assert response[1] == 201
