from flask import Flask, request, jsonify
from flask_cors import cross_origin
from src.feature.OnemeasureAuth import *
from src.feature.OnemeasureAdmin import *

app = Flask(__name__)


###################### Auth #########################
@app.route("/Login", methods=["POST"])
@cross_origin()
def login():
    email = request.json['email']
    password = request.json['password']
    return jsonify(login_user(email, password))


@app.route("/Register", methods=["POST"])
@cross_origin()
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    return jsonify(register_user(first_name, last_name, email, password))


###################### Admin #########################

@app.route("/External", methods=["POST"])
@cross_origin()
def fetch_external_data():
    month = request.json['month']
    year = request.json['year']
    return jsonify(update_external_data(month, year))


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
    print('connect flask')
