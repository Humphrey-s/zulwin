from models.base_model import BaseModel


class Item(BaseModel):
	"""Item being sold"""
	name = ""
	id = ""
	category = ""
	seller_id = ""
	buyer_ids = [];
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