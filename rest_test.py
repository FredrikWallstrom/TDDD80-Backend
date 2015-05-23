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

    # Test, error_handler(404).
    # Try to add a new user with wrong url.
    def test_error_handler_404(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        # Wrong url.
        user = self.client.post(base_url + '/add_useeer', data=data)
        # Failed creation, wrong url.
        self.assertTrue(user.status_code == 404)

    # Test, get user from database by a given username.
    def test_get_user(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get user.
        user = self.client.get(base_url + '/get_user/' + 'foo')
        user = user.json
        # Check if the len of the list is 1 and the key is "user".
        for key, values in user.items():
            if len(values) == 1 and key == "user":
                assert True
            else:
                assert False

        # Get one user that don't exists.
        user = self.client.get(base_url + '/get_user/' + 'boo')
        user = user.json
        # Check if the len of the list is 0 and the key is "user".
        for key, values in user.items():
            if len(values) == 0 and key == "user":
                assert True
            else:
                assert False

    # Test, get post from database by given post_id.
    def test_get_post_by_id(self):
        base_url = 'http://127.0.0.1:3548'

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Get post.
        post = self.client.get(base_url + '/get_post_by_id/' + "1")
        post = post.json
        # Check if the len of the list is 1 and the key is "post".
        for key, values in post.items():
            if len(values) == 1and key == "post":
                assert True
            else:
                assert False

        # Get one post that don't exists.
        post = self.client.get(base_url + '/get_post_by_id/' + '2')
        post = post.json
        # Check if the len of the list is 0 and the key is "post".
        for key, values in post.items():
            if len(values) == 0 and key == "post":
                assert True
            else:
                assert False

    # Test, get user from database by given user_id.
    def test_get_user_by_id(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get user
        user = self.client.get(base_url + '/get_user_by_id/' + '1')
        user = user.json
        # Check if the len of the list is 1 and the key is "user".
        for key, values in user.items():
            if len(values) == 1 and key == "user":
                assert True
            else:
                assert False

        # Get one user that don't exists.
        user = self.client.get(base_url + '/get_user_by_id/' + '2')
        user = user.json
        # Check if the len of the list is 0 and the key is "user".
        for key, values in user.items():
            if len(values) == 0 and key == "user":
                assert True
            else:
                assert False

    # Test, all users.
    def test_all_users(self):
        base_url = 'http://127.0.0.1:3548'

        # Get all users without users should give empty list.
        users = self.client.get(base_url + '/all_users')
        users = users.json
        # Check if the len of the list is 0 and the key is "users".
        for key, values in users.items() :
            if len(values) == 0 and key == "users":
                assert True
            else:
                assert False

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get users
        users = self.client.get(base_url + '/all_users')
        users = users.json
        # Check if the len of the list is 1 and the key is "users".
        for key, values in users.items():
            if len(values) == 1 and key == "users":
                assert True
            else:
                assert False

        # Create a user.
        username = 'boo'
        password = 'bar'
        email = 'boo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get users.
        users = self.client.get(base_url + '/all_users')
        users = users.json
        # Check if the len of the list is 2 and the key is "users".
        for key, values in users.items():
            if len(values) == 2 and key == "users":
                assert True
            else:
                assert False

    # Test, all posts.
    def test_all_posts(self):
        base_url = 'http://127.0.0.1:3548'

        # Get all posts without any post added, should give empty list.
        posts = self.client.get(base_url + '/all_posts')
        posts = posts.json
        # Check if the len of the list is 0 and the key is "posts".
        for key, values in posts.items() :
            if len(values) == 0 and key == "posts":
                assert True
            else:
                assert False

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Get all posts
        posts = self.client.get(base_url + '/all_posts')
        posts = posts.json

        # Check if the len of the list is 1 and the key is "posts".
        for key, values in posts.items():
            if len(values) == 1 and key == "posts":
                assert True
            else:
                assert False

        # Create post.
        user_id = "1"
        recipe_name = "Sandwich"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Get all posts
        posts = self.client.get(base_url + '/all_posts')
        posts = posts.json
        # Check if the len of the list is 2 and the key is "posts".
        for key, values in posts.items():
            if len(values) == 2 and key == "posts":
                assert True
            else:
                assert False

    # Test, all likes on post
    def test_all_likes_on_post(self):
        base_url = 'http://127.0.0.1:3548'

        # Get all likes on one post, this post don't exists so it should give no likes.
        users = self.client.get(base_url + '/all_likes_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "likes".
        for key, values in users.items():
            if len(values) == 0 and key == "likes":
                assert True
            else:
                assert False

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Get all likes on one post, this post don't got any likes.
        users = self.client.get(base_url + '/all_likes_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "likes".
        for key, values in users.items():
            if len(values) == 0 and key == "likes":
                assert True
            else:
                assert False

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)
        # The user now like the post.
        data = json.dumps({'liker': username, 'postid': 1})
        self.client.post(base_url + '/like_post', data=data)

        # Get all likes on one post, the post now got one like.
        users = self.client.get(base_url + '/all_likes_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 1 and the key is "likes".
        for key, values in users.items():
            if len(values) == 1 and key == "likes":
                assert True
            else:
                assert False

    # Test, all_comments on post
    def test_all_comments_on_post(self):
        base_url = 'http://127.0.0.1:3548'

        # Get all comments on one post, this post don't exists so it should give no comments.
        users = self.client.get(base_url + '/all_comments_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "comments".
        for key, values in users.items():
            if len(values) == 0 and key == "comments":
                assert True
            else:
                assert False

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Get all comments on the post, this post don't got any comments so the it should give no comments.
        users = self.client.get(base_url + '/all_comments_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "comments".
        for key, values in users.items():
            if len(values) == 0 and key == "comments":
                assert True
            else:
                assert False

        # Create Comment on the post.
        post_id = "1"
        user_id = "1"
        comment_text = "FooBar"
        data = json.dumps({"post_id": post_id, "user_id": user_id, "comment_text": comment_text})
        self.client.post(base_url + "/add_comment", data=data)

        # Get all comments on the post, this post got one comment now.
        users = self.client.get(base_url + '/all_comments_on_post/' + '1')
        users = users.json
        # Check if the len of the list is 1 and the key is "comments".
        for key, values in users.items():
            if len(values) == 1 and key == "comments":
                assert True
            else:
                assert False

    # Test, get followers by id
    def test_get_followers_by_id(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get all followers on one user, this user don't got any followers.
        users = self.client.get(base_url + '/get_followers_by_id/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "users".
        for key, values in users.items():
            if len(values) == 0 and key == "users":
                assert True
            else:
                assert False

        # Create a user.
        username = 'fooo'
        password = 'bar'
        email = 'fooo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Now we got two users, now we let user two follow user one.
        data = json.dumps({"followerID": "2", "followedID": "1"})
        self.client.post(base_url + "/follow_user", data=data)

        # Get all followers on the first user, this user got one follower.
        users = self.client.get(base_url + '/get_followers_by_id/' + '1')
        users = users.json
        # Check if the len of the list is 1 and the key is "users".
        for key, values in users.items():
            if len(values) == 1 and key == "users":
                assert True
            else:
                assert False

        # Create a user.
        username = 'booo'
        password = 'bar'
        email = 'booo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Now we let user three follow user one.
        data = json.dumps({"followerID": "3", "followedID": "1"})
        self.client.post(base_url + "/follow_user", data=data)

        # Get all followers on the first user, this user got two follower.
        users = self.client.get(base_url + '/get_followers_by_id/' + '1')
        users = users.json
        # Check if the len of the list is 2 and the key is "users".
        for key, values in users.items():
            if len(values) == 2 and key == "users":
                assert True
            else:
                assert False

        # Now we let user one follow user two.
        data = json.dumps({"followerID": "1", "followedID": "2"})
        self.client.post(base_url + "/follow_user", data=data)

        # Get all followers on the second user, this user got one follower.
        users = self.client.get(base_url + '/get_followers_by_id/' + '2')
        users = users.json
        # Check if the len of the list is 1 and the key is "users".
        for key, values in users.items():
            if len(values) == 1 and key == "users":
                assert True
            else:
                assert False

    # Test, followed by id
    def test_followed_by_id(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Create a user.
        username = 'fooo'
        password = 'bar'
        email = 'fooo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Get all followed users by a given users id. The first user don't got any followed users.
        users = self.client.get(base_url + '/followed_by_id/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "users".
        for key, values in users.items():
            if len(values) == 0 and key == "users":
                assert True
            else:
                assert False

        # Now we let user two follow user one.
        data = json.dumps({"followerID": "2", "followedID": "1"})
        self.client.post(base_url + "/follow_user", data=data)

        # Get all followed users by a given users id. The first user don't got any followed users.
        users = self.client.get(base_url + '/followed_by_id/' + '1')
        users = users.json
        # Check if the len of the list is 0 and the key is "users".
        for key, values in users.items():
            if len(values) == 0 and key == "users":
                assert True
            else:
                assert False

        # Get all followed users by a given users id. The second user is following one user.
        # User one is followed by user 2.
        # So return one followed user
        users = self.client.get(base_url + '/followed_by_id/' + '2')
        users = users.json
        # Check if the len of the list is 1 and the key is "users".
        for key, values in users.items():
            if len(values) == 1 and key == "users":
                assert True
            else:
                assert False

    # Test, add user
    def test_add_user(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        user = self.client.post(base_url + '/add_user', data=data)
        # Successful creation
        self.assertTrue(user.status_code == 200)

        # Create a user with same name.
        username = 'foo'
        password = 'bar'
        email = 'diff'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        user = self.client.post(base_url + '/add_user', data=data)
        # Failed creation, username already exists.
        self.assertTrue(user.status_code == 400)

        # Create a user with same email.
        username = 'diff'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        user = self.client.post(base_url + '/add_user', data=data)
        # Failed creation, email already exists.
        self.assertTrue(user.status_code == 400)

    # Test, like post.
    def test_like_post(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # User like the post.
        postid = "1"
        liker = username
        data = json.dumps({'postid': postid, 'liker': liker})
        like = self.client.post(base_url + '/like_post', data=data)

        like = like.json
        # Check if the result of the post returned "liked" and the key should be "result"
        for key, values in like.items():
            if values == "liked" and key == "result":
                assert True
            else:
                assert False

        # User like the post again (Unlike).
        postid = "1"
        liker = username
        data = json.dumps({'postid': postid, 'liker': liker})
        like = self.client.post(base_url + '/like_post', data=data)

        like = like.json
        # Check if the result of the post returned "un_liked" and the key should be "result"
        for key, values in like.items():
            if values == "un_liked" and key == "result":
                assert True
            else:
                assert False

    # Test, follow user
    def test_follow_user(self):
        base_url = 'http://127.0.0.1:3548'

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Create a second user.
        username = 'boo'
        password = 'bar'
        email = 'boo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Now we got two users, now we let user one follow user two.
        data = json.dumps({"followerID": "1", "followedID": "2"})
        follow = self.client.post(base_url + "/follow_user", data=data)
        self.assertTrue(follow.status_code == 200)

        follow = follow.json
        # Check if the result of the follow returned "followed" and the key should be "result"
        for key, values in follow.items():
            if values == "followed" and key == "result":
                assert True
            else:
                assert False

        # User one follow user two again (UnFollow).
        data = json.dumps({"followerID": "1", "followedID": "2"})
        follow = self.client.post(base_url + "/follow_user", data=data)
        self.assertTrue(follow.status_code == 200)

        follow = follow.json
        # Check if the result of the follow returned "un_followed" and the key should be "result"
        for key, values in follow.items():
            if values == "un_followed" and key == "result":
                assert True
            else:
                assert False

    # Test, add post.
    def test_add_post(self):
        base_url = 'http://127.0.0.1:3548'

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        location = "no location added"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information, "location": location})
        post = self.client.post(base_url + "/add_post", data=data)
        # Successful creation.
        self.assertTrue(post.status_code == 200)

    # Test, add comment.
    def test_add_comment(self):
        base_url = 'http://127.0.0.1:3548'

        # Create post.
        user_id = "1"
        recipe_name = "Chicken"
        post_information = "foo"
        recipe_information = "bar"
        data = json.dumps({"user_id": user_id, "recipe_name": recipe_name, "post_information": post_information,
                           "recipe_information": recipe_information})
        self.client.post(base_url + "/add_post", data=data)

        # Create a user.
        username = 'foo'
        password = 'bar'
        email = 'foo@bar'
        data = json.dumps({'email': email, 'username': username, 'password': password})
        self.client.post(base_url + '/add_user', data=data)

        # Create Comment on the post.
        post_id = "1"
        user_id = "1"
        comment_text = "FooBar"
        data = json.dumps({"post_id": post_id, "user_id": user_id, "comment_text": comment_text})
        comment = self.client.post(base_url + "/add_comment", data=data)
        self.assertTrue(comment.status_code == 200)

        comment = comment.json
        # Check if the result of the comment returned "ok" and the key should be "result"
        for key, values in comment.items():
            if values == "ok" and key == "result":
                assert True
            else:
                assert False


if __name__ == '__main__':
    unittest.main()
