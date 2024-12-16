#!/usr/bin/python3
from flask import jsonify, request, current_app, url_for, abort
from api.v1.views import app_views
from models import storage
from uuid import uuid4
import jwt
import requests as r
from datetime import datetime, timedelta
from models.item import Item
from models.user import User




@app_views.route("/items", strict_slashes=False)
def get_items():
	"""return all users"""
	all_items = storage.all(Item).values()

	all_items = [item.to_dict() for item in all_items]
	return jsonify(all_items)


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

@app_views.route("/items/<item_id>", methods=["DELETE"], strict_slashes=False)
def delete_item(item_id):
	"""delete Item"""
	all_items = storage.all(Item).values()

	for i in all_items:
		if i.id == item_id:
			storage.delete(i)
			storage.reload()
			return jsonify({"success": True})
	
	return jsonify({"success": False})

@app_views.route("/items/<item_id>", methods=["UPDATE"])
def update_item(item_id):
	"""update item"""
	all_items = storage.all(Item).values()

	for i in all_items:
		if i.id == item_id:
			i.update({
				"key": "featured",
				"value": {
				"featured": True,
				"date": datetime.today().strftime('%Y-%m-%d')
				}})

			return jsonify({"sucess": True, "item": i.to_dict()})
	else:
		return jsonify({"success": False, "message": "update failed"})



@app_views.route("/items/featured", methods=["GET"], strict_slashes=False)
def get_featured():
	"""Get featured"""
	all_items = storage.all(Item).values()
	all_ft = []

	for i in all_items:
		a = i.to_dict()
		if "featured" in a.keys():
			if a["featured"]["featured"] == True:
				all_ft.append(i.to_dict())
	else:
		return all_ft


@app_views.route("/items/new", strict_slashes=False)
def get_new():
	"""Gets New Items"""
	storage.reload()
	all_items = storage.all(Item).values()
	all_items = [item.to_dict() for item in all_items]

	today = datetime.now()
	new_items = []

	for i in all_items:
		date_item = datetime.strptime(i["created_at"], "%Y-%m-%d %H:%M:%S")

		if today - date_item < timedelta(days=2):
			new_items.append(i)
	else:
		return jsonify(new_items)



@app_views.route("/items/expired", strict_slashes=False)
def get_expired():
	"""Get Expired Items"""
	storage.reload()
	all_items = storage.all(Item).values()

	all_items = [item.to_dict() for item in all_items]

	today = datetime.now()
	ex_items = []

	for i in all_items:
		date_item = datetime.strptime(i["expiry_date"], "%Y-%m-%d")

		if today >= date_item:
			ex_items.append(i)
	else:
		return jsonify(ex_items)


@app_views.route("/items/stats", strict_slashes=False)
def get_stats():
	"""Get item stats"""
	storage.reload()
	all_items = storage.all(Item).values()
	all_items = [item.to_dict() for item in all_items]

	total = len(all_items)
	today = datetime.now()
	new_items = []
	ex_items = []
	featured = 0
	deleted = 0
	carted = 0

	for i in all_items:
		if "expiry_date" in i.keys():
			date_item1 = datetime.strptime(i["expiry_date"], "%Y-%m-%d")
			if today >= date_item1:
				ex_items.append(i)

		date_item2 = datetime.strptime(i["created_at"], "%Y-%m-%d %H:%M:%S")

		if today - date_item2 < timedelta(days=2):
			new_items.append(i)

		if "featured" in i.keys():
			featured += 1 
		
		if "carted" in i.keys():
			carted += 1
	else:
		expired = len(ex_items)
		new = len(new_items)
	
	stats = {
	"total": total,
	"expired": expired,
	"new": new, 
	"featured": featured,
	"deleted": deleted,
	"carted": carted
	}
	
	return jsonify(stats)
