from crypt import methods
import uuid
from flask import Flask, jsonify, request, Response, render_template
import requests, json
from Helper.helper import generate_random_code
from fileManager.fileManager import fileUpload
#import geocoder
from Model import Business, Transaction, User, Code, db, Fileupload, Business
from Notification.Email.sendEmail import send_notification_email
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


get_env = dotenv_values(".env")  

CORS(app)
app.config['SECRET_KEY'] = get_env['SECRET_KEY']        



@app.route('/test', methods=['POST'])
def testd():
    try:
        print((request.json)['test'] )
        # user = User.getAllUsers((request.json)['email'])

        msg = {
            "code": 200,
            "helpString": 'Successful'
        }
        response = Response( json.dumps(msg), status=200, mimetype='application/json')
        return response    
    except Exception as e:
        # print(e)
        return {"tes": str(e)}

@app.route('/v1/callback/mfs', methods=['POST'])
def callbackMfs():
    try:
        request_data = request.json
        # print("mfs callback >>> ", request_data )
        msg = {
            "code": 200,
            "helpString": 'Successful',
            "data": request_data
        }
        response = Response( json.dumps(msg), status=200, mimetype='application/json')
        return response 
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

@app.route('/user/<string:id>', methods=['GET'])
def user(id):
    if request.method == 'GET':
        try:
            request_data = User.getUserById(id)
            # print("mfs callback >>> ", request_data )
            msg = {
                "code": 200,
                "message": 'Successful',
                "data": request_data
            }
            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response 
        except Exception as e:
            # print(e)
            return {"code": 203, "message": 'Failed', "error": str(e)}
    else:
        return {"code": 400, "message": 'Failed' }
        
@app.route('/v1/business/registration/', methods=['POST'])
def add_user_registration():
    request_data = request.get_json()
    msg = {}
    # print("fff")
    role = 'BUSINESS' # user role
    try:
        password = hashlib.sha256((request_data['password']).encode()).hexdigest()  
        if User.query.filter_by(email=request_data['email']).first() is None:
            # if request_data['password'] request_data['email']     
            if request_data['type'] == "BUSINESS":
                try:
                    business_id = str(uuid.uuid4())

                    business_detail = Business.createBusiness( request_data['business_name'], request_data['email'], request_data['phone'], request_data['digital_address'], request_data['address'], request_data['first_name'], request_data['last_name'], request_data['other_name'], password, request_data['description'], role, business_id)
                    # business_detail = Business( business_name=request_data['business_name'], email=request_data['email'], phone=request_data['phone'], digital_address=request_data['digital_address'], address=request_data['address'], business_account_status='PENDING', created_by=request_data['email'], updated_by=request_data['email'] )
                    # db.session.add(business_detail)
                    # print("===<<<>>>===")
                    # db.session.commit()
                    # db.session.close()

                    # print("business_detail >>", business_detail)
                    msg = {
                            "code": 200,
                            "msg": "user added",
                            # "data": 'f{instance_dict}'
                    }
                    if str(business_detail) != "None":
                        # print("======", business_detail.business_id)

                        # new_detail = User.createUser(request_data['first_name'], request_data['last_name'], request_data['other_name'], request_data['business_name'],  password, request_data['email'], request_data['phone'], request_data['description'], role, request_data['address'], request_data['digital_address'], business_detail)

                        # instance_dict = {column.name: getattr(new_detail, column.name) for column in new_detail.__table__.columns}
                        # print(f'New instance as JSON:\n{instance_dict}')
                        pass
                        
                    else:
                        pass
                except Exception as e:
                    msg = {
                        "code": 201,
                        "error": str(e),
                        "helpString": 'Data passed" }'
                    }


                response = Response( json.dumps(msg), status=200, mimetype='application/json')
                return response
            else:
                msg = {
                    "code": 202,
                    "error": "user already registtered",
                    "helpString": 'Data passed" }'
                }
                response = Response( json.dumps(msg), status=200, mimetype='application/json')
                return response
        else:
            invalidUserOjectErrorMsg = {
                "code": 203,
                # "error": str(e),
                "helpString": 'Data passed" }'
            }
            response = Response(json.dumps(invalidUserOjectErrorMsg), status=200, mimetype='application/json')
            return response
    except Exception as e:
        invalidUserOjectErrorMsg = {
            "code": 204,
            "error": str(e),
            "helpString": 'Data passed" }'
        }
        response = Response(json.dumps(invalidUserOjectErrorMsg), status=200, mimetype='application/json')
        return response

