from app import models, db

users = models.User.query.all()
for e in users:
    db.session.delete(e)
db.session.commit()



