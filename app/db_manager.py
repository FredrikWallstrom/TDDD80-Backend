from datetime import datetime
from .models import User, Post, Comment
from app import db


# Get the user from the database from a given username.
def get_user(username):
    return User.query.filter_by(username=username).first()


# Get all users from the database
def get_all_users():
    return User.query.all()


# Get the details from server and create a user.
def create_user(user_details):
    username = user_details.get('username')
    # Control if the username already exists in the database.
    if User.query.filter_by(username=username).first():
        return "username already exists"

    email = user_details.get('email')
    # Control if the email already exists in the database.
    if User.query.filter_by(email=email).first():
        return "email already exists"

    password = user_details.get('password')
    profile_picture = "default"

    # Create user and add it to the database.
    user = User(username, email, password, profile_picture)
    db.session.add(user)
    return db.session.commit()


# Get all posts from the database
def get_all_posts():
    return Post.query.order_by("timestamp desc").all()


# Get the user from the database from a given userID.
def user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


# Get all user that like one post by given postID.
def likes_on_post(post_id):
    return User.query.filter(User.post.any(id=post_id)).all()


# Get the post by a given postID.
def post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first()


# Create and return a post.
def create_post(post_details):
    # Get posts details.
    user_id = post_details.get('user_id')
    recipe_name = post_details.get('recipe_name')
    post_information = post_details.get('post_information')
    recipe_information = post_details.get('recipe_information')
    location = post_details.get('location')
    timestamp = datetime.utcnow()
    # Create post.
    post = Post(user_id, recipe_name, post_information, recipe_information, location, timestamp)
    # Add it to database.
    db.session.add(post)
    return db.session.commit()


# Create and return a comment.
def create_comment(comment_details):
    # Get comment details.
    post_id = comment_details.get('post_id')
    user_id = comment_details.get('user_id')
    comment_text = comment_details.get('comment_text')
    # Create comment.
    comment = Comment(post_id, user_id, comment_text)
    # Add it to the database.
    db.session.add(comment)
    return db.session.commit()


# Get all comments on one post by a given postID.
def comments_on_post(post_id):
    return Comment.query.filter_by(post_id=post_id).all()











