from app import app
from wally_json_control import Wally

if __name__ == '__main__':
   app.run(debug=True, port=5000, host='0.0.0.0')
