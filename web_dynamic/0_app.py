#!/usr/bin/python3
import os
from flask import Flask, abort, render_template, redirect, url_for
from flask import jsonify, session, flash, make_response, request
from models.user import User
from models.item import Item
from models import storage
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
from uuid import uuid4
import bcrypt
import json
import requests


app = Flask(__name__)

CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["UPLOAD_FOLDER"] = os.path.join('web_dynamic', 'static', 'assets', 'public')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

Session(app)
socketio = SocketIO(app)


@app.errorhandler(404)
def not_found(error):
	"""handles 404 errors"""
	return make_response(render_template("/404.html"), 404)


@app.route("/home/<user_id>", strict_slashes=False)
@app.route("/home", strict_slashes=False)
def home(user_id=None):
	"""home page"""
	if user_id: # Fetch user data from API
		response = requests.get(f"http://127.0.0.1:5001/api/v1/users/{user_id}")

		if response.status_code == 200:
			data = response.json() # Parse JSON data into a dictionary
			data["username"] = data.get("first_name", "") + " " + data.get("last_name", "")
			session[user_id] = data # Convert data to string for cookie storage
			r = make_response(render_template("/home.html", cache_id=uuid4(), user=data))

			# Create the response and set the cookie
			r.set_cookie('elvideri',
				value=json.dumps(data), # Convert data to string for cookie storage
				max_age=3600,
				path="/",
				secure=False,
				httponly=True,
				samesite='Lax')

			return r
		else:
			return f"Error: Unable to retrieve data for user_id {user_id}", response.status_code
	else:
		data = get_cookie()
		if data is None:
			return render_template("/home_2.html",
				cache_id = uuid4())
		else:
			return render_template("/home.html",
				cache_id = uuid4(),
				user = data)


@app.route("/za/<user_type>/profile")
def member_profile(user_type):
	"""member profile page"""
	data = get_cookie()
	if data is None:
		return redirect(url_for(register))
	else:
		if user_type == "member":
			return render_template("/profile.html",
				cache_id=uuid4(),
				user = data)
		else:
			return render_template("/profile_seller.html",
				cache_id=uuid4(),
				user = data)



@app.route("/t/<item>/<id>", methods=["GET"])
def item(item, id):
	"""Get"""
	all_items = storage.all(Item).values()
	all_users = storage.all(User).values()

	for i in all_items:
		if i.id == id:
			for u in all_users:
				if u.id == i.seller_id:
					return render_template("/item.html",
						item = i.to_dict(),
						cache_id = uuid4(),
						seller = u.to_dict())
	else:
		return abort(404)


@app.route("/membership/<user_id>", strict_slashes=False)
@app.route("/membership", strict_slashes=False)
def membership(user_id=None):
    """Shows benefits of being a member"""
    if user_id:
        # Fetch user data from API
        response = requests.get(f"http://127.0.0.1:5001/api/v1/users/{user_id}")
        
        if response.status_code == 200:
            data = response.json()  # Parse JSON data into a dictionary
            data["username"] = data.get("first_name", "") + " " + data.get("last_name", "")
            
            # Store data in session
            session[user_id] = data
            
            # Create the response and set the cookie
            r = make_response(render_template("membership.html", cache_id=uuid4(), user=data))
            r.set_cookie('elvideri',
                         value=json.dumps(data),  # Convert data to string for cookie storage
                         max_age=3600,
                         path="/",
                         secure=False,
                         httponly=True,
                         samesite='Lax')
            return r
        else:
            return f"Error: Unable to retrieve data for user_id {user_id}", response.status_code
    else:
        # Return the template if no user_id is provided
        return make_response(render_template("membership.html", cache_id=uuid4()))


@app.route("/about/sell/<user_id>", strict_slashes=False)
@app.route("/about/sell")
def about_sell(user_id=None):
	"""about sell"""
	if user_id:
		response = requests.get(f"http://127.0.0.1:5001/api/v1/users/{user_id}")

		if response.status_code == 200:
			data = response.json()
			data["username"] = data.get("first_name", "") + " " + data.get("last_name", "")

			session[user_id] = data

			r = make_response(render_template("about_sell.html", cache_id = uuid4(), user = data))

			r.set_cookie('elvideri',
				value=json.dumps(data),
				max_age=3600,
				path="/",
				secure=False,
				httponly=True,
				samesite='Lax')

			return r
		else:
			return f"Error: Unable to retrieve data for user_id {user_id}", response.status_code
	else:
		data = get_cookie()
		if data is None:
			return make_response(render_template("about_sell.html", cache_id=uuid4()))
		else:
			return make_response(render_template("about_sell.html", cache_id=uuid4(), user = data))


@app.route("/register")
def register():
	"""page where a user registers/creates an account"""
	type = request.args.get("type")
	
	if type == "seller":
		return render_template("register.html", cache_id = uuid4(), type=type)
	else:
		return render_template("register.html", cache_id = uuid4(), type=type)


@app.route("/mail_redirect")
def redirect_mail_check():
	"""check mail entered and redirects appropriately"""
	status = request.args.get("status")
	email = request.args.get("email")
	type = request.args.get("type")

	if status == "0":
		return redirect(url_for("join_zulwin", email = email, type=type))
	else:
		return redirect(url_for("into_zulwin", email= email, type=type))


@app.route("/join")
def join_zulwin():
	"""sign up or join"""
	email = request.args.get("email")
	code = str(uuid4())[:4]
	return render_template("/signup.html", cache_id = uuid4(), email = email, type=request.args.get("type"))

	
@app.route("/into_zulwin")
def into_zulwin():
	"""sign in""" 
	return render_template("/signin.html", cache_id = uuid4(), email = request.args.get("email"), type = request.args.get("type"))


@app.route("/sell")
def sell():
	all_user = storage.all(User).values()
	data = get_cookie();
	print(data)
	if data is None:
		return render_template("/sell.html",
			cache_id = uuid4())
	else:
		return render_template("/sell.html",
			cache_id = uuid4(),
			user = data
		)

""" SAVING IMAGE """
@app.route("/save_image", methods=["POST"], strict_slashes=False)
def save_image():
	"""save image"""
	filename = request.form.get("filename")
	file = request.files['file']

	if file.filename == '':
		return jsonify({'error': 'No selected file'}), 400

	if file:
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(":", "-"))
		file.save(filepath)
		return jsonify({'success': True, 'file_path': filepath}), 200



"""" SETTING COOKIE  """
def get_cookie():
	"""gets cookies"""
	cookie_value = request.cookies.get('elvideri')
	
	if cookie_value:
		data = json.loads(cookie_value)
		return data
	else:
		return None

	
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