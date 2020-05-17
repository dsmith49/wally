from flask import Flask
from wally_controller import Wally

app = Flask(__name__)
wally = Wally()
app.config['wally'] = wally

from app import routes

