#!/usr/bin/python3
import os
from flask import Flask, abort, render_template, redirect, url_for
from flask import jsonify, session, flash, make_response, request
from models.user import User
from models.item import Item
from models import storage
#from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
from uuid import uuid4
import bcrypt
import json
import requests


app = Flask(__name__)

CORS(app, supports_credentials=True, resources={r"/*": {
	"origins": "http://localhost:5000",
	"methods": ["GET", "POST", "PUT", "DELETE", "UPDATE"]}
	})

app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["UPLOAD_FOLDER"] = os.path.join('web_dynamic', 'static', 'assets', 'public')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Session(app)
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
			return render_template("/home.html",
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



@app.route("/za/<user_type>/inbox")
def member_inbox(user_type):
	"""member inbox page"""
	data = get_cookie()
	if data is None:
		return redirect(url_for(register))
	else:
		if user_type == "member":
			return render_template("/inbox.html",
				cache_id=uuid4(),
				user = data)
		else:
			return render_template("/inbox_seller.html",
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


@app.route("/help")
def help():
	return render_template("help.html", cache_id=uuid4())


@app.route("/t/add_cart", methods=["POST"], strict_slashes=False)
def add_cart():
	"""add cart"""
	item_id = request.form.get("item_id")
	item = storage.get(item_id)
	seller = storage.get(item.seller_id)

	cart = {"item": item.to_dict(), "seller": seller.to_dict()}

	data = get_cookie()

	if data is None:
		if "cart" not in session:
			session["user"] = "guest"
			session["cart"] = []

		session["cart"].append(cart)
		session.modified = True
		return session.get("cart", [])
	else:
		print(item)
		if "cart" not in session:
			session["user"] = "guest"
			session["cart"] = []

		session["cart"].append(cart)
		session.modified = True
		return session.get("cart", [])


@app.route("/t/get_cart", methods=["GET"], strict_slashes=False)
def get_no_carts():
	"""returns no of carts for a user"""
	if "cart" not in session:
		return jsonify({"cart_count": 0});
	else:
		carts = session.get("cart", [])
		return jsonify({"cart_count": len(carts)})


@app.route("/cart")
def cart():
	"""return cart page"""
	accounts = {"subtotal": 0, "total": 0}

	if "cart" in session:
		carts = session.get("cart", [])
		for c in carts:
			accounts["subtotal"] += int(c["item"]["price"])
			accounts["total"] += int(c["item"]["price"])
	else:
		carts = []

	if len(carts) == 0:
		carts = None
		accounts = None


	return render_template("bag.html", cache_id=uuid4(), carts = carts, accounts=accounts)


@app.route("/favorites")
def favorite():
	"""favourites page"""
	return render_template("fav.html", cache_id=uuid4())


def initialize_favorites():
	if 'favorites' not in session:
		session['favorites'] = []


@app.route('/za/add_favorite', methods=['POST'])
def add_favorite():
	initialize_favorites()
	item = request.json
	favorites = session['favorites']

	if item["id"] not in favorites:
		favorites.append(item["id"])

	session['favorites'] = favorites
	return jsonify({'message': 'Favorite added', 'favorites': session['favorites']})


@app.route('/za/favorites', methods=['GET'])
def get_favorites():
	initialize_favorites()
	all_items = storage.all(Item).values()

	favorites = [ i.to_dict() for i in all_items if i.id in session["favorites"]]
	return jsonify(favorites)


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

""" ADMIN ONLY """
@app.route("/admin/dashboard")
def admin_dashboard():
	"""admin dashboard"""
	return render_template("/admin.html", cache_id=uuid4())


@app.route("/admin/d/<model>")
def d_model(model):
	"""urls for dif admin models"""

	if model == "product":
		response = requests.get(f"http://127.0.0.1:5001/api/v1/items/stats")

		if response.status_code == 200:
			stats = response.json()
			return render_template("/item_admin.html", cache_id=uuid4(), stats=stats)
		else:
			abort(500)

	elif model == "user":
		return render_template("/user_admin.html", cache_id=uuid4())
	else:
		return redirect(url_for("admin_dashboard"))


@app.route("/admin/d/inbox")
def admin_inbox():
	"""admin inboxes user"""
	return render_template("/admin_inbox.html", cache_id=uuid4())


if __name__ == "__main__":
    """starts app application"""
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)