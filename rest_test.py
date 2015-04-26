import os
import unittest
from app import app, db
from flask import json
from config import basedir
from flask.ext.testing import TestCase


class RestApiTests(TestCase):

    def create_app(self):
        """Required method. Always implement this so that app is returned with context."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False  # This must be disabled for post to succeed during tests
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test, add a new user.
    def test_add_user(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        first_user = self.client.post(base_url + '/add_user', data=data)
        # Successful creation
        self.assertTrue(first_user.status_code == 200)

        # Create a user with same name
        username = 'foo'
        password = 'bar'
        email = 'diff'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        second_user = self.client.post(base_url + '/add_user', data=data)
        # Failed creation
        self.assertTrue(second_user.status_code == 400)

        # Create a user with same email
        username = 'diff'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        second_user = self.client.post(base_url + '/add_user', data=data)
        # Failed creation
        self.assertTrue(second_user.status_code == 400)


if __name__ == '__main__':
    unittest.main()
