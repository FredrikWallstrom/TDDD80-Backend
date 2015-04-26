__author__ = 'Fredrik'

from app import db
from app.models import Post
from datetime import datetime

p1 = Post(recipe_name="Test", post_information="Test mot server", recipe_information="Stek Hårt",
          timestamp=datetime.utcnow(), user_id=2)

db.session.add(p1)
db.session.commit()