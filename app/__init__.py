from flask import Flask
from wally_json_control import Wally

app = Flask(__name__)
wally = Wally()
app.config['wally'] = wally

from app import routes

