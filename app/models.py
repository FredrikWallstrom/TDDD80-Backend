from app import db

# Followers table.
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))
# Likes table.
likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('liked_post_id', db.Integer, db.ForeignKey('post.id')))


# User table.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)

    # Relation between Post table and User table.
    posts = db.relationship('Post', backref=db.backref('author', lazy='select'))
    # Relation between Comment table and User table.
    comments = db.relationship('Comment', backref=db.backref('author', lazy='select'))
    # relation between followers table and User table.
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # Follow one user if he not already follow the user.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.add(self)
            db.session.commit()
            return "followed"

    # UnFollow one user.
    def un_follow(self, user):
        self.followed.remove(user)
        db.session.add(self)
        db.session.commit()
        return "un_followed"

    # Check if user already follow the user.
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # Get all followers that follow a given user.
    def followers_by_id(self):
        return User.query.join(followers, (followers.c.follower_id == User.id))\
            .filter(followers.c.followed_id == self.id)

    # Get all users that are followed by a given user.
    def followed_by_id(self):
        return User.query.join(followers, (followers.c.followed_id == User.id))\
            .filter(followers.c.follower_id == self.id)

    # Represent object as a dict.
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # Init the user.
    def __init__(self, username, email, password, profile_picture):
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture


# Post table.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_name = db.Column(db.String, nullable=False)
    post_information = db.Column(db.String, nullable=False)
    recipe_information = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    # Relation between Comment table and Post table.
    comments = db.relationship('Comment', backref=db.backref('post', lazy='select'))
    # Relation between Likes table and Post table.
    likes = db.relationship('User',
                            secondary=likes,
                            backref=db.backref('post', lazy='dynamic'),
                            lazy='dynamic')

    # Like one post if he not already liking the post.
    def like(self, user):
        if not self.is_liking(user):
            self.likes.append(user)
            db.session.add(self)
            db.session.commit()
            return "liked"

    # UnLike one post.
    def un_like(self, user):
        self.likes.remove(user)
        db.session.add(self)
        db.session.commit()
        return "un_liked"

    # This method will check if the user is liking the given post or not.
    def is_liking(self, user):
        return self.likes.filter(likes.c.user_id == user.id).count() > 0

    # Represent object as a dict.
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # Init the post.
    def __init__(self, user_id, recipe_name, post_information, recipe_information, location, timestamp):
        self.user_id = user_id
        self.recipe_name = recipe_name
        self.post_information = post_information
        self.recipe_information = recipe_information
        self.location = location
        self.timestamp = timestamp


# Comment table.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_text = db.Column(db.String, nullable=False)

    # Represent object as a dict.
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # Init the Comment.
    def __init__(self, post_id, user_id, comment_text):
        self.post_id = post_id
        self.user_id = user_id
        self.comment_text = comment_text

