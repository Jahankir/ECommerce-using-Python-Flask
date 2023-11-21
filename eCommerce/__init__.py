from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '75b73ad469e9c65a472e2f46bdbc7260c87e3850'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
db = PyMongo(app).db
bcrypt = Bcrypt(app)

from eCommerce import routes