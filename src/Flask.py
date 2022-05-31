from flask import Flask, request, jsonify
from flask_cors import cross_origin
from src.feature.Auth import *
from src.feature.Admin import *

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


@app.route("/Approve", methods=["POST"])
@cross_origin()
def approve_new_user():
    user_id = request.json['user_id']
    return jsonify(approve_user(user_id))


@app.route("/Unapprove", methods=["POST"])
@cross_origin()
def unapprove_new_user():
    user_id = request.json['user_id']
    return jsonify(unapprove_user(user_id))


@app.route("/Active", methods=["POST"])
@cross_origin()
def active_current_contractor():
    contractor_id = request.json['contractor_id ']
    return jsonify(active_contractor(contractor_id))


@app.route("/Disable", methods=["POST"])
@cross_origin()
def disable_current_contractor():
    contractor_id = request.json['contractor_id']
    return jsonify(disable_contractor(contractor_id))


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
    print('connect flask')
