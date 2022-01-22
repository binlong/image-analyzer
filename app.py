from uuid import UUID, uuid4

from flask import Flask

app = Flask(__name__)


@app.route("/images")
def get_images():
    return "Hello, World!"


@app.route("/images/<uuid:image_id>")
def get_image(image_id: UUID):
    return uuid4()
