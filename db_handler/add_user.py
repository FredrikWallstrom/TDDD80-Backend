__author__ = 'Fredrik'

from app import db
from app.models import User

p1 = User(email="test@gmail.com", username="Fredde", password="hejsan", profile_picture="heeej")

db.session.add(p1)
db.session.commit()
