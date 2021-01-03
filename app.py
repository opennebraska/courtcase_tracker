# app.py
from flask import Flask, request
from flask_cors import CORS, cross_origin
from get_cases import query_cases
from add_data import get_cases, insert_cases
from datetime import datetime
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/cases/', methods=['GET'])
def cases():
    landlord = request.args.get("landlord", None)
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    return query_cases(landlord=landlord, start_date=start_date, end_date=end_date)

@app.route('/adddata/', methods=['GET'])
def adddata():
    if request.args.get("date", None):
        date_str = datetime.strptime(request.args.get("date", None), '%Y-%m-%d').strftime('%m/%d/%Y')
        county = request.args.get("county", "Douglas")
        cases = get_cases(county, date_str)
        if cases:
            insert_cases(cases)
    return "<h1>Thanks!</h1>"

# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
