from app import app, db
from flask import json, request
from app.db_manager import get_user, get_all_users, create_user, get_all_posts, post_by_id, \
    likes_on_post, create_post, create_comment, comments_on_post, user_by_id


# Error handler if something goes wrong with database.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    d = {"code": 500}
    # Add status code because I use status codes when i run the tests.
    return json.jsonify(d), 500


# Error handler if something goes wrong if the resource don't exist.
@app.errorhandler(404)
def internal_error(error):
    d = {"code": "404"}
    # Add status code because I use status codes when i run the tests.
    return json.jsonify(d), 404


# Get the user by the given username.
@app.route('/get_user/<username>', methods=['GET'])
def user(username):
    result = []
    searched_user = get_user(username)
    if searched_user is not None:
        searched_user = searched_user.as_dict()
        result.append(searched_user)
    return json.jsonify({"user": result})


# Get the post by a given postID.
@app.route('/get_post_by_id/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    result = []
    post = post_by_id(post_id)
    if post is not None:
        result.append(post.as_dict())
    return json.jsonify({"post": result})


# Get the user by the given userID.
@app.route('/get_user_by_id/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    result = []
    searched_user = user_by_id(user_id)
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


# Get all posts.
@app.route('/all_posts', methods=["GET"])
def all_posts():
    result = []
    posts = get_all_posts()
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({"posts": result})


# Get all likes on a post by a given postID.
@app.route('/all_likes_on_post/<post_id>', methods=['GET'])
def all_likes_on_post(post_id):
    result = []
    users = likes_on_post(post_id)
    if users is not None:
        for user in users:
            result.append(user.as_dict())
    return json.jsonify({'likes': result})


# Get all comments on a post by a give postID.
@app.route('/all_comments_on_post/<post_id>', methods=['GET'])
def all_comments_on_post(post_id):
    result = []
    comments = comments_on_post(post_id)
    if comments is not None:
        for comment in comments:
            result.append(comment.as_dict())
    return json.jsonify({'comments': result})

# Get all followers that follows one user.
@app.route('/get_followers_by_id/<user_id>', methods=['GET'])
def get_followers_by_id(user_id):
    result = []
    user = user_by_id(user_id)
    users = user.followers_by_id().all()
    if users is not None:
        for user in users:
            result.append(user.as_dict())
    return json.jsonify({'users': result})


# Get all users that are followed by one user.
@app.route('/followed_by_id/<user_id>', methods=['GET'])
def followed_by_id(user_id):
    result = []
    user = user_by_id(user_id)
    users = user.followed_by_id().all()
    if users is not None:
        for user in users:
            result.append(user.as_dict())
    return json.jsonify({'users': result})


# Add user.
@app.route('/add_user', methods=['POST'])
def add_user():
    # Get details from the server.
    details = request.get_json(force=True)
    # Create one user and add it to the database if username or email don't already exists.
    result = create_user(details)
    # Control to check if everything went ok.
    if result == "username already exists":
        # Add status code because I use status codes when i run the tests.
        return json.jsonify({'result': 'username already exists'}), 400
    elif result == "email already exists":
        return json.jsonify({'result': 'email already exists'}), 400
    else:
        return json.jsonify({'result': 'ok'}), 200


# Add like to a post.
@app.route('/like_post', methods=['POST'])
def like_post():
    details = request.get_json(force=True)

    # Get the username of the user who liked the post.
    liker = details["liker"]
    # Get the postID that have been liked.
    post_id = details["postid"]

    # Get the post.
    post = post_by_id(post_id)
    # Get the user.
    user = get_user(liker)

    # Try to like the post, if the user already liked the post
    # it will return a string that says that the user want to unlike the post instead.
    like = post.like(user)

    # Check if the user want to unlike the post.
    if like != "liked":
        like = post.un_like(user)

    # Add status code because I use status codes when i run the tests.
    return json.jsonify({'result': like}), 200


# Follow one user.
@app.route('/follow_user', methods=['POST'])
def follow_user():
    details = request.get_json(force=True)

    # Get the id on the user that want to follow.
    follower_id = details["followerID"]
    # Get the id on the user that is going to be followed.
    followed_id = details["followedID"]

    # Get the users.
    follower_user = user_by_id(follower_id)
    followed_user = user_by_id(followed_id)

    # Try to follow the user, if the user already followed the user
    # it will return a string that says that the user want to unFollow the user instead.
    follow = follower_user.follow(followed_user)

    # Check if the user want to unFollow the user.
    if follow != "followed":
        follow = follower_user.un_follow(followed_user)

    # Add status code because I use status codes when i run the tests.
    return json.jsonify({'result': follow}), 200


# Create one post and add it to the database.
@app.route('/add_post', methods=['POST'])
def add_post():
    details = request.get_json(force=True)
    create_post(details)
    # Add status code because I use status codes when i run the tests.
    return json.jsonify({'result': 'ok'}), 200


# Add one comment to the database.
@app.route('/add_comment', methods=['POST'])
def add_comments():
    details = request.get_json(force=True)
    create_comment(details)
    # Add status code because I use status codes when i run the tests.
    return json.jsonify({'result': 'ok'}), 200