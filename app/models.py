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

    posts = db.relationship('Post', backref=db.backref('author', lazy='select'))
    comments = db.relationship('Comment', backref=db.backref('author', lazy='select'))
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # Follow one user if he don't already do that.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # UnFollow one user.
    def un_follow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    # Control to check if user already follow the user.
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # Return all liked posts by given user.
    # TODO This method is not used at the moment, can be good to have to see how the querys work.
    # TODO Little confused about that sometimes.
    # TODO This method get all liked post that a user have liked.
    def liked_posts(self):
        return Post.query.join(likes, (likes.c.liked_post_id == Post.id)).filter(likes.c.user_id == self.id)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return '{}--{}--{}'.format(self.id, self.username, self.email, self.password, self.profile_picture)


# Post table.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_name = db.Column(db.String, nullable=False)
    post_information = db.Column(db.String, nullable=False)
    recipe_information = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime)

    # Relation between Comment table and Post table.
    # The owner of all comments is a post. Backref points back to the owner.
    comments = db.relationship('Comment', backref=db.backref('post', lazy='select'))
    # Relation between Likes table and Post table.
    # The owner of all likes is a post. Backref points back to the owner.
    likes = db.relationship('User',
                            secondary=likes,
                            backref=db.backref('post', lazy='dynamic'),
                            lazy='dynamic')

    # This method will check if the user wanna do an unlike or like a post.
    def like(self, user):
        if not self.is_liking(user):
            self.likes.append(user)
            return self
        else:
            return "un_like"

    # This method will be called if the user wanna unlike a post.
    def un_like(self, user):
        self.likes.remove(user)
        return self

    # This method will check if the user is liking the given post or not.
    def is_liking(self, user):
        return self.likes.filter(likes.c.user_id == user.id).count() > 0

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return '{}--{}--{}--{}'.format(self.id, self.recipe_name, self.recipe_information, self.timestamp)


# Comment table.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_text = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.post_id

