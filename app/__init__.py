from flask import Flask
from wally_json_control import Wally

app = Flask(__name__)
wally = Wally()
app.config.from_object( wally )

from app import routes

