from app.src.config.Service import *
import pandas as pd
import json


class BOQ(object):
    @staticmethod
    def get_all_BOQ_list(BOQ_id):
        # BOQ_id = 1
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
        # BOQ_total_price = 0
        # for i in df['total_price']:
        #     BOQ_total_price = BOQ_total_price + i
        # df['BOQ_total_price'] = BOQ_total_price
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def update_BOQ_list(list_name, BOQ_list_id):
        cursor = builder.cursor()
        sql_update_BOQ_list = '''UPDATE BOQLists SET BOQLists.list_name = %s  WHERE BOQLists.BOQ_list_id = %s'''
        cursor.execute(sql_update_BOQ_list, (list_name, BOQ_list_id))
