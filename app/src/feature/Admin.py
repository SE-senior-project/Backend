from app.src.config.Service import *
import requests
import pandas as pd
import json


class Admin(object):
    @staticmethod
    def update_external_data(mm):
        if type(mm) == str:
            print('month :' + mm)
            cursor = builder.cursor()
            url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
            payload = {
                'DDMonth': mm,
                'DDYear': '2565',
                'DDProvince': '50',
                'texttable': 'csi_price_north_web_avg',
                'text_name': 'unit_code_N',
                'B1': '%B5%A1%C5%A7'
            }
            try:
                r = requests.post(url, data=payload).content
                check = requests.post(url, data=payload)
                print('pass')
            except:
                print('fail')

            if check.status_code == 200:
                df = pd.read_html(r)[0]
                df.dropna(inplace=True)
                df.drop(df.index[14:37], inplace=True)
                df.drop(df.index[27:29], inplace=True)
                df.drop(df.index[91:100], inplace=True)
                material_price = df[3].to_numpy()
                n = len(material_price)
                sql_update_external_data = '''UPDATE Materials SET material_price = %s  WHERE material_id = %s'''
                for i in range(1, n, 1):
                    cursor.execute(sql_update_external_data, (material_price[i], i))
                builder.commit()
                return {
                    "message": "update external successfully"
                }
            else:
                return {
                    "message": "update external unsuccessfully"
                }
        else:
            return {
                "message": "update external unsuccessfully"
            }

    @staticmethod
    def get_all_waiting_user():
        cursor = builder.cursor()
        sql_waiting_user = '''
            SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status, Users.user_id
            FROM Contractors
            INNER JOIN Users
            ON Contractors.user_id = Users.user_id
            WHERE Users.status = 0 
        '''
        cursor.execute(sql_waiting_user)
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['contractor_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status',
                                   'user_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_active_contractor():
        cursor = builder.cursor()
        sql_active_user = '''
                       SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status, Users.user_id
                       FROM Contractors
                       INNER JOIN Users
                       ON Contractors.user_id = Users.user_id
                       WHERE Contractors.active = 1
                       AND Users.status =1
                   '''
        cursor.execute(sql_active_user)
        result = cursor.fetchall()

        builder.commit()
        df = pd.DataFrame(result,
                          columns=['contractor_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status',
                                   'user_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_disable_contractor():

        cursor = builder.cursor()
        sql_disable_user = '''
                       SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status, Users.user_id
                       FROM Contractors
                       INNER JOIN Users
                       ON Contractors.user_id = Users.user_id
                       WHERE Contractors.active = 0
                       AND Users.status =1
                   '''
        cursor.execute(sql_disable_user)
        result = cursor.fetchall()

        builder.commit()
        df = pd.DataFrame(result,
                          columns=['contractor_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status',
                                   'user_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def approve_user(user_id):
        if type(user_id) == int and user_id > 0:
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
            if user_id <= temp:
                try:
                    sql_approve_user = '''UPDATE Users SET status = 1  WHERE user_id = %s'''
                    cursor.execute(sql_approve_user, (user_id,))
                    builder.commit()
                    print('Approved user')
                    return {
                        "message": "approval successfully"
                    }
                except:
                    print('Approve fail')
            else:
                builder.commit()
                return {
                    "message": "approval unsuccessfully"
                }
        else:
            return {
                "message": "approval unsuccessfully"
            }

    @staticmethod
    def unapprove_user(user_id):
        if type(user_id) == int and user_id > 0:
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
            if user_id <= temp:
                try:
                    cursor = builder.cursor()
                    sql_unapprove_user = '''DELETE FROM Users  WHERE user_id = %s'''
                    cursor.execute(sql_unapprove_user, (user_id,))
                    builder.commit()
                    print('Unpproved user')
                    return {
                        "message": "unapproval successfully"
                    }
                except:
                    print('Unpproved fail')
            else:
                builder.commit()
                return {
                    "message": "unapproval unsuccessfully"
                }
        else:
            return {
                "message": "unapproval unsuccessfully"
            }

    @staticmethod
    def active_contractor(contractor_id):
        if type(contractor_id) == int and contractor_id > 0:
            cursor = builder.cursor()
            sql_latest_contractor_id = '''
                                                 SELECT contractor_id
                                                 FROM Contractors
                                                 ORDER BY contractor_id  ASC '''
            cursor.execute(sql_latest_contractor_id)
            result = cursor.fetchall()
            temp = json.dumps(result[len(result) - 1])
            temp = temp.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\,!"\r\])' + U'\xa8'))
            temp = int(temp)
            if contractor_id <= temp:
                try:
                    cursor = builder.cursor()
                    sql_active_contractor = '''UPDATE Contractors SET active = 1  WHERE contractor_id = %s'''
                    cursor.execute(sql_active_contractor, (contractor_id,))
                    builder.commit()
                    print('Actived user')
                    return {
                        "message": "active successfully"
                    }
                except:
                    print('Active fail')
            else:
                builder.commit()
                return {
                    "message": "active unsuccessfully"
                }
        else:
            return {
                "message": "active unsuccessfully"
            }

    @staticmethod
    def disable_contractor(contractor_id):
        if type(contractor_id) == int and contractor_id > 0:
            cursor = builder.cursor()
            sql_latest_contractor_id = '''
                                                        SELECT contractor_id
                                                        FROM Contractors
                                                        ORDER BY contractor_id  ASC '''
            cursor.execute(sql_latest_contractor_id)
            result = cursor.fetchall()
            temp = json.dumps(result[len(result) - 1])
            temp = temp.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\,!"\r\])' + U'\xa8'))
            temp = int(temp)
            if contractor_id <= temp:
                try:
                    cursor = builder.cursor()
                    sql_disable_contractor = '''UPDATE Contractors SET active = 0  WHERE contractor_id = %s'''
                    cursor.execute(sql_disable_contractor, (contractor_id,))
                    builder.commit()
                    print('Disabled user')
                    return {
                        "message": "disable successfully"
                    }

                except:
                    print('Disable fail')
            else:
                builder.commit()
                return {
                    "message": "disable unsuccessfully"
                }
        else:
            return {
                "message": "disable unsuccessfully"
            }
