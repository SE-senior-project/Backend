# from flask_cors import cross_origin
# from app.src.config.InitApp import InitApp
# from flask import Flask, request, jsonify
# @cross_origin()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@127.0.0.1/onemeasure'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

from flask import Flask, request, jsonify
from src.config.InitApp import *
from src.feature.Auth import *
from src.feature.Admin import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# InitApp

class FlaskController:
    ###################### InitApp #########################
    @staticmethod
    def Build_all_table():
        InitApp.build_all_table()

    ###################### Auth #########################
    @staticmethod
    @app.route("/Login", methods=["POST"])
    def Login_user():
        email = request.json['email']
        password = request.json['password']
        return jsonify(Auth.login_user(email, password))

    @staticmethod
    @app.route("/Register", methods=["POST"])
    def Register_user():
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
        return jsonify(Auth.register_user(first_name, last_name, email, password))

    # ###################### Admin #########################
    @staticmethod
    @app.route("/New_User", methods=["GET"])
    def Get_all_waiting_user():
        return jsonify(Admin.get_all_waiting_user())

    @staticmethod
    @app.route("/Active_Contractor", methods=["GET"])
    def Get_all_active_contractor():
        return jsonify(Admin.get_all_active_contractor())

    @staticmethod
    @app.route("/Disable_Contractor", methods=["GET"])
    def Get_all_disable_contractor():
        return jsonify(Admin.get_all_disable_contractor())

    @staticmethod
    @app.route("/External", methods=["POST"])
    def Update_external_data():
        mm = request.json['mm']
        return jsonify(Admin.update_external_data(mm))

    @staticmethod
    @app.route("/Approve", methods=["POST"])
    def Approve_user():
        user_id = request.json['user_id']
        return jsonify(Admin.approve_user(user_id))

    @staticmethod
    @app.route("/Unapprove", methods=["POST"])
    def Unapprove_user():
        user_id = request.json['user_id']
        return jsonify(Admin.unapprove_user(user_id))

    @staticmethod
    @app.route("/Active", methods=["POST"])
    def Active_contractor():
        contractor_id = request.json['contractor_id']
        return jsonify(Admin.active_contractor(contractor_id))

    @staticmethod
    @app.route("/Disable", methods=["POST"])
    def Disable_contractor():
        contractor_id = request.json['contractor_id']
        return jsonify(Admin.disable_contractor(contractor_id))


# FlaskController.Build_all_table()
if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)
