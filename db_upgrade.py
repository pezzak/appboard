#!sandbox/bin/python
from migrate.versioning import api
from migrate.exceptions import DatabaseNotControlledError
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from db_create import db_create

try:
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
except DatabaseNotControlledError:
    db_create()
