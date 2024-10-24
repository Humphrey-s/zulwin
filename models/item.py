from models.base_model import BaseModel, Base
import models
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Item(BaseModel, Base):
	"""Item being sold"""

	if models.storage_t == "db":
		__tablename__ = 'items'
		name = Column(String(128), nullable=False)
		category = Column(String(128), nullable=False)
		seller_id = Column(String(60), ForeignKey('users.id'), nullable=False)
		buyer_ids = Column(String(128), nullable=False)
		paid = Column(String(128), nullable=False)
	else:
		name = ""
		category = ""
		seller_id = ""
		price = ""
		buyer_ids = []
		paid = ""

	def __init__(self, *args, **kwargs):
		"""Initializes"""
		if kwargs is None:
			super().__init__(self, *args, **kwargs)
		else:
			if "id" not in kwargs.keys():
				super().__init__(self, *args, **kwargs)
				for key, value in kwargs.items():
					setattr(self, key, value)
			else:
				for key, value in kwargs.items():
					setattr(self, key, value)