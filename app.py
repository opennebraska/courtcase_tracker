# app.py
from flask import Flask, request
from flask_cors import CORS, cross_origin
from get_cases import query_cases, connect_to_db
from main import get_data, update_db
from datetime import datetime
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/cases/', methods=['GET'])
def cases():
    return query_cases(connect_to_db(), 'test')

@app.route('/adddata/', methods=['GET'])
def adddata():
    # Retrieve the name from url parameter
    date_time_str = request.args.get("date", None)
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    table_rows = get_data(date_time_obj.strftime('%m/%d/%Y'))
    update_db(connect_to_db(), table_rows)
    return "<h1>Thanks!</h1>"

# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
