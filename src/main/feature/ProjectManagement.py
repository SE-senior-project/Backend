from src.main.config.Service import *
import pandas as pd
import json
import numpy as np


class ProjectManagement(object):
    @staticmethod
    def add_project(project_name, customer_name, project_description, deadline, status, contractor_id):
        try:
            cursor = builder.cursor()
            if type(project_name) != str or type(customer_name) != str or type(project_description) != str or type(
                    status) != int or type(contractor_id) != int or contractor_id < 1 or status < 0 or status > 1:
                return {
                    "message": "invalid input"
                }
            sql_generate_project = '''
                   INSERT INTO Projects (Projects.project_name, customer_name, project_description, deadline, status, contractor_id)
                VALUES (%s ,%s, %s, %s, %s, %s)
                '''
            cursor.execute(sql_generate_project,
                           (project_name, customer_name, project_description, deadline, status, contractor_id))
            builder.commit()
            return {
                "message": "add project successfully"
            }
        except:
            return {
                "message": "add project unsuccessfully"
            }

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
    def add_material(material_name, material_price, project_material_total, project_id):
        cursor = builder.cursor()
        if type(material_name) != str or type(
                material_price) != float or material_price < 0 or material_name == "" or type(
            project_id) != int or type(project_material_total) != int or project_material_total < 1:
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
                cursor.execute(sql_update, (num, project_material_id))
                builder.commit()
                return {
                    "message": "add material successfully"
                }

    @staticmethod
    def get_all_project(contractor_id, status):
        if type(contractor_id) != int or type(status) != int or contractor_id <= 0 or status > 1:
            return {
                "message": "get project unsuccessfully"
            }
        cursor = builder.cursor()
        sql_all_project = '''
                   SELECT *
                   FROM Projects
                   WHERE Projects.contractor_id = %s AND Projects.status = %s
                '''
        cursor.execute(sql_all_project, (contractor_id, status,))
        result = cursor.fetchall()
        edit = np.copy(result)
        if result:
            print(result)
            count = 0
            for i in result:
                datetime = i[4]
                deadline = datetime.strftime('%d / %m / %Y')
                edit[count][4] = deadline
                print(edit[count][4])
                count = count + 1
            builder.commit()
            df = pd.DataFrame(edit,
                              columns=['project_id', 'project_name', 'project_description',
                                       'customer_name', 'deadline', 'status', 'contractor_id'])
            json_result = df.to_json(orient="records")
            output = json.loads(json_result)
            return output
        else:
            return {
                "message": "get project unsuccessfully"
            }

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
        if type(material_category) == str:
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
            print(output)
            return output
        else:
            return {
                "message": "fetching type unsuccessfully"
            }

    @staticmethod
    def get_all_selection_in_type(material_type):
        if type(material_type) == str:
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
        else:
            return {
                "message": "fetching unit type unsuccessfully"
            }

    ######### new update ########
    @staticmethod
    def number_material(project_material_total, project_material_id):
        cursor = builder.cursor()
        print("project material id: " + str(project_material_id))
        print("total: " + str(project_material_total))
        if type(project_material_total) != int or type(
                project_material_id) != int or project_material_total <= 0 or project_material_id < 1:
            return {
                "message": "number material is update unsuccessfully."
            }
        sql_increase = '''
                   UPDATE ProjectMaterials 
                   SET ProjectMaterials.project_material_total = %s
                   WHERE ProjectMaterials.project_material_id = %s
                '''
        cursor.execute(sql_increase, (project_material_total, project_material_id))
        builder.commit()
        return {
            "message": "number material is update successfully."
        }

    @staticmethod
    def get_all_total_material_selection(project_id):
        cursor = builder.cursor()
        sql = '''
                               SELECT *
                               FROM ProjectMaterials
                               WHERE ProjectMaterials.project_id = %s
                            '''
        cursor.execute(sql, (project_id,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['project_material_id', 'project_material_name', 'project_material_price',
                                   'project_material_total', 'project_id'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def total_material_selection(project_id):
        try:
            cursor = builder.cursor()
            sql_category = '''
                                   SELECT project_material_price, project_material_total
                                   FROM ProjectMaterials
                                   WHERE ProjectMaterials.project_id = %s
                                '''
            cursor.execute(sql_category, (project_id,))
            result = cursor.fetchall()
            if len(result) == 0 or type(project_id) != int:
                return {
                    "message": "no this project_id in the database"
                }
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
        except:
            return {
                "message": "get total material selection unsuccessfully"
            }

    @staticmethod
    def delete_material_selection(project_material_id):
        try:
            cursor = builder.cursor()
            if type(project_material_id) != int or project_material_id < 1:
                return {
                    "message": "unknown this project_material_id"
                }
            sql_category = '''
                                   DELETE FROM ProjectMaterials
                                   WHERE ProjectMaterials.project_material_id = %s
                                '''
            cursor.execute(sql_category, (project_material_id,))
            builder.commit()
            return {
                "message": "delete successfully"
            }
        except:
            return {
                "message": "delete unsuccessfully"
            }

    @staticmethod
    def active_status_project(status, project_id):
        try:
            cursor = builder.cursor()
            if type(status) != int or type(project_id) != int or project_id < 1 or status > 1 or status < 0:
                return {
                    "message": "unknown this project_id"
                }
            sql_increase = '''
                       UPDATE Projects
                       SET Projects.status = %s
                       WHERE Projects.project_id = %s
                    '''
            cursor.execute(sql_increase, (status, project_id))
            builder.commit()
            return {
                "message": "active status project successfully"
            }
        except:
            return {
                "message": "active status project unsuccessfully"
            }

    @staticmethod
    def search_result(material_name):
        cursor = builder.cursor()
        print(material_name)
        if type(material_name) != str:
            return {
                "message": "invalid input"
            }
        sql_search = '''
                                                  SELECT *
                                                  FROM Materials
                                                  WHERE material_name = %s
                                               '''
        cursor.execute(sql_search, (material_name,))
        result = cursor.fetchall()
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['material_id', 'material_name', 'material_price', 'material_unit',
                                   'material_category', 'material_type'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output
