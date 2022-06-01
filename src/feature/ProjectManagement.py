from src.config.Service import *
import pandas as pd
import json


def generate_project(contractor_id):
    cursor = builder.cursor()
    sql_generate_project = '''
           SELECT *
           FROM Projects
           WHERE Projects.contractor_id = %s
       '''
    cursor.execute(sql_generate_project, (contractor_id,))
    result = cursor.fetchall()
    df = pd.DataFrame(result,
                      columns=['project_id', 'project_name', 'project_description', 'customer_name', 'date_line',
                               'contractor_id ', 'project_material_id '])
    json_result = df.to_json(orient="records")
    output = json.loads(json_result)
    return output
