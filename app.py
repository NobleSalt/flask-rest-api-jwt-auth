from template import routes
from user import routes
import datetime
from functools import wraps
from flask_jwt_extended import JWTManager
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

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)