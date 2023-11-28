from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
db = PyMongo(app).db
bcrypt = Bcrypt(app)

from eCommerce import routes
