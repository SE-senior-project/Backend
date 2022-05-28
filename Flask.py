from flask import Flask, request, jsonify
from flask_cors import cross_origin
from src.feature.OnemeasureAuth import *

app = Flask(__name__)


@app.route("/Login", methods=["POST"])
@cross_origin()
def Login():
    email = request.json['email']
    password = request.json['password']
    return jsonify(Login_user(email, password))


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
    print('connect flask')
