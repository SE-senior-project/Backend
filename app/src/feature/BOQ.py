from app.src.config.Service import *
import pandas as pd
import json


class BOQ(object):
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
        sql_update_BOQ_list = '''UPDATE BOQLists SET list_name = %s, total_quantity = %s, unit = %s, cost_of_materials_per_unit =%s, total_cost_materials= %s, cost_of_wage_per_unit =%s ,total_wages =%s, total_price = %s WHERE BOQ_list_id = %s'''

        total_cost_materials = total_quantity * cost_of_materials_per_unit
        total_wages = total_quantity * cost_of_wage_per_unit
        total_price = total_cost_materials + total_wages
        cursor.execute(sql_update_BOQ_list,
                       (list_name, total_quantity, unit, cost_of_materials_per_unit, total_cost_materials,
                        cost_of_wage_per_unit, total_wages, total_price, BOQ_list_id))
