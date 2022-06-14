import numpy as np

from app.src.config.Service import *
import pandas as pd
import json
import numpy as np

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
    def get_all_material():
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
        if type(project_id) == int:
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
                                       'project_material_total', 'project_id'])
            json_result = df.to_json(orient="records")
            output = json.loads(json_result)
            return output
        else:
            return {
                "message": "fetching project unsuccessfully"
            }

    @staticmethod
    def add_material(material_name, material_price, project_material_total, project_id):
        cursor = builder.cursor()
        if material_price < 0 or material_name == "" or type(project_id) != int or type(
                project_material_total) != int or project_material_total < 1:
            return {
                "message": "invalid input"
            }
        else:
            sql_find_duplicate = '''
                           SELECT *
                           FROM ProjectMaterials
                           WHERE project_material_name = %s
                        '''
            cursor.execute(sql_find_duplicate, (material_name,))
            result = cursor.fetchall()
            df = pd.DataFrame(result,
                              columns=['project_material_id', 'project_material_name', 'project_material_price',
                                       'project_material_total', 'project_id'])
            if len(result) == 0:
                try:
                    sql_add_material = '''
                     INSERT INTO ProjectMaterials (ProjectMaterials.project_material_name, ProjectMaterials.project_material_price, ProjectMaterials.project_material_total, ProjectMaterials.project_id)
                        VALUES (%s ,%s, %s, %s)
                    '''
                    cursor.execute(sql_add_material,
                                   (material_name, material_price, project_material_total, project_id,))
                    builder.commit()
                    print('insert pass')
                    return {
                        "message": "add material successfully"
                    }
                except:
                    print('insert fail')
            else:
                sql_update = '''
                                  UPDATE ProjectMaterials 
                                  SET project_material_total = %s
                                  WHERE project_material_id = %s
                               '''
                project_material_id = df['project_material_id'].iloc[0]
                num = df['project_material_total'].iloc[0]
                num = num + 1
                num = np.int16(num).item()
                project_material_id = np.int16(project_material_id).item()
                print(type(num))
                print(type(project_material_id))
                cursor.execute(sql_update, (num, project_material_id))
                builder.commit()
                return {
                    "message": "add material successfully"
                }

    @staticmethod
    def get_all_project(contractor_id, status):
        cursor = builder.cursor()
        sql_all_project = '''
                   SELECT *
                   FROM Projects
                   WHERE Projects.contractor_id = %s AND Projects.status = %s
                '''
        cursor.execute(sql_all_project, (contractor_id, status,))
        result = cursor.fetchall()
        datetime = result[0][4]
        deadline = datetime.strftime('%d / %m / %Y')
        edit = np.copy(result)
        edit[0][4] = deadline
        builder.commit()
        df = pd.DataFrame(edit,
                          columns=['project_id', 'project_name', 'project_description',
                                   'customer_name', 'deadline', 'status', 'contractor_id'])
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
        sql_increase = '''
                   UPDATE ProjectMaterials 
                   SET ProjectMaterials.project_material_total = %s
                   WHERE ProjectMaterials.project_material_id = %s
                '''
        cursor.execute(sql_increase, (project_material_total, project_material_id))
        builder.commit()

    @staticmethod
    def get_all_total_material_selection(project_id):
        cursor = builder.cursor()
        sql_category = '''
                               SELECT *
                               FROM ProjectMaterials
                               WHERE ProjectMaterials.project_id = %s
                            '''
        cursor.execute(sql_category, (project_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_material_id', 'project_material_name', 'project_material_price', 'project_material_total', 'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def total_material_selection():
        cursor = builder.cursor()
        sql_category = '''
                               SELECT project_material_price, project_material_total
                               FROM ProjectMaterials
                            '''
        cursor.execute(sql_category)
        result = cursor.fetchall()
        add = 1
        ans = 0
        for i in result:
            for j in i:
                add = j * add
            ans = add + ans
            add = 1
        total = [ans]
        builder.commit()
        df = pd.DataFrame(total,
                          columns=['total'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def delete_material_seletion(project_material_id):
        cursor = builder.cursor()
        sql_category = '''
                               DELETE FROM ProjectMaterials
                               WHERE ProjectMaterials.project_material_id = %s
                            '''
        cursor.execute(sql_category, (project_material_id,))
        builder.commit()

