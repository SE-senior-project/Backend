from app.src.config.Service import *
import requests
import pandas as pd


class Admin(object):
    @staticmethod
    def update_external_data(ml, yl):
        # currentMonth = datetime.now().month]
        ml = str(ml)
        yl = str(yl)
        print('month :' + ml)
        print('year :' + yl)
        try:
            cursor = builder.cursor()
            url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
            payload = {
                'DDMonth': ml,
                'DDYear': yl,
                'DDProvince': '50',
                'texttable': 'csi_price_north_web_avg',
                'text_name': 'unit_code_N',
                'B1': '%B5%A1%C5%A7'
            }
            r = requests.post(url, data=payload).content
            df = pd.read_html(r)[0]
            material_price = df[3].to_numpy()
            n = len(material_price) - 1
            sql_update_external_data = '''UPDATE Materials SET material_price = %s  WHERE material_id = %s'''
            for i in range(1, n, 1):
                cursor.execute(sql_update_external_data, (material_price[i], i))
            builder.commit()
            print('Updated external data')
        except:
            print('Update external data fail')

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
