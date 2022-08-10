from app.src.config.Service import *
import requests
import pandas as pd
import json


class CheckList(object):

    @staticmethod
    def get_checklist():
        cursor = builder.cursor()
        sql_checklist = '''
                                              SELECT *
                                              FROM Checklists
                                           '''
        cursor.execute(sql_checklist)
        result = cursor.fetchall()
        print(result)
        builder.commit()
        df = pd.DataFrame(result,
                          columns=['checklist_id', 'checklist_name'])
        json_result = df.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def select_checkList(checklist_id, project_id):
        cursor = builder.cursor()
        insert_checklist = '''
                                 INSERT INTO ProjectCheckLists (checklist_id,project_id) 
                                 VALUES (%s ,%s);
                                                                      '''
        cursor.execute(insert_checklist, (checklist_id, project_id))
        builder.commit()
        return {'message': 'insert checklist pass'}

    @staticmethod
    def get_select_checkList(project_id):
        cursor = builder.cursor()
        sql_select_checklist = '''
                                                       SELECT *
                                                       FROM ProjectCheckLists
                                                       WHERE ProjectCheckLists.project_id = %s
                                                    '''
        cursor.execute(sql_select_checklist, (project_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result,
                          columns=['project_checklist_id', 'checklist_id', 'project_id'])
        checklist_id = '''
                                                             SELECT checklist_id
                                                             FROM Checklists
                                                             WHERE Checklists.checklist_id = %s
                                                          '''
        checklist_name = '''
                                                                     SELECT checklist_name
                                                                     FROM Checklists
                                                                     WHERE Checklists.checklist_id = %s
                                                                  '''
        df2 = pd.DataFrame(columns=['checklist_id', 'checklist_name'])
        list_id = []
        list_name = []
        for i in df['checklist_id']:
            cursor.execute(checklist_id, (int(i),))
            res = cursor.fetchall()
            val = json.dumps(res)
            list_id.append(val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8')))
            cursor.execute(checklist_name, (int(i),))
            res2 = cursor.fetchall()
            val = json.dumps(res2, ensure_ascii=False)
            list_name.append(val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8')))

        builder.commit()
        df2['checklist_id'] = list_id
        df2['checklist_name'] = list_name

        json_result = df2.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def get_task(checklist_id):
        cursor = builder.cursor()
        sql_select_checklist = '''
                                                    SELECT *
                                                    FROM ProjectCheckLists
                                                    WHERE ProjectCheckLists.checklist_id = %s
                                                 '''
        cursor.execute(sql_select_checklist, (checklist_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result,
                          columns=['project_checklist_id', 'checklist_id', 'project_id'])

        Cid = int(df['checklist_id'].iloc[0])
        sql_select_task = '''
                                                          SELECT *
                                                          FROM Tasks
                                                          WHERE Tasks.checklist_id = %s
                                                       '''
        cursor.execute(sql_select_task, (Cid,))
        task = cursor.fetchall()
        builder.commit()
        df2 = pd.DataFrame(task,
                           columns=['task_id', 'task_name', 'task_description', 'checklist_id'])
        json_result = df2.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def select_task(checklist_id, project_id):
        return 1

    # @staticmethod
    # def get_task(checklist_id):
    #     return 1
