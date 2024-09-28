#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from flask import jsonify, make_response
from models.user import User
from models import storage
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
from uuid import uuid4


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
	return render_template("/home.html")


if __name__ == "__main__":
    """starts app application"""
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)