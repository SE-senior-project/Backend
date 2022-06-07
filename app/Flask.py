# from flask_cors import cross_origin
# from app.src.config.InitApp import InitApp
# from flask import Flask, request, jsonify
# @cross_origin()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@127.0.0.1/onemeasure'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

from flask import Flask, request, jsonify
# from src.config.InitApp import InitApp
from src.feature.Auth import *
from src.feature.Admin import *
from flask_cors import CORS
from pympler import muppy
muppy.get_objects()
app = Flask(__name__)
CORS(app)


# InitApp


###################### Auth #########################
@app.route("/Login", methods=["POST"])
def Login_user():
    email = request.json['email']
    password = request.json['password']
    return jsonify(Auth.login_user(email, password))


@app.route("/Register", methods=["POST"])
def Register_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    return jsonify(Auth.register_user(first_name, last_name, email, password))


# ###################### Admin #########################
@app.route("/New_User", methods=["GET"])
def Get_all_waiting_user():
    return jsonify(Admin.get_all_waiting_user())


@app.route("/Active_Contractor", methods=["GET"])
def Get_all_active_contractor():
    return jsonify(Admin.get_all_active_contractor())


@app.route("/Disable_Contractor", methods=["GET"])
def Get_all_contractor():
    return jsonify(Admin.get_all_disable_contractor())


@app.route("/External", methods=["POST"])
def Update_external_data():
    mm = request.json['mm']
    return jsonify(Admin.update_external_data(mm))


@app.route("/Approve", methods=["POST"])
def Approve_user():
    user_id = request.json['user_id']
    return jsonify(Admin.approve_user(user_id))


@app.route("/Unapprove", methods=["POST"])
def Unapprove_user():
    user_id = request.json['user_id']
    return jsonify(Admin.unapprove_user(user_id))


@app.route("/Active", methods=["POST"])
def Active_contractor():
    contractor_id = request.json['contractor_id']
    return jsonify(Admin.active_contractor(contractor_id))


@app.route("/Disable", methods=["POST"])
def Disable_contractor():
    contractor_id = request.json['contractor_id']
    return jsonify(Admin.disable_contractor(contractor_id))


if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080, debug=True)
    app.run(host='127.0.0.1', port=6000, debug=True)
