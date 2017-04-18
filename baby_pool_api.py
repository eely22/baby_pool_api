from api_version import version as api_version
import time
import json
import uuid
import urllib
import os
import boto3
import datetime

from flask import Flask, request, session, g, url_for, Response, request, jsonify

# create our app
app = Flask(__name__)

# enable CORS on everything
from flask_cors import CORS
CORS(app)

# helper function to get the current time in millis()
current_milli_time = lambda: int(round(time.time() * 1000))

#functions to manage database connections
app.config.update(dict(
    TABLE_NAME='baby_pool'
))

#default return type to JSON, since this is really what we use
class JSONResponse(Response):
    default_mimetype = 'application/json'

# will return 400 when called
@app.errorhandler(400)
def bad_request(error=None):
        """
        Handle 400 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 400,
            'error': 'BadRequest: ' + request.url,
            "message": error if error is not None else '',
        }
        resp = jsonify(message)
        resp.status_code = 400

        return resp

# will return 500 when called
@app.errorhandler(500)
def internal_error(error=None):
        """
        Handle 500 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 500,
            'error': 'ServerError: ' + request.url,
            "message": error if error is not None else '',
        }
        resp = jsonify(message)
        resp.status_code = 500

        return resp

# Routes
# ------------------------------------------------------------------------------
@app.route('/baby_pool/version')
def version():
    return json.dumps({'version': api_version})

@app.route('/baby_pool', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        try:
            client = boto3.client('dynamodb')
            response = convert_scan_response(client.scan(TableName=app.config['TABLE_NAME'])['Items'])
        except Exception as ex:
            return internal_error(ex.message)

        return JSONResponse(json.dumps(response))

    elif request.method == 'POST':
        try:
            params = get_payload(request)

            email = params['email']
            weight = params['weight']
            date = params["date"]
            sex = params["sex"]
            comment = params["comment"]
        except:
            return bad_request("Invalid parameters")

        try:
            client = boto3.client('dynamodb')
            response = client.put_item(TableName=app.config['TABLE_NAME'], Item={
                'email': {'S': email}, 'weight': {'S': weight},
                'date': {'S': date}, 'sex': {'S': sex}, 'comment': {'S': comment},
                'submitted': {'S': datetime.datetime.now().strftime("%m/%d/%y")},
                'submitted_int': {'N': str(current_milli_time())}})
        except Exception as ex:
            return internal_error(ex.message)

        return JSONResponse(json.dumps({"message": "ok"}))

# Helper functions
# ------------------------------------------------------------------------------
def get_payload(request):

    if request.method == 'POST':
        # if POST, the data may be in the data array as json or form, depending on how it was handed in
        # Postman seems to hand it in as json while others seem to hand it in through form data
        data = request.get_json(force=True, silent=True)
        return data if data is not None else request.form
    else:
        return request.args

def convert_scan_response(items):
    parsed_items = []
    for item in items:
        obj = {}
        for key in item.keys():
            obj[key] = item[key][item[key].keys()[0]]
        parsed_items.append(obj)
    return parsed_items



# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()