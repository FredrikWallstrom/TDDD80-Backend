__author__ = 'Fredrik'

from app import models, db

posts = models.Post.query.all()
for e in posts:
    db.session.delete(e)
db.session.commit()
