from app.src.config.Service import *
import requests
import pandas as pd
import json


class Admin(object):
    @staticmethod
    def update_external_data(mm):
        print('month :' + mm)
        try:
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
            r = requests.post(url, data=payload).content
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
            print('Updated external data')
        except:
            print('Update external data fail')

    @staticmethod
    def get_all_waiting_user():
        try:
            cursor = builder.cursor()
            sql_waiting_user = '''
                SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status
                FROM Contractors
                INNER JOIN Users
                ON Contractors.user_id = Users.user_id
                WHERE Users.status = 0 
            '''
            cursor.execute(sql_waiting_user)
            result = cursor.fetchall()
            builder.commit()
            df = pd.DataFrame(result,
                              columns=['user_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status'])
            json_result = df.to_json(orient="records")
            output = json.loads(json_result)
            print('Already send waiting_user')
        except:
            print('Sending fail')
        return output

    @staticmethod
    def get_all_active_contractor():
        try:
            cursor = builder.cursor()
            sql_active_user = '''
                       SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status
                       FROM Contractors
                       INNER JOIN Users
                       ON Contractors.user_id = Users.user_id
                       WHERE Contractors.active = 1
                   '''
            cursor.execute(sql_active_user)
            result = cursor.fetchall()
            builder.commit()
            df = pd.DataFrame(result,
                              columns=['user_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status'])
            json_result = df.to_json(orient="records")
            output = json.loads(json_result)
            print('Already send active_contractor')
        except:
            print('Sending fail')
        return output

    @staticmethod
    def get_all_disable_contractor():
        try:
            cursor = builder.cursor()
            sql_disable_user = '''
                       SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Contractors.email,Contractors.active,Users.role,Users.status
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
                              columns=['user_id', 'first_name', 'last_name', 'email', 'active', 'role', 'status'])
            json_result = df.to_json(orient="records")
            output = json.loads(json_result)
            print('Already send disable_contractor')
        except:
            print('Sending fail')
        return output

    @staticmethod
    def approve_user(user_id):
        try:
            cursor = builder.cursor()
            sql_approve_user = '''UPDATE Users SET status = 1  WHERE user_id = %s'''
            cursor.execute(sql_approve_user, (user_id,))
            builder.commit()
            print('Approved user')
        except:
            print('Approve fail')

    @staticmethod
    def unapprove_user(user_id):
        try:
            cursor = builder.cursor()
            sql_unapprove_user = '''DELETE FROM Users   WHERE user_id = %s'''
            cursor.execute(sql_unapprove_user, (user_id,))
            builder.commit()
            print('Unpproved user')
        except:
            print('Unpproved fail')

    @staticmethod
    def active_contractor(contractor_id):
        try:
            cursor = builder.cursor()
            sql_active_contractor = '''UPDATE Contractors SET active = 1  WHERE contractor_id = %s'''
            cursor.execute(sql_active_contractor, (contractor_id,))
            builder.commit()
            print('Actived user')
        except:
            print('Active fail')

    @staticmethod
    def disable_contractor(contractor_id):
        try:
            cursor = builder.cursor()
            sql_disable_contractor = '''UPDATE Contractors SET active = 0  WHERE contractor_id = %s'''
            cursor.execute(sql_disable_contractor, (contractor_id,))
            builder.commit()
            print('Disabled user')
        except:
            print('Disable fail')
