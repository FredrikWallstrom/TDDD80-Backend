from app import app
from flask import json, request
from app.db_manager import *

# Error handler if something goes wrong with database.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    d = {"code": 500}
    return json.jsonify(d)


# Error handler if something goes wrong if the resource don't exist.
@app.errorhandler(404)
def internal_error(error):
    d = {"code": "404"}
    return json.jsonify(d)


# Get the user by the given username.
@app.route('/get_user/<username>', methods=['GET'])
def user(username):
    result = []
    searched_user = get_user(username)
    if searched_user is not None:
        searched_user = searched_user.as_dict()
        result.append(searched_user)
    return json.jsonify({"user": result})


# Get the user by the given ID.
@app.route('/get_user_by_id/<identity>', methods=['GET'])
def user_by_id(identity):
    result = []
    searched_user = get_user_by_id(identity)
    if searched_user is not None:
        searched_user = searched_user.as_dict()
        result.append(searched_user)
    return json.jsonify({"user": result})


# Get all register users.
@app.route('/all_users', methods=['GET'])
def all_users():
    result = []
    users = get_all_users()
    if users is not None:
        for user in users:
            result.append(user.as_dict())
    return json.jsonify({"users": result})


# Add user.
@app.route('/add_user', methods=['POST'])
def add_user():
    user_details = request.get_json(force=True)
    result = create_user(user_details)
    if result == "username already exists":
        # Add error code because I use error codes when i run the tests.
        return json.jsonify({'result': 'username already exists'}), 400
    elif result == "email already exists":
        # Add error code because I use error codes when i run the tests.
        return json.jsonify({'result': 'email already exists'}), 400
    else:
        db.session.add(result)
        db.session.commit()
        return json.jsonify({'result': 'ok'})

# Get all posts.
@app.route('/all_posts', methods=["GET"])
def all_posts():
    result = []
    posts = get_all_posts()
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({"posts": result})

# Add like to a post.
@app.route('/like_post', methods=['POST'])
def like_post():
    details = request.get_json(force=True)

    # Get the postID that have been liked and the username of the user who liked the post.
    liker = details["liker"]
    post_id = details["postid"]

    # Get the whole post and user.
    post = get_post_by_id(post_id)
    user = get_user(liker)

    # This will return like or unlike depend on if the user already liked the post or not.
    like = post.like(user)

    # Check if the user want unlike the post.
    if like != "un_like":
        db.session.add(like)
        db.session.commit()
        return json.jsonify({'result': 'liked'})
    # The user want to like the post.
    else:
        un_like = post.un_like(user)
        db.session.add(un_like)
        db.session.commit()
        return json.jsonify({'result': 'un_liked'})

# Get all likes on a post by a given postID.
@app.route('/all_likes_on_post/<post_id>', methods=['GET'])
def all_likes(post_id):
    result = []
    users = get_post_liker(post_id)
    if users is not None:
        for user in users:
            result.append(user.as_dict())
    return json.jsonify({'likes': result})

# Get all posts that one user likes.
# TODO This method is never used at them moment, maybe i will use it later.
# TODO It will get all posts that one person has liked.
@app.route('/all_liked_posts_by/<username>', methods=['GET'])
def all_liked_posts_by_user(username):
    result = []
    user = get_user(username)
    posts = user.liked_posts().all()
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({'post': result})



