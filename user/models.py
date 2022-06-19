import hashlib
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token

class User:

    def __init__(self) -> None:
        self.users = db.users

    def signup(self):
        # create user
        user = {
            "_id":uuid.uuid4().hex,
            "first_name" : request.get_json().get("first_name"),
            "last_name" : request.get_json().get("last_name"),
            "email" : request.get_json().get("email"),
            "password" : request.get_json().get("password")
        }

        # encrypt the password
        user["password"] = hashlib.sha256(user['password'].encode("utf-8")).hexdigest()
        print(user["password"])

        # check if the email exists
        if self.users.find_one({"email":user["email"]}):
            return jsonify({"error": "A user with This email already exists"}),400

        if self.users.insert_one(user):
            return jsonify(user),200

        return jsonify({"error": "A user with This email already exists"}),400

    def login(self):
        login_details = request.get_json() # store the json body request
        user_from_db = self.users.find_one({'email': login_details['email']})  # search for user in database

        if user_from_db:
            encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
            print(user_from_db['password']==encrpted_password)
            print(user_from_db['password'],encrpted_password)
            if encrpted_password == user_from_db['password']:
                access_token = create_access_token(identity=user_from_db['email']) # create jwt token
                return jsonify(access_token=access_token), 200

        return jsonify({'msg': 'The email or password is incorrect'}), 401

    def fetch_all(self):
        all_data = self.users.find({})

        return jsonify(list(all_data)), 200
    
    def refresh_token(self):
        login_details = request.get_json() # store the json body request
        user_from_db = self.users.find_one({'email': login_details['email']})  # search for user in database

        if user_from_db:
            encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
            print(user_from_db['password']==encrpted_password)
            print(user_from_db['password'],encrpted_password)
            if encrpted_password == user_from_db['password']:
                access_token = create_refresh_token(identity=user_from_db['email']) # create jwt token
                return jsonify(access_token=access_token), 200

        return jsonify({'msg': 'The email or password is incorrect'}), 401

    # def logout(self):

    #     return jsonify({"error": "A user with This email already exists"}),400
