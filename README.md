# image-analyzer
This project uses python and Flask to develop a REST API that utilizes google cloud vision to detect objects in an image and stores the data inside sqlite3 database.

# Install Dependencies
* pip install poetry
* poetry shell
* poetry install
* setup GOOGLE_APPLICATION_CREDENTIALS in .env file.
  * To request credentials please follow the instructions from Google at https://cloud.google.com/vision/docs/quickstart-client-libraries

# DB Functions
### Creating your own sqlite db (remove image.db)
* ensure you created empty file `image.db` inside `api` folder
* flask db init
* flask db migrate -m "Create initial tables"
* flask db upgrade

### Working off sqlite db in project
* flask db migrate -m "new changes"
* flask db upgrade

# Run Application
* flask run

# Running Tests
* flask run pytest

# Running flake8
* flask run flake8