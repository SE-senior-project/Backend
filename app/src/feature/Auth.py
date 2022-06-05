from app.src.config.Service import *
import json
import pandas as pd
import jwt
import hashlib


class Auth(object):
    @staticmethod
    def login_user(email, password):
        # email = 'fax43@gmail.com'
        # password = 'fax4321'
        print('Email :' + str(email))
        print('Password :' + str(password))
        cursor = builder.cursor()
        sql_login = '''
                SELECT Contractors.contractor_id,Contractors.active,Contractors.first_name,Users.role,Users.status
                FROM Contractors
                INNER JOIN Users
                ON Contractors.user_id = Users.user_id
                WHERE Contractors.email = %s 
                AND Contractors.password = %s 
            '''
        password = hashlib.md5(password.encode()).hexdigest()
        val = (email, password)
        cursor.execute(sql_login, val)
        result = cursor.fetchall()
        print(result)
        if len(result) == 0:
            print('result not match')
            return {
                'check': False
            }
        df = pd.DataFrame(result,
                          columns=['contractor_id', 'active', 'first_name', 'role', 'status'])
        payload_data = {
            "password": password,
            "email": email
        }
        token = jwt.encode(
            payload_data,
            key='my_super_secret'
        )
        df['token'] = token
        user = [{
            'id': df['contractor_id'].iloc[0],
            'username': df['first_name'].iloc[0],
            'status': df['status'].iloc[0],
            'role': df['role'].iloc[0],
            'active': df['active'].iloc[0]
        }]
        df['user'] = user

        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        print("Pass valid")
        return output

    @staticmethod
    def add_user():
        cursor = builder.cursor()
        try:
            sql_register = '''
                  INSERT INTO Users ( role,status) VALUES ('contractor' ,0)
                  '''
            cursor.execute(sql_register)
            builder.commit()
            print('insert pass')
        except:
            print('insert fail')

    @staticmethod
    def register_user(first_name, last_name, email, password):
        print('User_Firstname :' + str(first_name))
        print('User_Lastname :' + str(last_name))
        print('User_Email :' + str(email))
        print('User_Password :' + str(password))
        Auth.add_user()
        cursor = builder.cursor()
        sql_latest_user_id = '''
                  SELECT user_id
                  FROM Users
                  ORDER BY user_id  ASC '''
        cursor.execute(sql_latest_user_id)
        result = cursor.fetchall()
        temp = json.dumps(result[len(result) - 1])
        temp = temp.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\,!"\r\])' + U'\xa8'))
        temp = int(temp)
        print(temp)

        sql_register = '''
          INSERT INTO `Contractors` ( `first_name`,`last_name`,`email`,`password`,`active`,`user_id`) VALUES (%s ,%s ,%s ,%s ,%s,%s)
          '''
        val = (first_name, last_name, email, password, 0, temp)
        cursor.execute(sql_register, val)
        builder.commit()
