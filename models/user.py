from models.base_model import BaseModel, Base
import models
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import bcrypt


class User(BaseModel, Base):
	"""defines users"""
	if models.storage_t == 'db':
		__tablename__ = 'users'
		email = Column(String(128), nullable=False)
		password = Column(String(128), nullable=False)
		username = Column(String(128), nullable=True)
	else:
		carts = []

	def __init__(self, *args, **kwargs):
		"""initializes user instance"""
		if kwargs is None:
			super().__init__(self, *args, **kwargs)
		else:
			if "id" not in kwargs.keys():
				super().__init__(self, *args, **kwargs)
				for key, value in kwargs.items():
					if key == "password":
						salt = bcrypt.gensalt()
						psswd = kwargs["password"]
						hashed = bcrypt.hashpw(psswd.encode("utf-8"), salt)
						self.password = hashed.decode("utf-8")
					else:
						setattr(self, key, value)
			else:
				for key, value in kwargs.items():
					setattr(self, key, value)