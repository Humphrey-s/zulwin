from models.base_model import BaseModel, Base
import models
import sqlalchemy
from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
import bcrypt


class User(BaseModel, Base):
	"""defines users"""
	if models.storage_t == 'db':
		__tablename__ = 'users'
		first_name = Column(String(128), nullable=False)
		last_name = Column(String(128), nullable=False)
		email = Column(String(128), nullable=False)
		birthday = Column(String(128), nullable=True)
		type = Column(String(128), nullable=True)
		university = Column(String(128), nullable=True)
		mobile = Column(String(128), nullable=False)
		username = Column(String(128), nullable=False)
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

	def add_item_to_cart(self, item):
		self.cart.append(item)
		self.save()

	def remove_item_from_cart(self, item_id):
		self.cart = [item for item in self.cart if item['id'] != item_id]
		self.save()

	def get_cart_items(self):
		return self.cart