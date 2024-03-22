
import email
from enum import unique
import hashlib
from locale import currency
import re
from textwrap import indent
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defer, undefer, relationship, load_only, sessionmaker
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from Helper.helper import generate_transaction_referance
from Settings import app
from datetime import datetime
# from flask_script import Manager
from flask_migrate import Migrate
import json
# from sendEmail import Email 
from sqlalchemy import ForeignKey
import uuid
from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy(app)
migrate = Migrate(app, db)

list_business_account_status = ['PENDING', 'APPROVED', 'REJECTED']
list_transaction_status = ['PENDING', 'SUCCESSFULL', 'FAILED']

def alchemy_to_json(obj, visited=None):
    if visited is None:
        visited = set()
    if obj in visited:
        return None  # Prevent infinite recursion
    visited.add(obj)
    if isinstance(obj.__class__, DeclarativeMeta):
        fields = {}
        exclude_fields = ["query", "registry", "query_class", "password", "apikey", "business"]
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x not in exclude_fields]:
            data = obj.__getattribute__(field)
            try:
                if not callable(data):
                    # Check if the attribute is an instance of a SQLAlchemy model                    
                    if isinstance(data.__class__, DeclarativeMeta):
                        # Handle file relationship
                        fields[field] = alchemy_to_json(data, visited)
                    elif isinstance(data, list) and data and isinstance(data[0].__class__, DeclarativeMeta):
                        # Handle nested objects
                        fields[field] = [alchemy_to_json(item, visited) for item in data]
                    else:
                        # this will fail on non-encodable values, like other classes
                        json.dumps(data)
                        fields[field] = data
                else:
                    pass
            except TypeError:
                fields[field] = str(data)
        return fields

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True) # datatype
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    other_name = db.Column(db.String(80), nullable=True)
    logo = db.Column(db.String(120), nullable=True)
    account_type = db.Column(db.String(22), nullable=True) 
    active_status = db.Column(db.String(80), nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # Add a foreign key, reference to the Business table
    business_id = db.Column(db.String(36), db.ForeignKey('business.business_id'))
    # Define a relationship to access the Business object from a User object
    business = db.relationship('Business', back_populates='user')
    
    def json(self):
        return {
                'id': self.id,
                'email': self.email,
                'role': self.role,
                'phone': self.phone, 
                'first_name': self.first_name, 
                'last_name': self.last_name, 
                'other_name': self.other_name, 
                'logo': self.logo, 
                'account_type': self.account_type, 
                'created_by': self.created_by,
                'updated_by': self.updated_by,
                'business_id': self.business_id, 
                'created_on': self.created_on,
                'updated_on': self.updated_on }
    def _repr_(self):
        return json.dumps({
                'id': self.id,
                'email': self.email,
                'role': self.role,
                'phone': self.phone, 
                'first_name': self.first_name, 
                'last_name': self.last_name, 
                'other_name': self.other_name, 
                'logo': self.logo, 
                'account_type': self.account_type, 
                'created_by': self.created_by,
                'updated_by': self.updated_by,
                'business_id': self.business_id, 
                'created_on': self.created_on,
                'updated_on': self.updated_on })

    def getUserById(id):
        new_data = User.query.filter_by(id=id).first()
        new_data_object = alchemy_to_json(new_data)
        return new_data_object

    def getAllUsers(_email):
        joined_table_data = []
        # user_data = db.session.query(User).filter_by(email=_email).join(Business).all()
        user_data = db.session.query(User, Business).filter_by(email=_email).join(Business).all()

        # get joined tables data
        for user, business in user_data:
            joined_table_data.append({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'other_name': user.other_name, 
                    'logo': user.logo, 
                    'account_type': user.account_type, 
                    'created_by': user.created_by,
                    'updated_by': user.updated_by,
                    'business_id': user.business_id, 
                    'created_on': user.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_on': user.updated_on.strftime("%Y-%m-%d %H:%M:%S")
                },
                'business': {
                    'business_name': business.business_name,
                    'business_id': business.business_id,
                    'business_name': business.business_name,
                    'email': business.email,
                    'phone': business.phone,
                    'digital_address': business.digital_address,
                    'address': business.address,
                    'business_account_status': business.business_account_status,
                    'created_by': business.created_by,
                    'updated_by': business.updated_by,
                    'created_on': business.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_on': business.updated_on.strftime("%Y-%m-%d %H:%M:%S"),
                    'kyc_id': business.kyc_id,
                    'settlement_id': business.settlement_id,
                    'apikey_id': business.apikey_id
                }
            })
        # Convert the result to a JSON-formatted string
        result_json = json.dumps(joined_table_data, indent=2)
        return  result_json

    def createUser(_first_name, _last_name, _other_name, _business_name, _password, _email, _phone, _description, _role, _digital_address, _address, business_detail):
        user_id = str(uuid.uuid4())
        new_user = User( email=_email, password=_password, role=_role, phone=_phone, first_name=_first_name, last_name=_last_name, other_name=_other_name, created_by=_email, updated_by=_email, business_id=business_detail.business_id, id=user_id )
 
        try:
            # Start a new session
            with app.app_context():
                db.session.add(new_user)
        except Exception as e:
            # db.session.rollback()  # Rollback the transaction in case of an error
            print(f"Error:: {e}")
        finally:
            # db.session.close()
            db.session.commit()
            db.session.close()
        return new_user

    def update_user(_key, _value, _user_data):
        if _key == 'password':
            password = hashlib.sha256((_value).encode()).hexdigest()
            # print(_key, _value, _user_data)
            _user_data.password = password
            # print(password)
            
        db.session.commit()
