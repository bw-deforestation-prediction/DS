from flask import Flask, Response, request, jsonify

# Flask App Factory
application = Flask(__name__)


# User should want two things, country and year...
@application.route("/database", methods=['POST', 'GET'])
def test():
    r = Response(response="Wow this worked", status=200,
                 mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
