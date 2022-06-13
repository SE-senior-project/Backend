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
        sql_project_materials = '''
               SELECT *
               FROM ProjectMaterials
               WHERE ProjectMaterials.project_id = %s
            '''
        cursor.execute(sql_project_materials, (project_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_material_id', 'project_material_name', 'project_material_price',
                                   'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def add_material(material_name, material_price, project_material_total, project_id):
        cursor = builder.cursor()
        if material_price < 0 or material_name == "" or type(project_id) != int or type(project_material_total) != int or project_material_total < 1:
            return {
                "message": "invalid input"
            }
        else:
            try:
                sql_add_material = '''
                    INSERT INTO ProjectMaterials (ProjectMaterials.project_material_name, ProjectMaterials.project_material_price, ProjectMaterials.project_material_total, ProjectMaterials.project_id)
                    VALUES (%s ,%s, %s, %s)
                    '''
                cursor.execute(sql_add_material, (material_name, material_price, project_material_total, project_id,))
                builder.commit()
                print('insert pass')
                return {
                    "message": "add material successfully"
                }
            except:
                print('insert fail')
            return {
                "message": "add material unsuccessfully"
            }

    @staticmethod
    def get_all_project(contractor_id):
        cursor = builder.cursor()
        sql_all_project = '''
                   SELECT *
                   FROM Projects
                   WHERE Projects.contractor_id = %s
                '''
        cursor.execute(sql_all_project, (contractor_id,))
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
        sql_category = '''
                               SELECT material_category, material_id
                               FROM Materials
                            '''
        cursor.execute(sql_category)
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['category_name', 'category_id'])
        df = df.drop_duplicates(subset=['category_name'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_selection_type(material_category):
        cursor = builder.cursor()
        sql_type = '''
                                  SELECT material_type
                                  FROM Materials
                                  WHERE material_category = %s
                               '''
        cursor.execute(sql_type, (material_category,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['material_type'])
        df = df.drop_duplicates(subset=['material_type'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_all_selection_in_type(material_type):
        cursor = builder.cursor()
        sql_type = '''
                                      SELECT *
                                      FROM Materials
                                      WHERE material_type = %s
                                   '''
        cursor.execute(sql_type, (material_type,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['material_id', 'material_name', 'material_price', 'material_unit',
                                   'material_category', 'material_type'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output
      
    @staticmethod
    def number_material(project_material_total, project_material_id):
        cursor = builder.cursor()
        print(project_material_total)
        sql_increase = '''
                   UPDATE ProjectMaterials 
                   SET ProjectMaterials.project_material_total = %s
                   WHERE ProjectMaterials.project_material_id = %s
                '''
        cursor.execute(sql_increase, (project_material_total, project_material_id))
        builder.commit()