class Business(db.Model):
    __tablename__ = 'business'
    business_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    business_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    digital_address = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(80), nullable=True)
    business_account_status = db.Column(db.String(12), nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # Define a relationship to access the User objects associated with the Business
    user = db.relationship('User', back_populates='business')

    kyc_id = db.Column(db.String(36), db.ForeignKey('kyc.kyc_id'))
    kyc = db.relationship('Kyc', back_populates='business')
    file_id = db.Column(db.String(36), db.ForeignKey('file.id'), nullable=True)
    file = db.relationship('Fileupload', back_populates='business')
    settlement_id = db.Column(db.String(36), db.ForeignKey('settlement.settlement_id'))
    settlement = db.relationship('Settlement', back_populates='business')
    apikey_id = db.Column(db.String(36), db.ForeignKey('apikey.apikey_id'))
    apikey = db.relationship('Apikey', back_populates='business')

    def getBusinessById(id):
        new_data = Business.query.filter_by(business_id=id).first()
        # Render nested objects
        new_data_object = alchemy_to_json(new_data)
        return new_data_object

    def createBusiness( _business_name, _email, _phone, _digital_address, _address, _first_name, _last_name, _other_name, _password, _description, _role, _business_id):
        user = User.query.filter_by(email=_email).first()
        if user is None:
            new_business = Business( business_name=_business_name, email=_email, phone=_phone, digital_address=_digital_address, address=_address, business_account_status=list_business_account_status[0], created_by=_email, updated_by=_email, business_id=_business_id )
            try:
                # db.session.add(new_business)
                # db.session.commit()
                with app.app_context():
                    db.session.add(new_business)
                    db.session.commit()
                    # db.session.close()
                    # print(" business_id >> ", new_business.business_id)
                    # print( _first_name, _last_name, _other_name, _business_name)
                    User.createUser( _first_name, _last_name, _other_name, _business_name, _password, _email, _phone, _description, _role, _digital_address, _address, new_business)        
                return new_business  # Return the created instance after commit
            except Exception as e:
                # db.session.rollback()  # Rollback the transaction in case of an error
                print(f"Error: {e}")
                return None  # Return None to indicate failure
            finally:
                # db.session.close()
                return new_business
        else:
            return "user already"

    def updateBusinessById(request, id):

        new_data = Business.query.filter_by(business_id=id).first()
        print(request)
        if request['business_name'] :
            new_data.business_name = request['business_name']
        if request['email'] :
            new_data.email = request['email']
        if request['phone'] :
            new_data.phone = request['phone']
        if request['digital_address'] :
            new_data.digital_address = request['digital_address']
        if request['address'] :
            new_data.address = request['address']
        if request['business_account_status'] :
            new_data.business_account_status = request['business_account_status']
        db.session.commit()
        # db.session.close()
        return alchemy_to_json(new_data)
class Kyc(db.Model):
    __tablename__ = 'kyc'
    kyc_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    registration_documents = db.Column(db.String(120), nullable=True)
    director_1_document = db.Column(db.String(120), nullable=True)
    director_2_document = db.Column(db.String(120), nullable=True)
    other_documents = db.Column(db.String(120), nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    business = db.relationship('Business', back_populates='kyc')

class Settlement(db.Model):
    __tablename__ = 'settlement'
    settlement_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    account_holder_name = db.Column(db.String(80), nullable=True)
    account_number = db.Column(db.String(80), nullable=True)
    bank_name = db.Column(db.String(80), nullable=True)
    bank_branch_name = db.Column(db.String(80), nullable=True)
    bank_swift_code = db.Column(db.String(80), nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    business = db.relationship('Business', back_populates='settlement')
    # business_id

class Apikey(db.Model):
    __tablename__ = 'apikey'
    apikey_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    apikey_name = db.Column(db.String(80), nullable=True)
    apikey_description = db.Column(db.String(80), nullable=True)
    apikey_status = db.Column(db.String(12), nullable=True)
    apikey = db.Column(db.String(80), nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    business = db.relationship('Business', back_populates='apikey')
    # transaction_id = db.Column(db.String(36), db.ForeignKey('transaction.transaction_id'))
    transaction = db.relationship('Transaction', back_populates='apikey')


transaction_type = ["Credit", "Debit"]

class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    transaction_reference = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False) # generate reference id
    amount = db.Column(db.String(12), nullable=True)
    currency = db.Column(db.String(12), nullable=True)
    fee = db.Column(db.String(12), nullable=True)
    tax = db.Column(db.String(12), nullable=True)
    source_metadata = db.Column(db.String(422), nullable=True)
    destination_metadata = db.Column(db.String(422), nullable=True)
    apikey_reference = db.Column(db.String(422), nullable=True)
    external_service_provider = db.Column(db.String(255), nullable=True)
    channel = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    service = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)    
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    apikey = db.relationship('Apikey', back_populates='transaction')

    def createTransaction(_amount, _currency, _channel, _note, _service, _source_metadata, _destination_metadata, _apikey_reference):
        transaction_id = str(uuid.uuid4())
        transaction_reference = generate_transaction_referance()
        new_data = Transaction( transaction_id=transaction_id, transaction_reference=transaction_reference, amount=_amount, currency=_currency, channel=_channel, status=list_transaction_status[0], note=_note, service=_service, source_metadata=str(_source_metadata), destination_metadata=str(_destination_metadata), apikey_reference=_apikey_reference ) 
        try:
            # Start a new session
            with app.app_context():
                db.session.add(new_data)
        except Exception as e:
            print(f"Error:: {e}")
        finally:
            # db.session.close()
            db.session.commit()
            db.session.close()
        return new_data

class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    code = db.Column(db.String(80), nullable=True)
    type = db.Column(db.String(80), nullable=True)
    account = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def createCode(_email, _code, _type):
        _id = str(uuid.uuid4())
        new_data = Code( account=_email, code=_code, type=_type, id=_id )
        try:
            # Start a new session
            with app.app_context():
                db.session.add(new_data)
        except Exception as e:
            # db.session.rollback()  # Rollback the transaction in case of an error
            print(f"Error:: {e}")
        finally:
            db.session.commit()
            db.session.close()
            pass
        return new_data

class Fileupload(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    file = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(80), nullable=True)
    business = db.relationship('Business', back_populates='file')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def getFileById(id):
        new_data = db.session.query(Fileupload).filter(id==id).first()
        # print(new_data)
        if new_data:
            return alchemy_to_json(new_data)
        

    def createFile(_file, _description, _business):
        _id = str(uuid.uuid4())
        # print(_id, _file)
        new_data = Fileupload( file=_file, description=_description, id=_id )
        try:
            # Start a new session
            with app.app_context():
                db.session.add(new_data)
                db.session.commit()
                # Refresh the instance to make sure attributes are up-to-date
                db.session.refresh(new_data)
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            # return str(e)
        finally:
            db.session.close()
        return new_data


    def updateFile(file, description, business, id):
        # print(">>>>>>>>", id, db.session.query(Fileupload).filter(id==id).first())
        new_data = Fileupload.query.filter_by(id=id).first()
        if file:
            new_data.file = file
        if description:
            new_data.description = description
        db.session.commit()
        print(">>>", new_data.updated_on)
        # db.session.close()
        return alchemy_to_json(new_data)

