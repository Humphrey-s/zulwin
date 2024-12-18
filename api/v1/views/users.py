#!/usr/bin/python3
from flask import jsonify, request, current_app, url_for, abort
from api.v1.views import app_views
from models import storage
from uuid import uuid4
import jwt
from models.user import User
from models.item import Item




@app_views.route("/users", methods=["GET"])
def get_users():
	"""get users"""
	all_users = storage.all(User).values()
	
	return jsonify([u.to_dict() for u in all_users])


@app_views.route("/users/<user_id>", methods=["GET"])
def get_s_user(user_id):
	"""get specific user"""
	all_users = storage.all(User).values()

	for u in all_users:
		if u.id == user_id:
			return jsonify(u.to_dict())
	else:
		abort(404)



@app_views.route("/get_user_profile")
def get_user_profile():
    """get user profile"""
    token = request.cookies.get('token')

    if token is None:
        return jsonify({"status": False})
    
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"current_user": data})
    except jwt.ExpiredSignatureError:
        return jsonify({"status": False, "message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": False, "message": "Invalid token"}), 401



@app_views.route("/user", methods=["POST"])
def create_user():
	"""create user"""
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	email = request.form.get("email")
	type = request.form.get("type")
	mobile = request.form.get("mobile_no")
	password = request.form.get("password")
	birthday = request.form.get("birthday")

	dct = {
	"username": first_name + " " + last_name,
	"first_name": first_name,
	"last_name": last_name,
	"email": email,
	"mobile": mobile,
	"type": type,
	"password": password,
	"birthday": birthday,
	}

	instance = User(**dct)
	instance.save()
	storage.reload()
	r = instance.to_dict()
	return jsonify(r)


@app_views.route("/check_mail", methods=["POST", "GET"])
def check_mail():
	"""check if a user/email exists"""
	all_users = storage.all(User).values()
	email = request.form.get("email")

	print(email)
	for u in all_users:
		if u.email == email:
			return jsonify({"status": True, "email": email, "id": u.id})
	else:
		return jsonify({"status": False, "email": email})


@app_views.route("/user/items/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_item(user_id):
	"""get user items"""
	all_items = storage.all(Item).values()
	array = []

	for i in all_items:
		if i.seller_id == user_id:
			array.append(i.to_dict())
	else:
		return jsonify(array)


@app_views.route("/send_mail/<receiver_email>")
def send_mail(receiver_email):
	"""sends_mail"""
	from email.mime.text import MIMEText 
	from email.mime.image import MIMEImage 
	from email.mime.application import MIMEApplication 
	from email.mime.multipart import MIMEMultipart 
	import smtplib, ssl 
	import os
	from uuid import uuid4


	sender_email = "zulwinteam@gmail.com"
	password = "znqo ztne ckcc aubv"

	message = MIMEMultipart("alternative")
	message["Subject"] = "[Zulwin ] Verify your email address"
	message["From"] = sender_email
	message["To"] = receiver_email

	code = str(uuid4())[:4]

	text = f"""\
	<html>
	<body>
		<h1>Welcome to Zulwin </h1>
		<p>Your OTP verification code for login: {code}<p></br>
		<p>If this email is not intended for you kindly ignore</p>
	</body>
	</html> 
	"""
	content = MIMEText(text, "html")
	message.attach(content)

	context = ssl.create_default_context()

	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.as_string())

	return jsonify({"code": code})
