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
        if type(checklist_id) == int and type(project_id) == int:
            if checklist_id > 9:
                return {
                    "message": "Cannot found this checklist"
                }
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
                    'message': 'Select task successfully'
                }
            else:
                builder.commit()
                return {
                    'message': 'already has checklist'
                }
        else:
            return {
                "message": "invalid parameter type"
            }

    @staticmethod
    def get_select_task(project_id):
        if type(project_id) == int:
            cursor = builder.cursor()
            sql_select_task = ''' SELECT * FROM Tasks WHERE Tasks.project_id = %s '''
            cursor.execute(sql_select_task, (project_id,))
            result = cursor.fetchall()
            df = pd.DataFrame(result,
                              columns=['task_id', 'checklist_id', 'project_id'])
            checklist_id = ''' SELECT checklist_id FROM Checklists WHERE Checklists.checklist_id = %s '''
            checklist_name = ''' SELECT checklist_name FROM Checklists WHERE Checklists.checklist_id = %s '''
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

            builder.commit()
            df2['checklist_id'] = list_id
            df2['checklist_name'] = list_name
            df2['task_id'] = df['task_id']

            json_result = df2.to_json(orient="records")
            output = json.loads(json_result)
            return output
        else:
            return {
                "message": "invalid parameter type"
            }

    @staticmethod
    def check_checkbox(checkbox_id):
        if type(checkbox_id) == int:
            try:
                cursor = builder.cursor()
                sql_select_status = ''' SELECT status FROM CheckBoxes WHERE checkbox_id = %s'''
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
            except:
                print('Has no this checkbox id in database')
        else:
            return {
                "message": "invalid parameter type"
            }

    @staticmethod
    def get_list(task_id):
        # task_id = 1
        if type(task_id) == int:
            cursor = builder.cursor()
            try:
                sql_select_task = ''' SELECT checklist_id FROM Tasks WHERE Tasks.task_id = %s '''
                cursor.execute(sql_select_task, (task_id,))
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns=['checklist_id'])
                checklist_id = int(df['checklist_id'].iloc[0])
                # sql_select_checklist_name = '''SELECT checklist_name FROM Checklists WHERE Checklists.checklist_id =
                # %s '''
                # cursor.execute(sql_select_checklist_name, (checklist_id,))
                # result_checklist_name = cursor.fetchall()
                # dfname = pd.DataFrame(result_checklist_name, columns=['checklist_name'])
                # print(dfname)

                sql_select_list = ''' SELECT * FROM Lists WHERE Lists.checklist_id = %s '''
                cursor.execute(sql_select_list, (checklist_id,))
                lists = cursor.fetchall()
                df2 = pd.DataFrame(lists, columns=['list_id', 'list_name', 'list_description', 'checklist_id'])
                sql_find_length = ''' SELECT * FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
                cursor.execute(sql_find_length, (task_id,))
                find_length = cursor.fetchall()

                # print(len(find_length))
                if len(find_length) == 0:
                    insert_list = '''INSERT INTO CheckBoxes ( checkbox_id,list_name,list_description,status,task_id) 
                    VALUES (NULL,%s,%s,%s,%s); '''
                    count = 0
                    for i in df2['list_name']:
                        cursor.execute(insert_list, (i, df2['list_description'].iloc[count], 0, task_id))
                        count = count + 1
                    sql_CheckBoxes = ''' SELECT * FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
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
                    checkStatus = []
                    for i in df3['status']:
                        if i == 1:
                            checkStatus.append(i)
                    if len(checkStatus) == len(df3['status']):
                        df3['equal'] = "equal"
                        # df3['task_name'] = str(dfname['checklist_name'].iloc[0]) + ' task complete'
                    else:
                        df3['equal'] = "not equal"
                        # df3['task_name'] = dfname['checklist_name']

                    builder.commit()
                    json_result = df3.to_json(orient="records")
                    output = json.loads(json_result)
                    return output
            except:
                print('Has no this task id in database')

        else:
            return {
                "message": "invalid parameter type"
            }
