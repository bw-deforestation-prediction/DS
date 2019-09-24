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
@application.route("/reception/<tek>", methods=['POST'])
def retrieval(tek):
    # Here we should get the country and year they asked for.
    # TODO: ask backend for a sample request of year and country name
    # TODO: Forest Percent/ Forest Area/ Agr Land Perc/ Pop /
    try:
        if request.method == 'POST':
            # Give response that says 'Yes, that worked here's data'
            # {"Country Name":""}
            #
            #
            json_got = spout(tek)
            r = Response(response=df.iloc[[1]].to_json(), status=200,
                         mimetype="application/json")
            r.headers["Content-Type"] = "text/xml; charset=utf-8"
            return json_got
            # If they do a GET it auto doesn't allow tmyk wow
    except Exception as e:
        r = Response(response="Something broke but unsure of what",
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


def spout(json_asked):
    # Perhaps this can be the function to retrieve the apropos data
    content = request.json
    print(content['test'])
    return jsonify({"yea": "no"})

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
