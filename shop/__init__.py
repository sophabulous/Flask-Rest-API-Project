from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthybites.db"
app.config['SECRET_KEY']='hfouewhfoiwefoquw'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes to register them
from shop.products import routes
from shop.cart import cart
