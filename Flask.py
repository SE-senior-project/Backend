from flask import Flask, request, jsonify
from flask_cors import cross_origin
from Config import *

# import json
# import mysql.connector
#
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="0808601871",
#     database='foodrecipe'
# )

app = Flask(__name__)


@app.route("/Login", methods=["POST"])
@cross_origin()
def Login():
    email = request.json['email']
    password = request.json['password']
    print(email)
    print(password)

    return jsonify(Login_user(email, password))


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
