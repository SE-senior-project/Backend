from flask import Flask, request, jsonify
from flask_cors import cross_origin
# from app.src.config.InitApp import InitApp
from src.feature.Auth import *
from src.feature.Admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@127.0.0.1/onemeasure'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# InitApp()
CORS(app)


###################### Auth #########################

@app.route("/Login", methods=["POST"])
# @cross_origin()
def login():
    email = request.json['email']
    password = request.json['password']
    return jsonify(Auth.login_user(email, password))


@app.route("/Register", methods=["POST"])
# @cross_origin()
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    return jsonify(Auth.register_user(first_name, last_name, email, password))


# ###################### Admin #########################

@app.route("/", methods=["POST"])
# @cross_origin()
def fetch_external_data():
    month = request.json['month']
    year = request.json['year']
    return jsonify(Admin.update_external_data(month, year))


@app.route("/Approve", methods=["POST"])
# @cross_origin()
def approve_new_user():
    user_id = request.json['user_id']
    return jsonify(Admin.approve_user(user_id))


@app.route("/Unapprove", methods=["POST"])
# @cross_origin()
def unapprove_new_user():
    user_id = request.json['user_id']
    return jsonify(Admin.unapprove_user(user_id))


@app.route("/Active", methods=["POST"])
# @cross_origin()
def active_current_contractor():
    contractor_id = request.json['contractor_id ']
    return jsonify(Admin.active_contractor(contractor_id))


@app.route("/Disable", methods=["POST"])
# @cross_origin()
def disable_current_contractor():
    contractor_id = request.json['contractor_id']
    return jsonify(Admin.disable_contractor(contractor_id))


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
    print('connect flask')
