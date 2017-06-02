import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'postgresql://flask:flask@localhost/flask'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

apiusers = {
    "test": "test"
}

REPO_URL = 'https://gitlab.test.ru'

REPO_PROJECT_NAMESPACE = {
    'proj': 'namespace/project'
}

APPS_PER_PAGE = 35

DEFAULT_ENVIRONMENT = 'production'
