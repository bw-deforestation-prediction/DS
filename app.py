from flask import Flask, Response, request, jsonify

# Flask App Factory
application = Flask(__name__)


# Test endpoint to see if working
@application.route("/", methods=['POST', 'GET'])
def test():
    r = Response(response="This worked", status=200,
                 mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


# User should want two things, country and year...
@application.route("/want", methods=['POST', 'GET'])
def retrieval():
    r = Response(response="", status=200,
                 mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    # Should somehow return the database's apropos country and year (no duh)
    return r

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
