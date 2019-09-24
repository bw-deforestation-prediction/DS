from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import pandas as pd
import json

df = pd.read_csv('test.csv')

# Flask App Factory
application = Flask(__name__)
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
    # Here we should get the country and year they asked for.
    # TODO: ask backend for a sample request of year and country name
    # TODO: use forest coverage percentage
    try:
        if request.method == 'GET':
            country = request.args.get('country')  # If no key then null
            year = request.args.get('year')  # If no key then null
            return spout(country, year)
            # If they do a GET it auto doesn't allow tmyk wow
    except Exception as e:
        r = Response(response=f"Something broke: {e}",
                     status=404,
                     mimetype="application/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r


# This endpoint gives them a big list of possible country names in JSON
@application.route("/countries", methods=['GET'])
def cNames():
    # Not sure if they want a big list of country names so they don't
    # have to manually do that, but here it is
    # TODO: unsure if they want Row #: Cname or just the country names
    a = pd.DataFrame(df['Country Name'].unique(), columns=['cname']).to_json()
    r = Response(response=a,
                 status=200,
                 mimetype="application/json")
    r.headers["Content-Type"] = "text/json; charset=utf-8"
    return r


def spout(c, y):
    # Perhaps this can be the function to retrieve the apropos data
    f = float(df[(df['Country Name'] == c) & (df['Year'] == int(y))]['Forest Land Percent'])
    print(f)
    return jsonify({'Forest Coverage Percent': f})

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
