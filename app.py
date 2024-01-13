from flask import Flask, jsonify, request, Response
import requests, json
#import geocoder
from Model import User
# from sendEmail import Email 
from Settings import *
import jwt, datetime
from functools import wraps
from flask_cors import CORS
import hashlib
# from pyisemail import is_email 
import sys
#import winrt.windows.devices.geolocation as wdg, asyncio
from email.mime.text import MIMEText
#from safrs import SAFRSBase, SAFRSAPI
#from api_spec import spec
#from swagger import swagger_ui_blueprint, SWAGGER_URL
# Created instance of the class
from dotenv import dotenv_values


get_env = dotenv_values (".env")  

CORS(app)
app.config['SECRET_KEY'] = get_env['SECRET_KEY']        


@app.route('/test', methods=['POST'])
def testd():
    try:
        print((request.json)['test'] )
        User.createUser()
        return "test"
    except Exception as e:
        # print(e)
        return {"tes": str(e)}


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = request_data['username']
    password = hashlib.sha256(request_data['password'].encode()).hexdigest()
    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return { "user": match, "access_key": jwt.decode( token, app.config['SECRET_KEY'], algorithms=['HS256'] ), "token": token  }
    else:
        return Response('', 401, mimetype='application/json')
    
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        #token = request.args.get('token')
        #print(request.headers['Token'])
        #print(token)
        try:
            jwt.decode( request.headers['Token'], app.config['SECRET_KEY'], algorithms=['HS256'] )
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid Token', "status": 301 })
    return wrapper

@app.route('/v1/auth/business/registration', methods=['POST'])
def add_user_registration():
    request_data = request.get_json()
    msg = {}

    role = 'BUSINESS' # user role
    password = hashlib.sha256((request_data['password']).encode()).hexdigest()
    if User.query.filter_by(email=request_data['email']).count() < 1:  
        # if request_data['password'] request_data['email']     
        if request_data['type'] == "MERCHANT":
            try:
                User.createUser(request_data['first_name'], request_data['last_name'], request_data['other_name'], request_data['business_name'],  password, request_data['email'], request_data['phone'], request_data['description'], role)

                msg = {
                    "code": 200,
                    "error": "user added",
                    "helpString": 'Data passed" }'
                }
            except Exception as e:
                msg = {
                    "code": 200,
                    "error": str(e),
                    "helpString": 'Data passed" }'
                }

            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response
        else:
            msg = {
                "code": 201,
    			"error": "user already registtered",
    			"helpString": 'Data passed" }'
    		}
            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response
    else:
        invalidUserOjectErrorMsg = {
            "code": 204,
			"error": "user already registtered",
			"helpString": 'Data passed" }'
		}
        response = Response(json.dumps(invalidUserOjectErrorMsg), status=200, mimetype='application/json')
        return response
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)