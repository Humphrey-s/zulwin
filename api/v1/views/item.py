#!/usr/bin/python3
from flask import jsonify, request, current_app, url_for, abort
from api.v1.views import app_views
from models import storage
from uuid import uuid4
import jwt
import requests as r
from datetime import datetime
from models.item import Item
from models.user import User



@app_views.route("/create_item", methods=["POST"], strict_slashes=False)
def create_item():
	"""creates item"""	
	date = datetime.now().date()
	time = datetime.now().time().strftime("%H:%M:%S")
	image_path = f"{request.form.get('seller_id')}-{date}-{time}-{request.form.get('filename')}"

	dct = {
	"seller_id": request.form.get("seller_id"),
	"name": request.form.get("name"),
	"description": request.form.get("description"),
	"price": request.form.get("price"),
	"location": request.form.get("location"),
	"image": image_path.replace(":", '-'),
	"expiry_date": request.form.get("expiry_date")
	}

	instance = Item(**dct)
	instance.save()

	return instance.to_dict()




