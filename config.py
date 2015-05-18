import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Point at the database in the openshift server.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'database.db')

# For local and test run
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


