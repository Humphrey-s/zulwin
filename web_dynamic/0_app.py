#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from flask import jsonify, session, flash, make_response, request
from models.user import User
from models.item import Item
from models import storage
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
from uuid import uuid4
import bcrypt


app = Flask(__name__)

CORS(app)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


socketio = SocketIO(app)


@app.errorhandler(404)
def not_found(error):
	"""handles 404 errors"""
	return make_response(render_template("/404.html"), 404)

@app.route("/home")
def home():
	"""home page"""
	if session["user_id"]:
		user_id = session["user_id"]

		all_user = storage.all(User).values()
		for u in all_user:
			if u.id == user_id:
				return render_template("/home.html",
					cache_id = uuid4(),
					user = u.to_dict())
		else:
			pass

	return render_template("/home.html",
		cache_id = uuid4(),
		)




"""    SIGN IN AND SIGN UP STARTS HERE    """

@app.route("/signup/authIn", methods=["GET", "POST"])
def more():
	return render_template("/signup.html",
		cache_id = uuid4())

@app.route("/resource/s/aOuth", methods=["POST"])
def resource_signup():

	username = request.form.get("name")
	email = request.form.get("email")
	password = request.form.get("password")

	dct = {"username": username, "email": email, "password": password, "id": uuid4()}

	print(dct)
	session["signup_details"] = dct
	return session["signup_details"]

@app.route("/auth/OTP")
def resource_signup_otp():

	code = str(uuid4())[:4]
	email = session["signup_details"]["email"]
	send_mail(session["signup_details"]["email"])
	return render_template("otp.html", code = code, cache_id = uuid4(), email = email)

@app.route("/resource/s/create")
def create_user():
	"""create user"""
	dct = session["signup_details"]
	dct.pop("id")

	instance = User(**dct)
	instance.save()

	return redirect("/signin/authIn")

@app.route("/signin/authIn")
def signin():
	"""sign in page"""
	return render_template("signin.html", cache_id = uuid4())

@app.route("/resource/s/loginauth", methods=["POST"])
def login_auth():
	"""login authentication"""
	email = request.form.get("email")
	password = request.form.get("password")

	all_users = storage.all(User).values()
	emails_dct = {user.email: user for user in all_users}

	if email in emails_dct.keys():
		user = emails_dct[email]
		passwd = user.password.encode("utf-8")

		r = bcrypt.checkpw(password.encode("utf-8"), passwd)

		if r is True:
			session["username"] = user.username
			session["email"] = user.email
			session["user_id"] = user.id
			flash("signed in successfully")
			return redirect(url_for("home"))
		else:
			flash("Invalid credentrials")
			return redirect(url_for("signin"))
	else:
		flash("Invalid credentrials")
		return redirect(url_for("signin"))


def send_mail(receiver_email):
	"""sends_mail"""
	from email.mime.text import MIMEText 
	from email.mime.image import MIMEImage 
	from email.mime.application import MIMEApplication 
	from email.mime.multipart import MIMEMultipart 
	import smtplib, ssl 
	import os


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

	return code

"""  SIGN IN & LOGIN ENDS  """


if __name__ == "__main__":
    """starts app application"""
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)