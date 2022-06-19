import datetime
from functools import wraps
import hashlib
import uuid
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from flask import Flask, render_template, request, jsonify
import pymongo
from decouple import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
jwt = JWTManager(app)  # initialize JWTManager
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)  # define the life span of the token

# database
client = pymongo.MongoClient(config('MONGODB_URL'))

db = client.my_flask_collection

# routes

# template - models
class Template:

    def create(self):
        temp = {
            "_id": uuid.uuid4().hex,
            "template_name": request.get_json().get("template_name"),
            "subject": request.get_json().get("subject"),
            "body": request.get_json().get("body"),
        }

        if db.template.insert_one(temp):
            return jsonify({"message": "Successfully Added New Template"}), 200

        return jsonify({"error": "There is an problem with your data !"}), 400

    def fetch_one(self, id):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:
            return jsonify(single_temp), 200

        return jsonify({"error": "This template was not found !"}), 400

    def delete_one(self, id):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:
            db.template.delete_one({"_id": id})
            return jsonify({"message": "You Have Successfully Deleted A Template"}), 200

        return jsonify({"error": "This template was not found !"}), 400

    def fetch_all(self):
        all_data = db.template.find({})

        return jsonify(list(all_data)), 200

    def update_one(self, id, update):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:

            return jsonify(single_temp), 200

        return jsonify({"error": "This template was not found !"}), 400


# Template
@app.route('/template', methods=['POST'])
def create():
    return Template().create()


@app.route('/template', methods=['GET'])
def get_all():
    return Template().fetch_all()


@app.route('/template/<id>', methods=['GET'])
def get_one(id):
    return Template().fetch_one(id)


@app.route('/template/<id>', methods=['UPDATE'])
def update(id):
    return Template().update_one(id=id)


@app.route('/template/<id>', methods=['DELETE'])
def delete(id):
    return Template().delete_one(id=id)

# template - models

# users - models
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

# routes
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

# users - models

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/safe')
def safe():
    return render_template('safe.html')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.users.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

            return f(current_user, *args,  **kwargs)
    return decorator