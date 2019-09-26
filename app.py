from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import requests  # pythons default requests

df = pd.read_csv('test.csv')

# Flask App Factory
application = Flask(__name__)
# Wrap application in CORS so that it when calling from localhost
# addresses the computer won't disallow the request...due to CORS.
CORS(application)

error_msg = f'''
Something broke!
Use the /countries or /years endpoints to get a list
of possible values.
'''


# Test endpoint to see if working
@application.route("/", methods=['POST', 'GET'])
def test():
    r = Response(response="This worked!", status=200,
                 mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


# User will get a simple return of country and year
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
        r = Response(response=error_msg+str(e),
                     status=404,
                     mimetype="application/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r


# User is getting a detailed breakdown of country in that year.
@application.route("/reception/detail", methods=['GET'])
def maxRetrieval():
    '''
    Here we should get all important data for the
    country and year they asked for.
    '''
    try:
        if request.method == 'GET':
            country = request.args.get('country')  # If no key then null
            year = request.args.get('year')  # If no key then null
            return spout(country, year, detail=1)
    except Exception as e:
        # Unfortunately I'm not going to wrap this in indv. strings.
        r = Response(response=error_msg+str(e),
                     status=404,
                     mimetype="application/xml")
        r.headers["Content-Type"] = "text/xml; charset=utf-8"
        return r


# This endpoint gives a big list of possible country names in JSON.
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


# This endpoint gives a list of possible years in JSON.
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


def spout(c=None, y=None, detail=0):
    '''
    Takes country and year and returns wrapped JSON object
    '''
    if c is None and y is None:
        r = Response(response='What? No country and year specified.',
                     status=404,
                     mimetype="application/json")
        r.headers["Content-Type"] = "text/json; charset=utf-8"
        return r

    if detail == 0:
        # Returns a list of all the years for a specified country.
        if y is None:
            jStr = df[df['Country Name'] == c][
                ['Year', 'Forest Land Percent']].to_json(orient='table',
                                                         index=False)
            j1 = json.loads(jStr)['data']
            return(jsonify(j1))
        # Or if year is specified: give just that year's forest land %.
        elif y is not None:
            f = float(df[(df['Country Name'] == c) & (df['Year'] == int(y))]['Forest Land Percent'])  # noqa
            # Returns Flask.Response object
            return jsonify({'Forest Coverage Percent': f})
        else:
            return 1

    elif detail == 1:
        # Returns a list of all the details for a specified country
        # for all the years.
        if y is None:
            jStr = df[df['Country Name'] == c][
                ['Year',
                 'Forest Land Percent',
                 'Agriculture Land Percentage',
                 'Population',
                 'GDP Per Capita (2019 USD)']].to_json(orient='table',
                                                       index=False)
            j1 = json.loads(jStr)['data']
            return(jsonify(j1))

        # Returns a list of all the details for specified country
        # and specific year.
        elif y is not None:
            filtered = df[(df['Country Name'] == c) & (df['Year'] == int(y))]
            cn = filtered['Country Name'].to_string(index=False).strip()
            ct = filtered['Country Code'].to_string(index=False).strip()
            yr = int(filtered['Year'])
            ff = float(filtered['Forest Land Percent'])
            ap = float(filtered['Agriculture Land Percentage'])
            pp = float(filtered['Population'])
            my = float(filtered['GDP Per Capita (2019 USD)'])
            # Unfortunately must be in separate JSON thingies because
            # if not it'll be unpredictably unordered it seems like.
            return jsonify(
                {'Country Name': cn},
                {'Country Code': ct},
                {'Year': yr},
                {'Forest Land Percentage': ff},
                {'Agri Land Percentage': ap},
                {'Population': pp},
                {'GDP per Capita (2019USD)': my}
            )
        else:
            return 1


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
