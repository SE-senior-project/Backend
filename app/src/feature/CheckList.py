from app.src.config.Service import *
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
        sql_select_task = ''' SELECT checklist_id,task_id FROM Tasks WHERE Tasks.project_id = %s '''
        cursor.execute(sql_select_task, (project_id,))
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['checklist_id', 'task_id'])
        checklist_name = ''' SELECT checklist_name FROM Checklists WHERE Checklists.checklist_id = %s '''
        df2 = pd.DataFrame(columns=['task_id', 'checklist_id', 'checklist_name'])
        list_name = []
        for i in df['checklist_id']:
            cursor.execute(checklist_name, (int(i),))
            res2 = cursor.fetchall()
            val = json.dumps(res2, ensure_ascii=False)
            list_name.append(val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8')))
        df2['checklist_id'] = df['checklist_id']
        df2['checklist_name'] = list_name
        df2['task_id'] = df['task_id']

        ######################################### List ###################################
        sql_select_list_name = ''' SELECT list_name FROM Lists WHERE Lists.checklist_id = %s'''
        sql_select_list_description = '''SELECT list_description FROM Lists WHERE Lists.checklist_id = %s '''
        List_name = []
        List_description = []
        for i in df2['checklist_id']:
            cursor.execute(sql_select_list_name, (int(i),))
            list_name = cursor.fetchall()
            list_name = json.dumps(list_name, ensure_ascii=False)
            list_name = list_name.translate(str.maketrans('', '', '([$\'_&+,\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            list_name = list(list_name.split(" "))
            List_name.append(list_name)

            cursor.execute(sql_select_list_description, (int(i),))
            list_description = cursor.fetchall()
            list_description = json.dumps(list_description, ensure_ascii=False)
            list_description = list_description.translate(
                str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            list_description = list(list_description.split(','))
            List_description.append(list_description)

        ############################################################checkbox#######################
        sql_find_length = ''' SELECT * FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
        insert_list = '''INSERT INTO CheckBoxes ( checkbox_id,list_name,list_description,status,task_id) VALUES (NULL,%s,%s,%s,%s);'''

        sql_CheckBoxes_checkbox_id = '''SELECT checkbox_id FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
        sql_CheckBoxes_list_name = '''SELECT list_name FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
        sql_CheckBoxes_list_description = '''SELECT list_description FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''
        sql_CheckBoxes_status = '''SELECT status FROM CheckBoxes WHERE CheckBoxes.task_id = %s '''

        Checkbox_id = []
        CheckBoxes_list_name = []
        CheckBoxes_list_description = []
        CheckBoxes_status = []
        count_j = 0
        count_k = 0
        returnOutput = []
        for i in df2['task_id']:
            cursor.execute(sql_find_length, (int(i),))
            find_length = cursor.fetchall()
            if len(find_length) == 0:
                for j in List_name:
                    for k in j:
                        cursor.execute(insert_list, (k, List_description[count_j][count_k], 0, int(i)))
                        count_k = count_k + 1
                    count_k = 0
                    count_j = count_j + 1
            count_j = 0

            cursor.execute(sql_CheckBoxes_checkbox_id, (int(i),))
            checkbox_id = cursor.fetchall()
            checkbox_id = json.dumps(checkbox_id)
            checkbox_id = checkbox_id.translate(
                str.maketrans('', '', '([$\'_&+,\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            checkbox_id = list(checkbox_id.split(" "))
            checkbox_id = [eval(x) for x in checkbox_id]
            # Checkbox_id.append(checkbox_id)

            cursor.execute(sql_CheckBoxes_list_name, (int(i),))
            checkbox_list_name = cursor.fetchall()
            checkbox_list_name = json.dumps(checkbox_list_name, ensure_ascii=False)
            checkbox_list_name = checkbox_list_name.translate(
                str.maketrans('', '', '([$\'_&+,\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            checkbox_list_name = list(checkbox_list_name.split(" "))
            # CheckBoxes_list_name.append(checkbox_list_name)

            cursor.execute(sql_CheckBoxes_list_description, (int(i),))
            checkbox_list_description = cursor.fetchall()
            checkbox_list_description = json.dumps(checkbox_list_description, ensure_ascii=False)
            checkbox_list_description = checkbox_list_description.translate(
                str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            checkbox_list_description = list(checkbox_list_description.split(','))
            # CheckBoxes_list_description.append(checkbox_list_description)

            cursor.execute(sql_CheckBoxes_status, (int(i),))
            checkbox_status = cursor.fetchall()
            checkbox_status = json.dumps(checkbox_status)
            checkbox_status = checkbox_status.translate(
                str.maketrans('', '', '([$\'_&+,\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
            checkbox_status = list(checkbox_status.split(" "))
            checkbox_status = [eval(x) for x in checkbox_status]
            # CheckBoxes_status.append(checkbox_status)

            returnOutput.append({
                'checklist_name': df2.iloc[0, 2],
                'task_id': i,
                'checkbox': {
                    'check_box_id': checkbox_id,
                    'list_name': checkbox_list_name,
                    'list_description': checkbox_list_description,
                    'status': checkbox_status
                }
            })
        print(returnOutput)
        # output = json.loads(returnOutput)
        # returnOutput = json.dumps(returnOutput, ensure_ascii=False)
        # print(type(returnOutput))
        # dfList = pd.DataFrame(
        #     {'checklist_name': df2['checklist_name'], 'task_id': df2['task_id'],
        #      'checkbox': returnOutput
        #      })
        #
        # builder.commit()
        # json_result = dfList.to_json(orient="records")
        # output = json.loads(json_result)
        return returnOutput

    @staticmethod
    def check_checkbox(checkbox_id):
        cursor = builder.cursor()
        sql_select_status = '''SELECT status FROM CheckBoxes WHERE checkbox_id = %s  '''
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

    # @staticmethod
    # def get_list(task_id):
    #     cursor = builder.cursor()
    #     sql_select_task = '''
    #                                                 SELECT checklist_id
    #                                                 FROM Tasks
    #                                                 WHERE Tasks.task_id = %s
    #                                              '''
    #     cursor.execute(sql_select_task, (task_id,))
    #     result = cursor.fetchall()
    #     df = pd.DataFrame(result, columns=['checklist_id'])
    #     checklist_id = int(df['checklist_id'].iloc[0])
    #
    #     sql_select_list = '''
    #                                                                  SELECT *
    #                                                                  FROM Lists
    #                                                                  WHERE Lists.checklist_id = %s
    #                                                               '''
    #     cursor.execute(sql_select_list, (checklist_id,))
    #     lists = cursor.fetchall()
    #     df2 = pd.DataFrame(lists, columns=['list_id', 'list_name', 'list_description', 'checklist_id'])
    #
    #     sql_find_length = '''
    #                                                               SELECT *
    #                                                               FROM CheckBoxes
    #                                                               WHERE CheckBoxes.task_id = %s
    #                                                            '''
    #     cursor.execute(sql_find_length, (task_id,))
    #     find_length = cursor.fetchall()
    #
    #     if len(find_length) == 0:
    #         insert_list = '''
    #                                      INSERT INTO CheckBoxes ( checkbox_id,list_name,status,task_id)
    #                                      VALUES
    #                                      (NULL,%s,%s,%s);
    #                                      '''
    #         sql_update_list = '''UPDATE CheckBoxes SET list_description = %s WHERE task_id = %s'''
    #         for i in df2['list_name']:
    #             cursor.execute(insert_list, (i, 0, task_id))
    #         for i in df2['list_description']:
    #             cursor.execute(sql_update_list, (i, task_id))
    #
    #         sql_CheckBoxes = '''
    #                                                                       SELECT *
    #                                                                       FROM CheckBoxes
    #                                                                       WHERE CheckBoxes.task_id = %s
    #                                                                    '''
    #         cursor.execute(sql_CheckBoxes, (task_id,))
    #         CheckBoxes = cursor.fetchall()
    #         df3 = pd.DataFrame(CheckBoxes,
    #                            columns=['checkbox_id', 'list_name', 'list_description', 'status', 'task_id'])
    #
    #         builder.commit()
    #         json_result = df3.to_json(orient="records")
    #         output = json.loads(json_result)
    #         print('There is no list in the checkbox')
    #         return output
    #
    #     else:
    #         print('already has list in checkbox')
    #         df3 = pd.DataFrame(find_length,
    #                            columns=['checkbox_id', 'list_name', 'list_description', 'status', 'task_id'])
    #
    #         builder.commit()
    #         json_result = df3.to_json(orient="records")
    #         output = json.loads(json_result)
    #         return output
