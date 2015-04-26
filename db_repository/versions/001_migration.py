from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('user_id', Integer),
    Column('comment_text', String, nullable=False),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('followed_id', Integer),
)

likes = Table('likes', post_meta,
    Column('user_id', Integer),
    Column('liked_post_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('recipe_name', String, nullable=False),
    Column('recipe_information', String, nullable=False),
    Column('timestamp', DateTime),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String, nullable=False),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('profile_picture', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].create()
    post_meta.tables['followers'].create()
    post_meta.tables['likes'].create()
    post_meta.tables['post'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].drop()
    post_meta.tables['followers'].drop()
    post_meta.tables['likes'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['user'].drop()
