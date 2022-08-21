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
    def select_task(checklist_id, project_id):
        cursor = builder.cursor()
        find_checklist_id = '''
                                    SELECT checklist_id
                                    FROM Tasks
                                    WHERE checklist_id =%s AND project_id =%s
        '''
        cursor.execute(find_checklist_id, (checklist_id, project_id))
        result = cursor.fetchall()
        if len(result) == 0:
            insert_task = '''
                                       INSERT INTO Tasks (checklist_id,project_id) 
                                       VALUES (%s ,%s);
                                                                            '''
            cursor.execute(insert_task, (checklist_id, project_id))
            builder.commit()
            return {
                'message': 'Select id successfully'
            }
        else:
            builder.commit()
            return {
                'message': 'already has checklist'
            }

    @staticmethod
    def get_select_task(project_id):
        project_id = 1
        cursor = builder.cursor()
        sql_select_task = '''
                                                       SELECT *
                                                       FROM Tasks
                                                       WHERE Tasks.project_id = %s
                                                    '''
        cursor.execute(sql_select_task, (project_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result,
                          columns=['task_id', 'checklist_id', 'project_id'])
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
        df2 = pd.DataFrame(columns=['task_id', 'checklist_id', 'checklist_name'])
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

        df2['checklist_id'] = list_id
        df2['checklist_name'] = list_name
        df2['task_id'] = df['task_id']




        sql_select_task = '''
                                                            SELECT checklist_id
                                                            FROM Tasks
                                                            WHERE Tasks.task_id = %s
                                                         '''
        all_checklist_id = []
        for i in df2['task_id']:
            cursor.execute(sql_select_task, (int(i),))
            result = cursor.fetchall()
            val = json.dumps(result)
            val = val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            val = int(val)
            all_checklist_id.append(val)

        All_checklist_id = pd.DataFrame(all_checklist_id,
                                        columns=['checklist_id'])

        sql_select_list_id = '''
                                                                            SELECT list_id
                                                                            FROM Lists
                                                                            WHERE Lists.checklist_id = %s
                                                                         '''
        sql_select_list_name = '''
                                                                                    SELECT list_name
                                                                                    FROM Lists
                                                                                    WHERE Lists.checklist_id = %s
                                                                                 '''
        sql_select_list_description = '''
                                                                                    SELECT list_description
                                                                                    FROM Lists
                                                                                    WHERE Lists.checklist_id = %s
                                                                                 '''
        sql_select_checklist_id = '''
                                                                                    SELECT checklist_id
                                                                                    FROM Lists
                                                                                    WHERE Lists.checklist_id = %s
                                                                                 '''

        dfList = pd.DataFrame(columns=['list_id', 'list_name', 'list_description', 'checklist_id'])

        List_id = []
        List_name = []
        List_description = []
        Checklist_id = []
        for i in All_checklist_id['checklist_id']:
            cursor.execute(sql_select_list_id, (int(i),))
            list_id = cursor.fetchall()
            list_id = json.dumps(list_id)
            list_id = list_id.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            List_id.append(list_id)

            cursor.execute(sql_select_list_name, (int(i),))
            list_name = cursor.fetchall()
            list_name = json.dumps(list_name, ensure_ascii=False)
            list_name = list_name.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            List_name.append(list_name)

            cursor.execute(sql_select_list_description, (int(i),))
            list_description = cursor.fetchall()
            list_description = json.dumps(list_description, ensure_ascii=False)
            list_description = list_description.translate(
                str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            List_description.append(list_description)

            cursor.execute(sql_select_checklist_id, (int(i),))
            checklist_id = cursor.fetchall()
            checklist_id = json.dumps(checklist_id)
            checklist_id = checklist_id.translate(
                str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            Checklist_id.append(checklist_id)

            # All_list.append(result)
            # val = json.dumps(result, ensure_ascii=False)
            # val = val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            # print(result)

        builder.commit()
        json_result = df2.to_json(orient="records")
        output = json.loads(json_result)
        return output

    @staticmethod
    def check_checkbox(checkbox_id):
        cursor = builder.cursor()
        sql_select_status = '''
                                                            SELECT status
                                                            FROM CheckBoxes
                                                            WHERE checkbox_id = %s
                                                         '''
        cursor.execute(sql_select_status, (checkbox_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['status'])
        print('now current status :' + str(df['status'].iloc[0]))
        if df['status'].iloc[0] == 0:
            sql_update_status = '''UPDATE CheckBoxes SET status = 1 WHERE checkbox_id = %s'''
            cursor.execute(sql_update_status, (checkbox_id,))
            builder.commit()
        else:
            sql_update_status = '''UPDATE CheckBoxes SET status = 0 WHERE checkbox_id = %s'''
            cursor.execute(sql_update_status, (checkbox_id,))
            builder.commit()
        return {
            'message': 'status has change'
        }

    @staticmethod
    def get_list(task_id):
        cursor = builder.cursor()
        sql_select_task = '''
                                                    SELECT checklist_id
                                                    FROM Tasks
                                                    WHERE Tasks.task_id = %s
                                                 '''
        cursor.execute(sql_select_task, (task_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['checklist_id'])
        checklist_id = int(df['checklist_id'].iloc[0])

        sql_select_list = '''
                                                                     SELECT *
                                                                     FROM Lists
                                                                     WHERE Lists.checklist_id = %s
                                                                  '''
        cursor.execute(sql_select_list, (checklist_id,))
        lists = cursor.fetchall()
        df2 = pd.DataFrame(lists, columns=['list_id', 'list_name', 'list_description', 'checklist_id'])

        sql_find_length = '''
                                                                  SELECT *
                                                                  FROM CheckBoxes
                                                                  WHERE CheckBoxes.task_id = %s
                                                               '''
        cursor.execute(sql_find_length, (task_id,))
        find_length = cursor.fetchall()

        if len(find_length) == 0:
            insert_list = '''
                                         INSERT INTO CheckBoxes ( checkbox_id,list_name,status,task_id)
                                         VALUES
                                         (NULL,%s,%s,%s);
                                         '''
            sql_update_list = '''UPDATE CheckBoxes SET list_description = %s WHERE task_id = %s'''
            for i in df2['list_name']:
                cursor.execute(insert_list, (i, 0, task_id))
            for i in df2['list_description']:
                cursor.execute(sql_update_list, (i, task_id))

            sql_CheckBoxes = '''
                                                                          SELECT *
                                                                          FROM CheckBoxes
                                                                          WHERE CheckBoxes.task_id = %s
                                                                       '''
            cursor.execute(sql_CheckBoxes, (task_id,))
            CheckBoxes = cursor.fetchall()
            df3 = pd.DataFrame(CheckBoxes,
                               columns=['checkbox_id', 'list_name', 'list_description', 'status', 'task_id'])

            builder.commit()
            json_result = df3.to_json(orient="records")
            output = json.loads(json_result)
            print('There is no list in the checkbox')
            return output

        else:
            print('already has list in checkbox')
            df3 = pd.DataFrame(find_length,
                               columns=['checkbox_id', 'list_name', 'list_description', 'status', 'task_id'])

            builder.commit()
            json_result = df3.to_json(orient="records")
            output = json.loads(json_result)
            return output