@app.route('/v1/business/<string:id>', methods=['PATCH'])
def update_resource(id):
    # Fetch the resource from your data source (e.g., database)
    resource = User.getUserById(id)

    validate_list = ["id", "password"]
    validate_status = False
    msg = {}
    if resource is None:
        return jsonify({'error': 'Resource not found'}), 404
    # Get the data from the request
    data = request.get_json()
    get_req_keys = None
    get_req_keys_value_pair = None
    # Update only the provided fields
    for key, value in data.items():
        if key in validate_list:
            validate_status = True
            if get_req_keys is None:
                get_req_keys = key
                get_req_keys_value_pair = f'"{key}": "{value}"'
            else:
                get_req_keys = f"{get_req_keys}, {key}"
                get_req_keys_value_pair = f'{get_req_keys_value_pair}, "{key}": "{value}"'
            try:
                User.update_user(key, value, resource)
                msg = {
                        "code": 200,
                        "msg": f"user detail(s) updated: {get_req_keys}",
                        # "data": 'f{instance_dict}'
                }
            except Exception as e:
                msg = {
                    "code": 501,
                    "error :" : str(e),
                    "msg": "server error" 
                }
    # print(json.dumps(get_req_keys_value_pair))
    if validate_status is False:
        msg = {
            "code": 201,
            "msg": str(validate_list)
        }
    # print("resource", resource)

    response = Response( json.dumps(msg), status=200, mimetype='application/json')
    return response  
    
@app.route('/v1/otp/email', methods=['POST'])
def send_notification():
    data = request.get_json()
    to_email = data['email']
    print(to_email)
    subject = 'Notification Subject'
    users = User.query.filter_by(email=to_email).first()
    print(users)
    try:
        if users:
            code = generate_random_code()
            render_html = render_template('email.html', code=code)
            Code.createCode(to_email, code, "OTP")
            if send_notification_email(to_email, subject, render_html):
                return 'Notification sent successfully!'
            else:
                return 'Failed to send notification.'
        else:
            return 'User does not exist'
    except Exception as e:
        return str(e)
        pass

@app.route('/')
def index():
    return render_template('/fileUpload.html')

@app.route('/upload', methods=['POST'])
def upload():
    return fileUpload(request)

@app.route('/upload/<string:id>', methods=['PATCH', 'GET'])
def uploadUpdate(id):
    if request.method == 'GET':
        return Fileupload.getFileById(id)
    if request.method == 'PATCH':
        return fileUpload(request, id)

@app.route('/business/<string:id>', methods=['PATCH', 'GET'])
def business(id):
    if request.method == 'GET':
        return Business.getBusinessById(id)
    if request.method == 'PATCH':
        request_data = request.get_json()
        return Business.updateBusinessById(request_data, id)

@app.route('/transaction/<string:id>', methods=['GET'])
def transaction(id):
    if request.method == 'GET':
        try:
            request_data = Transaction.getTransactionById(id, request.args.get('page', 1), request.args.get('per_page', 1000) )
            # print("mfs callback >>> ", request_data )
            msg = {
                "code": 200,
                "message": 'Successful',
                "data": request_data
            }
            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response 
        except Exception as e:
            # print(e)
            return {"code": 203, "message": 'Failed', "error": str(e)}
    else:
        return {"code": 400, "message": 'Failed' }

@app.route('/transaction/business/<string:id>', methods=['GET'])
def transactionBusiness(id):
    if request.method == 'GET':
        try:
            request_data = Transaction.getTransactionByBusinesId(id, request.args.get('page', 1), request.args.get('per_page', 1000) )
            # print("mfs callback >>> ", request_data )
            msg = {
                "code": 200,
                "message": 'Successful',
                "data": request_data
            }
            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response 
        except Exception as e:
            # print(e)
            return {"code": 203, "message": 'Failed', "error": str(e)}
    else:
        return {"code": 400, "message": 'Failed' }

@app.route('/transaction/update/<string:id>', methods=['PATCH'])
def transactionBusiness(id):
    if request.method == 'PATCH':
        try:
            request_data = request.get_json()
            Transaction.updateTransaction(request_data['status'], id)
            # print("mfs callback >>> ", request_data )
            msg = {
                "code": 200,
                "message": 'Successful',
                "data": request_data
            }
            response = Response( json.dumps(msg), status=200, mimetype='application/json')
            return response 
        except Exception as e:
            # print(e)
            return {"code": 203, "message": 'Failed', "error": str(e)}
    else:
        return {"code": 400, "message": 'Failed' }

if __name__ == "__main__":
    app.run(debug=True, port=5001)