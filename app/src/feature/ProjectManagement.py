from app.src.config.Service import *
import pandas as pd
import json


class ProjectManagement(object):
    @staticmethod
    def generate_project(contractor_id):
        cursor = builder.cursor()
        sql_generate_project = '''
           SELECT *
           FROM Projects
           WHERE Projects.contractor_id = %s
        '''
        cursor.execute(sql_generate_project, (contractor_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_id', 'project_name', 'project_description', 'customer_name', 'date_line',
                                   'contractor_id ', 'project_material_id '])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_materials():
        cursor = builder.cursor()
        sql_generate_project = '''
               SELECT *
               FROM Materials
            '''
        cursor.execute(sql_generate_project)
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['material_id', 'material_name', 'material_price', 'material_unit',
                                   'material_category',
                                   'material_type '])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_project_material(project_id):
        cursor = builder.cursor()
        sql_generate_project = '''
               SELECT *
               FROM ProjectMaterials
               WHERE ProjectMaterials.project_id = %s
            '''
        cursor.execute(sql_generate_project, (project_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_material_id', 'project_material_name', 'project_material_price',
                                   'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_project(contractor_id):
        cursor = builder.cursor()
        sql_generate_project = '''
                   SELECT *
                   FROM Projects
                   WHERE Projects.contractor_id = %s
                '''
        cursor.execute(sql_generate_project, (contractor_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_id', 'project_name', 'project_description',
                                   'customer_name', 'deadline', 'contractor_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_category():
        cursor = builder.cursor()
        sql_generate_project = '''
                               SELECT material_category
                               FROM Materials
                            '''
        cursor.execute(sql_generate_project)
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['category_name'])
        df = df.drop_duplicates()
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output
