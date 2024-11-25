#!/usr/bin/python3
from flask import Flask, jsonify
from flask_cors import CORS
from uuid import uuid4
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = uuid4().hex
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(error):
	"""returns 404 error"""
	return jsonify({"error": "page not found"})



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)