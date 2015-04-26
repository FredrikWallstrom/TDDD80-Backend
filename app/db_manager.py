from .models import *


# Get the user from the database from a given username.
def get_user(username):
    return User.query.filter_by(username=username).first()


# Get all users from the database
def get_all_users():
    return User.query.all()


# Get the details from server and create a user.
def create_user(user_details):
    username = user_details.get('username')
    if User.query.filter_by(username=username).first():
        return "username already exists"

    email = user_details.get('email')
    if User.query.filter_by(email=email).first():
        return "email already exists"

    password = user_details.get('password')
    profile_picture = "default"
    return User(username, email, password, profile_picture)


# Get all posts from the database
def get_all_posts():
    return Post.query.all()


# Get the user from the database from a given ID.
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()


# Get all user that like one post by given postID.
def get_post_liker(post_id):
    return User.query.filter(User.post.any(id=post_id)).all()


# Get the post by a given postID.
def get_post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first()



