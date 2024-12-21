from models.base_model import BaseModel, Base
import models
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

def one_year_from_now():
	return (datetime.now() + timedelta(days=365)).strftime('%d-%m-%Y')

class Item(BaseModel, Base):
	"""Item being sold"""

	if models.storage_t == "db":
		__tablename__ = 'items'
		name = Column(String(128), nullable=True)
		category = Column(String(128), nullable=True)
		description = Column(String(128), nullable=True)
		expiry_date = Column(Date, default=one_year_from_now())
		seller_id = Column(String(60), nullable=False)
		featured = Column(String(128), nullable=True)
		paid = Column(String(128), nullable=True)
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