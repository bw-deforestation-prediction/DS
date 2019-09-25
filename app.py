from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import pandas as pd
import json

df = pd.read_csv('test.csv')

# Flask App Factory
application = Flask(__name__)
# Wrap application in CORS so that it when calling from localhost
# addresses the computer won't disallow the request...due to CORS.
CORS(application)


# Test endpoint to see if working
@application.route("/", methods=['POST', 'GET'])
def test():
    r = Response(response="This worked", status=200,
                 mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


# User should want two things, country and year...
@application.route("/reception", methods=['GET'])
def retrieval():
    '''
    Here we should get the data for the country and year they asked for.
    '''
    try:
        if request.method == 'GET':
            country = request.args.get('country')  # If no key then null
            year = request.args.get('year')  # If no key then null
            return spout(country, year)
    except Exception as e:
        # Unfortunately I'm not going to wrap this in indv. strings
        r = Response(response=f"""
Something broke,
perhaps the year or country name is wrong.
!!!{e}!!!
Use the /countries or /years endpoints to get a list
of possible values.
""",
                     status=404,
                     mimetype="application/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r


# This endpoint gives a big list of possible country names in JSON
@application.route("/countries", methods=['GET'])
def cNames():
    '''
    Returns a JSON list of country names
    '''
    a = pd.DataFrame(df['Country Name'].unique(), columns=['cname']).to_json()
    r = Response(response=a,
                 status=200,
                 mimetype="application/json")
    r.headers["Content-Type"] = "text/json; charset=utf-8"
    return r


# This endpoint gives a list of possible years in JSON
@application.route("/years", methods=['GET'])
def aYears():
    '''
    Returns a JSON list of years
    '''
    a = pd.DataFrame(df['Year'].unique(), columns=['years']).to_json()
    r = Response(response=a,
                 status=200,
                 mimetype="application/json")
    r.headers["Content-Type"] = "text/json; charset=utf-8"
    return r


def spout(c, y):
    '''
    Takes country and year and returns wrapped JSON object
    '''
    f = float(df[(df['Country Name'] == c) & (df['Year'] == int(y))]['Forest Land Percent'])

    print(f)
    # Returns Flask.Response object (so no need to wrap again in Response)
    return jsonify({'Forest Coverage Percent': f})

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
