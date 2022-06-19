from flask import jsonify
from app import app, db
from user.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/auth/signup',methods=['POST'])
def signup():

    return User().signup()

@app.route('/auth/login',methods=['POST'])
def login():

    return User().login()

@app.route('/users',methods=['GET'])
@jwt_required()
def users():

    return User().fetch_all()

@app.route("/auth/refresh-token", methods=["GET","POST"])
@jwt_required()
def refresh_token():
	current_user = get_jwt_identity() # Get the identity of the current user
	user_from_db = db.users.find_one({'email' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404
