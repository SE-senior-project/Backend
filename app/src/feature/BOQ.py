from app.src.config.Service import *
import pandas as pd
import json


class BOQ(object):
    @staticmethod
    def get_BOQ(contractor_id):
        cursor = builder.cursor()
        sql_BOQ_list = '''
                                   SELECT *
                                   FROM BOQs
                                   WHERE contractor_id = %s
                                '''
        print('Contractor id:' + str(contractor_id))
        cursor.execute(sql_BOQ_list, (contractor_id,))
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['id', 'BOQ_name', 'contractor_id'])
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
