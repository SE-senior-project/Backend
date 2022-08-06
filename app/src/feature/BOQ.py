from app.src.config.Service import *
import pandas as pd
import json


# from datetime import datetime
# import requests


class BOQ(object):

    @staticmethod
    def get_BOQ(project_id):
        cursor = builder.cursor()
        sql_BOQ_list = '''
                                   SELECT *
                                   FROM BOQs
                                   WHERE project_id = %s
                                '''
        print('Project id:' + str(project_id))
        cursor.execute(sql_BOQ_list, (project_id,))
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['id', 'BOQ_name', 'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_customer_view(project_id):
        cursor = builder.cursor()
        sql_customer_view = '''
                                     SELECT *
                                     FROM CustomerViews
                                     WHERE project_id = %s
                                  '''
        print('Project id:' + str(project_id))
        cursor.execute(sql_customer_view, (project_id,))
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['id', 'customer_view_name', 'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_BOQ_list(BOQ_id):
        cursor = builder.cursor()
        sql_BOQ_list = '''
                                 SELECT *
                                 FROM BOQLists
                                 WHERE BOQLists.BOQ_id = %s
                              '''
        print('BOQ id:' + str(BOQ_id))
        cursor.execute(sql_BOQ_list, (BOQ_id,))
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['BOQ_list_id', 'list_name', 'total_quantity', 'unit', 'cost_of_materials_per_unit',
                                   'total_cost_materials', 'cost_of_wage_per_unit', 'total_wages', 'total_price',
                                   'BOQ_id'])

        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_show_template(customer_id):
        cursor = builder.cursor()
        sql_BOQ_list = '''
                                    SELECT *
                                    FROM CustomerBOQLists
                                    WHERE customer_view_id = %s
                                 '''
        print('BOQ id:' + str(customer_id))
        cursor.execute(sql_BOQ_list, (customer_id,))
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['customer_BOQ_list_id', 'list_name', 'total_quantity', 'unit',
                                   'cost_of_materials_per_unit',
                                   'total_cost_materials', 'cost_of_wage_per_unit', 'total_wages', 'total_price',
                                   'customer_view_id'])

        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def update_BOQ_list(list_name, BOQ_list_id, total_quantity, unit, cost_of_materials_per_unit,
                        cost_of_wage_per_unit):
        cursor = builder.cursor()
        try:
            sql_update_BOQ_list = '''UPDATE BOQLists SET list_name = %s, total_quantity = %s, unit = %s, cost_of_materials_per_unit =%s, total_cost_materials= %s, cost_of_wage_per_unit =%s ,total_wages =%s, total_price = %s WHERE BOQ_list_id = %s'''

            total_cost_materials = total_quantity * cost_of_materials_per_unit
            total_wages = total_quantity * cost_of_wage_per_unit
            total_price = total_cost_materials + total_wages
            cursor.execute(sql_update_BOQ_list,
                           (list_name, total_quantity, unit, cost_of_materials_per_unit, total_cost_materials,
                            cost_of_wage_per_unit, total_wages, total_price, BOQ_list_id))
            return {
                "message": "update BOQ list successfully"
            }

        except:
            return {
                "message": "update BOQ list unsuccessfully"
            }

    @staticmethod
    def add_BOQ_list(list_name, BOQ_id, total_quantity, unit, cost_of_materials_per_unit,
                     cost_of_wage_per_unit):
        cursor = builder.cursor()
        try:
            sql_add_BOQ_list = '''INSERT INTO BOQLists 
            (list_name, total_quantity,unit,cost_of_materials_per_unit,total_cost_materials,cost_of_wage_per_unit,total_wages,total_price,BOQ_id)
                            VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s) '''

            total_cost_materials = total_quantity * cost_of_materials_per_unit
            total_wages = total_quantity * cost_of_wage_per_unit
            total_price = total_cost_materials + total_wages
            cursor.execute(sql_add_BOQ_list,
                           (list_name, total_quantity, unit, cost_of_materials_per_unit, total_cost_materials,
                            cost_of_wage_per_unit, total_wages, total_price, BOQ_id))
            return {
                "message": "add BOQ list successfully"
            }

        except:
            return {
                "message": "add BOQ list unsuccessfully"
            }

    @staticmethod
    def remove_BOQ_list(BOQ_list_id):
        cursor = builder.cursor()
        try:
            sql_remove_BOQ_list = '''
            DELETE FROM BOQLists
            WHERE BOQ_list_id = %s'''

            cursor.execute(sql_remove_BOQ_list, (BOQ_list_id,))
            return {
                "message": "remove BOQ list successfully"
            }

        except:
            return {
                "message": "remove BOQ list unsuccessfully"
            }

    # the reason ทำไมข้อมูลถึง -3 จากเดือนปัจจุบัน เพราะทาง front end ไม่สามารถใช้ข้อมูลจาก external ในเดิอนปัจจุบันได้เมื่อเปลี่ยนเดือน
    # เดือนปัจจุบันก็จะเปลี่ยนไป แต่ว่าจะยังคงใช้ไม่ได้ไปจนถึงวัน update website ของเดือนใหม่ จึงทำให้ ทาง front end -2
    # จากเดือนปัจจุบัน และเดือนที่ใช้ compare จึงจำเป็นต้อง -3 เพื่อเทียบกับเดือนปัจจุบันของ front end.
    # @staticmethod
    # def get_trend_material(project_id):
    #     # project_id = 1
    #     currentMonth = datetime.now().month
    #     mm = ""
    #     if currentMonth == int:
    #         if currentMonth == 1:
    #             mm = "01"
    #         elif currentMonth == 2:
    #             mm = "01"
    #         elif currentMonth == 3:
    #             mm = "01"
    #         elif currentMonth == 4:
    #             mm = "01"
    #         elif currentMonth == 5:
    #             mm = "02"
    #         elif currentMonth == 6:
    #             mm = "03"
    #         elif currentMonth == 7:
    #             mm = "04"
    #         elif currentMonth == 8:
    #             mm = "05"
    #         elif currentMonth == 9:
    #             mm = "06"
    #         elif currentMonth == 10:
    #             mm = "07"
    #         elif currentMonth == 11:
    #             mm = "08"
    #         elif currentMonth == 12:
    #             mm = "09"
    #         print("compare mm:" + mm)
    #         cursor = builder.cursor()
    #         url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
    #         payload = {
    #             'DDMonth': mm,
    #             'DDYear': '2565',
    #             'DDProvince': '50',
    #             'texttable': 'csi_price_north_web_avg',
    #             'text_name': 'unit_code_N',
    #             'B1': '%B5%A1%C5%A7'
    #         }
    #         try:
    #             r = requests.post(url, data=payload).content
    #             check_payload = requests.post(url, data=payload)
    #             print('pass')
    #         except:
    #             print('fail')
    #
    #         if check_payload.status_code == 200:
    #             print('status 200')
    #             df = pd.read_html(r)[0]
    #             df.dropna(inplace=True)
    #             df.drop(df.index[14:37], inplace=True)
    #             df.drop(df.index[27:29], inplace=True)
    #             df.drop(df.index[91:100], inplace=True)
    #             material_price = df[3].to_numpy()
    #             n = len(material_price)
    #             sql_update_external_data = '''UPDATE MaterialComparators SET material_comparator_price = %s  WHERE material_comparator_id = %s'''
    #             for i in range(1, n, 1):
    #                 cursor.execute(sql_update_external_data, (material_price[i], i))
    #
    #             sql_external_name = '''SELECT project_material_name  FROM ProjectMaterials  WHERE project_id = %s'''
    #             cursor.execute(sql_external_name, (project_id,))
    #             result = cursor.fetchall()
    #             find_price = pd.DataFrame(result,
    #                                       columns=['find_price'])
    #
    #             external_price = []
    #             external_name = []
    #             sql_external_price = '''SELECT material_price  FROM Materials  WHERE material_name = %s'''
    #             for i in find_price['find_price']:
    #                 cursor.execute(sql_external_price, (i,))
    #                 result = cursor.fetchall()
    #                 val = json.dumps(result)
    #                 external_price.append(
    #                     val.translate(str.maketrans('', '', '([$\'&+\n?@\[\]#|<>^*()%\\!"\r\])' + U'\xa8')))
    #
    #             sql_external_price = '''SELECT material_name  FROM Materials  WHERE material_name = %s'''
    #             for i in find_price['find_price']:
    #                 cursor.execute(sql_external_price, (i,))
    #                 result = cursor.fetchall()
    #                 val = str(result)
    #                 val = val.translate(str.maketrans('', '', '([$\'&+\n?@\[\]#|<>,^*()%\\!"\r\])' + U'\xa8'))
    #                 print(val)
    #                 external_name.append(val)
    #
    #             material = pd.DataFrame(external_price,
    #                                     columns=['material_price'])
    #             material['material_name'] = external_name
    #
    #             comparators_price = []
    #             sql_external_data_comparators = '''SELECT material_comparator_price  FROM MaterialComparators WHERE material_comparator_name = %s'''
    #             for i in material['material_name']:
    #                 cursor.execute(sql_external_data_comparators, (i,))
    #                 result = cursor.fetchall()
    #                 val = json.dumps(result)
    #                 comparators_price.append(
    #                     val.translate(str.maketrans('', '', '([$\'&+\n?@\[\]#|<>^*()%\\!"\r\])' + U'\xa8')))
    #
    #             material['material_comparators_price'] = comparators_price
    #
    #             comparison = []
    #             count = 0
    #             for i in material['material_price']:
    #                 res = float(i) - float(material['material_comparators_price'].iloc[count])
    #                 res = res * 100
    #                 res = res / float(material['material_comparators_price'].iloc[count])
    #                 comparison.append(res)
    #                 count = count + 1
    #
    #             last_compute = pd.DataFrame(comparison,
    #                                         columns=['comparison_percent'])
    #
    #             json_result = last_compute.to_json(orient="records")
    #             output = json.loads(json_result)
    #             return output
    #
    #         else:
    #             print('status is not 200')
    #             return {
    #                 'message': 'fetching trend fail'
    #             }
    #     else:
    #         return {
    #             'message': 'fetching trend fail'
    #         }

# first = [100.055, 200.00, 300.00]
# sec = [50.01, 300.05, 300.00]
# keep = []
# count = 0
# for i in sec:
#     res = float(i) - float(first[count])
#     res = res * 100
#     res = res / float(first[count])
#     keep.append(res)
#     count = count + 1
