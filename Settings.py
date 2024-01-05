from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# import mysql.connector
from sqlalchemy import create_engine

app = Flask(__name__)

DB_URL = "postgresql://testdiv:l2CG6UOFM0YPjWlmh4drBMEGqr2bECcb@dpg-cm61rhocmk4c73csvbsg-a.oregon-postgres.render.com/testdiv"
# DB_URL = "postgres://testdiv:l2CG6UOFM0YPjWlmh4drBMEGqr2bECcb@dpg-cm61rhocmk4c73csvbsg-a.oregon-postgres.render.com:5432/testdiv"
# DB_URL = "mysql+pymysql://id20870341_test:Test#test1@145.14.145.123:3306/id20870341_test"
# DB_URL = "mysql+pymysql://testdiv:testdivtestdiv@188.165.208.104:3306/college1_testdiv"


engine = create_engine(DB_URL)
print(engine)
# Example: Connect to the database and execute a simple query
# with engine.connect() as connection:
#     result = connection.execute ("SELECT '* From User'")
#     print(result.scaler())


app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False