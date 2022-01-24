import validators

from google.cloud import vision


def get_client():
    return vision.ImageAnnotatorClient()


def get_image(image_location):
    if validators.url(image_location):
        image = get_image_with_uri(image_location)
    else:
        image = get_image_with_file(image_location)

    return image


def get_image_with_file(file_path):
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    return vision.Image(content=content)


def get_image_with_uri(uri: str):
    image = vision.Image()
    image.source.image_uri = uri

    return image


def get_image_labels(image_location):
    image = get_image(image_location)
    response = get_client().label_detection(image=image)
    return response.label_annotations


def get_image_objects(image_location):
    image = get_image(image_location)
    response = get_client().object_localization(image=image)
    return response.localized_object_annotations
