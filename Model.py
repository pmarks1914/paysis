
import email
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defer
from sqlalchemy.orm import undefer
from sqlalchemy.orm import relationship
from sqlalchemy import or_
from Settings import app
from datetime import datetime
# from flask_script import Manager
from flask_migrate import Migrate
import json
from sqlalchemy.orm import load_only
# from sendEmail import Email 
from sqlalchemy import ForeignKey
import uuid

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=True)
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
    
    def createUser(_first_name, _last_name, _other_name, _business_name, _password, _email, _phone, _description, _role):
        new_user = User( email=_email, password=_password, role=_role, phone=_phone, first_name=_first_name, last_name=_last_name, other_name=_other_name, business=_business_name, created_by=_email, updated_by=_email )
        db.session.add(new_user)
        db.session.commit()

class Business(db.Model):
    __tablename__ = 'business'
    business_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    business_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)
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
    settlement_id = db.Column(db.String(36), db.ForeignKey('settlement.settlement_id'))
    settlement = db.relationship('Settlement', back_populates='business')
    apikey_id = db.Column(db.String(36), db.ForeignKey('apikey.apikey_id'))
    apikey = db.relationship('Apikey', back_populates='business')

    def createBusiness( _business_name, _email, _phone, _digital_address, _address, _business_account_status):
        new_business = Business( email=_email, phone=_phone, digital_address=_digital_address, address=_address, business_account_status=_business_account_status, created_by=_email, updated_by=_email )
        db.session.add(new_business)
        db.session.commit()


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
    transaction_id = db.Column(db.String(36), db.ForeignKey('transaction.transaction_id'))
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
    status_code = db.Column(db.String(50), nullable=True)
    status_message = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    service = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)    
    created_by = db.Column(db.String(80), nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    apikey = db.relationship('Apikey', back_populates='transaction')



app.app_context().push()
#     db.create_all()
# for table in db.Model.metadata.tables.values():
#     print(f"Table: {table.name}")
#     for column in table.c:
#         print(f"  Column: {column.name}, Type: {column.type}")