from google.cloud import vision


client = vision.ImageAnnotatorClient()


def get_image(file_path):
    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    return vision.Image(content=content)


def get_image_labels(file_path):
    image = get_image(file_path)
    response = client.label_detection(image=image)
    return response.label_annotations


def get_image_objects(file_path):
    image = get_image(file_path)
    response = client.object_localization(image=image)
    return response.localized_object_annotations