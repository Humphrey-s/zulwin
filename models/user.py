from models.base_model import BaseModel
import bcrypt


class User(BaseModel):
	"""defines users"""

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